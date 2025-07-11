"""
Configuration module for OBS Utils
Handles credentials and application settings with security features

Copyright 2025 CCVASS - Lima, Peru

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Contact: contact@ccvass.com
"""
import os
import json
import logging
import getpass
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class Config:
    """Configuration manager for OBS Utils with security features"""
    
    def __init__(self, config_file: str = "obs_config.json", use_encryption: bool = None):
        self.config_file = config_file
        self.use_encryption = use_encryption
        self._security = None
        
        # Auto-detect if encryption should be used
        if use_encryption is None:
            encrypted_file = f"{config_file}.enc"
            salt_file = f"{config_file}.salt"
            self.use_encryption = os.path.exists(encrypted_file) and os.path.exists(salt_file)
        
        if self.use_encryption:
            try:
                from security import ConfigSecurity
                self._security = ConfigSecurity(config_file)
            except ImportError:
                logger.warning("Security module not available, falling back to regular config")
                self.use_encryption = False
        
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """Load configuration from file or environment variables"""
        config = {}
        
        try:
            # Try encrypted configuration first
            if self.use_encryption and self._security:
                logger.info("Loading encrypted configuration")
                config = self._security.decrypt_config()
                if config is None:
                    logger.error("Failed to decrypt configuration, falling back to regular methods")
                    self.use_encryption = False
                else:
                    logger.info("Encrypted configuration loaded successfully")
                    # Still check environment variables for overrides
                    config = self._apply_env_overrides(config)
                    return config
            
            # Try regular file
            if os.path.exists(self.config_file):
                # Check file permissions for security
                self._check_file_permissions()
                
                try:
                    with open(self.config_file, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    logger.info(f"Configuration loaded from {self.config_file}")
                except (json.JSONDecodeError, IOError) as e:
                    logger.warning(f"Could not load config file {self.config_file}: {e}")
            
            # Apply environment variable overrides
            config = self._apply_env_overrides(config)
            
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            # Fallback to environment variables only
            config = self._load_from_env()
        
        return config
    
    def _check_file_permissions(self):
        """Check and warn about insecure file permissions"""
        try:
            if os.name == 'nt':  # Windows
                return  # Skip permission check on Windows
                
            file_stat = os.stat(self.config_file)
            # Check if file is readable by group or others (not secure)
            if file_stat.st_mode & 0o077:
                logger.warning(f"⚠️  Configuration file {self.config_file} has insecure permissions!")
                logger.warning("   Recommended: chmod 600 obs_config.json")
                logger.warning("   Or consider using encrypted configuration")
                
                # Offer to fix permissions
                try:
                    response = input("Fix file permissions now? (y/N): ")
                    if response.lower() == 'y':
                        os.chmod(self.config_file, 0o600)
                        logger.info("✅ File permissions updated to 600")
                except (EOFError, KeyboardInterrupt):
                    pass
        except Exception as e:
            logger.debug(f"Could not check file permissions: {e}")
    
    def _apply_env_overrides(self, config: Dict) -> Dict:
        """Apply environment variable overrides to config"""
        config.update({
            'access_key_id': os.getenv('OBS_ACCESS_KEY_ID', config.get('access_key_id', '')),
            'secret_access_key': os.getenv('OBS_SECRET_ACCESS_KEY', config.get('secret_access_key', '')),
            'server': os.getenv('OBS_SERVER', config.get('server', 'https://obs.sa-peru-1.myhuaweicloud.com/')),
            'region': os.getenv('OBS_REGION', config.get('region', 'sa-peru-1')),
            'max_keys': int(os.getenv('OBS_MAX_KEYS', config.get('max_keys', 1000))),
            'restore_days': int(os.getenv('OBS_RESTORE_DAYS', config.get('restore_days', 30))),
            'restore_tier': os.getenv('OBS_RESTORE_TIER', config.get('restore_tier', 'Expedited'))
        })
        return config
    
    def _load_from_env(self) -> Dict:
        """Load configuration from environment variables only"""
        return {
            'access_key_id': os.getenv('OBS_ACCESS_KEY_ID', ''),
            'secret_access_key': os.getenv('OBS_SECRET_ACCESS_KEY', ''),
            'server': os.getenv('OBS_SERVER', 'https://obs.sa-peru-1.myhuaweicloud.com/'),
            'region': os.getenv('OBS_REGION', 'sa-peru-1'),
            'max_keys': int(os.getenv('OBS_MAX_KEYS', 1000)),
            'restore_days': int(os.getenv('OBS_RESTORE_DAYS', 30)),
            'restore_tier': os.getenv('OBS_RESTORE_TIER', 'Expedited')
        }
    
    def get(self, key: str, default=None):
        """Get configuration value"""
        return self.config.get(key, default)
    
    def validate_credentials(self) -> bool:
        """Validate that required credentials are present"""
        required_fields = ['access_key_id', 'secret_access_key', 'server']
        for field in required_fields:
            if not self.config.get(field):
                return False
        return True
    
    def create_sample_config(self):
        """Create a sample configuration file"""
        sample_config = {
            "access_key_id": "YOUR_ACCESS_KEY_HERE",
            "secret_access_key": "YOUR_SECRET_KEY_HERE",
            "server": "https://obs.sa-peru-1.myhuaweicloud.com/",
            "region": "sa-peru-1",
            "max_keys": 1000,
            "restore_days": 30,
            "restore_tier": "Expedited"
        }
        
        sample_file = f"{self.config_file}.sample"
        with open(sample_file, 'w', encoding='utf-8') as f:
            json.dump(sample_config, f, indent=2)
        
        # Set secure permissions on sample file
        if os.name != 'nt':  # Not Windows
            os.chmod(sample_file, 0o600)
        
        logger.info(f"Sample configuration created: {sample_file}")
        print(f"Sample configuration file created: {sample_file}")
        print("Copy this file to obs_config.json and update with your credentials")
        print("For better security, consider using encrypted configuration:")
        print("  python security.py")
    
    def encrypt_configuration(self, password: str = None) -> bool:
        """Encrypt current configuration file"""
        if not self._security:
            try:
                from security import ConfigSecurity
                self._security = ConfigSecurity(self.config_file)
            except ImportError:
                logger.error("Security module not available")
                return False
        
        return self._security.encrypt_config(password)
    
    def is_encrypted(self) -> bool:
        """Check if configuration is encrypted"""
        if self._security:
            return self._security.is_encrypted()
        return False
    
    def secure_file_permissions(self):
        """Set secure permissions on configuration file"""
        if os.path.exists(self.config_file) and os.name != 'nt':
            os.chmod(self.config_file, 0o600)  # Read/write for owner only
            logger.info(f"✅ Set secure permissions on {self.config_file}")
            return True
        return False
