# User Guide: Tender Monitoring

*Documentation also available in Ukrainian: [user_guide_tender_monitoring_uk.md](user_guide_tender_monitoring_uk.md)*

## Overview
This guide explains how to use the tender monitoring features in GlobalScope MultiFrame to track tender proposals in various procurement systems.

## Prerequisites
- Completed [Platform Overview and Architecture](user_guide_platform_overview.md)
- Basic understanding of tender and procurement concepts
- System account access

## Understanding Tender Monitoring

### What is Tender Monitoring?
Tender monitoring is a system for tracking tender proposals in various public procurement systems to identify business opportunities. In the context of GlobalScope MultiFrame, this includes:
- **ProZorro Monitoring**: Tracking tenders on the Ukrainian ProZorro platform
- **TED Monitoring**: Tracking tenders on the European TED platform
- **SAM.gov Monitoring**: Tracking tenders on the American SAM.gov platform
- **UNGM Monitoring**: Tracking tenders on the global UNGM platform
- **Notifications**: Automatic notifications about new tenders

### Tender Monitoring Features
The tender monitoring system offers several key capabilities:
- **Automatic Monitoring**: Regular scanning of tender platforms
- **Tender Filtering**: Filtering by categories, regions, and amounts
- **Notifications**: Instant notifications about relevant tenders
- **Tender Analysis**: Analysis of tender activity and trends
- **Data Export**: Export of tender information for further processing

## Setting Up Monitoring

### 1. Accessing Tender Monitoring
Accessing tender monitoring features:
1. Log into your GlobalScope MultiFrame account
2. Navigate to the "Procurement" module in the main menu
3. Click on "Tender Monitoring" in the left sidebar
4. Review available platforms for monitoring
5. Configure monitoring parameters

### 2. Selecting Platforms for Monitoring
Select platforms for tender monitoring:
1. Review the list of supported tender platforms
2. Activate monitoring for needed platforms
3. Configure scanning frequency for each platform
4. Set regions of interest for each platform
5. Save monitoring settings

### 3. Configuring Filters
Configure filters for tender monitoring:
1. Set tender categories for monitoring
2. Configure geographic filters
3. Set minimum and maximum tender amounts
4. Configure filters by customer types
5. Save filters for automatic application

## Monitoring Tenders

### 1. Viewing Active Tenders
Viewing active tenders:
1. Open the "Active Tenders" section
2. Review the list of recent tenders
3. Sort tenders by date, amount, or submission deadline
4. Filter tenders by categories or regions
5. Review details of each tender

### 2. Searching Tenders
Searching tenders by keywords:
1. Use the search bar to search for tenders
2. Enter keywords or phrases for search
3. Select platforms for search
4. Set time limits for search
5. Review search results

### 3. Analyzing Tender Activity
Analyzing tender activity:
1. Open the "Tender Analysis" section
2. Review tender activity charts
3. Analyze trends by categories
4. Compare activity of different regions
5. Identify seasonal patterns

## Tender Notifications

### 1. Configuring Notifications
Configure notifications about new tenders:
1. Open the "Notification Settings" section
2. Select notification types (email, push, SMS)
3. Configure notification frequency
4. Set priorities for different tender types
5. Save notification settings

### 2. Managing Notifications
Managing received notifications:
1. Review the list of received notifications
2. Filter notifications by type or date
3. Mark notifications as read
4. Archive important notifications
5. Configure automatic archiving rules

### 3. Exporting Information
Export tender information:
1. Select tenders for export
2. Select export format (CSV, Excel, PDF)
3. Configure fields for export
4. Add comments or notes
5. Start the export process

## Tender Analysis

### 1. Tender Statistics
Viewing tender activity statistics:
1. Open the "Statistics" section
2. Review overall tender statistics
3. Analyze statistics by platforms
4. Review statistics by categories
5. Compare statistics by periods

### 2. Trend Analysis
Analyzing tender trends:
1. Open the "Trend Analysis" section
2. Review tender activity charts
3. Analyze seasonal trends
4. Identify growing categories
5. Forecast future activity

### 3. Competitive Analysis
Analyzing competitive activity:
1. Open the "Competitive Analysis" section
2. Review the list of major participants
3. Analyze their tender activity
4. Compare participant success rates
5. Identify winner strategies

## Best Practices

### Monitoring
1. Regularly update monitoring filters
2. Set realistic expectations for tender quantity
3. Use multiple platforms for maximum coverage
4. Configure notifications for quick response
5. Document successful tender participation strategies

### Analysis
1. Regularly analyze tender activity
2. Use analytical tools to identify patterns
3. Compare your success with competitors
4. Adapt strategies based on analysis
5. Forecast future opportunities

### Security
1. Protect credentials for accessing tender platforms
2. Regularly update passwords
3. Monitor unauthorized access
4. Use two-factor authentication
5. Archive important information

## Troubleshooting

### Common Issues and Solutions

#### Issue: No New Tenders
- **Cause**: Too strict filters or connection issues
- **Solution**: Check filters, verify platform connections, contact support

#### Issue: Notification Delays
- **Cause**: High load or network issues
- **Solution**: Check network connection, configure notification frequency, contact support

#### Issue: Incorrect Tender Information
- **Cause**: Data source errors or synchronization issues
- **Solution**: Check original sources, contact support

#### Issue: Export Errors
- **Cause**: Insufficient access rights or technical issues
- **Solution**: Check access rights, contact support

#### Issue: Platform Unavailability
- **Cause**: Platform technical issues or integration problems
- **Solution**: Check platform status, contact support

## Related Features
- [Platform Overview and Architecture](user_guide_platform_overview.md)
- [Partner Program](user_guide_partner_program.md)
- [System Configuration](user_guide_system_configuration.md)
- [User Management](user_guide_user_management.md)
- [Health Check Monitoring](user_guide_health_check_monitoring.md)

## API Reference
For programmatic tender monitoring, refer to the following API endpoints:
- `POST /api/v1/tender/monitor` - Start tender monitoring
- `GET /api/v1/tender/list` - Get list of tenders
- `GET /api/v1/tender/search` - Search tenders by criteria
- `GET /api/v1/tender/statistics` - Get tender statistics
- `POST /api/v1/tender/export` - Export tender information

For detailed API documentation, see [API Documentation](api_documentation.md).