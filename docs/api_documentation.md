# GlobalScope MultiFrame 11.0 API Documentation

*Документація також доступна українською мовою: [api_documentation_uk.md](api_documentation_uk.md)*

# GlobalScope MultiFrame 11.0 API Documentation

## Overview
This document provides comprehensive documentation for the GlobalScope MultiFrame 11.0 API. The API is organized into functional areas to provide clear separation of concerns and ease of use.

## Base URL
```
http://localhost:8000
```

## Authentication
Most endpoints require authentication. Use the `/auth/login` endpoint to obtain a session token.

## API Endpoints

### System Endpoints
- `GET /system/` - Root endpoint
- `POST /system/mode/{mode}` - Set system mode

### Authentication Endpoints
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout

### Chip Design Endpoints
- `POST /chip/process` - Create chip process
- `POST /chip/zero-defect` - Ensure zero defect chip design

### Analytics Endpoints
- `GET /analytics/metrics/{chip_id}` - Get chip metrics
- `GET /analytics/trends/{chip_id}` - Get chip trends

### Security Endpoints
- `GET /security/threats` - Get security threats

### Hash Generation Endpoints
- `POST /hash/rtl` - Generate RTL hash

### Quantum Simulation Endpoints
- `POST /simulate/quantum/{chip_id}` - Run quantum simulation

### Collaboration Endpoints
- `POST /chip/collaboration/` - Start collaboration
- `POST /chip/collaboration/update` - Update collaboration

### Driver Generation Endpoints
- `POST /chip/driver/` - Generate driver
- `POST /chip/driver/firmware/update` - Update firmware

### Voice Command Endpoints
- `POST /voice/design` - Voice design
- `POST /voice/quest` - Voice quest

### BCI Interface Endpoints
- `POST /bci/command` - BCI command

### Community Endpoints
- `POST /community/forum/create` - Create forum
- `POST /community/post/add` - Add post
- `POST /community/ip/share` - Share IP block
- `POST /community/chat` - Send chat message

### Designer Network Endpoints
- `POST /designer/register` - Register designer
- `POST /designer/connect` - Connect designer
- `POST /designer/rate` - Rate designer

### Fabrication Endpoints
- `GET /fab/analytics/{fab_name}` - Get fab analytics

### AI Service Endpoints
- `GET /ai/trend/analyze/{chip_id}` - AI trend analysis
- `GET /ai/strategy/predict` - AI strategy prediction

### Auto Scaling Endpoints
- `POST /auto/scale` - Auto scale

### VR Training Endpoints
- `POST /vr/training/` - Start VR training

### IP Block Generation Endpoints
- `POST /ip/block/generate` - Generate IP block
- `POST /ip/block/publish` - Publish IP block
- `POST /ip/block/purchase` - Purchase IP block
- `POST /ip/block/calculate` - Calculate IP block parameters

### Marketplace Endpoints
- `POST /marketplace/design/upload` - Upload design
- `POST /marketplace/quantum/chip/design` - Quantum chip design
- `POST /marketplace/learning/quest/create` - Create learning quest

### DAO Voting Endpoints
- `POST /dao/interactive/tour` - Interactive tour

### Web3 Integration Endpoints
- `POST /web3/nft/mint` - Mint NFT
- `POST /web3/nft/transfer` - Transfer NFT

### IoT Integration Endpoints
- `POST /iot/connect` - Connect to IoT

### Zero Day Protection Endpoints
- `POST /zero/day/scan` - Scan for zero day vulnerabilities
- `POST /zero/day/mitigate` - Mitigate zero day vulnerabilities

### Partner Program Endpoints
- `POST /partner/register` - Register partner
- `POST /partner/government/subscription` - Government subscription
- `POST /partner/government/order` - Government order

### Tender Monitoring Endpoints
- `POST /tender/monitor` - Monitor tenders

### Admin Panel Endpoints
- `POST /admin/config/update` - Update configuration

### Health Check Endpoints
- `GET /health/` - Health check

## WebSocket Endpoints
- `WebSocket /ws/ar` - AR WebSocket connection

## Error Responses
All endpoints return a consistent error response format:
```json
{
  "status": "error",
  "message": "Error description"
}
```

## Success Responses
Most endpoints return a consistent success response format:
```json
{
  "status": "success",
  "data": {}
}
```

## Rate Limiting
The API implements rate limiting to prevent abuse. Exceeding the rate limit will result in a 429 Too Many Requests response.

## Versioning
The API version is specified in the URL path. Currently, version 1.0.0 is available.

## Support
For support, contact the GlobalScope MultiFrame team.