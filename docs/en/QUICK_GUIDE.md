# 🚀 Quick User Guide - OBS Utils

**Version:** 2025  
**Developed by:** [CCVASS](mailto:contact@ccvass.com) - Lima, Peru  
**License:** Apache 2.0

---

## 📋 Table of Contents

1. [Quick Installation](#-quick-installation)
2. [Initial Configuration](#-initial-configuration)
3. [Usage Modes](#-usage-modes)
4. [Complete Parameters](#-complete-parameters)
5. [Available Operations](#-available-operations)
6. [Practical Examples](#-practical-examples)
7. [Security Configuration](#-security-configuration)
8. [Quick Troubleshooting](#-quick-troubleshooting)

---

## 🚀 Quick Installation

```bash
# Clone repository
git clone <repository-url>
cd obs_utils

# Automatic installation
./setup.sh      # Linux/macOS
setup.bat       # Windows
```

---

## ⚙️ Initial Configuration

### Option 1: Secure Configuration (Recommended) 🔐
```bash
python obs_utils_improved.py --setup-secure-config
```

### Option 2: Environment Variables 🌍
```bash
export OBS_ACCESS_KEY_ID="your_access_key"
export OBS_SECRET_ACCESS_KEY="your_secret_key"
export OBS_SERVER="https://obs.sa-peru-1.myhuaweicloud.com/"
export OBS_REGION="sa-peru-1"
```

### Option 3: Configuration File 📁
```bash
python obs_utils_improved.py --create-config
# Edit obs_config.json with your credentials
```

---

## 🎯 Usage Modes

### Interactive Mode (Beginners)
```bash
python obs_utils_improved.py
```

### Command Line Mode (Advanced)
```bash
python obs_utils_improved.py --operation <operation> [parameters]
```

---

## 📝 Complete Parameters

### Main Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `--config` | string | Configuration file path | `--config my_config.json` |
| `--operation` | choice | Operation to perform | `--operation list` |
| `--bucket` | string | Bucket name | `--bucket my-bucket` |
| `--prefix` | string | Object prefix/path | `--prefix "folder/"` |
| `--object-key` | string | Specific object key | `--object-key "file.txt"` |
| `--download-path` | string | Local download path | `--download-path "./downloads/"` |
| `--search-text` | string | Text to search in names | `--search-text "backup"` |
| `--days` | integer | Days for restoration | `--days 30` |
| `--tier` | choice | Restoration tier | `--tier Expedited` |

### Configuration Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `--create-config` | flag | Create sample configuration file |
| `--setup-secure-config` | flag | Interactive secure configuration |
| `--encrypt-config` | flag | Encrypt existing configuration file |
| `--secure-permissions` | flag | Set secure permissions |

### Advanced Security Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `--setup-security-levels` | flag | Setup multi-level security system |
| `--list-security-levels` | flag | List configured security levels |
| `--enable-security-levels` | flag | Enable multi-level security |

---

## 🔧 Available Operations

### 1. **list** - List Objects
**Description:** Lists objects in a bucket
```bash
python obs_utils_improved.py --operation list --bucket my-bucket
python obs_utils_improved.py --operation list --bucket my-bucket --prefix "folder/"
```

### 2. **archive** - Archive (COLD)
**Description:** Moves objects to COLD storage (cheapest)
```bash
python obs_utils_improved.py --operation archive --bucket my-bucket
python obs_utils_improved.py --operation archive --bucket my-bucket --prefix "old-files/"
```

### 3. **warm** - WARM Storage
**Description:** Moves objects to WARM storage (infrequent access)
```bash
python obs_utils_improved.py --operation warm --bucket my-bucket
python obs_utils_improved.py --operation warm --bucket my-bucket --prefix "monthly-data/"
```

### 4. **restore** - Restore Archived
**Description:** Restores archived objects for temporary access
```bash
python obs_utils_improved.py --operation restore --bucket my-bucket
python obs_utils_improved.py --operation restore --bucket my-bucket --days 7 --tier Expedited
```

### 5. **download** - Download Objects
**Description:** Downloads objects to local directory
```bash
python obs_utils_improved.py --operation download --bucket my-bucket --download-path "./downloads/"
python obs_utils_improved.py --operation download --bucket my-bucket --prefix "reports/" --download-path "./reports/"
```

### 6. **search** - Search Objects
**Description:** Searches objects by name or pattern
```bash
python obs_utils_improved.py --operation search --search-text "backup"
python obs_utils_improved.py --operation search --bucket my-bucket --search-text ".pdf"
```

---

## 💡 Practical Examples

### Basic File Management

```bash
# List all files in a bucket
python obs_utils_improved.py --operation list --bucket documents

# List files from specific folder
python obs_utils_improved.py --operation list --bucket documents --prefix "2024/january/"

# Search for PDF files
python obs_utils_improved.py --operation search --bucket documents --search-text ".pdf"
```

### Storage Management

```bash
# Archive old files (move to COLD)
python obs_utils_improved.py --operation archive --bucket backups --prefix "2023/"

# Move files to WARM storage
python obs_utils_improved.py --operation warm --bucket logs --prefix "monthly-logs/"

# Restore archived files for 7 days
python obs_utils_improved.py --operation restore --bucket backups --prefix "2023/important/" --days 7
```

### Bulk Downloads

```bash
# Download entire folder
python obs_utils_improved.py --operation download --bucket projects --prefix "project-a/" --download-path "./project-a/"

# Download specific files
python obs_utils_improved.py --operation download --bucket documents --object-key "final-report.pdf" --download-path "./documents/"
```

### Operations with Custom Configuration

```bash
# Use specific configuration file
python obs_utils_improved.py --config ./configs/production.json --operation list --bucket prod-data

# Operation with encrypted configuration
python obs_utils_improved.py --config ./configs/secure_config.enc --operation archive --bucket sensitive-data
```

---

## 🔒 Security Configuration

### Secure Configuration Step by Step

```bash
# 1. Initial secure configuration
python obs_utils_improved.py --setup-secure-config

# 2. Encrypt existing configuration
python obs_utils_improved.py --encrypt-config

# 3. Set secure permissions
python obs_utils_improved.py --secure-permissions

# 4. Setup advanced security levels
python obs_utils_improved.py --setup-security-levels
```

### Security Verification

```bash
# List configured security levels
python obs_utils_improved.py --list-security-levels

# Enable multi-level security for session
python obs_utils_improved.py --enable-security-levels --operation list --bucket secure-bucket
```

---

## 🔍 Storage Classes

| Class | Description | Cost | Access Time | Recommended Use |
|-------|-------------|------|-------------|-----------------|
| **STANDARD** | Frequent access | High | Immediate | Active files |
| **WARM** | Infrequent access | Medium | Immediate | Monthly files |
| **COLD** | Archive | Low | Requires restoration | Backups, historical files |

### Restoration Tiers

| Tier | Time | Cost | Use |
|------|------|------|-----|
| **Expedited** | 1-5 minutes | High | Urgent |
| **Standard** | 3-5 hours | Medium | Normal |
| **Bulk** | 5-12 hours | Low | Bulk |

---

## 🛠️ Quick Troubleshooting

### Common Errors

#### Authentication Error
```bash
# Verify configuration
python obs_utils_improved.py --setup-secure-config

# Check environment variables
echo $OBS_ACCESS_KEY_ID
echo $OBS_SERVER
```

#### Permission Error
```bash
# Set secure permissions
python obs_utils_improved.py --secure-permissions

# Check file permissions
ls -la obs_config.json
```

#### Connection Error
```bash
# Check connectivity
ping obs.sa-peru-1.myhuaweicloud.com

# Verify region configuration
python obs_utils_improved.py --operation list --bucket test-bucket
```

### Diagnostic Commands

```bash
# Check installation
python --version
pip list | grep obs

# Check logs
tail -f logs/obs_utils.log

# Debug mode (add to command)
python obs_utils_improved.py --operation list --bucket test --verbose
```

---

## 📞 Support and Contact

### **CCVASS - Lima, Peru**
- **Email:** [contact@ccvass.com](mailto:contact@ccvass.com)
- **Year:** 2025
- **License:** Apache 2.0

### Help Resources
- **Complete Documentation:** [docs/en/](../en/)
- **Advanced Examples:** [EXAMPLES.md](EXAMPLES.md)
- **Security Guide:** [SECURITY.md](SECURITY.md)
- **Troubleshooting:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## 🎯 Most Used Commands

```bash
# Top 10 most common commands

# 1. List files
python obs_utils_improved.py --operation list --bucket my-bucket

# 2. Search files
python obs_utils_improved.py --operation search --search-text "backup"

# 3. Download folder
python obs_utils_improved.py --operation download --bucket data --prefix "reports/" --download-path "./reports/"

# 4. Archive old files
python obs_utils_improved.py --operation archive --bucket backups --prefix "2023/"

# 5. Secure configuration
python obs_utils_improved.py --setup-secure-config

# 6. Restore files
python obs_utils_improved.py --operation restore --bucket files --days 7

# 7. Move to WARM
python obs_utils_improved.py --operation warm --bucket logs --prefix "old-logs/"

# 8. List with filter
python obs_utils_improved.py --operation list --bucket documents --prefix "2024/"

# 9. Download specific file
python obs_utils_improved.py --operation download --bucket docs --object-key "important.pdf" --download-path "./"

# 10. Interactive mode
python obs_utils_improved.py
```

---

**Developed with ❤️ by CCVASS - Lima, Peru 🇵🇪**

**Need help?** Check the [Troubleshooting Guide](TROUBLESHOOTING.md) or contact [contact@ccvass.com](mailto:contact@ccvass.com).
