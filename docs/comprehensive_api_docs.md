# Comprehensive API Documentation for GlobalScope MultiFrame 11.0

*Документація також доступна українською мовою: [comprehensive_api_docs_uk.md](comprehensive_api_docs_uk.md)*

# Comprehensive API Documentation for GlobalScope MultiFrame 11.0

## Overview
This document provides detailed documentation for all API endpoints in the GlobalScope MultiFrame 11.0 platform. Each endpoint includes detailed descriptions, parameters, request/response examples, and error conditions.

## Base URL
```
http://localhost:8000
```

## Authentication
Most endpoints require authentication. Use the `/auth/login` endpoint to obtain a session token.

## API Endpoints by Functional Area

### 1. System Management

#### GET /system/
**Description**: Root endpoint that returns the system status.

**Response**:
```json
{
  "status": "online",
  "message": "HoloMisha programs the universe!"
}
```

#### POST /system/mode/{mode}
**Description**: Set the system execution mode.

**Parameters**:
- `mode` (path): The execution mode (DEVELOPMENT, PRODUCTION, TESTING)

**Response**:
```json
{
  "status": "success",
  "mode": "PRODUCTION"
}
```

**Error Response**:
```json
{
  "status": "error",
  "message": "Invalid mode"
}
```

### 2. Authentication

#### POST /auth/login
**Description**: Authenticate a user and obtain a session token.

**Parameters**:
- `username` (body): The user's username
- `token` (body): The authentication token

**Request**:
```json
{
  "username": "SuperHoloMisha",
  "token": "super_secret_token"
}
```

**Response**:
```json
{
  "status": "success",
  "session_id": "session_12345",
  "user_id": "user_123"
}
```

**Error Response**:
```json
{
  "status": "error",
  "message": "Invalid credentials"
}
```

#### POST /auth/logout
**Description**: Terminate a user session.

**Parameters**:
- `session_id` (body): The session ID to terminate

**Request**:
```json
{
  "session_id": "session_12345"
}
```

**Response**:
```json
{
  "status": "success",
  "message": "Session terminated"
}
```

### 3. Chip Design

#### POST /chip/process
**Description**: Create a new chip design process.

**Parameters**:
- `process_id` (body): Unique identifier for the process
- `chip_data` (body): Data describing the chip to be designed

**Request**:
```json
{
  "process_id": "process_001",
  "chip_data": {
    "type": "quantum_processor",
    "cores": 128,
    "frequency": "4.5GHz"
  }
}
```

**Response**:
```json
{
  "status": "success",
  "process_id": "process_001",
  "message": "Process initialized"
}
```

**Error Response**:
```json
{
  "status": "error",
  "message": "Security validation failed"
}
```

#### POST /chip/zero-defect
**Description**: Ensure a chip design is defect-free.

**Parameters**:
- `user_id` (body): ID of the user initiating the process
- `chip_id` (body): ID of the chip to validate
- `chip_data` (body): Data describing the chip
- `lang` (query): Language for notifications (default: "uk")

**Request**:
```json
{
  "user_id": "user_123",
  "chip_id": "chip_001",
  "chip_data": {
    "type": "quantum_processor",
    "cores": 128,
    "frequency": "4.5GHz"
  }
}
```

**Response**:
```json
{
  "status": "success",
  "chip_id": "chip_001",
  "message": "Zero-defect validation passed"
}
```

### 4. Analytics

#### GET /analytics/metrics/{chip_id}
**Description**: Retrieve performance metrics for a specific chip.

**Parameters**:
- `chip_id` (path): ID of the chip to analyze

**Response**:
```json
{
  "status": "success",
  "chip_id": "chip_001",
  "metrics": {
    "performance": 95.5,
    "efficiency": 87.2,
    "temperature": 45.3
  }
}
```

#### GET /analytics/trends/{chip_id}
**Description**: Analyze performance trends for a specific chip.

