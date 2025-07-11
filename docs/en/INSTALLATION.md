# Installation Guide

This guide will help you install and set up OBS Utils on your system.

## System Requirements

- **Python**: 3.7 or higher
- **Operating System**: Linux, macOS, Windows
- **Memory**: Minimum 512MB RAM
- **Disk Space**: 100MB for installation and logs
- **Connectivity**: Internet access to Huawei Cloud OBS

## Installation Methods

### Method 1: Automatic Installation (Recommended)

#### Linux/macOS
```bash
# Clone the repository
git clone <repository-url>
cd obs_utils

# Run automatic setup
chmod +x setup.sh
./setup.sh
```

#### Windows
```cmd
# Clone the repository
git clone <repository-url>
cd obs_utils

# Run automatic setup
setup.bat
```

### Method 2: Manual Installation

#### Step 1: Clone Repository
```bash
git clone <repository-url>
cd obs_utils
```

#### Step 2: Create Virtual Environment
```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 4: Verify Installation
```bash
python obs_utils_improved.py --help
```

## Post-Installation Setup

### 1. Configuration
Choose your preferred configuration method:
- [Encrypted Configuration](CONFIGURATION.md#encrypted-configuration) (Most Secure)
- [Environment Variables](CONFIGURATION.md#environment-variables) (Server Recommended)
- [Configuration File](CONFIGURATION.md#configuration-file) (Basic)

### 2. Security Setup
Follow the [Security Guide](SECURITY.md) to ensure proper security configuration.

### 3. Test Installation
```bash
# Test basic functionality
python obs_utils_improved.py --operation list --bucket test-bucket
```

## Troubleshooting

### Common Issues

#### Python Version Error
```bash
# Check Python version
python --version
python3 --version

# Use Python 3.7+
python3 obs_utils_improved.py
```

#### Permission Errors (Linux/macOS)
```bash
# Fix script permissions
chmod +x setup.sh
chmod +x obs_utils_improved.py
```

#### Module Not Found
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Windows-Specific Issues
See the [Windows Guide](WINDOWS_GUIDE.md) for Windows-specific installation instructions.

## Verification

After installation, verify everything works:

```bash
# Check version
python obs_utils_improved.py --version

# Test configuration
python obs_utils_improved.py --test-config

# Run interactive mode
python obs_utils_improved.py
```

## Next Steps

1. [Configure your credentials](CONFIGURATION.md)
2. [Review security settings](SECURITY.md)
3. [Try the examples](EXAMPLES.md)
4. [Read the API reference](API.md)

## Support

If you encounter issues during installation:
- Check the [Troubleshooting Guide](TROUBLESHOOTING.md)
- Review the logs in the `logs/` directory
- Contact [contact@ccvass.com](mailto:contact@ccvass.com)

---

**Developed by CCVASS - Lima, Peru 🇵🇪**
