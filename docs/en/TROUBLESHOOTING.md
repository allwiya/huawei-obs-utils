# Troubleshooting Guide

This guide helps you resolve common issues when using OBS Utils.

## Quick Diagnostics

### Test Your Configuration
```bash
python obs_utils_improved.py --test-config
```

### Check Logs
```bash
# View recent logs
tail -f logs/obs_utils.log

# View error logs only
grep ERROR logs/obs_utils.log
```

### Verify Installation
```bash
python obs_utils_improved.py --version
python obs_utils_improved.py --help
```

## Common Issues

### 1. Configuration Problems

#### Issue: "Configuration file not found"
```
Error: Configuration file 'obs_config.json' not found
```

**Solutions:**
```bash
# Create new configuration
python obs_utils_improved.py --create-config

# Or use environment variables
export OBS_ACCESS_KEY_ID="your_key"
export OBS_SECRET_ACCESS_KEY="your_secret"
export OBS_SERVER="https://obs.sa-peru-1.myhuaweicloud.com/"
export OBS_REGION="sa-peru-1"

# Or specify config file location
python obs_utils_improved.py --config-file /path/to/config.json
```

#### Issue: "Invalid credentials"
```
Error: Access denied or invalid credentials
```

**Solutions:**
1. **Verify credentials in Huawei Cloud Console:**
   - Go to "My Credentials" > "Access Keys"
   - Check if access key is active
   - Regenerate if necessary

2. **Check configuration:**
   ```bash
   # Test configuration
   python obs_utils_improved.py --test-config
   
   # Recreate configuration
   python obs_utils_improved.py --create-config
   ```

3. **Verify region and endpoint:**
   ```bash
   # Common endpoints
   # Peru: https://obs.sa-peru-1.myhuaweicloud.com/
   # Singapore: https://obs.ap-southeast-1.myhuaweicloud.com/
   ```

#### Issue: "Failed to decrypt configuration"
```
Error: Failed to decrypt configuration file
```

**Solutions:**
```bash
# Change encryption password
python obs_utils_improved.py --change-password

# Or recreate encrypted configuration
python obs_utils_improved.py --setup-secure-config
```

### 2. Connection Problems

#### Issue: "Connection timeout"
```
Error: Connection timeout or server not found
```

**Solutions:**
1. **Check internet connectivity:**
   ```bash
   ping obs.sa-peru-1.myhuaweicloud.com
   ```

2. **Verify endpoint URL:**
   - Ensure correct region endpoint
   - Check for typos in server URL
   - Verify HTTPS protocol

3. **Check firewall/proxy:**
   ```bash
   # Test with curl
   curl -I https://obs.sa-peru-1.myhuaweicloud.com/
   ```

#### Issue: "SSL Certificate verification failed"
```
Error: SSL certificate verification failed
```

**Solutions:**
```bash
# Update certificates (Linux)
sudo apt-get update && sudo apt-get install ca-certificates

# Update certificates (macOS)
brew install ca-certificates

# For development only (not recommended for production)
export PYTHONHTTPSVERIFY=0
```

### 3. Permission Problems

#### Issue: "Access denied to bucket"
```
Error: Access denied to bucket 'my-bucket'
```

**Solutions:**
1. **Check bucket permissions in OBS Console:**
   - Verify bucket exists
   - Check bucket policy
   - Verify IAM permissions

2. **Test with different bucket:**
   ```bash
   python obs_utils_improved.py --operation list --bucket test-bucket
   ```

#### Issue: "Permission denied accessing configuration file"
```
Error: Permission denied: obs_config.json
```

**Solutions:**
```bash
# Fix file permissions (Linux/macOS)
chmod 600 obs_config.json
chown $USER obs_config.json

# Windows (PowerShell as Administrator)
icacls obs_config.json /inheritance:r /grant:r "%USERNAME%:F"
```

### 4. Python Environment Issues

#### Issue: "ModuleNotFoundError"
```
ModuleNotFoundError: No module named 'obs'
```

**Solutions:**
```bash
# Activate virtual environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Or install specific module
pip install esdk-obs-python
```

#### Issue: "Python version not supported"
```
Error: Python 3.7+ required
```

**Solutions:**
```bash
# Check Python version
python --version
python3 --version

# Use correct Python version
python3 obs_utils_improved.py

# Or install Python 3.7+
# Ubuntu/Debian
sudo apt-get install python3.8

# macOS
brew install python@3.8

# Windows: Download from python.org
```

### 5. Storage Class Issues

#### Issue: "Cannot restore object"
```
Error: Object is not in COLD storage class
```

**Solutions:**
- Only objects in COLD storage can be restored
- Check object storage class first:
  ```bash
  python obs_utils_improved.py --operation list --bucket my-bucket
  ```

#### Issue: "Archive operation failed"
```
Error: Failed to change storage class
```

**Solutions:**
1. **Check object age:**
   - Objects must meet minimum storage duration
   - WARM: 30 days minimum
   - COLD: 90 days minimum

