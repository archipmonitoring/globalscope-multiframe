# HoloMesh Web Demo

Interactive web demonstration of HoloMesh Interaction Modes for CAD AI Optimization.

## Quick Start

To run the web demo quickly, simply execute the batch file:

```batch
run_web_demo.bat
```

Then open your browser and navigate to http://localhost:5000

## Overview

This web demo provides an interactive interface to experience the HoloMesh interaction modes:
- Professional Mode
- Innovative Mode
- Semi-Automatic Mode
- Manual Mode

## Features

- Real-time simulation of optimization processes
- Visual representation of different interaction modes
- Performance metrics display
- Configuration details visualization
- Responsive design for all devices
- **Interactive 3D chip design visualization** (NEW!)
- Live statistics and performance monitoring

## Requirements

- Python 3.7+
- Flask
- Bootstrap 5
- Font Awesome
- Modern web browser with WebGL support

## Installation

```bash
# Navigate to the web_demo directory
cd web_demo

# Install required packages
pip install flask
```

## Running the Demo

You can run the demo in several ways:

### Option 1: Using the batch file (Windows)

Double-click on `run_web_demo.bat` in the main project directory, or run from command line:

```batch
..\run_web_demo.bat
```

### Option 2: Manual execution

```bash
# Navigate to the web_demo directory
cd web_demo

# Run the Flask application
python app.py
```

### Option 3: Using the start_server.py script

From the main project directory:

```bash
python start_server.py
```

After starting the server, open your browser and navigate to:
- Main page: http://localhost:5000/
- Dashboard: http://localhost:5000/dashboard

## Usage

1. Select a CAD tool (Yosys, NextPNR, or Verilator)
2. Choose an interaction mode by clicking on the mode cards
3. Select an optimization strategy
4. Enable/disable confidentiality for Manual Mode
5. Click "Run Optimization" to see the results
6. **Interact with the 3D visualization** using mouse controls

## 3D Visualization Features (NEW!)

The HoloMesh Web Demo now includes interactive 3D visualization of chip designs:

- Rotate the model by clicking and dragging
- Zoom in/out using the mouse wheel
- Pan by holding Shift and dragging
- Update the visualization with the "Update Visualization" button

The visualization uses Three.js and WebGL for high-performance rendering.

## Architecture

The demo consists of:
- Flask backend for API endpoints
- HTML/CSS/JavaScript frontend with Bootstrap
- Three.js for 3D visualization
- Integration with the core CAD AI Optimizer

## Testing

To test the web UI, you can run:

```batch
..\test_web_ui.bat
```

Or from command line:

```bash
python ..\test_web_ui.py
```

## Customization

You can customize the demo by modifying:
- `app.py` - Backend logic and API endpoints
- `templates/index.html` - Frontend interface
- `templates/dashboard.html` - Dashboard interface
- `static/styles.css` - Additional CSS styles
- `static/js/threejs_visualization.js` - 3D visualization module

## HoloMesh Interaction Modes

### Professional Mode
Standard optimization for general CAD tasks with clean architectural separation.

### Innovative Mode
Creative exploration and experimental optimization for research and development.

### Semi-Automatic Mode
Human-AI collaboration with HoloMesh recommendations:
- Easy switching between professional and innovative tools
- Error elimination through AI assistance
- Multi-tool operation through HoloMesh interface

### Manual Mode
Professional tool guidance with confidentiality controls:
- HoloMesh acts as a guide and reference center
- Consultations on demand without interfering with development
- Confidentiality enabled by default
- Option to disable confidentiality for system learning

## Documentation

Additional documentation can be found in:
- [3D Visualization Guide](docs/3d_visualization_guide.md)
- [Roadmap](../HOLOMESH_WEB_DEMO_ROADMAP.md)
- [Implementation Summary](../HOLOMESH_WEB_DEMO_SUMMARY.md)

## Contributing

We welcome contributions to improve the HoloMesh Web Demo. Please follow the standard contribution guidelines.

## License

This project is part of the GlobalScope MultiFrame CAD AI Optimization Platform.

## Contact

For questions or support, please contact the GlobalScope development team.