import requests
import json
import time

def check_server_running():
    """Check if the server is running"""
    try:
        response = requests.get("http://localhost:5000", timeout=5)
        return response.status_code == 200
    except:
        return False

def test_web_ui():
    """Test the enhanced web UI endpoints"""
    base_url = "http://localhost:5000"
    
    # Check if server is running
    print("Checking if HoloMesh web server is running...")
    if not check_server_running():
        print("⚠️  Server is not running. Please start the server first using run_web_demo.bat")
        print("   Then run this test script again.")
        return
    
    print("✓ Server is running. Testing web UI...")
    print("")
    
    # Test main page
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        print(f"✅ Main page status code: {response.status_code}")
        print(f"   Content length: {len(response.text)} characters")
    except Exception as e:
        print(f"❌ Error accessing main page: {e}")
    
    # Test dashboard page
    try:
        response = requests.get(f"{base_url}/dashboard", timeout=10)
        print(f"✅ Dashboard page status code: {response.status_code}")
        print(f"   Content length: {len(response.text)} characters")
    except Exception as e:
        print(f"❌ Error accessing dashboard page: {e}")
    
    # Test API endpoints
    try:
        response = requests.get(f"{base_url}/api/modes", timeout=10)
        print(f"✅ API modes endpoint status code: {response.status_code}")
        if response.status_code == 200:
            modes = response.json()
            print(f"   Available modes: {[mode['value'] for mode in modes]}")
    except Exception as e:
        print(f"❌ Error accessing modes API: {e}")
    
    try:
        response = requests.get(f"{base_url}/api/tools", timeout=10)
        print(f"✅ API tools endpoint status code: {response.status_code}")
        if response.status_code == 200:
            tools = response.json()
            print(f"   Available tools: {[tool['value'] for tool in tools]}")
    except Exception as e:
        print(f"❌ Error accessing tools API: {e}")
    
    print("")
    print("🎉 Web UI test completed!")

if __name__ == "__main__":
    test_web_ui()