"""
Tender Monitor for GlobalScope MultiFrame Platform
Monitors government tender announcements and ensures quality compliance
"""
import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Any, List
import aiohttp
from bs4 import BeautifulSoup
import re

from src.lib.utils import get_logger
from src.lib.event_bus import event_bus
from src.security.security_logging_service import SecurityLoggingService
from src.lib.redis_client import redis_client

logger = get_logger("TenderMonitor")
security_logger = SecurityLoggingService()

class TenderMonitor:
    """
    Monitors government tender announcements and ensures quality compliance
    """
    
    def __init__(self):
        self.monitored_sources = []
        self.tender_cache = {}
        logger.info("TenderMonitor initialized")
    
    async def add_tender_source(self, source_url: str, source_name: str, 
                              tender_keywords: List[str]) -> Dict[str, Any]:
        """
        Add government tender source to monitor
        
        Args:
            source_url: URL of government tender portal
            source_name: Name of the source
            tender_keywords: Keywords to filter relevant tenders
            
        Returns:
            Dictionary with operation status
        """
        try:
            source_data = {
                "url": source_url,
                "name": source_name,
                "keywords": tender_keywords,
                "last_checked": datetime.utcnow().isoformat(),
                "active": True
            }
            
            self.monitored_sources.append(source_data)
            
            # Store in Redis
            await redis_client.set_json(f"tender_source:{source_name}", source_data)
            
            logger.info(f"Tender source {source_name} added for monitoring")
            await security_logger.log_security_event("system", "tender_source_added", {
                "source_name": source_name,
                "url": source_url,
                "keywords": tender_keywords
            })
            
            return {
                "status": "success",
                "message": f"Tender source {source_name} added successfully"
            }
            
        except Exception as e:
            logger.error(f"Failed to add tender source {source_name}: {str(e)}")
            await security_logger.log_security_event("system", "tender_source_add_failed", {
                "source_name": source_name,
                "error": str(e)
            })
            return {
                "status": "error",
                "message": f"Failed to add tender source: {str(e)}"
            }
    
    async def monitor_tenders(self) -> List[Dict[str, Any]]:
        """
        Monitor all registered tender sources for new announcements
        
        Returns:
            List of new tender announcements
        """
        try:
            new_tenders = []
            
            for source in self.monitored_sources:
                if not source["active"]:
                    continue
                
                try:
                    tenders = await self._scrape_tender_source(source)
                    new_tenders.extend(tenders)
                except Exception as e:
                    logger.error(f"Failed to scrape tender source {source['name']}: {str(e)}")
                    continue
            
            # Process new tenders
            processed_tenders = []
            for tender in new_tenders:
                processed_tender = await self._process_tender(tender)
                processed_tenders.append(processed_tender)
            
            # Store in cache
            self.tender_cache = {t["id"]: t for t in processed_tenders}
            
            # Notify via event bus
            if processed_tenders:
                await event_bus.publish("new_tenders_found", {
                    "tender_count": len(processed_tenders),
                    "tenders": processed_tenders,
                    "timestamp": datetime.utcnow().isoformat()
                })
            
            logger.info(f"Found {len(processed_tenders)} new tenders")
            return processed_tenders
            
        except Exception as e:
            logger.error(f"Tender monitoring failed: {str(e)}")
            await security_logger.log_security_event("system", "tender_monitoring_failed", {
                "error": str(e)
            })
            return []
    
    async def _scrape_tender_source(self, source: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Scrape tender source for announcements
        
        Args:
            source: Tender source configuration
            
        Returns:
            List of tender announcements
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(source["url"]) as response:
                    if response.status == 200:
                        content = await response.text()
                        soup = BeautifulSoup(content, 'html.parser')
                        
                        # Parse tenders based on source structure
                        tenders = await self._parse_tenders(soup, source)
                        return tenders
                    else:
                        logger.warning(f"Failed to fetch {source['url']}: {response.status}")
                        return []
                        
        except Exception as e:
            logger.error(f"Scraping failed for {source['name']}: {str(e)}")
            return []
    
    async def _parse_tenders(self, soup: BeautifulSoup, source: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Parse tenders from HTML content
        
        Args:
            soup: BeautifulSoup object with HTML content
            source: Tender source configuration
            
        Returns:
            List of parsed tenders
        """
        tenders = []
        
        # This is a simplified parser - in real implementation would be customized per source
        tender_elements = soup.find_all(['div', 'tr', 'li'], class_=re.compile(r'tender|auction|procurement'))
        
        for element in tender_elements:
            try:
                # Extract tender information
                title_elem = element.find(['h1', 'h2', 'h3', 'h4', 'td', 'div'], class_=re.compile(r'title|name'))
                title = title_elem.get_text().strip() if title_elem else "Unknown Tender"
                
                # Check if tender matches our keywords
                if not any(keyword.lower() in title.lower() for keyword in source["keywords"]):
                    continue
                
                # Extract other details
                description_elem = element.find(['p', 'td', 'div'], class_=re.compile(r'description|details'))
                description = description_elem.get_text().strip() if description_elem else ""
                
                price_elem = element.find(['span', 'td', 'div'], class_=re.compile(r'price|cost|amount'))
                price_text = price_elem.get_text().strip() if price_elem else ""
                
                deadline_elem = element.find(['span', 'td', 'div'], class_=re.compile(r'deadline|date'))
                deadline = deadline_elem.get_text().strip() if deadline_elem else ""
                
                link_elem = element.find('a', href=True)
                link = link_elem['href'] if link_elem else source["url"]
                
                # Create tender object
                tender = {
                    "id": f"tender_{hash(title + price_text)}",
                    "source": source["name"],
                    "title": title,
                    "description": description,
                    "price": price_text,
                    "deadline": deadline,
                    "link": link,
                    "scraped_at": datetime.utcnow().isoformat(),
                    "keywords_matched": [kw for kw in source["keywords"] if kw.lower() in title.lower()]
                }
                
                tenders.append(tender)
                
            except Exception as e:
                logger.warning(f"Failed to parse tender element: {str(e)}")
                continue
        
        return tenders
    
    async def _process_tender(self, tender: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process tender for quality and compliance checks
        
        Args:
            tender: Raw tender data
            
        Returns:
            Processed tender with quality metrics
        """
        # Add quality compliance fields
        tender["quality_verified"] = False
        tender["compliance_score"] = 0.0
        tender["risk_level"] = "unknown"
        tender["verification_needed"] = True
        
        # Check for chip-related keywords
        chip_keywords = ["чіп", "chip", "мікросхема", "microchip", "processor", "processor"]
        is_chip_tender = any(kw in tender["title"].lower() or kw in tender["description"].lower() 
                           for kw in chip_keywords)
        
        if is_chip_tender:
            tender["is_chip_tender"] = True
            # Add chip quality requirements
            tender["chip_requirements"] = {
                "performance_min": "TBD",
                "security_level": "standard",
                "reliability_target": 0.999,
                "verification_required": True
            }
        else:
            tender["is_chip_tender"] = False
        
        return tender
    
    async def get_tender_by_id(self, tender_id: str) -> Dict[str, Any]:
        """
        Get tender by ID
        
        Args:
            tender_id: Tender identifier
            
        Returns:
            Tender data or error message
        """
        if tender_id in self.tender_cache:
            return {
                "status": "success",
                "tender": self.tender_cache[tender_id]
            }
        else:
            return {
                "status": "error",
                "message": f"Tender {tender_id} not found"
            }
    
    async def start_monitoring_loop(self, interval_seconds: int = 3600):
        """
        Start continuous tender monitoring loop
        
        Args:
            interval_seconds: Check interval in seconds
        """
        logger.info(f"Starting tender monitoring loop with {interval_seconds}s interval")
        
        while True:
            try:
                await self.monitor_tenders()
                await asyncio.sleep(interval_seconds)
            except asyncio.CancelledError:
                logger.info("Tender monitoring loop cancelled")
                break
            except Exception as e:
                logger.error(f"Tender monitoring loop error: {str(e)}")
                await asyncio.sleep(interval_seconds)

# Global instance
tender_monitor = TenderMonitor()