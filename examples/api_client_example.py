"""
API Client Example for GlobalScope MultiFrame 11.0
This file demonstrates how to use the GlobalScope MultiFrame 11.0 API.
"""
import requests
import json
import asyncio
import websockets

class GlobalScopeAPIClient:
    """Client for interacting with the GlobalScope MultiFrame 11.0 API."""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session_token = None
    
    def login(self, username, token):
        """Authenticate with the API."""
        url = f"{self.base_url}/auth/login"
        data = {
            "username": username,
            "token": token
        }
        response = requests.post(url, json=data)
        if response.status_code == 200 and response.json().get("status") == "success":
            self.session_token = response.json().get("session_token")
            print("Login successful")
            return True
        else:
            print("Login failed")
            return False
    
    def logout(self, session_id):
        """Logout from the API."""
        url = f"{self.base_url}/auth/logout"
        data = {
            "session_id": session_id
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("Logout successful")
            return True
        else:
            print("Logout failed")
            return False
    
    def create_chip_process(self, process_id, chip_data):
        """Create a new chip design process."""
        url = f"{self.base_url}/chip/process"
        data = {
            "process_id": process_id,
            "chip_data": chip_data
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print(f"Chip process {process_id} created successfully")
            return response.json()
        else:
            print(f"Failed to create chip process {process_id}")
            return None
    
    def ensure_zero_defect(self, user_id, chip_id, chip_data, lang="uk"):
        """Run zero defect engine."""
        url = f"{self.base_url}/chip/zero-defect"
        data = {
            "user_id": user_id,
            "chip_id": chip_id,
            "chip_data": chip_data,
            "lang": lang
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print(f"Zero defect process for chip {chip_id} completed successfully")
            return response.json()
        else:
            print(f"Failed to run zero defect process for chip {chip_id}")
            return None
    
    def get_chip_metrics(self, chip_id):
        """Get metrics for a chip."""
        url = f"{self.base_url}/analytics/metrics/{chip_id}"
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Metrics for chip {chip_id} retrieved successfully")
            return response.json()
        else:
            print(f"Failed to retrieve metrics for chip {chip_id}")
            return None
    
    def get_chip_trends(self, chip_id, hours=24):
        """Get trends for a chip."""
        url = f"{self.base_url}/analytics/trends/{chip_id}?hours={hours}"
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Trends for chip {chip_id} retrieved successfully")
            return response.json()
        else:
            print(f"Failed to retrieve trends for chip {chip_id}")
            return None
    
    def get_security_threats(self):
        """Get security threats."""
        url = f"{self.base_url}/security/threats"
        response = requests.get(url)
        if response.status_code == 200:
            print("Security threats retrieved successfully")
            return response.json()
        else:
            print("Failed to retrieve security threats")
            return None
    
    def generate_rtl_hash(self, rtl_code, algorithm="sha256"):
        """Generate RTL hash."""
        url = f"{self.base_url}/hash/rtl"
        data = {
            "rtl_code": rtl_code,
            "algorithm": algorithm
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("RTL hash generated successfully")
            return response.json()
        else:
            print("Failed to generate RTL hash")
            return None
    
    def run_quantum_simulation(self, chip_id, sim_type, params):
        """Run quantum simulation."""
        url = f"{self.base_url}/simulate/quantum/{chip_id}"
        data = {
            "sim_type": sim_type,
            "params": params
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print(f"Quantum simulation for chip {chip_id} completed successfully")
            return response.json()
        else:
            print(f"Failed to run quantum simulation for chip {chip_id}")
            return None
    
    def check_health(self):
        """Check system health."""
        url = f"{self.base_url}/health/"
        response = requests.get(url)
        if response.status_code == 200:
            print("Health check completed successfully")
            return response.json()
        else:
            print("Health check failed")
            return None

async def connect_to_ar_websocket(base_url="ws://localhost:8000"):
    """Connect to the AR WebSocket."""
    websocket_url = f"{base_url.replace('http', 'ws')}/ws/ar"
    try:
        async with websockets.connect(websocket_url) as websocket:
            print("Connected to AR WebSocket")
            while True:
                message = await websocket.recv()
                print(f"Received: {message}")
    except Exception as e:
        print(f"WebSocket connection error: {e}")

def main():
    """Main function demonstrating API usage."""
    # Create API client
    client = GlobalScopeAPIClient()
    
    # Login
    if client.login("SuperHoloMisha", "super_token"):
        # Create chip process
        chip_data = {
            "type": "quantum_chip",
            "params": {
                "cores": 4,
                "frequency": 3.5
            }
        }
        client.create_chip_process("process_1", chip_data)
        
        # Run zero defect engine
        client.ensure_zero_defect("SuperHoloMisha", "chip_1", chip_data)
        
        # Get chip metrics
        client.get_chip_metrics("chip_1")
        
        # Get chip trends
        client.get_chip_trends("chip_1", 24)
        
        # Get security threats
        client.get_security_threats()
        
        # Generate RTL hash
        client.generate_rtl_hash("module example; endmodule")
        
        # Run quantum simulation
        client.run_quantum_simulation("chip_1", "OPTIMIZATION", {"qubits": 10})
        
        # Check health
        client.check_health()
        
        # Logout
        client.logout("session_SuperHoloMisha_123")
    
    print("API client example completed")

if __name__ == "__main__":
    main()