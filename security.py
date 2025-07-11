#!/usr/bin/env python3
"""
Security module for OBS Utils
Provides encryption/decryption for configuration files

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
import base64
import getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import logging

logger = logging.getLogger(__name__)

class ConfigSecurity:
    """Handles encryption and decryption of configuration files"""
    
    def __init__(self, config_file: str = "obs_config.json"):
        self.config_file = config_file
        self.encrypted_file = f"{config_file}.enc"
        self.salt_file = f"{config_file}.salt"
    
    def _generate_key(self, password: str, salt: bytes = None) -> tuple:
        """Generate encryption key from password"""
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt
    
    def _hash_password(self, password: str) -> str:
        """Generate SHA-256 hash of password for testing purposes"""
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest()
    
    def encrypt_config(self, password: str = None) -> bool:
        """Encrypt configuration file"""
        try:
            # Check if config file exists
            if not os.path.exists(self.config_file):
                logger.error(f"Configuration file {self.config_file} not found")
                return False
            
            # Get password if not provided
            if password is None:
                password = getpass.getpass("Enter password to encrypt configuration: ")
                confirm_password = getpass.getpass("Confirm password: ")
                if password != confirm_password:
                    logger.error("Passwords do not match")
                    return False
            
            # Read configuration
            with open(self.config_file, 'r') as f:
                config_data = f.read()
            
            # Generate key and salt
            key, salt = self._generate_key(password)
            
            # Encrypt data
            fernet = Fernet(key)
            encrypted_data = fernet.encrypt(config_data.encode())
            
            # Save encrypted file
            with open(self.encrypted_file, 'wb') as f:
                f.write(encrypted_data)
            
            # Save salt
            with open(self.salt_file, 'wb') as f:
                f.write(salt)
            
            # Set restrictive permissions
            os.chmod(self.encrypted_file, 0o600)  # Read/write for owner only
            os.chmod(self.salt_file, 0o600)
            
            # Optionally remove original file
            response = input("Remove original unencrypted file? (y/N): ")
            if response.lower() == 'y':
                os.remove(self.config_file)
                logger.info(f"Original file {self.config_file} removed")
            
            logger.info(f"Configuration encrypted successfully: {self.encrypted_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error encrypting configuration: {e}")
            return False
    
    def decrypt_config(self, password: str = None) -> dict:
        """Decrypt configuration file and return config dict"""
        try:
            # Check if encrypted files exist
            if not os.path.exists(self.encrypted_file) or not os.path.exists(self.salt_file):
                logger.error("Encrypted configuration files not found")
                return None
            
            # Get password if not provided
            if password is None:
                password = getpass.getpass("Enter password to decrypt configuration: ")
            
            # Read salt
            with open(self.salt_file, 'rb') as f:
                salt = f.read()
            
            # Generate key
            key, _ = self._generate_key(password, salt)
            
            # Read encrypted data
            with open(self.encrypted_file, 'rb') as f:
                encrypted_data = f.read()
            
            # Decrypt data
            fernet = Fernet(key)
            decrypted_data = fernet.decrypt(encrypted_data)
            
            # Parse JSON
            config = json.loads(decrypted_data.decode())
            logger.info("Configuration decrypted successfully")
            return config
            
        except Exception as e:
            logger.error(f"Error decrypting configuration: {e}")
            return None
    
    def create_encrypted_config(self, config_data: dict, password: str = None) -> bool:
        """Create encrypted configuration directly from dict"""
        try:
            # Get password if not provided
            if password is None:
                password = getpass.getpass("Enter password for new encrypted configuration: ")
                confirm_password = getpass.getpass("Confirm password: ")
                if password != confirm_password:
                    logger.error("Passwords do not match")
                    return False
            
            # Convert config to JSON
            config_json = json.dumps(config_data, indent=2)
            
            # Generate key and salt
            key, salt = self._generate_key(password)
            
            # Encrypt data
            fernet = Fernet(key)
            encrypted_data = fernet.encrypt(config_json.encode())
            
            # Save encrypted file
            with open(self.encrypted_file, 'wb') as f:
                f.write(encrypted_data)
            
            # Save salt
            with open(self.salt_file, 'wb') as f:
                f.write(salt)
            
            # Set restrictive permissions
            os.chmod(self.encrypted_file, 0o600)
            os.chmod(self.salt_file, 0o600)
            
            logger.info(f"Encrypted configuration created: {self.encrypted_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating encrypted configuration: {e}")
            return False
    
    def change_password(self, old_password: str = None, new_password: str = None) -> bool:
        """Change encryption password"""
        try:
            # Decrypt with old password
            config = self.decrypt_config(old_password)
            if config is None:
                return False
            
            # Get new password
            if new_password is None:
                new_password = getpass.getpass("Enter new password: ")
                confirm_password = getpass.getpass("Confirm new password: ")
                if new_password != confirm_password:
                    logger.error("Passwords do not match")
                    return False
            
            # Re-encrypt with new password
            return self.create_encrypted_config(config, new_password)
            
        except Exception as e:
            logger.error(f"Error changing password: {e}")
            return False
    
    def is_encrypted(self) -> bool:
        """Check if configuration is encrypted"""
        return os.path.exists(self.encrypted_file) and os.path.exists(self.salt_file)


class SecureConfig:
    """Enhanced Config class with security features"""
    
    def __init__(self, config_file: str = "obs_config.json", use_encryption: bool = False):
        self.config_file = config_file
        self.use_encryption = use_encryption
        self.security = ConfigSecurity(config_file)
        self.config = {}
        self._load_config()
    
    def _load_config(self):
        """Load configuration with security checks"""
        try:
            # Check if encrypted version exists
            if self.security.is_encrypted():
                logger.info("Loading encrypted configuration")
                self.config = self.security.decrypt_config()
                if self.config is None:
                    raise ValueError("Failed to decrypt configuration")
            else:
                # Load regular config file
                if os.path.exists(self.config_file):
                    # Check file permissions
                    file_stat = os.stat(self.config_file)
                    if file_stat.st_mode & 0o077:  # Check if readable by group/others
                        logger.warning(f"Configuration file {self.config_file} has insecure permissions")
                        logger.warning("Consider encrypting the configuration or setting permissions to 600")
                    
                    with open(self.config_file, 'r') as f:
                        self.config = json.load(f)
                else:
                    # Try environment variables
                    self.config = self._load_from_env()
            
            # Validate credentials
            if not self.validate_credentials():
                raise ValueError("Invalid or missing credentials")
                
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            raise
    
    def _load_from_env(self) -> dict:
        """Load configuration from environment variables"""
        return {
            "access_key_id": os.getenv('OBS_ACCESS_KEY_ID', ''),
            "secret_access_key": os.getenv('OBS_SECRET_ACCESS_KEY', ''),
            "server": os.getenv('OBS_SERVER', 'https://obs.sa-peru-1.myhuaweicloud.com/'),
            "region": os.getenv('OBS_REGION', 'sa-peru-1'),
            "max_keys": int(os.getenv('OBS_MAX_KEYS', '1000')),
            "restore_days": int(os.getenv('OBS_RESTORE_DAYS', '30')),
            "restore_tier": os.getenv('OBS_RESTORE_TIER', 'Expedited')
        }
    
    def get(self, key: str, default=None):
        """Get configuration value"""
        return self.config.get(key, default)
    
    def validate_credentials(self) -> bool:
        """Validate that required credentials are present"""
        required_keys = ['access_key_id', 'secret_access_key', 'server']
        return all(self.config.get(key) for key in required_keys)
    
    def encrypt_configuration(self, password: str = None) -> bool:
        """Encrypt current configuration"""
        return self.security.encrypt_config(password)
    
    def secure_file_permissions(self):
        """Set secure permissions on configuration file"""
        if os.path.exists(self.config_file):
            os.chmod(self.config_file, 0o600)  # Read/write for owner only
            logger.info(f"Set secure permissions on {self.config_file}")


def setup_secure_config():
    """Interactive setup for secure configuration"""
    print("=== OBS Utils - Secure Configuration Setup ===")
    print()
    
    # Get configuration method
    print("Choose configuration security method:")
    print("1. Encrypted configuration file")
    print("2. Environment variables only")
    print("3. Regular file with secure permissions")
    
    choice = input("Select option (1-3): ").strip()
    
    if choice == "1":
        setup_encrypted_config()
    elif choice == "2":
        setup_env_variables()
    elif choice == "3":
        setup_secure_file()
    else:
        print("Invalid choice")

def setup_encrypted_config():
    """Setup encrypted configuration"""
    print("\n=== Setting up Encrypted Configuration ===")
    
    # Get credentials
    config_data = {}
    config_data['access_key_id'] = input("Enter Access Key ID: ").strip()
    config_data['secret_access_key'] = getpass.getpass("Enter Secret Access Key: ")
    config_data['server'] = input("Enter OBS Server URL [https://obs.sa-peru-1.myhuaweicloud.com/]: ").strip()
    if not config_data['server']:
        config_data['server'] = "https://obs.sa-peru-1.myhuaweicloud.com/"
    
    config_data['region'] = input("Enter Region [sa-peru-1]: ").strip()
    if not config_data['region']:
        config_data['region'] = "sa-peru-1"
    
    config_data['max_keys'] = 1000
    config_data['restore_days'] = 30
    config_data['restore_tier'] = "Expedited"
    
    # Create encrypted configuration
    security = ConfigSecurity()
    if security.create_encrypted_config(config_data):
        print("✅ Encrypted configuration created successfully!")
        print(f"Files created: {security.encrypted_file}, {security.salt_file}")
        print("⚠️  Keep your password safe - it cannot be recovered!")
    else:
        print("❌ Failed to create encrypted configuration")

def setup_env_variables():
    """Setup environment variables"""
    print("\n=== Setting up Environment Variables ===")
    print("Add these variables to your shell profile (.bashrc, .zshrc, etc.):")
    print()
    
    access_key = input("Enter Access Key ID: ").strip()
    secret_key = getpass.getpass("Enter Secret Access Key: ")
    server = input("Enter OBS Server URL [https://obs.sa-peru-1.myhuaweicloud.com/]: ").strip()
    if not server:
        server = "https://obs.sa-peru-1.myhuaweicloud.com/"
    
    print("\n# Add these lines to your shell profile:")
    print(f'export OBS_ACCESS_KEY_ID="{access_key}"')
    print(f'export OBS_SECRET_ACCESS_KEY="{secret_key}"')
    print(f'export OBS_SERVER="{server}"')
    print('export OBS_REGION="sa-peru-1"')

def setup_secure_file():
    """Setup regular file with secure permissions"""
    print("\n=== Setting up Secure Configuration File ===")
    
    config_data = {}
    config_data['access_key_id'] = input("Enter Access Key ID: ").strip()
    config_data['secret_access_key'] = getpass.getpass("Enter Secret Access Key: ")
    config_data['server'] = input("Enter OBS Server URL [https://obs.sa-peru-1.myhuaweicloud.com/]: ").strip()
    if not config_data['server']:
        config_data['server'] = "https://obs.sa-peru-1.myhuaweicloud.com/"
    
    config_data['region'] = input("Enter Region [sa-peru-1]: ").strip()
    if not config_data['region']:
        config_data['region'] = "sa-peru-1"
    
    config_data['max_keys'] = 1000
    config_data['restore_days'] = 30
    config_data['restore_tier'] = "Expedited"
    
    # Write configuration file
    with open("obs_config.json", 'w') as f:
        json.dump(config_data, f, indent=2)
    
    # Set secure permissions
    os.chmod("obs_config.json", 0o600)
    
    print("✅ Secure configuration file created!")
    print("File permissions set to 600 (owner read/write only)")


if __name__ == "__main__":
    setup_secure_config()
