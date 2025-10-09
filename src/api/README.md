# GlobalScope MultiFrame 11.0 API

## Overview

*Документація також доступна українською мовою: [README_uk.md](README_uk.md)*

*Дивіться [політику мови](../../docs/language_policy.md) для отримання додаткової інформації про мовні версії.*

## Overview
This directory contains the API implementation for the GlobalScope MultiFrame 11.0 chip design platform. The API is built using FastAPI and provides RESTful endpoints for all system functionality.

## Directory Structure
```
src/api/
├── __init__.py          # Package initialization
├── main_app.py          # Main FastAPI application
├── api_config.py        # API router registration
├── routers.py           # All API endpoints organized by functionality
└── README.md            # This file
```

## Key Files

### main_app.py
The main FastAPI application that serves as the entry point for the API. It:
- Creates the FastAPI app instance
- Configures middleware (CORS, etc.)
- Registers all API routers
- Handles startup and shutdown events

### api_config.py
Contains the `register_routers` function that registers all API routers with the main application. This provides a centralized location for router management.

### routers.py
Contains all API endpoints organized by functional areas:
- System Management
- Authentication
- Chip Design
- Analytics
- Security
- Simulation
- Collaboration
- Community
- Marketplace
- Integration
- Administration

## Functional Areas

Each functional area has its own router with appropriate tags and prefixes:

1. **System** (`/system`) - Root endpoint and system mode management
2. **Authentication** (`/auth`) - User login/logout
3. **Chip Design** (`/chip`) - Chip process creation and zero defect engineering
4. **Analytics** (`/analytics`) - Chip metrics and trend analysis
5. **Security** (`/security`) - Threat monitoring and zero-day protection
6. **Hash Generation** (`/hash`) - RTL hash generation
7. **Quantum Simulation** (`/simulate/quantum`) - Quantum Monte Carlo simulations
8. **Collaboration** (`/chip/collaboration`) - Family collaboration features
9. **Driver Generation** (`/chip/driver`) - Chip driver generation
10. **Voice Commands** (`/voice`) - Voice-based chip design
11. **BCI Interface** (`/bci`) - Brain-Computer Interface commands
12. **Community** (`/community`) - Forum and chat functionality
13. **Designer Network** (`/designer`) - Designer registration and connection
14. **Fabrication** (`/fab`) - Fab analytics
15. **AI Services** (`/ai`) - AI trend analysis and strategy prediction
16. **Auto Scaling** (`/auto/scale`) - Automatic resource scaling
17. **VR Training** (`/vr/training`) - Virtual reality training
18. **IP Block Generation** (`/ip/block`) - IP block creation and management
19. **Marketplace** (`/marketplace`) - IP block trading and learning quests
20. **DAO Voting** (`/dao`) - Decentralized Autonomous Organization voting
21. **IoT Integration** (`/iot`) - Internet of Things integration
22. **Web3 Integration** (`/web3`) - NFT minting and transferring
23. **Zero Day Protection** (`/zero/day`) - Zero-day vulnerability protection
24. **Partner Program** (`/partner`) - Partner registration and management
25. **Tender Monitoring** (`/tender`) - Tender monitoring
26. **Admin Panel** (`/admin`) - Administration functions
27. **Health Check** (`/health`) - System health monitoring
28. **CAD Enhancements** (`/api/v1/cad/enhancements`) - Caching, task queue, and WebSocket progress for CAD operations

## WebSocket Endpoints

### AR WebSocket (`/ws/ar`)
Real-time communication for AR notifications and updates.

## Usage

### Starting the API Server
```bash
uvicorn src.api.main_app:app --host 0.0.0.0 --port 8000
```

### API Documentation
Once the server is running, API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

### Running Tests
```bash
python -m pytest tests/test_api.py
```

## Extending the API

### Adding New Endpoints
1. Add new endpoint functions to `routers.py` in the appropriate router
2. If creating a new functional area, create a new router
3. Register the new router in `api_config.py`

### Adding New Functional Areas
1. Create a new router in `routers.py`
2. Add the router to the imports in `api_config.py`
3. Register the router in the `register_routers` function

## Design Principles

1. **Separation of Concerns** - Each functional area is isolated
2. **Consistent Error Handling** - Standardized error response format
3. **Type Safety** - Pydantic models for request/response validation
4. **Documentation** - OpenAPI/Swagger annotations for all endpoints
5. **Asynchronous Processing** - All endpoints are async for maximum throughput
6. **Event-Driven Architecture** - Decoupled communication through event bus

## Security

1. **Authentication** - Token-based authentication for protected endpoints
2. **Input Validation** - Pydantic models validate all inputs
3. **Rate Limiting** - Built-in rate limiting to prevent abuse
4. **CORS** - Configured to allow only trusted origins

## Performance

1. **Asynchronous Processing** - Non-blocking I/O for maximum throughput
2. **Connection Pooling** - Efficient database and service connections
3. **Caching** - Appropriate caching for improved performance

## Database

The system uses Redis as its primary data store with the following key patterns:

- `user:*` - User profiles and authentication data
- `driver:*` - Generated chip drivers
- `collab:*` - Collaboration sessions
- `process:*` - Chip design processes
- `nft:*` - Web3 NFT records
- `quest:*` - Learning quests
- `config:*` - System configuration
- `analytics:*` - Performance metrics

Counters for generating unique IDs:
- `driver_counter`
- `collab_counter`
- `process_counter`
- `quest_counter`
- `nft_counter`

## Demo Data

To initialize the database with demo data for testing:

```bash
python init_demo_data.py
```

To verify the demo data was loaded correctly:

```bash
python verify_demo_data.py
```

## Monitoring

1. **Health Checks** - `/health/` endpoint for system status
2. **Logging** - Comprehensive logging for debugging and auditing
3. **Metrics** - Performance metrics collection