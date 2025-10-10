// web_demo/static/js/threejs_visualization.js
// 3D Visualization for HoloMesh using A-Frame

export class HoloMesh3DVisualizer {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.scene = null;
        this.chipEntity = null;
        this.init();
    }

    init() {
        if (!this.container) return;

        // Create A-Frame scene
        this.scene = document.createElement('a-scene');
        this.scene.setAttribute('embedded', '');
        this.scene.setAttribute('vr-mode-ui', 'enabled: false');

        // Add assets
        const assets = document.createElement('a-assets');
        const texture = document.createElement('img');
        texture.id = 'chipTexture';
        texture.src = '/static/images/chip_texture.jpg';
        assets.appendChild(texture);
        this.scene.appendChild(assets);

        // Add camera
        const cameraEntity = document.createElement('a-entity');
        cameraEntity.setAttribute('position', '0 1.6 3');
        const camera = document.createElement('a-camera');
        camera.setAttribute('look-controls', 'enabled: true');
        camera.setAttribute('wasd-controls', 'enabled: false');
        cameraEntity.appendChild(camera);
        this.scene.appendChild(cameraEntity);

        // Add chip model
        this.chipEntity = document.createElement('a-entity');
        this.chipEntity.id = 'chipModel';
        this.chipEntity.setAttribute('position', '0 1.5 -1');
        this.chipEntity.setAttribute('rotation', '0 45 0');

        const chipBox = document.createElement('a-box');
        chipBox.setAttribute('width', '3');
        chipBox.setAttribute('height', '0.2');
        chipBox.setAttribute('depth', '3');
        chipBox.setAttribute('color', '#6a11cb');
        chipBox.setAttribute('src', '#chipTexture');
        chipBox.setAttribute('shadow', 'cast: true; receive: true');
        this.chipEntity.appendChild(chipBox);

        // Add circuit patterns
        const pattern1 = document.createElement('a-box');
        pattern1.setAttribute('width', '0.1');
        pattern1.setAttribute('height', '0.02');
        pattern1.setAttribute('depth', '0.5');
        pattern1.setAttribute('position', '0.5 0.11 0.3');
        pattern1.setAttribute('rotation', '0 0 0');
        pattern1.setAttribute('color', '#2575fc');
        chipBox.appendChild(pattern1);

        const pattern2 = document.createElement('a-box');
        pattern2.setAttribute('width', '0.15');
        pattern2.setAttribute('height', '0.02');
        pattern2.setAttribute('depth', '0.3');
        pattern2.setAttribute('position', '-0.7 0.11 -0.4');
        pattern2.setAttribute('rotation', '0 0 0');
        pattern2.setAttribute('color', '#ff00cc');
        chipBox.appendChild(pattern2);

        const pattern3 = document.createElement('a-box');
        pattern3.setAttribute('width', '0.08');
        pattern3.setAttribute('height', '0.02');
        pattern3.setAttribute('depth', '0.7');
        pattern3.setAttribute('position', '0.2 0.11 0.8');
        pattern3.setAttribute('rotation', '0 0 0');
        pattern3.setAttribute('color', '#28a745');
        chipBox.appendChild(pattern3);

        this.scene.appendChild(this.chipEntity);

        // Add lighting
        const ambientLight = document.createElement('a-light');
        ambientLight.setAttribute('type', 'ambient');
        ambientLight.setAttribute('color', '#445');
        this.scene.appendChild(ambientLight);

        const directionalLight = document.createElement('a-light');
        directionalLight.setAttribute('type', 'directional');
        directionalLight.setAttribute('color', '#fff');
        directionalLight.setAttribute('intensity', '0.5');
        directionalLight.setAttribute('position', '-1 2 1');
        this.scene.appendChild(directionalLight);

        const pointLight = document.createElement('a-light');
        pointLight.setAttribute('type', 'point');
        pointLight.setAttribute('color', '#6a11cb');
        pointLight.setAttribute('intensity', '0.8');
        pointLight.setAttribute('position', '2 3 -1');
        this.scene.appendChild(pointLight);

        // Add environment
        const sky = document.createElement('a-sky');
        sky.setAttribute('color', '#0f0c29');
        this.scene.appendChild(sky);

        // Add scene to container
        this.container.innerHTML = '';
        this.container.appendChild(this.scene);
    }

    updateChipModel(data) {
        if (!this.chipEntity) return;

        // Update chip properties based on optimization data
        const chipBox = this.chipEntity.querySelector('a-box');
        if (data.optimized_params) {
            // Example: change color based on efficiency
            const efficiency = data.final_metrics?.resource_efficiency || 0.5;
            const hue = Math.floor(efficiency * 120); // 0-120 (red to green)
            chipBox.setAttribute('color', `hsl(${hue}, 100%, 50%)`);
        }

        // Animate update
        this.chipEntity.setAttribute('animation', {
            property: 'rotation',
            to: `0 ${parseInt(this.chipEntity.getAttribute('rotation').y) + 360} 0`,
            dur: 1000,
            easing: 'easeInOutQuad'
        });
    }
}