**Parameters**:
- `chip_id` (path): ID of the chip to analyze
- `hours` (query): Number of hours to analyze (default: 24)

**Response**:
```json
{
  "status": "success",
  "chip_id": "chip_001",
  "trends": {
    "performance": [92.1, 93.5, 94.2, 95.5],
    "efficiency": [85.2, 86.1, 86.8, 87.2],
    "temperature": [42.1, 43.5, 44.2, 45.3]
  }
}
```

### 5. Security

#### GET /security/threats
**Description**: Retrieve information about blocked security threats.

**Response**:
```json
{
  "status": "success",
  "threats_blocked": 42,
  "recent_threats": [
    {
      "type": "DDoS",
      "timestamp": "2025-09-29T10:30:00Z",
      "source": "192.168.1.100"
    }
  ]
}
```

### 6. Hash Generation

#### POST /hash/rtl
**Description**: Generate a hash for RTL code.

**Parameters**:
- `rtl_code` (body): The RTL code to hash
- `algorithm` (body): Hash algorithm to use (default: "sha256")

**Request**:
```json
{
  "rtl_code": "module example(...",
  "algorithm": "sha256"
}
```

**Response**:
```json
{
  "status": "success",
  "hash": "a1b2c3d4e5f6...",
  "algorithm": "sha256"
}
```

### 7. Quantum Simulation

#### POST /simulate/quantum/{chip_id}
**Description**: Run a quantum simulation for a chip design.

**Parameters**:
- `chip_id` (path): ID of the chip to simulate
- `sim_type` (body): Type of simulation (OPTIMIZATION, VALIDATION, PERFORMANCE)
- `params` (body): Simulation parameters

**Request**:
```json
{
  "sim_type": "OPTIMIZATION",
  "params": {
    "qubits": 128,
    "iterations": 1000
  }
}
```

**Response**:
```json
{
  "status": "success",
  "chip_id": "chip_001",
  "results": {
    "optimized_design": "...",
    "performance_improvement": 15.5
  }
}
```

**Error Response**:
```json
{
  "status": "error",
  "message": "Invalid simulation type"
}
```

### 8. Collaboration

#### POST /chip/collaboration/
**Description**: Start a collaboration session for chip design.

**Parameters**:
- `user_id` (body): ID of the user initiating collaboration
- `chip_id` (body): ID of the chip to collaborate on
- `chip_data` (body): Data describing the chip
- `collaborators` (body): List of user IDs to collaborate with
- `lang` (query): Language for notifications (default: "uk")

**Request**:
```json
{
  "user_id": "user_123",
  "chip_id": "chip_001",
  "chip_data": {
    "type": "quantum_processor",
    "cores": 128
  },
  "collaborators": ["user_456", "user_789"]
}
```

**Response**:
```json
{
  "status": "success",
  "collab_id": "collab_001",
  "chip_id": "chip_001",
  "message": "Collaboration started"
}
```

#### POST /chip/collaboration/update
**Description**: Update an existing collaboration session.

**Parameters**:
- `user_id` (body): ID of the user updating the collaboration
- `collab_id` (body): ID of the collaboration to update
- `update_data` (body): Data to update the collaboration with
- `lang` (query): Language for notifications (default: "uk")

**Request**:
```json
{
  "user_id": "user_123",
  "collab_id": "collab_001",
  "update_data": {
    "status": "in_progress",
    "notes": "Completed initial design review"
  }
}
```

**Response**:
```json
{
  "status": "success",
  "collab_id": "collab_001",
  "message": "Collaboration updated"
}
```

### 9. Driver Generation

#### POST /chip/driver/
**Description**: Generate a driver for a chip.

**Parameters**:
- `user_id` (body): ID of the user generating the driver
- `chip_id` (body): ID of the chip to generate a driver for
- `chip_data` (body): Data describing the chip
- `lang` (query): Language for notifications (default: "uk")

