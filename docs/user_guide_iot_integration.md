# User Guide: IoT Integration

*Documentation also available in Ukrainian: [user_guide_iot_integration_uk.md](user_guide_iot_integration_uk.md)*

## Overview
This guide explains how to use the IoT integration features in GlobalScope MultiFrame to connect to fabs through MQTT and OPC UA protocols for real-time data acquisition.

## Prerequisites
- Completed [Platform Overview and Architecture](user_guide_platform_overview.md)
- Basic understanding of IoT concepts and industrial protocols
- System account access
- Access to integrated fabs

## Understanding IoT Integration

### What is IoT Integration?
IoT integration is a system for connecting to fabs through Internet of Things protocols to obtain real-time data. In the context of GlobalScope MultiFrame, this includes:
- **MQTT Connection**: Using the MQTT protocol for data exchange
- **OPC UA Connection**: Using the OPC UA protocol for integration with industrial systems
- **Data Collection**: Automatic collection of data from fab equipment
- **Real-time Monitoring**: Tracking production parameters in real-time

### IoT Integration Features
The IoT integration system offers several key capabilities:
- **Protocol Support**: Support for MQTT and OPC UA protocols
- **Automatic Connection**: Automatic establishment of connections to fabs
- **Secure Data Transfer**: Protected data transfer between fabs and the platform
- **Connection Status Monitoring**: Tracking connection statuses
- **Event Logging**: Recording connection and data transfer events

## Connecting to Fabs

### 1. Accessing the IoT Section
Access IoT integration features:
1. Log into your GlobalScope MultiFrame account
2. Navigate to the "Manufacturing" module in the main menu
3. Click on "IoT Integration" in the left sidebar
4. Review the list of available fabs for connection

### 2. Selecting a Fab for Connection
Select a fab for connection:
1. Review the list of integrated fabs
2. Select the fab you want to connect to
3. Check the availability of the fab for connection
4. Review supported protocols
5. Click "Connect" to establish the connection

### 3. Selecting Connection Protocol
Select a protocol for connection:
1. Choose between MQTT or OPC UA protocols
2. Check connection settings for the selected protocol
3. Enter required authentication parameters
4. Configure connection security parameters
5. Confirm connection to establish communication

## Connection Monitoring

### 1. Viewing Connection Status
View fab connection statuses:
1. Open the "Connection Status" panel
2. Review the list of active connections
3. Check the last connection time
4. Review data transfer statistics
5. Track any connection errors

### 2. Tracking Data Transfer
Track real-time data transfer:
1. Navigate to the "Data Monitoring" section
2. Select a connection for monitoring
3. Review the incoming data stream
4. Analyze the frequency and volume of data transferred
5. Track data delays and losses

### 3. Event Logging
Review connection event logs:
1. Open the "Event Logs" section
2. Filter events by type or time
3. Review details of each event
4. Analyze errors and warnings
5. Export logs for further analysis

## IoT Connection Security

### 1. Connection Authentication
Configure authentication for IoT connections:
1. Set credentials for each fab
2. Use certificates for secure connection
3. Configure two-factor authentication
4. Regularly update access keys
5. Monitor unauthorized access attempts

### 2. Data Encryption
Ensure data encryption:
1. Use TLS/SSL for data transfer encryption
2. Configure message-level encryption
3. Use secure encryption algorithms
4. Regularly update encryption certificates
5. Verify the integrity of transferred data

### 3. Security Monitoring
Monitor IoT connection security:
1. Use intrusion detection systems
2. Configure alerts for suspicious activities
3. Regularly check security logs
4. Implement access security policies
5. Conduct security audits of connections

## Connection Parameter Configuration

### 1. Protocol Configuration
Configure connection protocol parameters:
1. Select protocol (MQTT or OPC UA)
2. Configure connection parameters
3. Set timeouts and retry intervals
4. Configure quality of service parameters
5. Save configuration for future connections

### 2. Certificate Management
Manage security certificates:
1. Upload fab certificates
2. Update certificate expiration dates
3. Revoke compromised certificates
4. Configure automatic certificate updates
5. Archive certificate history

### 3. Automatic Connection Setup
Configure automatic connection:
1. Set automatic connection rules
2. Configure retry conditions
3. Set maximum connection attempt count
4. Configure connection status notifications
5. Test automatic connection operation

## Best Practices

### Connection Management
1. Regularly check connection statuses
2. Set up backup connection options
3. Monitor communication channel performance
4. Document connection configurations
5. Conduct regular maintenance

### Security
1. Use strong passwords and certificates
2. Regularly update software
3. Limit access to critical systems
4. Monitor connection activity
5. Implement the principle of least privilege

### Reliability
1. Set up failure recovery mechanisms
2. Use backup communication channels
3. Configure automatic reconnection
4. Monitor communication quality
5. Conduct regular connection testing

## Troubleshooting

### Common Issues and Solutions

#### Issue: Unable to connect to fab
- **Cause**: Incorrect connection parameters or network issues
- **Solution**: Check connection parameters, test network connection, contact support

#### Issue: Data loss during transfer
- **Cause**: Unstable network connection or equipment issues
- **Solution**: Check network connection, configure transfer buffers, contact support

#### Issue: Authentication errors
- **Cause**: Invalid credentials or expired certificates
- **Solution**: Update credentials, check certificate expiration dates, contact support

#### Issue: High data transfer latency
- **Cause**: Network congestion or equipment issues
- **Solution**: Optimize transfer parameters, check equipment, contact support

#### Issue: Unsupported protocol
- **Cause**: Fab uses an unsupported protocol
- **Solution**: Check supported protocols, contact administrator, contact support

## Related Features
- [Platform Overview and Architecture](user_guide_platform_overview.md)
- [Fab Analytics](user_guide_fab_analytics.md)
- [Auto Scaling](user_guide_auto_scaling.md)
- [Quantum Security](user_guide_quantum_security.md)
- [Threat Monitoring](user_guide_threat_monitoring.md)

## API Reference
For programmatic management of IoT integration, refer to the following API endpoints:
- `POST /api/v1/iot/connect` - Connect to fab
- `GET /api/v1/iot/status/{fab_name}` - Get connection status
- `GET /api/v1/iot/data/{fab_name}` - Get real-time data
- `POST /api/v1/iot/disconnect` - Disconnect from fab
- `GET /api/v1/iot/logs/{fab_name}` - Get event logs

For detailed API documentation, see [API Documentation](api_documentation.md).