# API Reference

This document provides detailed information about the OBS Utils API and command-line interface.

## Command Line Interface

### Basic Syntax
```bash
python obs_utils_improved.py [OPTIONS] [OPERATION_OPTIONS]
```

### Global Options

| Option | Description | Example |
|--------|-------------|---------|
| `--help` | Show help message | `--help` |
| `--version` | Show version information | `--version` |
| `--config-file` | Specify configuration file | `--config-file config.json` |
| `--log-level` | Set logging level | `--log-level DEBUG` |
| `--test-config` | Test configuration | `--test-config` |

### Configuration Options

| Option | Description | Example |
|--------|-------------|---------|
| `--create-config` | Create basic configuration file | `--create-config` |
| `--setup-secure-config` | Setup encrypted configuration | `--setup-secure-config` |
| `--change-password` | Change encryption password | `--change-password` |

### Operation Options

#### List Operation
```bash
python obs_utils_improved.py --operation list [OPTIONS]
```

| Option | Description | Default | Example |
|--------|-------------|---------|---------|
| `--bucket` | Bucket name | Required | `--bucket my-bucket` |
| `--prefix` | Object prefix filter | None | `--prefix "folder/"` |
| `--max-keys` | Maximum objects to list | 1000 | `--max-keys 500` |

#### Archive Operation
```bash
python obs_utils_improved.py --operation archive [OPTIONS]
```

| Option | Description | Default | Example |
|--------|-------------|---------|---------|
| `--bucket` | Bucket name | Required | `--bucket my-bucket` |
| `--prefix` | Object prefix filter | None | `--prefix "old-files/"` |
| `--days-old` | Archive files older than N days | 30 | `--days-old 90` |
| `--dry-run` | Show what would be archived | False | `--dry-run` |

#### Warm Operation
```bash
python obs_utils_improved.py --operation warm [OPTIONS]
```

| Option | Description | Default | Example |
|--------|-------------|---------|---------|
| `--bucket` | Bucket name | Required | `--bucket my-bucket` |
| `--prefix` | Object prefix filter | None | `--prefix "infrequent/"` |
| `--dry-run` | Show what would be moved | False | `--dry-run` |

#### Restore Operation
```bash
python obs_utils_improved.py --operation restore [OPTIONS]
```

| Option | Description | Default | Example |
|--------|-------------|---------|---------|
| `--bucket` | Bucket name | Required | `--bucket my-bucket` |
| `--prefix` | Object prefix filter | None | `--prefix "archived/"` |
| `--days` | Restore duration in days | 1 | `--days 7` |

#### Download Operation
```bash
python obs_utils_improved.py --operation download [OPTIONS]
```

| Option | Description | Default | Example |
|--------|-------------|---------|---------|
| `--bucket` | Bucket name | Required | `--bucket my-bucket` |
| `--prefix` | Object prefix filter | None | `--prefix "reports/"` |
| `--local-path` | Local download directory | `./downloads` | `--local-path /tmp/obs` |
| `--overwrite` | Overwrite existing files | False | `--overwrite` |

#### Search Operation
```bash
python obs_utils_improved.py --operation search [OPTIONS]
```

| Option | Description | Default | Example |
|--------|-------------|---------|---------|
| `--search-text` | Text to search in object names | Required | `--search-text "backup"` |
| `--bucket` | Specific bucket to search | All buckets | `--bucket my-bucket` |
| `--case-sensitive` | Case-sensitive search | False | `--case-sensitive` |

## Python API

### OBSManager Class

#### Initialization
```python
from obs_manager import OBSManager

# Initialize with configuration file
manager = OBSManager(config_file="obs_config.json")

# Initialize with credentials
manager = OBSManager(
    access_key_id="your_key",
    secret_access_key="your_secret",
    server="https://obs.sa-peru-1.myhuaweicloud.com/",
    region="sa-peru-1"
)
```

#### Methods

##### list_objects(bucket_name, prefix=None, max_keys=1000)
List objects in a bucket.

**Parameters:**
- `bucket_name` (str): Name of the bucket
- `prefix` (str, optional): Object prefix filter
- `max_keys` (int): Maximum number of objects to return

**Returns:**
- `list`: List of object dictionaries

**Example:**
```python
objects = manager.list_objects("my-bucket", prefix="folder/")
for obj in objects:
    print(f"Object: {obj['key']}, Size: {obj['size']}")
```

##### archive_objects(bucket_name, prefix=None, days_old=30, dry_run=False)
Archive objects to COLD storage.

**Parameters:**
- `bucket_name` (str): Name of the bucket
- `prefix` (str, optional): Object prefix filter
- `days_old` (int): Archive objects older than this many days
- `dry_run` (bool): If True, only show what would be archived

**Returns:**
- `dict`: Results with counts and processed objects

**Example:**
```python
result = manager.archive_objects("my-bucket", days_old=90)
print(f"Archived {result['archived_count']} objects")
```

##### warm_objects(bucket_name, prefix=None, dry_run=False)
Move objects to WARM storage.

**Parameters:**
- `bucket_name` (str): Name of the bucket
- `prefix` (str, optional): Object prefix filter
- `dry_run` (bool): If True, only show what would be moved

