# Security Policy

## 🔒 Security Overview

OBS Utils implements multiple layers of security to protect your Huawei Cloud credentials and data:

- **AES-256 Encryption**: All credentials are encrypted using industry-standard encryption
- **Multi-level Security**: Different passwords for different operation levels
- **Secure File Permissions**: Automatic detection and warnings for insecure configurations
- **Environment Variable Support**: Secure credential management through environment variables

## 🛡️ Security Levels

### Level 1: READ_ONLY
- **Operations**: List, search, download
- **Password Required**: No
- **Risk Level**: Low

### Level 2: STANDARD
- **Operations**: Archive, restore, warm storage
- **Password Required**: Operator password
- **Risk Level**: Medium

### Level 3: DESTRUCTIVE
- **Operations**: Delete objects
- **Password Required**: Supervisor password
- **Risk Level**: High

### Level 4: ADMIN
- **Operations**: Full system management, configuration changes
- **Password Required**: Administrator password
- **Risk Level**: Critical

## 🔐 Secure Configuration

### Option 1: Encrypted Configuration (Recommended)
```bash
python obs_utils_improved.py --setup-secure-config
```

### Option 2: Environment Variables
```bash
export OBS_ACCESS_KEY_ID="your_access_key"
export OBS_SECRET_ACCESS_KEY="your_secret_key"
export OBS_SERVER="https://obs.sa-peru-1.myhuaweicloud.com/"
export OBS_REGION="sa-peru-1"
```

### Option 3: Secure File Permissions
```bash
# Create configuration file
python obs_utils_improved.py --create-config

# Set secure permissions (Linux/macOS)
chmod 600 obs_config.json

# Windows: Right-click → Properties → Security → Advanced
```

## ⚠️ Security Warnings

The system automatically detects and warns about:

- **Insecure file permissions** (readable by others)
- **Plain text credentials** in configuration files
- **Missing encryption** for sensitive data
- **Weak passwords** for security levels

## 🚨 Reporting Security Vulnerabilities

If you discover a security vulnerability, please report it to:

- **Email**: security@ccvass.com
- **Subject**: [SECURITY] OBS Utils Vulnerability Report
- **Include**: 
  - Detailed description of the vulnerability
  - Steps to reproduce
  - Potential impact
  - Suggested fix (if available)

### Response Timeline

- **Initial Response**: Within 24 hours
- **Vulnerability Assessment**: Within 72 hours
- **Fix Development**: Within 1 week for critical issues
- **Public Disclosure**: After fix is available and tested

## 🔧 Security Best Practices

### For Administrators
1. **Use encrypted configuration** with strong passwords
2. **Regularly rotate** access keys and passwords
3. **Monitor access logs** for unusual activity
4. **Implement least privilege** access principles
5. **Keep software updated** to latest version

### For Operators
1. **Never share passwords** or access keys
2. **Use environment variables** in production
3. **Log out** from interactive sessions
4. **Report suspicious activity** immediately
5. **Follow company security policies**

### For Developers
1. **Never commit credentials** to version control
2. **Use secure coding practices**
3. **Validate all inputs**
4. **Handle errors securely**
5. **Regular security audits**

## 🔍 Security Auditing

### Automated Checks
- **Bandit**: Static security analysis
- **Safety**: Known vulnerability scanning
- **File permission checks**: Automatic detection
- **Credential validation**: Secure authentication testing

### Manual Auditing
```bash
# Check file permissions
ls -la obs_config.json

# Verify encryption status
python -c "from security import ConfigSecurity; ConfigSecurity.check_encryption_status()"

# Test security levels
python obs_utils_improved.py --test-security-levels
```

## 📋 Security Checklist

### Initial Setup
- [ ] Encrypted configuration created
- [ ] Strong passwords set for all levels
- [ ] File permissions secured (600)
- [ ] Environment variables configured (if used)
- [ ] Access keys validated

### Regular Maintenance
- [ ] Passwords rotated (quarterly)
- [ ] Access keys rotated (monthly)
- [ ] Security logs reviewed
- [ ] Software updated
- [ ] Permissions verified

### Incident Response
- [ ] Incident documented
- [ ] Affected systems identified
- [ ] Credentials rotated
- [ ] Security team notified
- [ ] Lessons learned documented

## 📞 Security Contacts

- **Primary**: security@ccvass.com
- **Emergency**: +51-xxx-xxx-xxxx
- **General**: contact@ccvass.com

---

**Last Updated**: July 2025  
**Version**: 2.0.0  
**Maintained by**: CCVASS Security Team
