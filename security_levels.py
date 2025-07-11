#!/usr/bin/env python3
"""
Security Levels Module for OBS Utils
Implements multi-level password protection for different operations

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
import getpass
import hashlib
from typing import Dict, List, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import logging

logger = logging.getLogger(__name__)

class SecurityLevel:
    """Security level definitions"""
    READ_ONLY = "read_only"          # List, search, download
    STANDARD = "standard"            # Archive, restore, warm storage
    DESTRUCTIVE = "destructive"      # Delete operations (future)
    ADMIN = "admin"                  # Bucket management, configuration changes

class MultiLevelSecurity:
    """Multi-level password security system"""
    
    def __init__(self, config_file: str = "obs_security_levels.json"):
        self.config_file = config_file
        self.encrypted_file = f"{config_file}.enc"
        self.salt_file = f"{config_file}.salt"
        self.security_config = {}
        self._load_security_config()
    
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
        """Hash password for storage"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _load_security_config(self):
        """Load security configuration"""
        try:
            # Try encrypted version first
            if os.path.exists(self.encrypted_file) and os.path.exists(self.salt_file):
                master_password = getpass.getpass("Enter master password for security levels: ")
                self.security_config = self._decrypt_security_config(master_password)
            elif os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.security_config = json.load(f)
            else:
                # Create default configuration
                self.security_config = self._create_default_config()
        except Exception as e:
            logger.error(f"Error loading security configuration: {e}")
            self.security_config = self._create_default_config()
    
    def _create_default_config(self) -> Dict:
        """Create default security configuration"""
        return {
            "levels": {
                SecurityLevel.READ_ONLY: {
                    "password_hash": None,
                    "operations": ["list", "search", "download"],
                    "description": "Read-only operations (list, search, download)"
                },
                SecurityLevel.STANDARD: {
                    "password_hash": None,
                    "operations": ["archive", "warm", "restore"],
                    "description": "Standard operations (archive, restore, change storage class)"
                },
                SecurityLevel.DESTRUCTIVE: {
                    "password_hash": None,
                    "operations": ["delete", "purge"],
                    "description": "Destructive operations (delete objects, purge buckets)"
                },
                SecurityLevel.ADMIN: {
                    "password_hash": None,
                    "operations": ["create_bucket", "delete_bucket", "manage_permissions"],
                    "description": "Administrative operations (bucket management)"
                }
            },
            "settings": {
                "require_confirmation": True,
                "log_all_operations": True,
                "session_timeout": 3600  # 1 hour
            }
        }
    
    def _encrypt_security_config(self, master_password: str) -> bool:
        """Encrypt security configuration"""
        try:
            config_json = json.dumps(self.security_config, indent=2)
            key, salt = self._generate_key(master_password)
            
            fernet = Fernet(key)
            encrypted_data = fernet.encrypt(config_json.encode())
            
            with open(self.encrypted_file, 'wb') as f:
                f.write(encrypted_data)
            
            with open(self.salt_file, 'wb') as f:
                f.write(salt)
            
            # Set secure permissions
            if os.name != 'nt':
                os.chmod(self.encrypted_file, 0o600)
                os.chmod(self.salt_file, 0o600)
            
            return True
        except Exception as e:
            logger.error(f"Error encrypting security config: {e}")
            return False
    
    def _decrypt_security_config(self, master_password: str) -> Dict:
        """Decrypt security configuration"""
        try:
            with open(self.salt_file, 'rb') as f:
                salt = f.read()
            
            key, _ = self._generate_key(master_password, salt)
            
            with open(self.encrypted_file, 'rb') as f:
                encrypted_data = f.read()
            
            fernet = Fernet(key)
            decrypted_data = fernet.decrypt(encrypted_data)
            
            return json.loads(decrypted_data.decode())
        except Exception as e:
            logger.error(f"Error decrypting security config: {e}")
            raise ValueError("Invalid master password or corrupted security configuration")
    
    def setup_security_levels(self):
        """Interactive setup for security levels"""
        print("🔐 Multi-Level Security Setup")
        print("=" * 40)
        print()
        
        # Ask for master password
        master_password = getpass.getpass("Create master password for security system: ")
        confirm_password = getpass.getpass("Confirm master password: ")
        
        if master_password != confirm_password:
            print("❌ Passwords do not match")
            return False
        
        print("\nSetting up security levels...")
        print("Leave password empty to disable a security level")
        print()
        
        for level_name, level_config in self.security_config["levels"].items():
            print(f"\n📋 {level_name.upper()} Level")
            print(f"   Operations: {', '.join(level_config['operations'])}")
            print(f"   Description: {level_config['description']}")
            
            password = getpass.getpass(f"   Set password for {level_name} level (or ENTER to skip): ")
            
            if password:
                level_config["password_hash"] = self._hash_password(password)
                print(f"   ✅ Password set for {level_name} level")
            else:
                level_config["password_hash"] = None
                print(f"   ⚠️  No password set for {level_name} level (unrestricted)")
        
        # Save encrypted configuration
        if self._encrypt_security_config(master_password):
            print("\n✅ Security levels configured and encrypted successfully!")
            
            # Remove unencrypted file if it exists
            if os.path.exists(self.config_file):
                os.remove(self.config_file)
            
            return True
        else:
            print("\n❌ Failed to save security configuration")
            return False
    
    def get_operation_level(self, operation: str) -> Optional[str]:
        """Get required security level for an operation"""
        for level_name, level_config in self.security_config["levels"].items():
            if operation in level_config["operations"]:
                return level_name
        return SecurityLevel.READ_ONLY  # Default to read-only
    
    def verify_access(self, operation: str) -> bool:
        """Verify access for an operation"""
        required_level = self.get_operation_level(operation)
        level_config = self.security_config["levels"].get(required_level, {})
        
        # If no password is set for this level, allow access
        if not level_config.get("password_hash"):
            logger.info(f"Operation '{operation}' allowed (no password required for {required_level} level)")
            return True
        
        # Ask for password
        print(f"\n🔐 Security Check Required")
        print(f"Operation: {operation}")
        print(f"Security Level: {required_level.upper()}")
        print(f"Description: {level_config.get('description', 'N/A')}")
        
        max_attempts = 3
        for attempt in range(max_attempts):
            password = getpass.getpass(f"Enter password for {required_level} level: ")
            password_hash = self._hash_password(password)
            
            if password_hash == level_config["password_hash"]:
                logger.info(f"Access granted for operation '{operation}' at {required_level} level")
                return True
            else:
                remaining = max_attempts - attempt - 1
                if remaining > 0:
                    print(f"❌ Invalid password. {remaining} attempts remaining.")
                else:
                    print("❌ Access denied. Maximum attempts exceeded.")
        
        logger.warning(f"Access denied for operation '{operation}' at {required_level} level")
        return False
    
    def require_confirmation(self, operation: str, details: str = "") -> bool:
        """Require user confirmation for sensitive operations"""
        if not self.security_config["settings"].get("require_confirmation", True):
            return True
        
        required_level = self.get_operation_level(operation)
        
        # Only require confirmation for standard and above
        if required_level in [SecurityLevel.STANDARD, SecurityLevel.DESTRUCTIVE, SecurityLevel.ADMIN]:
            print(f"\n⚠️  Confirmation Required")
            print(f"Operation: {operation}")
            print(f"Security Level: {required_level.upper()}")
            if details:
                print(f"Details: {details}")
            
            response = input("Do you want to proceed? (yes/no): ").lower().strip()
            return response in ['yes', 'y']
        
        return True
    
    def list_security_levels(self):
        """List all configured security levels"""
        print("\n🔐 Security Levels Configuration")
        print("=" * 50)
        
        for level_name, level_config in self.security_config["levels"].items():
            password_status = "✅ Protected" if level_config.get("password_hash") else "⚠️  Unprotected"
            
            print(f"\n📋 {level_name.upper()} Level - {password_status}")
            print(f"   Operations: {', '.join(level_config['operations'])}")
            print(f"   Description: {level_config['description']}")
        
        print(f"\nSettings:")
        print(f"   Require Confirmation: {self.security_config['settings']['require_confirmation']}")
        print(f"   Log All Operations: {self.security_config['settings']['log_all_operations']}")
        print(f"   Session Timeout: {self.security_config['settings']['session_timeout']} seconds")


def setup_multi_level_security():
    """Setup function for multi-level security"""
    security = MultiLevelSecurity()
    return security.setup_security_levels()


if __name__ == "__main__":
    # Interactive setup
    setup_multi_level_security()
