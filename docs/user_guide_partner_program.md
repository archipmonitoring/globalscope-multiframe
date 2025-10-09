# User Guide: Partner Program

*Documentation also available in Ukrainian: [user_guide_partner_program_uk.md](user_guide_partner_program_uk.md)*

## Overview
This guide explains how to use the partner program features in GlobalScope MultiFrame to register partners, obtain government subscriptions, and place government orders.

## Prerequisites
- Completed [Platform Overview and Architecture](user_guide_platform_overview.md)
- Basic understanding of partnership and integration concepts
- System account access
- Access to partner API keys

## Understanding the Partner Program

### What is the Partner Program?
The partner program is a system for integrating with external services and organizations to extend the functionality of the GlobalScope MultiFrame platform. In the context of the program, this includes:
- **Partner Registration**: Integration with supported services
- **Government Subscriptions**: Free access for government structures
- **Government Orders**: Special terms for government orders
- **Regional Support**: Support for different regions and jurisdictions

### Partner Program Features
The partner program offers several key capabilities:
- **Partner Registration**: Registration of new partners in the system
- **Government Subscriptions**: Activation of free subscriptions for government
- **Government Orders**: Placement of special orders for government
- **API Key Management**: Management of partner access keys
- **Regional Support**: Support for different regions and languages

## Partner Registration

### 1. Accessing the Partner Program
Accessing partner program features:
1. Log into your GlobalScope MultiFrame account
2. Navigate to the "Partnership" module in the main menu
3. Click on "Partner Program" in the left sidebar
4. Review the list of supported partners
5. Select "Register New Partner" to begin the process

### 2. Selecting Partner Type
Select the partner type for registration:
1. Review the list of supported partners
2. Select the appropriate partner type from the list
3. Review the registration requirements
4. Check partner availability in regions
5. Click "Continue" to proceed to the next step

### 3. Entering Partner Data
Enter data for partner registration:
1. Enter the user ID for registration
2. Enter the partner name
3. Enter the partner API key
4. Select the partner's region of operation
5. Confirm registration to complete the process

## Government Subscriptions

### 1. Activating Government Subscription
Activating free government subscription:
1. Navigate to the "Government Subscriptions" section
2. Enter the government structure user ID
3. Select the government structure region
4. Confirm subscription activation
5. Check activation status in the event log

### 2. Managing Government Subscriptions
Managing active government subscriptions:
1. Review the list of active government subscriptions
2. Filter subscriptions by region or date
3. Review details of each subscription
4. Update subscription status when needed
5. Revoke subscriptions that are no longer needed

### 3. Usage Monitoring
Monitoring government subscription usage:
1. Open the "Usage Monitoring" section
2. Review subscription usage statistics
3. Analyze usage trends
4. Identify anomalies in usage
5. Generate usage reports

## Government Orders

### 1. Placing Government Orders
Placing special government orders:
1. Navigate to the "Government Orders" section
2. Enter the government structure user ID
3. Enter chip data for the order
4. Select the region for order fulfillment
5. Confirm order placement

### 2. Order Tracking
Tracking government order status:
1. Review the list of active government orders
2. Filter orders by region or date
3. Review details of each order
4. Receive notifications about status changes
5. Export order history for reporting

### 3. Order Management
Managing government orders:
1. Update order fulfillment status
2. Add comments to orders
3. Assign responsible personnel for fulfillment
4. Set fulfillment deadlines
5. Close completed orders

## API Key Management

### 1. API Key Generation
Generating new API keys for partners:
1. Open the "API Key Management" section
2. Select the partner for key generation
3. Configure access rights for the key
4. Set key expiration date
5. Generate and save the new API key

### 2. Key Usage Monitoring
Monitoring API key usage:
1. Review key usage statistics
2. Analyze request frequency
3. Identify suspicious activity
4. Configure alerts for limit exceedances
5. Block compromised keys

### 3. Key Revocation
Revoking inactive or compromised keys:
1. Select the key to revoke
2. Verify the reason for revocation
3. Confirm revocation
4. Notify the partner about revocation
5. Generate a new key if needed

## Best Practices

### Partner Integration
1. Verify compatibility with supported services
2. Document all integrations
3. Regularly update API keys
4. Monitor integration performance
5. Have backup plans for critical integrations

### Government Services
1. Ensure high security level for government data
2. Comply with all regulatory requirements
3. Prioritize government orders
4. Ensure transparency in order fulfillment
5. Regularly report on government activity

### Security
1. Use strong API keys
2. Regularly update access keys
3. Monitor all API requests
4. Set limits on request quantity
5. Block suspicious activity

## Troubleshooting

### Common Issues and Solutions

#### Issue: Unsupported Partner
- **Cause**: Attempt to register an unsupported partner
- **Solution**: Check the list of supported partners, contact support to add a new partner

#### Issue: Invalid API Key
- **Cause**: Incorrect or expired API key
- **Solution**: Check key expiration, generate a new key, contact support

#### Issue: Government Subscription Activation Error
- **Cause**: Incorrect user ID or region
- **Solution**: Verify user data, confirm region, contact support

#### Issue: Unable to Place Government Order
- **Cause**: No active subscription or technical issues
- **Solution**: Check for subscription, contact support

#### Issue: API Limits Exceeded
- **Cause**: Too many requests
- **Solution**: Check limits, optimize requests, contact support to increase limits

## Related Features
- [Platform Overview and Architecture](user_guide_platform_overview.md)
- [System Configuration](user_guide_system_configuration.md)
- [Tender Monitoring](user_guide_tender_monitoring.md)
- [User Management](user_guide_user_management.md)
- [Health Check Monitoring](user_guide_health_check_monitoring.md)

## API Reference
For programmatic management of the partner program, refer to the following API endpoints:
- `POST /api/v1/partner/register` - Register a new partner
- `POST /api/v1/partner/government/subscription` - Activate government subscription
- `POST /api/v1/partner/government/order` - Place government order
- `GET /api/v1/partner/list` - Get list of partners
- `POST /api/v1/partner/apikey/generate` - Generate new API key

For detailed API documentation, see [API Documentation](api_documentation.md).