2. **Verify permissions:**
   - Ensure write permissions to bucket
   - Check IAM policies

### 6. Performance Issues

#### Issue: "Operation is very slow"

**Solutions:**
1. **Use prefix filtering:**
   ```bash
   # Instead of listing all objects
   python obs_utils_improved.py --operation list --bucket huge-bucket
   
   # Use prefix to limit scope
   python obs_utils_improved.py --operation list --bucket huge-bucket --prefix "2024/"
   ```

2. **Adjust max-keys:**
   ```bash
   # Reduce batch size for large buckets
   python obs_utils_improved.py --operation list --bucket my-bucket --max-keys 100
   ```

3. **Check network connectivity:**
   ```bash
   # Test download speed
   speedtest-cli
   ```

#### Issue: "Memory usage too high"

**Solutions:**
1. **Process in smaller batches:**
   ```bash
   # Use prefix to process folders separately
   python obs_utils_improved.py --operation archive --bucket my-bucket --prefix "folder1/"
   python obs_utils_improved.py --operation archive --bucket my-bucket --prefix "folder2/"
   ```

2. **Increase system memory or use a machine with more RAM**

### 7. Windows-Specific Issues

#### Issue: "Script execution policy error"
```
Error: Execution of scripts is disabled on this system
```

**Solutions:**
```powershell
# Run as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or run directly
python obs_utils_improved.py
```

#### Issue: "Path too long error"
```
Error: The filename or extension is too long
```

**Solutions:**
1. **Enable long path support:**
   - Run `gpedit.msc` as Administrator
   - Navigate to: Computer Configuration > Administrative Templates > System > Filesystem
   - Enable "Enable Win32 long paths"

2. **Use shorter paths:**
   ```bash
   # Use shorter local download paths
   python obs_utils_improved.py --operation download --local-path C:\temp
   ```

## Debugging Steps

### 1. Enable Debug Logging
```bash
python obs_utils_improved.py --log-level DEBUG --operation list --bucket my-bucket
```

### 2. Check Log Files
```bash
# View all logs
cat logs/obs_utils.log

# View only errors
grep ERROR logs/obs_utils.log

# View recent activity
tail -20 logs/obs_utils.log
```

### 3. Test Individual Components

#### Test Configuration Loading
```bash
python -c "from config import load_config; print(load_config())"
```

#### Test OBS Connection
```bash
python -c "from obs_manager import OBSManager; m = OBSManager(); print('Connection OK')"
```

#### Test Credentials
```bash
python obs_utils_improved.py --test-config
```

### 4. Validate Environment

#### Check Python Environment
```bash
python --version
pip list | grep obs
which python
```

#### Check File Permissions
```bash
ls -la obs_config.json
ls -la logs/
```

#### Check Network
```bash
nslookup obs.sa-peru-1.myhuaweicloud.com
telnet obs.sa-peru-1.myhuaweicloud.com 443
```

## Getting Help

### 1. Collect Information
Before seeking help, collect this information:
- Python version: `python --version`
- OS version: `uname -a` (Linux/macOS) or `systeminfo` (Windows)
- Error message (full text)
- Log files from `logs/` directory
- Configuration method used

### 2. Check Documentation
- [Installation Guide](INSTALLATION.md)
- [Configuration Guide](CONFIGURATION.md)
- [Security Guide](SECURITY.md)
- [Examples](EXAMPLES.md)

### 3. Contact Support
- **Email**: [contact@ccvass.com](mailto:contact@ccvass.com)
- **Include**: Error details, logs, system information
- **Subject**: "OBS Utils Support - [Brief Description]"

### 4. Community Resources
- Check existing issues in the repository
- Review Huawei Cloud OBS documentation
- Search for similar problems online

## Prevention Tips

### 1. Regular Maintenance
```bash
# Test configuration monthly
python obs_utils_improved.py --test-config

# Check log file sizes
du -h logs/

# Rotate logs if needed
mv logs/obs_utils.log logs/obs_utils.log.old
```

### 2. Security Best Practices
- Regularly rotate access keys
- Use encrypted configuration
- Set proper file permissions
- Monitor access logs

### 3. Performance Optimization
- Use appropriate batch sizes
- Filter operations with prefixes
- Monitor network connectivity
- Keep Python and dependencies updated

### 4. Backup Configuration
```bash
# Backup configuration (encrypted)
cp obs_config.json.enc obs_config.json.enc.backup

# Backup environment variables
env | grep OBS > obs_env_backup.txt
```

## Error Codes Reference

| Exit Code | Description | Common Causes |
|-----------|-------------|---------------|
| 0 | Success | Operation completed successfully |
| 1 | General error | Various runtime errors |
| 2 | Configuration error | Missing or invalid configuration |
| 3 | Authentication error | Invalid credentials |
| 4 | Network error | Connection problems |
| 5 | Permission error | Access denied |

---

**Still having issues?** Contact [contact@ccvass.com](mailto:contact@ccvass.com) with detailed error information.

**Developed by CCVASS - Lima, Peru 🇵🇪**
