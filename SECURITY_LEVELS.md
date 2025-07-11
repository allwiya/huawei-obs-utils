# 🔒 Multi-Level Security System

## Overview

OBS Utils implements a sophisticated multi-level security system that provides different levels of access control based on the sensitivity and risk level of operations.

## 🎯 Security Levels

### 🟢 Level 1: READ_ONLY
**Risk Level**: Low  
**Password Required**: None  
**Color Code**: Green

#### Allowed Operations:
- ✅ List objects in buckets
- ✅ Search for objects
- ✅ Download objects
- ✅ View object metadata
- ✅ Generate download URLs

#### Use Cases:
- Data analysts reviewing files
- Backup verification
- Content auditing
- Report generation

#### Example Commands:
```bash
# List objects (no password required)
python obs_utils_improved.py --operation list --bucket my-bucket

# Search for files
python obs_utils_improved.py --operation search --search-text "backup"

# Download files
python obs_utils_improved.py --operation download --bucket my-bucket --prefix "reports/"
```

---

### 🟡 Level 2: STANDARD
**Risk Level**: Medium  
**Password Required**: Operator Password  
**Color Code**: Yellow

#### Allowed Operations:
- ✅ All READ_ONLY operations
- ✅ Archive objects to COLD storage
- ✅ Move objects to WARM storage
- ✅ Restore archived objects
- ✅ Change storage classes
- ✅ Set object metadata

#### Use Cases:
- Regular data management
- Storage optimization
- Lifecycle management
- Cost optimization

#### Example Commands:
```bash
# Archive old files (requires operator password)
python obs_utils_improved.py --operation archive --bucket my-bucket --prefix "old-files/"

# Restore archived files
python obs_utils_improved.py --operation restore --bucket my-bucket --prefix "archived/"
```

---

### 🟠 Level 3: DESTRUCTIVE
**Risk Level**: High  
**Password Required**: Supervisor Password  
**Color Code**: Orange

#### Allowed Operations:
- ✅ All STANDARD operations
- ⚠️ Delete individual objects
- ⚠️ Delete multiple objects
- ⚠️ Empty bucket contents
- ⚠️ Modify critical metadata

#### Use Cases:
- Data cleanup operations
- Compliance requirements
- Storage space management
- Emergency data removal

#### Example Commands:
```bash
# Delete specific objects (requires supervisor password)
python obs_utils_improved.py --operation delete --bucket my-bucket --prefix "temp/"

# Bulk delete operations
python obs_utils_improved.py --operation bulk-delete --bucket my-bucket --file delete-list.txt
```

---

### 🔴 Level 4: ADMIN
**Risk Level**: Critical  
**Password Required**: Administrator Password  
**Color Code**: Red

#### Allowed Operations:
- ✅ All DESTRUCTIVE operations
- 🚨 Create/delete buckets
- 🚨 Modify bucket policies
- 🚨 Change security settings
- 🚨 Manage user permissions
- 🚨 System configuration changes

#### Use Cases:
- System administration
- Security configuration
- Infrastructure management
- Emergency system recovery

#### Example Commands:
```bash
# Create new bucket (requires admin password)
python obs_utils_improved.py --operation create-bucket --bucket new-bucket

# Modify security settings
python obs_utils_improved.py --operation configure-security --enable-encryption
```

## 🔐 Password Management

### Setting Up Security Levels
```bash
# Enable multi-level security
python obs_utils_improved.py --enable-security-levels

# Set individual passwords
python obs_utils_improved.py --set-operator-password
python obs_utils_improved.py --set-supervisor-password
python obs_utils_improved.py --set-admin-password
```

### Password Requirements

#### Operator Password
- **Minimum Length**: 8 characters
- **Complexity**: Letters and numbers
- **Rotation**: Every 90 days

#### Supervisor Password
- **Minimum Length**: 12 characters
- **Complexity**: Letters, numbers, and symbols
- **Rotation**: Every 60 days

#### Administrator Password
- **Minimum Length**: 16 characters
- **Complexity**: Strong mix of all character types
- **Rotation**: Every 30 days

## 🛡️ Security Implementation

### Authentication Flow
```
1. User initiates operation
2. System determines required security level
3. If password required:
   a. Prompt for password
   b. Verify against encrypted hash
   c. Grant/deny access
4. Execute operation with appropriate permissions
```

### Encryption Details
- **Algorithm**: AES-256-GCM
- **Key Derivation**: PBKDF2 with SHA-256
- **Salt**: Unique per password
- **Iterations**: 100,000+

