# User Guide: System Configuration

*Documentation also available in Ukrainian: [user_guide_system_configuration_uk.md](user_guide_system_configuration_uk.md)*

## Overview
This guide explains how to use the system configuration features in GlobalScope MultiFrame to manage platform settings and system parameters.

## Prerequisites
- Completed [Platform Overview and Architecture](user_guide_platform_overview.md)
- Basic understanding of system administration concepts
- System administrator account access

## Understanding System Configuration

### What is System Configuration?
System configuration is a set of parameters and settings that define the behavior of the GlobalScope MultiFrame platform. In the context of the system, this includes:
- **Flexible Configuration**: Ability to change system parameters in real-time
- **Persistent Storage**: Permanent storage of configurations in Redis
- **Parameter Management**: Centralized management of all system parameters
- **Secure Updates**: Protected configuration updates with logging

### System Configuration Features
The configuration system offers several key capabilities:
- **Parameter Updates**: Ability to update any system parameters
- **Persistent Storage**: Storage of configurations across reboots
- **Change Logging**: Recording of all configuration changes for audit
- **Parameter Validation**: Verification of entered values correctness
- **Change Rollback**: Ability to revert to previous settings

## Accessing the Admin Panel

### 1. Logging In
Logging into the admin panel:
1. Log into your GlobalScope MultiFrame account
2. Ensure you have administrator rights
3. Navigate to the "Administration" module in the main menu
4. Click on "Admin Panel" in the left sidebar
5. Pass additional authentication if required

### 2. Panel Navigation
Navigating the admin panel:
1. Familiarize yourself with the admin panel sections
2. Use the sidebar to navigate between sections
3. Use search to find specific parameters
4. Review configuration change history
5. Use bookmarks for quick access to frequently used settings

### 3. Viewing Current Configuration
Viewing current system configuration:
1. Open the "Configuration" section in the admin panel
2. Review general information about current configuration
3. Use filters to group parameters
4. Export configuration for backup
5. Compare current configuration with previous versions

## Updating System Parameters

### 1. Searching for Parameters
Searching for required system parameters:
1. Use the search bar to find parameters
2. Use categories to filter parameters
3. Review the description of each parameter before changing
4. Check the current parameter value
5. Review possible parameter values

### 2. Changing Parameters
Changing system parameters:
1. Select the parameter you want to change
2. Click the "Edit" button next to the parameter
3. Enter the new parameter value
4. Verify the correctness of the entered value
5. Confirm changes and apply them

### 3. Saving Configurations
Saving modified configurations:
1. Review all modified parameters before saving
2. Add a comment to changes for future audit
3. Select the "Save Configuration" option
4. Confirm saving with persistent storage
5. Verify saving success in the event log

## Configuration Management

### 1. Change History
Viewing configuration change history:
1. Open the "Configuration History" section
2. Review the list of all configuration changes
3. Filter changes by date, user, or parameter
4. Review details of each change
5. Export history for audit

### 2. Change Rollback
Rolling back configuration changes:
1. Select a previous configuration version from history
2. Review differences between versions
3. Confirm the need for rollback
4. Apply configuration rollback
5. Verify system stability after rollback

### 3. Backup
Creating configuration backups:
1. Open the "Backup" section
2. Select the current configuration for backup
3. Specify the backup storage location
4. Add description and tags for identification
5. Start the backup creation process

## Configuration Security

### 1. Access Control
Managing access to configurations:
1. Configure user roles for configuration access
2. Set restrictions on changing critical parameters
3. Configure two-factor authentication for administrators
4. Set access expiration for configurations
5. Monitor unauthorized access attempts

### 2. Change Logging
Monitoring configuration changes:
1. Review the log of all configuration changes
2. Configure alerts for critical changes
3. Analyze change patterns to detect anomalies
4. Export logs for external audit
5. Archive change history for long-term storage

### 3. Parameter Validation
Verifying configuration parameter correctness:
1. Use built-in validators to check values
2. Configure custom validation rules for parameters
3. Check parameter compatibility before changing
4. Test changes in an isolated environment
5. Restore previous values when errors are detected

## Best Practices

### Configuration Management
1. Document all configuration changes
2. Use test environments for experiments
3. Regularly create configuration backups
4. Establish naming standards for parameters
5. Conduct regular configuration audits

### Security
1. Restrict configuration access to authorized personnel only
2. Use strong passwords and two-factor authentication
3. Regularly update the system and fix vulnerabilities
4. Monitor all configuration changes
5. Establish recovery mechanisms after incidents

### Reliability
1. Check compatibility of changes before applying
2. Use rollback mechanisms when problems occur
3. Test critical changes in an isolated environment
4. Monitor system stability after changes
5. Have a recovery plan for critical failures

## Troubleshooting

### Common Issues and Solutions

#### Issue: Unable to save configuration
- **Cause**: Insufficient access rights or connection issues
- **Solution**: Check access rights, verify Redis connection, contact the main administrator

#### Issue: Incorrect parameter values
- **Cause**: Input errors or incorrect values
- **Solution**: Use validators, check compatibility, rollback changes

#### Issue: Configuration loss after reboot
- **Cause**: Incorrect configuration saving
- **Solution**: Ensure persistent storage option is selected, check Redis connection

#### Issue: Parameter conflicts
- **Cause**: Incompatible parameter values
- **Solution**: Check documentation, use compatibility checking tools

#### Issue: Slow admin panel operation
- **Cause**: Large number of parameters or network issues
- **Solution**: Optimize filters, check network connection, contact support

## Related Features
- [Platform Overview and Architecture](user_guide_platform_overview.md)
- [Partner Program](user_guide_partner_program.md)
- [Health Check Monitoring](user_guide_health_check_monitoring.md)
- [User Management](user_guide_user_management.md)
- [Tender Monitoring](user_guide_tender_monitoring.md)

## API Reference
For programmatic management of configurations, refer to the following API endpoints:
- `POST /api/v1/admin/config/update` - Update system configuration
- `GET /api/v1/admin/config/current` - Get current configuration
- `GET /api/v1/admin/config/history` - Get configuration change history
- `POST /api/v1/admin/config/rollback` - Rollback configuration to previous version
- `POST /api/v1/admin/config/backup` - Create configuration backup

For detailed API documentation, see [API Documentation](api_documentation.md).