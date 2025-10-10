// web_demo/index.js
// Node.js server for WebXR service

const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const path = require('path');

const app = express();
const server = http.createServer(app);
const io = socketIo(server, {
    cors: {
        origin: "*",
        methods: ["GET", "POST"]
    }
});

// Serve static files
app.use(express.static(path.join(__dirname, 'public')));

// Serve A-Frame
app.get('/aframe.min.js', (req, res) => {
    res.sendFile(path.join(__dirname, 'node_modules/aframe/dist/aframe.min.js'));
});

// WebSocket connection
io.on('connection', (socket) => {
    console.log('User connected to WebXR service');

    // Handle AR notifications
    socket.on('ar_notification', (data) => {
        console.log('AR Notification:', data);
        // Broadcast to all clients
        io.emit('ar_update', data);
    });

    // Handle chip visualization requests
    socket.on('visualize_chip', (data) => {
        console.log('Visualizing chip:', data);
        // Broadcast to all clients
        io.emit('chip_visualization', data);
    });

    socket.on('disconnect', () => {
        console.log('User disconnected from WebXR service');
    });
});

// Start server
const PORT = process.env.PORT || 5001;
server.listen(PORT, () => {
    console.log(`WebXR service running on port ${PORT}`);
});