import sys
import os

# Change to the web_demo directory
os.chdir(os.path.join(os.path.dirname(__file__), 'web_demo'))

# Add the web_demo directory to the path
sys.path.append(os.getcwd())

# Import and run the Flask app
from app import app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)