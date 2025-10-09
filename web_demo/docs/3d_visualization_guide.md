# HoloMesh 3D Visualization Guide

## Overview

This guide explains how to use and extend the 3D visualization features in the HoloMesh Web Demo. The visualization module uses Three.js to render interactive 3D representations of chip designs.

## Features

1. **Interactive 3D Rendering**: Rotate, zoom, and pan the 3D chip model
2. **Real-time Updates**: Visualization updates based on optimization results
3. **Responsive Design**: Adapts to different screen sizes
4. **Performance Optimized**: Efficient rendering using WebGL

## File Structure

```
web_demo/
├── static/
│   ├── js/
│   │   └── threejs_visualization.js  # Main visualization module
│   └── docs/
│       └── 3d_visualization_guide.md # This document
└── templates/
    └── index.html                    # Integration point
```

## Integration

The 3D visualization is integrated into the main page through:

1. A container div with ID `visualizationContainer`
2. Module import in the JavaScript section
3. Initialization in the DOMContentLoaded event

## API Endpoints

### GET /api/visualization-data

Returns data for 3D visualization:

```json
{
  "chip_dimensions": {
    "width": 3.0,
    "height": 0.2,
    "length": 3.0
  },
  "circuit_patterns": [
    {
      "width": 0.1,
      "length": 0.5,
      "position": {"x": 0.5, "y": 0.11, "z": 0.3},
      "rotation": 0.5
    }
  ],
  "connection_points": [
    {
      "position": {"x": 0.1, "y": 0.12, "z": 0.1}
    }
  ],
  "optimization_metrics": {
    "area": 85.5,
    "power_consumption": 12.3,
    "performance_score": 92.7
  }
}
```

## Customization

### Changing Visual Properties

To modify the appearance of the 3D model, edit the following in `threejs_visualization.js`:

1. **Colors**: Modify the color values in the material definitions
2. **Lighting**: Adjust the ambient and directional light properties
3. **Geometry**: Change the dimensions in the geometry definitions

### Adding New Elements

To add new elements to the visualization:

1. Create new geometry and material objects
2. Create a mesh with the geometry and material
3. Add the mesh to the scene or group

Example:
```javascript
// Create a new sphere
const geometry = new THREE.SphereGeometry(0.5, 32, 32);
const material = new THREE.MeshPhongMaterial({ color: 0xff0000 });
const sphere = new THREE.Mesh(geometry, material);
this.scene.add(sphere);
```

## Performance Considerations

1. **Limit Polygon Count**: Keep geometry complexity reasonable
2. **Use Instancing**: For repeated elements, use instanced meshes
3. **Optimize Textures**: Use compressed textures when possible
4. **Dispose Resources**: Clean up when components are removed

## Troubleshooting

### Visualization Not Loading

1. Check browser console for JavaScript errors
2. Verify Three.js library URLs are accessible
3. Ensure the container element exists in the DOM

### Poor Performance

1. Reduce the number of elements in the scene
2. Lower the renderer's pixel ratio for high-DPI screens
3. Implement level-of-detail (LOD) for complex models

## Future Enhancements

1. **Model Import**: Support for importing actual chip design files
2. **Animation**: Animated transitions between different optimization states
3. **Annotations**: Clickable elements with detailed information
4. **Export**: Save visualization as images or 3D models

## Contributing

To contribute to the 3D visualization features:

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Test thoroughly
5. Submit a pull request

## License

This visualization module is part of the GlobalScope MultiFrame CAD AI Optimization Platform.