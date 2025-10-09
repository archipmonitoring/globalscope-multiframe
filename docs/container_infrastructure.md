# Container Infrastructure Documentation

## Overview

The GlobalScope MultiFrame 11.0 platform uses Docker containers to provide a consistent and reproducible environment for chip design workflows. This documentation covers the container infrastructure with CAD tools integration.

## API Integration

The CAD tools are accessible through REST API endpoints that allow users to run simulations, synthesis, and place-and-route operations programmatically.

### CAD Tools API Endpoints

1. **Tool Availability Check** - `GET /api/v1/cad/tools/available`
2. **Tool Versions** - `GET /api/v1/cad/tools/versions`
3. **Verilator Simulation** - `POST /api/v1/cad/verilator/simulate`
4. **Yosys Synthesis** - `POST /api/v1/cad/yosys/synthesize`
5. **NextPNR Place and Route** - `POST /api/v1/cad/nextpnr/pnr`
6. **CAD Health Check** - `GET /api/v1/cad/health`
7. **CAD Results** - `GET /api/v1/cad/result/{tool}/{project_id}`

### CAD Monitoring API Endpoints

1. **CAD Monitoring Health** - `GET /api/v1/monitoring/cad/health`
2. **Overall CAD Metrics** - `GET /api/v1/monitoring/cad/overall`
3. **All CAD Tool Metrics** - `GET /api/v1/monitoring/cad/all`
4. **Specific Tool Metrics** - `GET /api/v1/monitoring/cad/tool/{tool_name}`
5. **Top CAD Tools** - `GET /api/v1/monitoring/cad/top-tools`

### Authentication

All CAD API endpoints require proper authentication through the platform's authentication system.

### Rate Limiting

API calls are subject to rate limiting to ensure fair usage of computational resources.

### Available Endpoints

1. **Tool Availability Check** - `GET /api/v1/cad/tools/available`
2. **Tool Versions** - `GET /api/v1/cad/tools/versions`
3. **Verilator Simulation** - `POST /api/v1/cad/verilator/simulate`
4. **Yosys Synthesis** - `POST /api/v1/cad/yosys/synthesize`
5. **NextPNR Place and Route** - `POST /api/v1/cad/nextpnr/pnr`
6. **CAD Health Check** - `GET /api/v1/cad/health`
7. **CAD Results** - `GET /api/v1/cad/result/{tool}/{project_id}`

### Authentication

All CAD API endpoints require proper authentication through the platform's authentication system.

### Rate Limiting

API calls are subject to rate limiting to ensure fair usage of computational resources.

## Container Architecture

### Core Services

1. **holomisha-core-cad** - Main application service with CAD tools
2. **redis-master** - Data storage and caching
3. **kong** - API gateway and load balancing
4. **prometheus** - Monitoring and metrics collection
5. **grafana** - Visualization and dashboard
6. **cad-worker** - Background worker for CAD operations

## Docker Images

### Base Image
- **Ubuntu 22.04** - Latest LTS version for stability and security

### Installed CAD Tools

1. **Verilator 4.224** - Fast and robust Verilog simulator
2. **Yosys 0.36** - Framework for Verilog RTL synthesis
3. **NextPNR 0.6** - Portable FPGA place and route tool
4. **Icarus Verilog** - Verilog simulation and synthesis tool
5. **GTKWave** - Waveform viewer

### System Dependencies

- Python 3.10+
- Build tools (gcc, make, cmake)
- Development libraries (Boost, Eigen3)
- Qt5 for GUI components
- Security tools and utilities

## Dockerfile Structure

### Base Setup
```dockerfile
FROM ubuntu:22.04

# System dependencies installation
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-dev \
    build-essential cmake git wget curl \
    clang llvm libboost-all-dev libeigen3-dev \
    qtbase5-dev qt5-qmake libqt5svg5-dev \
    # ... additional dependencies
```

### CAD Tool Installation

#### Verilator
```dockerfile
# Install Verilator
RUN git clone https://github.com/verilator/verilator.git /verilator \
    && cd /verilator \
    && git checkout v4.224 \
    && autoconf \
    && ./configure \
    && make -j$(nproc) \
    && make install
```

#### Yosys
```dockerfile
# Install Yosys
RUN git clone https://github.com/YosysHQ/yosys.git /yosys \
    && cd /yosys \
    && git checkout yosys-0.36 \
    && make -j$(nproc) \
    && make install
```

#### NextPNR
```dockerfile
# Install NextPNR
RUN git clone https://github.com/YosysHQ/nextpnr.git /nextpnr \
    && cd /nextpnr \
    && git checkout nextpnr-0.6 \
    && cmake . -DARCH=generic \
    && make -j$(nproc) \
    && make install
```

### Verification
```dockerfile
# Verify CAD tools installation
RUN verilator --version && \
    yosys -V && \
    nextpnr-generic --version && \
    iverilog -V
```

## Docker Compose Configuration

### Service Definitions

#### Main Application Service
```yaml
holomisha-core-cad:
  build:
    context: .
    dockerfile: Dockerfile.cad
  ports:
    - "8000:8000"
  environment:
    - REDIS_HOST=redis-master
    - CAD_TOOLS_AVAILABLE=true
  depends_on:
    - redis-master
  volumes:
    - ./projects:/app/projects
    - ./chip_designs:/app/chip_designs
    - /var/run/docker.sock:/var/run/docker.sock
  privileged: true
  cap_add:
    - SYS_ADMIN
  security_opt:
    - seccomp:unconfined
```