### Session Management
- **Session Timeout**: 30 minutes of inactivity
- **Auto-lock**: After 3 failed attempts
- **Session Logging**: All activities recorded

## 📊 Security Level Matrix

| Operation | READ_ONLY | STANDARD | DESTRUCTIVE | ADMIN |
|-----------|-----------|----------|-------------|-------|
| List objects | ✅ | ✅ | ✅ | ✅ |
| Download | ✅ | ✅ | ✅ | ✅ |
| Search | ✅ | ✅ | ✅ | ✅ |
| Archive | ❌ | ✅ | ✅ | ✅ |
| Restore | ❌ | ✅ | ✅ | ✅ |
| Delete objects | ❌ | ❌ | ✅ | ✅ |
| Delete bucket | ❌ | ❌ | ❌ | ✅ |
| Modify security | ❌ | ❌ | ❌ | ✅ |

## 🚨 Security Alerts

### Automatic Warnings
- **Unusual Activity**: Multiple failed login attempts
- **Privilege Escalation**: Attempts to access higher levels
- **Bulk Operations**: Large-scale destructive operations
- **Off-hours Access**: Access outside normal business hours

### Alert Notifications
```bash
# Configure email alerts
python obs_utils_improved.py --configure-alerts --email admin@company.com

# Set up Slack notifications
python obs_utils_improved.py --configure-alerts --slack-webhook https://hooks.slack.com/...
```

## 🔧 Configuration Examples

### Basic Setup
```json
{
  "security_levels": {
    "enabled": true,
    "default_level": "READ_ONLY",
    "require_password_for": ["STANDARD", "DESTRUCTIVE", "ADMIN"],
    "session_timeout": 1800,
    "max_failed_attempts": 3
  }
}
```

### Advanced Setup
```json
{
  "security_levels": {
    "enabled": true,
    "default_level": "READ_ONLY",
    "require_password_for": ["STANDARD", "DESTRUCTIVE", "ADMIN"],
    "session_timeout": 1800,
    "max_failed_attempts": 3,
    "password_policy": {
      "min_length": 12,
      "require_uppercase": true,
      "require_lowercase": true,
      "require_numbers": true,
      "require_symbols": true,
      "rotation_days": 60
    },
    "audit_logging": {
      "enabled": true,
      "log_file": "security_audit.log",
      "log_level": "INFO"
    },
    "alerts": {
      "email": "security@company.com",
      "slack_webhook": "https://hooks.slack.com/...",
      "failed_login_threshold": 3,
      "bulk_operation_threshold": 100
    }
  }
}
```

## 📋 Best Practices

### For System Administrators
1. **Regular Password Rotation**: Follow the rotation schedule
2. **Principle of Least Privilege**: Grant minimum required access
3. **Audit Logs Review**: Weekly review of security logs
4. **Backup Security Config**: Secure backup of security settings
5. **Incident Response Plan**: Documented procedures for security incidents

### For Operators
1. **Strong Passwords**: Use password managers
2. **Secure Sessions**: Always log out when finished
3. **Report Suspicious Activity**: Immediate reporting of anomalies
4. **Follow Procedures**: Adhere to established security protocols
5. **Regular Training**: Stay updated on security practices

### For Developers
1. **Secure Coding**: Follow secure development practices
2. **Input Validation**: Validate all user inputs
3. **Error Handling**: Secure error messages
4. **Code Reviews**: Security-focused code reviews
5. **Testing**: Regular security testing

## 🔍 Troubleshooting

### Common Issues

#### "Password Required" Error
```bash
# Check current security level
python obs_utils_improved.py --check-security-level

# Reset password if forgotten
python obs_utils_improved.py --reset-password --level STANDARD
```

#### "Access Denied" Error
```bash
# Verify user permissions
python obs_utils_improved.py --check-permissions

# Request access elevation
python obs_utils_improved.py --request-elevation --level DESTRUCTIVE
```

#### "Session Expired" Error
```bash
# Re-authenticate
python obs_utils_improved.py --login

# Extend session timeout
python obs_utils_improved.py --extend-session
```

## 📞 Support

For security-related questions or issues:

- **Security Team**: security@ccvass.com
- **Documentation**: [Security Guide](docs/en/SECURITY.md)
- **Emergency**: +51-xxx-xxx-xxxx

---

**Last Updated**: July 2025  
**Version**: 2.0.0  
**Maintained by**: CCVASS Security Team
