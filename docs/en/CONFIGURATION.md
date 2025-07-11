# Configuration Guide

This guide explains how to configure OBS Utils with your Huawei Cloud credentials using different security methods.

## Configuration Methods

### Method 1: Encrypted Configuration (Most Secure) 🔐

This method stores your credentials in an encrypted file using AES-256 encryption.

#### Setup
```bash
python obs_utils_improved.py --setup-secure-config
```

#### Interactive Setup Process
1. Enter your OBS credentials
2. Create a strong encryption password
3. Credentials are encrypted and stored securely
4. File permissions are set to 600 (owner read/write only)

#### Benefits
- ✅ Credentials encrypted with AES-256
- ✅ Secure file permissions
- ✅ Password-protected access
- ✅ Automatic security validation

### Method 2: Environment Variables (Server Recommended) 🌍

Best for server environments and CI/CD pipelines.

#### Linux/macOS Setup
```bash
export OBS_ACCESS_KEY_ID="your_access_key"
export OBS_SECRET_ACCESS_KEY="your_secret_key"
export OBS_SERVER="https://obs.sa-peru-1.myhuaweicloud.com/"
export OBS_REGION="sa-peru-1"
```

#### Windows Setup
```cmd
set OBS_ACCESS_KEY_ID=your_access_key
set OBS_SECRET_ACCESS_KEY=your_secret_key
set OBS_SERVER=https://obs.sa-peru-1.myhuaweicloud.com/
set OBS_REGION=sa-peru-1
```

#### Persistent Environment Variables

**Linux/macOS** (add to ~/.bashrc or ~/.zshrc):
```bash
echo 'export OBS_ACCESS_KEY_ID="your_access_key"' >> ~/.bashrc
echo 'export OBS_SECRET_ACCESS_KEY="your_secret_key"' >> ~/.bashrc
echo 'export OBS_SERVER="https://obs.sa-peru-1.myhuaweicloud.com/"' >> ~/.bashrc
echo 'export OBS_REGION="sa-peru-1"' >> ~/.bashrc
source ~/.bashrc
```

**Windows** (System Properties > Environment Variables):
1. Open System Properties
2. Click "Environment Variables"
3. Add new system variables

### Method 3: Configuration File (Basic) 📁

Simple file-based configuration.

#### Create Configuration
```bash
python obs_utils_improved.py --create-config
```

#### Manual Configuration
Create `obs_config.json`:
```json
{
    "access_key_id": "your_access_key",
    "secret_access_key": "your_secret_key",
    "server": "https://obs.sa-peru-1.myhuaweicloud.com/",
    "region": "sa-peru-1"
}
```

#### Secure File Permissions
```bash
# Linux/macOS
chmod 600 obs_config.json

# Windows (PowerShell as Administrator)
icacls obs_config.json /inheritance:r /grant:r "%USERNAME%:F"
```

## Huawei Cloud Regions

Common OBS endpoints by region:

| Region | Endpoint |
|--------|----------|
| **South America (Peru)** | `https://obs.sa-peru-1.myhuaweicloud.com/` |
| **Asia Pacific (Singapore)** | `https://obs.ap-southeast-1.myhuaweicloud.com/` |
| **Europe (Paris)** | `https://obs.eu-west-101.myhuaweicloud.com/` |
| **North America (Mexico)** | `https://obs.na-mexico-1.myhuaweicloud.com/` |
| **Asia Pacific (Hong Kong)** | `https://obs.ap-southeast-1.myhuaweicloud.com/` |

## Getting Your Credentials

### Step 1: Access Huawei Cloud Console
1. Go to [Huawei Cloud Console](https://console.huaweicloud.com/)
2. Log in to your account

### Step 2: Create Access Keys
1. Click on your username (top right)
2. Select "My Credentials"
3. Go to "Access Keys" tab
4. Click "Create Access Key"
5. Download the credentials file

### Step 3: Note Your Region
1. Go to OBS Console
2. Check the region in the URL or dropdown
3. Use the corresponding endpoint

## Configuration Priority

OBS Utils checks for configuration in this order:

1. **Command line arguments** (highest priority)
2. **Environment variables**
3. **Encrypted configuration file**
4. **Plain configuration file** (lowest priority)

## Testing Configuration

### Test Connection
```bash
python obs_utils_improved.py --test-config
```

### List Buckets (Verify Access)
```bash
python obs_utils_improved.py --operation list
```

### Interactive Mode Test
```bash
python obs_utils_improved.py
# Select option 1 (List objects)
```

## Security Best Practices

### ✅ Recommended
- Use encrypted configuration for local development
- Use environment variables for servers/containers
- Set proper file permissions (600)
- Use strong encryption passwords
- Regularly rotate access keys

### ❌ Avoid
- Storing credentials in code
- Using world-readable configuration files
- Sharing configuration files
- Using weak encryption passwords
- Committing credentials to version control

## Advanced Configuration

### Custom Configuration File Location
```bash
python obs_utils_improved.py --config-file /path/to/custom/config.json
```

### Multiple Profiles
Create different configuration files for different environments:
```bash
# Development
python obs_utils_improved.py --config-file config-dev.json

# Production
python obs_utils_improved.py --config-file config-prod.json
```

### Logging Configuration
Set logging level via environment variable:
```bash
export OBS_LOG_LEVEL=DEBUG  # DEBUG, INFO, WARNING, ERROR
```

## Troubleshooting

### Common Issues

#### Invalid Credentials
```
Error: Access denied or invalid credentials
```
**Solution**: Verify your access key and secret key are correct.

#### Wrong Region/Endpoint
```
Error: Connection timeout or server not found
```
**Solution**: Check your region and server endpoint match your bucket location.

#### Permission Denied
```
Error: Permission denied accessing configuration file
```
**Solution**: Check file permissions and ownership.

#### Encryption Password Issues
```
Error: Failed to decrypt configuration
```
**Solution**: Verify your encryption password is correct.

### Getting Help

1. Check the [Troubleshooting Guide](TROUBLESHOOTING.md)
2. Review logs in `logs/` directory
3. Test with `--test-config` flag
4. Contact [contact@ccvass.com](mailto:contact@ccvass.com)

## Next Steps

1. [Review security settings](SECURITY.md)
2. [Try the examples](EXAMPLES.md)
3. [Read the API reference](API.md)
4. [Learn about troubleshooting](TROUBLESHOOTING.md)

---

**Developed by CCVASS - Lima, Peru 🇵🇪**
