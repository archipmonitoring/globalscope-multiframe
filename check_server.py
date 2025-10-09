import socket
import time

def check_server(host='localhost', port=5000, timeout=5):
    """Check if server is running on specified host and port"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception as e:
        print(f"Error checking server: {e}")
        return False

def main():
    print("Checking if HoloMesh web server is running...")
    
    if check_server():
        print("✓ Server is running on http://localhost:5000")
        print("You can access the web demo at:")
        print("  - Main page: http://localhost:5000/")
        print("  - Dashboard: http://localhost:5000/dashboard")
    else:
        print("✗ Server is not running")
        print("Please start the server using the run_web_demo.bat file or by running:")
        print("  cd web_demo && python app.py")

if __name__ == "__main__":
    main()