**Request**:
```json
{
  "user_id": "user_123",
  "chip_id": "chip_001",
  "chip_data": {
    "type": "quantum_processor",
    "cores": 128
  }
}
```

**Response**:
```json
{
  "status": "success",
  "driver_id": "driver_001",
  "chip_id": "chip_001",
  "message": "Driver generated"
}
```

#### POST /chip/driver/firmware/update
**Description**: Update firmware for a chip driver.

**Parameters**:
- `user_id` (body): ID of the user updating the firmware
- `driver_id` (body): ID of the driver to update
- `update_data` (body): Data for the firmware update
- `lang` (query): Language for notifications (default: "uk")

**Request**:
```json
{
  "user_id": "user_123",
  "driver_id": "driver_001",
  "update_data": {
    "version": "2.1.0",
    "changelog": "Performance improvements"
  }
}
```

**Response**:
```json
{
  "status": "success",
  "driver_id": "driver_001",
  "message": "Firmware updated"
}
```

### 10. Voice Commands

#### POST /voice/design
**Description**: Create a chip design using voice commands.

**Parameters**:
- `user_id` (body): ID of the user giving the voice command
- `voice_input` (body): The voice command text
- `lang` (query): Language for processing (default: "uk")

**Request**:
```json
{
  "user_id": "user_123",
  "voice_input": "Design a quantum processor with 128 cores"
}
```

**Response**:
```json
{
  "status": "success",
  "design_id": "design_001",
  "message": "Voice design processed"
}
```

#### POST /voice/quest
**Description**: Initiate a learning quest using voice commands.

**Parameters**:
- `user_id` (body): ID of the user giving the voice command
- `voice_input` (body): The voice command text
- `quest_id` (body): ID of the quest to initiate
- `lang` (query): Language for processing (default: "uk")

**Request**:
```json
{
  "user_id": "user_123",
  "voice_input": "Start quantum design tutorial",
  "quest_id": "quest_001"
}
```

**Response**:
```json
{
  "status": "success",
  "quest_id": "quest_001",
  "message": "Quest initiated"
}
```

### 11. BCI Interface

#### POST /bci/command
**Description**: Process a command from a Brain-Computer Interface.

**Parameters**:
- `user_id` (body): ID of the user sending the BCI command
- `command` (body): The BCI command
- `lang` (query): Language for processing (default: "uk")

**Request**:
```json
{
  "user_id": "user_123",
  "command": "design_chip"
}
```

**Response**:
```json
{
  "status": "success",
  "command": "design_chip",
  "message": "BCI command processed"
}
```

## Error Handling

All API endpoints follow consistent error handling patterns:

### Common Error Responses

#### 400 Bad Request
```json
{
  "status": "error",
  "message": "Invalid request parameters"
}
```

#### 401 Unauthorized
```json
{
  "status": "error",
  "message": "Authentication required"
}
```

#### 403 Forbidden
```json
{
  "status": "error",
  "message": "Access denied"
}
```

#### 404 Not Found
```json
{
  "status": "error",
  "message": "Resource not found"
}
```

#### 429 Too Many Requests
```json
{
  "status": "error",
  "message": "Rate limit exceeded"
}
```

#### 500 Internal Server Error
```json
{
  "status": "error",
  "message": "Internal server error"
}
```

## Rate Limiting

The API implements rate limiting to prevent abuse:
- 100 requests per minute per IP address
- 1000 requests per hour per authenticated user

Exceeding these limits will result in a 429 Too Many Requests response.

## Versioning

The API version is specified in the URL path:
```
http://localhost:8000/v1/endpoint
```

Currently, version 1.0.0 is available.

## WebSocket API

### WebSocket /ws/ar
**Description**: Real-time communication for AR notifications.

**Connection**:
```
WebSocket ws://localhost:8000/ws/ar
```

**Messages**:
- Client can send any text message (echoed back)
- Server sends AR notifications in real-time

## Support

For support, contact the GlobalScope MultiFrame team at support@holomisha.com.