#### Redis Service
```yaml
redis-master:
  image: redis:7.0
  ports:
    - "6379:6379"
  volumes:
    - redis_data:/data
  command: redis-server --appendonly yes
```

#### Kong API Gateway
```yaml
kong:
  image: kong:3.0
  environment:
    - KONG_DATABASE=off
    - KONG_PROXY_ACCESS_LOG=/dev/stdout
    - KONG_ADMIN_ACCESS_LOG=/dev/stdout
  ports:
    - "8001:8001"
    - "8000:8000"
  depends_on:
    - holomisha-core-cad
```

#### Monitoring Services
```yaml
prometheus:
  image: prom/prometheus:v2.45.0
  ports:
    - "9090:9090"
  volumes:
    - ./prometheus.yml:/etc/prometheus/prometheus.yml
    - prometheus_data:/prometheus
  command:
    - '--config.file=/etc/prometheus/prometheus.yml'
    - '--storage.tsdb.path=/prometheus'
    - '--storage.tsdb.retention.time=200h'
    - '--web.enable-lifecycle'

grafana:
  image: grafana/grafana:9.5.2
  ports:
    - "3000:3000"
  environment:
    - GF_SECURITY_ADMIN_PASSWORD=admin
  volumes:
    - grafana_data:/var/lib/grafana
  depends_on:
    - prometheus
```

#### CAD Worker Service
```yaml
cad-worker:
  build:
    context: .
    dockerfile: Dockerfile.cad
  command: ["python3", "-m", "src.chip_design.cad_worker"]
  environment:
    - REDIS_HOST=redis-master
    - WORKER_TYPE=cad
  depends_on:
    - redis-master
  volumes:
    - ./projects:/app/projects
    - ./chip_designs:/app/chip_designs
    - /var/run/docker.sock:/var/run/docker.sock
  privileged: true
  cap_add:
    - SYS_ADMIN
  security_opt:
    - seccomp:unconfined
```

## Security Considerations

### Privileged Mode
CAD tools may require privileged access for:
- Hardware acceleration
- Device access
- Low-level system operations

### Capabilities
- **SYS_ADMIN** - Required for some CAD operations
- **seccomp:unconfined** - For unrestricted system calls

### Volume Mounts
- **./projects** - Persistent storage for design projects
- **./chip_designs** - Storage for chip design files
- **/var/run/docker.sock** - Docker daemon access for container operations

## Performance Optimization

### Resource Allocation
- Multi-core builds using `make -j$(nproc)`
- Shared volumes for efficient file access
- Redis caching for frequently accessed data

### Container Isolation
- Separate services for different functions
- Resource limits to prevent one service from monopolizing resources
- Health checks for automatic restart on failure

## Troubleshooting

### Common Issues

1. **CAD Tools Not Found**
   - Verify installation in Dockerfile
   - Check PATH environment variables
   - Ensure tools are in `/usr/local/bin`

2. **Permission Denied**
   - Check privileged mode settings
   - Verify volume mount permissions
   - Confirm user permissions in container

3. **Build Failures**
   - Check dependency versions
   - Verify system requirements
   - Review build logs for specific errors

### Diagnostic Commands

```bash
# Check if CAD tools are available
docker-compose exec holomisha-core-cad verilator --version
docker-compose exec holomisha-core-cad yosys -V
docker-compose exec holomisha-core-cad nextpnr-generic --version

# Check directory permissions
docker-compose exec holomisha-core-cad ls -la /app/projects
docker-compose exec holomisha-core-cad ls -la /app/chip_designs

# Check running processes
docker-compose exec holomisha-core-cad ps aux
```

## Testing

### Automated Tests
Unit tests are available in [test_cad_tools.py](../tests/test_cad_tools.py) to verify:
- Tool availability
- Directory creation
- Basic functionality of CAD operations

### Manual Verification
```bash
# Run the test suite
cd e:\papka_fail\MG\GlobalScope MultiFrame-13
python -m pytest tests/test_cad_tools.py -v
```

## Best Practices

### Container Management
- Use specific version tags for reproducibility
- Regularly update base images for security patches
- Minimize layers in Dockerfile for faster builds
- Clean up temporary files after installation

### CAD Tool Usage
- Validate input files before processing
- Implement proper error handling
- Use firewall validation for security
- Cache results for performance

### Monitoring
- Monitor resource usage
- Track build times and success rates
- Log errors and warnings
- Set up alerts for critical failures

## Future Enhancements

### Planned Improvements
1. **Multi-architecture support** for ARM-based systems
2. **GPU acceleration** for compute-intensive operations
3. **Distributed computing** for large-scale designs
4. **Enhanced security** with reduced privileges where possible
5. **Automated updates** for CAD tools

### Scalability
- Horizontal scaling for worker processes
- Load balancing for high-demand operations
- Caching strategies for frequently used designs
- Database optimization for large datasets

This container infrastructure provides a robust foundation for chip design workflows with full CAD tool integration while maintaining security and performance best practices.