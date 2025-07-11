# OBS Utils - Huawei Cloud Object Storage Utilities

A comprehensive and **secure** tool for managing objects in **Huawei Cloud Object Storage Service (OBS)** with robust error handling, secure credential configuration, and modular architecture.

**Compatible with Linux, macOS and Windows** 🐧🍎🪟

---

**Developed by:** [CCVASS](mailto:contact@ccvass.com) - Lima, Peru  
**Year:** 2025  
**License:** Apache 2.0  
**Contact:** contact@ccvass.com

---

## 🔒 **NEW: Advanced Security Features**

- **🔐 Encrypted Configuration**: Credentials protected with AES-256 encryption
- **🛡️ Multiple Authentication Methods**: Encrypted files, environment variables, secure permissions
- **⚠️ Insecure Configuration Detection**: Automatic alerts for file permissions
- **🔑 Password Management**: Secure encryption password changes
- **📋 Complete Security Guide**: Best practices and step-by-step configuration

## 🌍 Documentation Languages

- **English**: [Complete Documentation](docs/en/)
- **Español**: [Documentación Completa](docs/es/) | [README en Español](README_ES.md)

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd obs_utils

# Run automatic setup
./setup.sh  # Linux/macOS
setup.bat   # Windows
```

### Configuration

Choose your preferred security method:

#### Option 1: Encrypted Configuration (Most Secure) 🔐
```bash
python obs_utils_improved.py --setup-secure-config
```

#### Option 2: Environment Variables (Recommended for Servers) 🌍
```bash
export OBS_ACCESS_KEY_ID="your_access_key"
export OBS_SECRET_ACCESS_KEY="your_secret_key"
export OBS_SERVER="https://obs.sa-peru-1.myhuaweicloud.com/"
export OBS_REGION="sa-peru-1"
```

#### Option 3: Configuration File (Basic) 📁
```bash
python obs_utils_improved.py --create-config
# Edit obs_config.json with your credentials
```

### Usage

#### Interactive Mode (Beginners)
```bash
python obs_utils_improved.py
```

#### Command Line Mode (Advanced)
```bash
# List objects in a bucket
python obs_utils_improved.py --operation list --bucket my-bucket

# Archive old files to COLD storage
python obs_utils_improved.py --operation archive --bucket my-bucket --prefix "old-files/"

# Search for files
python obs_utils_improved.py --operation search --search-text "backup"

# Download files
python obs_utils_improved.py --operation download --bucket my-bucket --prefix "reports/"
```

## ✨ Key Features

- 🔒 **Secure configuration**: Encrypted credentials, environment variables, or secure file permissions
- 🛡️ **Robust error handling**: Input validation and comprehensive exception handling
- 📝 **Advanced logging**: Structured logs in files and console with different levels
- 🧩 **Modular code**: Clear separation of responsibilities across multiple modules
- 🖥️ **Dual mode**: Interactive and command-line modes for maximum flexibility
- 📄 **Automatic pagination**: Efficient handling of large object quantities
- ✅ **Complete validation**: Secure and validated user input
- 🔄 **Batch operations**: Mass file processing
- 📊 **Visual progress**: Progress indicators and processed item counters
- **🔐 AES-256 Encryption**: Maximum protection for sensitive credentials
- **⚠️ Security Alerts**: Automatic detection of insecure configurations

## 📚 Available Operations

| Operation | Description | CLI Command |
|-----------|-------------|-------------|
| **list** | List objects in bucket | `--operation list --bucket my-bucket` |
| **archive** | Move to COLD storage (cheapest) | `--operation archive --bucket my-bucket` |
| **warm** | Move to WARM storage (infrequent access) | `--operation warm --bucket my-bucket` |
| **restore** | Restore archived objects | `--operation restore --bucket my-bucket` |
| **download** | Download objects | `--operation download --bucket my-bucket` |
| **search** | Search objects by name | `--operation search --search-text "backup"` |

## 🔧 Storage Classes

| Class | Description | Cost | Access Time |
|-------|-------------|------|-------------|
| **STANDARD** | Frequent access | High | Immediate |
| **WARM** | Infrequent access | Medium | Immediate |
| **COLD** | Archive | Low | Requires restoration |

## 📖 Documentation

### English Documentation
- **[📚 Quick User Guide](docs/en/QUICK_GUIDE.md)** - Complete parameters and examples
- [Installation Guide](docs/en/INSTALLATION.md)
- [Configuration Guide](docs/en/CONFIGURATION.md)
- [Security Guide](docs/en/SECURITY.md)
- [API Reference](docs/en/API.md)
- [Examples](docs/en/EXAMPLES.md)
- [Troubleshooting](docs/en/TROUBLESHOOTING.md)
- [Windows Guide](docs/en/WINDOWS_GUIDE.md)

### Spanish Documentation
- **[📚 Guía Rápida de Usuario](docs/es/GUIA_RAPIDA.md)** - Parámetros completos y ejemplos
- [Guía de Instalación](docs/es/INSTALACION.md)
- [Guía de Configuración](docs/es/CONFIGURACION.md)
- [Guía de Seguridad](docs/es/SEGURIDAD.md)
- [Referencia API](docs/es/API.md)
- [Ejemplos](docs/es/EJEMPLOS.md)
- [Solución de Problemas](docs/es/SOLUCION_PROBLEMAS.md)
- [Guía Windows](docs/es/GUIA_WINDOWS.md)

## 🖥️ System Requirements

- **Python**: 3.7 or higher
- **Operating System**: Linux, macOS, Windows
- **Memory**: Minimum 512MB RAM
- **Disk Space**: 100MB for installation and logs
- **Connectivity**: Internet access to Huawei Cloud OBS

## 🛠️ Development

### Project Structure
```
obs_utils/
├── obs_utils_improved.py    # Main script with CLI
├── obs_manager.py          # Main OBSManager class
├── config.py              # Configuration management
├── logger.py              # Logging system
├── security.py            # Security utilities
├── requirements.txt       # Python dependencies
├── setup.sh              # Installation script
├── README.md             # This documentation (English)
├── README_ES.md          # Spanish README
├── LICENSE               # Apache 2.0 License
└── docs/                 # Documentation directory
    ├── en/              # English documentation
    └── es/              # Spanish documentation
```

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to branch: `git push origin feature/new-feature`
5. Create Pull Request

## 📄 License

This project is licensed under the **Apache License 2.0**. See the [`LICENSE`](LICENSE) file for details.

## 🆘 Support

### **CCVASS Contact**
- **Email**: [contact@ccvass.com](mailto:contact@ccvass.com)
- **Company**: CCVASS - Lima, Peru
- **Year**: 2025

### **Help Resources**
- **Issues**: Report problems in the repository
- **Documentation**: Complete guides in [docs/](docs/) directory
- **Logs**: Check files in `logs/` for debugging
- **Huawei Cloud**: Official OBS documentation

---

**Developed with ❤️ by CCVASS - Lima, Peru 🇵🇪**

**Need help?** Check the [Troubleshooting Guide](docs/en/TROUBLESHOOTING.md) or contact [contact@ccvass.com](mailto:contact@ccvass.com).