**Returns:**
- `dict`: Results with counts and processed objects

##### restore_objects(bucket_name, prefix=None, days=1)
Restore objects from COLD storage.

**Parameters:**
- `bucket_name` (str): Name of the bucket
- `prefix` (str, optional): Object prefix filter
- `days` (int): Number of days to keep restored objects available

**Returns:**
- `dict`: Results with counts and processed objects

##### download_objects(bucket_name, prefix=None, local_path="./downloads", overwrite=False)
Download objects from bucket.

**Parameters:**
- `bucket_name` (str): Name of the bucket
- `prefix` (str, optional): Object prefix filter
- `local_path` (str): Local directory to download to
- `overwrite` (bool): Whether to overwrite existing files

**Returns:**
- `dict`: Results with counts and downloaded objects

##### search_objects(search_text, bucket_name=None, case_sensitive=False)
Search for objects by name.

**Parameters:**
- `search_text` (str): Text to search for in object names
- `bucket_name` (str, optional): Specific bucket to search
- `case_sensitive` (bool): Whether search is case-sensitive

**Returns:**
- `list`: List of matching objects

## Storage Classes

### STANDARD
- **Use case**: Frequently accessed data
- **Cost**: Highest storage cost, lowest access cost
- **Access time**: Immediate
- **Minimum storage duration**: None

### WARM
- **Use case**: Infrequently accessed data
- **Cost**: Medium storage cost, medium access cost
- **Access time**: Immediate
- **Minimum storage duration**: 30 days

### COLD
- **Use case**: Archive and backup data
- **Cost**: Lowest storage cost, highest access cost
- **Access time**: Requires restoration (1-12 hours)
- **Minimum storage duration**: 90 days

## Error Handling

### Common Exceptions

#### OBSException
Base exception for OBS-related errors.

```python
from obs_manager import OBSException

try:
    manager.list_objects("non-existent-bucket")
except OBSException as e:
    print(f"OBS Error: {e}")
```

#### ConfigurationError
Raised when configuration is invalid or missing.

```python
from config import ConfigurationError

try:
    manager = OBSManager()
except ConfigurationError as e:
    print(f"Configuration Error: {e}")
```

#### SecurityError
Raised when security validation fails.

```python
from security import SecurityError

try:
    manager.load_encrypted_config("config.enc", "wrong_password")
except SecurityError as e:
    print(f"Security Error: {e}")
```

## Response Formats

### Object Dictionary
```python
{
    "key": "folder/file.txt",
    "size": 1024,
    "last_modified": "2025-01-01T12:00:00Z",
    "etag": "d41d8cd98f00b204e9800998ecf8427e",
    "storage_class": "STANDARD",
    "owner": {
        "id": "owner_id",
        "display_name": "owner_name"
    }
}
```

### Operation Result Dictionary
```python
{
    "success": True,
    "processed_count": 150,
    "success_count": 148,
    "error_count": 2,
    "objects": [...],
    "errors": [...]
}
```

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `OBS_ACCESS_KEY_ID` | Access key ID | `AKIAIOSFODNN7EXAMPLE` |
| `OBS_SECRET_ACCESS_KEY` | Secret access key | `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY` |
| `OBS_SERVER` | OBS server endpoint | `https://obs.sa-peru-1.myhuaweicloud.com/` |
| `OBS_REGION` | OBS region | `sa-peru-1` |
| `OBS_LOG_LEVEL` | Logging level | `DEBUG`, `INFO`, `WARNING`, `ERROR` |

## Exit Codes

| Code | Description |
|------|-------------|
| 0 | Success |
| 1 | General error |
| 2 | Configuration error |
| 3 | Authentication error |
| 4 | Network error |
| 5 | Permission error |

## Examples

### Basic Usage
```bash
# List all objects in a bucket
python obs_utils_improved.py --operation list --bucket my-bucket

# Archive old files
python obs_utils_improved.py --operation archive --bucket my-bucket --days-old 90

# Download specific folder
python obs_utils_improved.py --operation download --bucket my-bucket --prefix "reports/2024/"
```

### Advanced Usage
```bash
# Dry run archive operation
python obs_utils_improved.py --operation archive --bucket my-bucket --dry-run

# Search with custom configuration
python obs_utils_improved.py --config-file prod-config.json --operation search --search-text "backup"

# Debug mode
python obs_utils_improved.py --log-level DEBUG --operation list --bucket my-bucket
```

### Python API Usage
```python
from obs_manager import OBSManager

# Initialize
manager = OBSManager(config_file="obs_config.json")

# List objects
objects = manager.list_objects("my-bucket")
print(f"Found {len(objects)} objects")

# Archive old objects
result = manager.archive_objects("my-bucket", days_old=90)
print(f"Archived {result['success_count']} objects")

# Search for backups
backups = manager.search_objects("backup", case_sensitive=False)
for backup in backups:
    print(f"Backup: {backup['key']}")
```

## Support

For API questions and issues:
- Check the [Examples](EXAMPLES.md) for practical usage
- Review the [Troubleshooting Guide](TROUBLESHOOTING.md)
- Contact [contact@ccvass.com](mailto:contact@ccvass.com)

---

**Developed by CCVASS - Lima, Peru 🇵🇪**
