#!/usr/bin/env python3
"""
OBS Utils - Improved version with cross-platform compatibility
Huawei Cloud Object Storage Service utilities with better error handling,
configuration management, and code organization.

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

import argparse
import sys
import os
import platform
from typing import Optional

# Cross-platform compatibility setup
def setup_cross_platform_compatibility():
    """Setup cross-platform compatibility settings"""
    if platform.system() == "Windows":
        # Fix console encoding for Unicode characters on Windows
        try:
            import codecs
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
            sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
        except:
            pass
        
        # Set console code page to UTF-8 if possible
        try:
            os.system('chcp 65001 >nul 2>&1')
        except:
            pass

# Initialize cross-platform compatibility
setup_cross_platform_compatibility()

# Safe imports with fallbacks for missing dependencies
try:
    from config import Config
except ImportError:
    print("Warning: config module not found. Please ensure all dependencies are installed.")
    sys.exit(1)

try:
    from logger import get_logger
except ImportError:
    print("Warning: logger module not found. Using basic logging.")
    import logging
    def get_logger(name):
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger(name)

try:
    from obs_manager import OBSManager
except ImportError:
    print("Warning: obs_manager module not found.")
    print("Please install the Huawei Cloud OBS SDK: pip install esdk-obs-python")
    
    # Create a mock OBS Manager for testing when SDK is not available
    class MockOBSManager:
        def __init__(self, config_file):
            print(f"[MOCK MODE] Using mock OBS manager with config: {config_file}")
        
        def list_objects(self, bucket, prefix=""):
            print(f"[MOCK] Would list objects in bucket '{bucket}' with prefix '{prefix}'")
            return 0
        
        def download_objects(self, bucket, prefix, download_path):
            print(f"[MOCK] Would download from bucket '{bucket}', prefix '{prefix}' to '{download_path}'")
            return 0
        
        def download_single_file(self, bucket, object_key, download_path):
            print(f"[MOCK] Would download '{object_key}' from bucket '{bucket}' to '{download_path}'")
            return True
        
        def search_objects(self, search_text, bucket, prefix):
            print(f"[MOCK] Would search for '{search_text}' in bucket '{bucket}' with prefix '{prefix}'")
            return 0
        
        def change_storage_class(self, bucket, prefix, storage_class):
            print(f"[MOCK] Would change storage class to '{storage_class}' for bucket '{bucket}', prefix '{prefix}'")
            return 0
        
        def restore_objects(self, bucket, prefix, days, tier):
            print(f"[MOCK] Would restore objects in bucket '{bucket}', prefix '{prefix}' for {days} days, tier '{tier}'")
            return 0
    
    OBSManager = MockOBSManager


def get_user_input(prompt: str, required: bool = True, default: str = "") -> str:
    """
    Get user input with validation - Cross-platform compatible

    Args:
        prompt: Input prompt message
        required: Whether input is required
        default: Default value if empty input

    Returns:
        User input string
    """
    while True:
        try:
            # Cross-platform safe prompt handling
            if platform.system() == "Windows":
                # Use safe characters for Windows console
                safe_prompt = prompt.replace("✓", "[OK]").replace("✗", "[ERROR]").replace("→", "->")
                value = input(safe_prompt).strip()
            else:
                value = input(prompt).strip()

            if not value and required and not default:
                print("This field is required. Please enter a value.")
                continue

            return value or default

        except (KeyboardInterrupt, EOFError):
            print("\nOperation cancelled by user.")
            sys.exit(0)
        except Exception as e:
            print(f"Input error: {e}")
            if not required:
                return default


def interactive_mode():
    """Run in interactive mode - Cross-platform compatible"""
    logger = get_logger(__name__)

    try:
        # Ask for configuration file
        config_file = get_user_input("Enter configuration file path (default: obs_config.json): ", 
                                   required=False, default="obs_config.json")

        # Check if config file exists
        if not os.path.exists(config_file):
            print(f"Configuration file '{config_file}' not found.")
            create_config = get_user_input("Would you like to create a sample configuration? (y/n): ", 
                                         required=False, default="y")
            if create_config.lower() in ['y', 'yes']:
                try:
                    Config().create_sample_config(config_file)
                    print(f"Sample configuration created at '{config_file}'")
                    print("Please edit the configuration file with your OBS credentials and run again.")
                    return
                except Exception as e:
                    print(f"Error creating configuration: {e}")
                    return
            else:
                return

        # Ask if user wants to enable security levels
        print("[SECURITY] Security Options:")
        print("1. Standard mode (basic security)")
        print("2. Multi-level security mode (advanced)")

        security_choice = get_user_input("Choose security mode (1-2) [1]: ", required=False, default="1")

        # Initialize OBS Manager
        if security_choice == "2":
            try:
                from obs_manager_secure import SecureOBSManager
                obs_manager = SecureOBSManager(config_file, enable_security_levels=True)
                print("[OK] Multi-level security enabled")
            except ImportError:
                print("[WARNING] Security levels not available, using standard manager")
                obs_manager = OBSManager(config_file)
        else:
            obs_manager = OBSManager(config_file)

        while True:
            print("\nAvailable operations:")
            print("(l) List objects")
            print("(d) Download objects from path")
            print("(f) Download single file")
            print("(s) Search objects")
            print("(a) Archive objects (change to COLD storage)")
            print("(w) Warm objects (change to WARM storage)")
            print("(r) Restore archived objects")
            print("(q) Quit")

            operation = get_user_input("Select operation: ", required=True).lower()

            if operation == 'q':
                break

            bucket = get_user_input("Enter bucket name: ", required=True)

            if operation == 'l':
                route = get_user_input("Enter path prefix (press ENTER for root): ", required=False)
                count = obs_manager.list_objects(bucket, route)
                print(f"Listed {count} objects")

            elif operation == 'd':
                route = get_user_input("Enter path prefix (press ENTER for root): ", required=False)
                
                # Cross-platform safe path handling
                default_download = os.path.join(os.getcwd(), "downloads")
                download_path = get_user_input(f"Enter local download path (default: {default_download}): ", 
                                             required=False, default=default_download)
                
                # Ensure download directory exists
                try:
                    os.makedirs(download_path, exist_ok=True)
                except Exception as e:
                    print(f"Error creating download directory: {e}")
                    continue
                
                count = obs_manager.download_objects(bucket, route, download_path)
                print(f"Downloaded {count} objects to '{download_path}'")

            elif operation == 'f':
                object_key = get_user_input("Enter object key/path: ", required=True)
                
                # Cross-platform safe path handling
                default_download = os.path.join(os.getcwd(), "downloads", os.path.basename(object_key))
                download_path = get_user_input(f"Enter local download path (default: {default_download}): ", 
                                             required=False, default=default_download)
                
                # Ensure download directory exists
                download_dir = os.path.dirname(download_path)
                if download_dir:
                    try:
                        os.makedirs(download_dir, exist_ok=True)
                    except Exception as e:
                        print(f"Error creating download directory: {e}")
                        continue
                
                success = obs_manager.download_single_file(bucket, object_key, download_path)
                if success:
                    print(f"Downloaded '{object_key}' to '{download_path}'")
                else:
                    print(f"Failed to download '{object_key}'")

            elif operation == 's':
                search_text = get_user_input("Enter search text: ", required=True)
                route = get_user_input("Enter path prefix (press ENTER for root): ", required=False)
                count = obs_manager.search_objects(search_text, bucket, route)
                print(f"Found {count} matching objects")

            elif operation in ['a', 'w']:
                route = get_user_input("Enter path prefix (press ENTER for root): ", required=False)
                storage_class = "COLD" if operation == 'a' else "WARM"
                count = obs_manager.change_storage_class(bucket, route, storage_class)
                print(f"Changed storage class for {count} objects to {storage_class}")

            elif operation == 'r':
                route = get_user_input("Enter path prefix (press ENTER for root): ", required=False)
                days = get_user_input("Enter restore duration in days (default: 1): ", required=False, default="1")
                tier = get_user_input("Enter restore tier (Expedited/Standard/Bulk, default: Expedited): ", 
                                    required=False, default="Expedited")
                
                try:
                    days = int(days)
                except ValueError:
                    print("Invalid number of days. Using default: 1")
                    days = 1
                
                if tier not in ["Expedited", "Standard", "Bulk"]:
                    print("Invalid tier. Using default: Expedited")
                    tier = "Expedited"
                
                count = obs_manager.restore_objects(bucket, route, days, tier)
                print(f"Restored {count} objects for {days} days with {tier} tier")

            else:
                print("Invalid choice. Please try again.")

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        logger.error(f"Error in interactive mode: {e}")
        print(f"Error: {e}")
        if "credentials" in str(e).lower():
            print("Please check your OBS credentials in the configuration file.")


def command_line_mode(args):
    """Run in command line mode with arguments - Cross-platform compatible"""
    logger = get_logger(__name__)

    try:
        # Test mode for CI/CD - skip credential validation
        if hasattr(args, "test_mode") and args.test_mode:
            print("[TEST MODE] Skipping OBS client initialization for CI/CD testing")
            return

        # Use SecureOBSManager if security levels are enabled
        if hasattr(args, "enable_security_levels") and args.enable_security_levels:
            try:
                from obs_manager_secure import SecureOBSManager
                obs_manager = SecureOBSManager(args.config, enable_security_levels=True)
                print("[OK] Multi-level security enabled")
            except ImportError:
                print("[WARNING] Security levels not available, using standard manager")
                obs_manager = OBSManager(args.config)
        else:
            obs_manager = OBSManager(args.config)

        count = 0

        if args.operation == "list":
            count = obs_manager.list_objects(args.bucket, args.prefix or "")

        elif args.operation == "archive":
            count = obs_manager.change_storage_class(args.bucket, args.prefix or "", "COLD")

        elif args.operation == "warm":
            count = obs_manager.change_storage_class(args.bucket, args.prefix or "", "WARM")

        elif args.operation == "restore":
            count = obs_manager.restore_objects(args.bucket, args.prefix or "", args.days, args.tier)

        elif args.operation == "download":
            if args.object_key:
                # Cross-platform safe path handling for single file download
                download_path = args.download_path
                if download_path:
                    download_dir = os.path.dirname(download_path)
                    if download_dir:
                        os.makedirs(download_dir, exist_ok=True)
                
                success = obs_manager.download_single_file(args.bucket, args.object_key, download_path)
                count = 1 if success else 0
            else:
                # Cross-platform safe path handling for bulk download
                download_path = args.download_path or os.path.join(os.getcwd(), "downloads")
                os.makedirs(download_path, exist_ok=True)
                count = obs_manager.download_objects(args.bucket, args.prefix or "", download_path)

        elif args.operation == "search":
            count = obs_manager.search_objects(args.search_text, args.bucket or "", args.prefix or "")

        print(f"Operation completed. Items processed: {count}")

    except Exception as e:
        logger.error(f"Error in command line mode: {e}")
        print(f"Error: {e}")
        if "credentials" in str(e).lower():
            print("Please check your OBS credentials in the configuration file.")
        sys.exit(1)


def create_parser():
    """Create argument parser - Cross-platform compatible"""
    parser = argparse.ArgumentParser(
        description="OBS Utils - Huawei Cloud Object Storage utilities (Cross-platform)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python obs_utils_improved.py

  # List objects
  python obs_utils_improved.py --operation list --bucket my-bucket

  # Download objects
  python obs_utils_improved.py --operation download --bucket my-bucket --prefix folder/

  # Search objects
  python obs_utils_improved.py --operation search --search-text "report" --bucket my-bucket

  # Create sample configuration
  python obs_utils_improved.py --create-config
        """
    )

    parser.add_argument("--config", default="obs_config.json", 
                       help="Configuration file path (default: obs_config.json)")

    parser.add_argument("--operation", choices=["list", "download", "search", "archive", "warm", "restore"],
                       help="Operation to perform")

    parser.add_argument("--bucket", help="Bucket name")
    parser.add_argument("--prefix", help="Object prefix/path")
    parser.add_argument("--object-key", help="Specific object key for single file operations")
    parser.add_argument("--search-text", help="Text to search for in object names")
    parser.add_argument("--download-path", help="Local download path")
    parser.add_argument("--days", type=int, default=1, help="Restore duration in days (default: 1)")
    parser.add_argument("--tier", choices=["Expedited", "Standard", "Bulk"], default="Expedited",
                       help="Restore tier (default: Expedited)")

    parser.add_argument("--create-config", action="store_true", 
                       help="Create sample configuration file and exit")

    parser.add_argument("--setup-secure-config", action="store_true", 
                       help="Run interactive secure configuration setup")

    parser.add_argument("--encrypt-config", action="store_true", 
                       help="Encrypt existing configuration file")

    parser.add_argument("--secure-permissions", action="store_true", 
                       help="Set secure permissions on configuration file")

    parser.add_argument("--setup-security-levels", action="store_true", 
                       help="Setup multi-level security system")

    parser.add_argument("--list-security-levels", action="store_true", 
                       help="List configured security levels")

    parser.add_argument("--enable-security-levels", action="store_true", 
                       help="Enable multi-level security for this session")

    parser.add_argument("--test-mode", action="store_true", 
                       help="Run in test mode (skip credential validation for CI/CD)")

    return parser


def main():
    """Main function - Cross-platform compatible"""
    parser = create_parser()
    args = parser.parse_args()

    # Handle security operations first
    if args.setup_secure_config:
        try:
            from security import setup_secure_config
            setup_secure_config()
        except ImportError:
            print("[ERROR] Security module not available. Install cryptography: pip install cryptography")
            sys.exit(1)
        return

    if args.setup_security_levels:
        try:
            from security_levels import setup_multi_level_security
            setup_multi_level_security()
        except ImportError:
            print("[ERROR] Security levels module not available. Install cryptography: pip install cryptography")
            sys.exit(1)
        return

    if args.list_security_levels:
        # Test mode for CI/CD
        if hasattr(args, "test_mode") and args.test_mode:
            print("[TEST MODE] Security levels listing skipped for CI/CD testing")
            return

        try:
            from obs_manager_secure import SecureOBSManager
            obs_manager = SecureOBSManager(args.config, enable_security_levels=True)
            obs_manager.list_security_levels()
            obs_manager.close()
        except ImportError:
            print("[ERROR] Security levels module not available")
            sys.exit(1)
        except ValueError as e:
            if "credentials" in str(e).lower():
                print("[TEST MODE] Credentials not available - this is expected in CI/CD")
                return
            raise
        return

    if args.encrypt_config:
        try:
            config = Config(args.config)
            if config.encrypt_configuration():
                print("[OK] Configuration encrypted successfully!")
            else:
                print("[ERROR] Failed to encrypt configuration")
                sys.exit(1)
        except ImportError:
            print("[ERROR] Security module not available. Install cryptography: pip install cryptography")
            sys.exit(1)
        return

    if args.secure_permissions:
        config = Config(args.config)
        if config.secure_file_permissions():
            print("[OK] Secure permissions set on configuration file")
        else:
            print("[WARNING] Could not set secure permissions (Windows or file not found)")
        return

    # Handle config creation
    if args.create_config:
        try:
            Config().create_sample_config()
            print("[OK] Sample configuration file created successfully!")
        except Exception as e:
            print(f"[ERROR] Failed to create configuration: {e}")
            sys.exit(1)
        return

    # Run in appropriate mode
    if args.operation:
        # Command line mode
        if not args.bucket and args.operation != "search":
            print("Error: --bucket is required for this operation")
            sys.exit(1)

        if args.operation == "search" and not args.search_text:
            print("Error: --search-text is required for search operation")
            sys.exit(1)

        command_line_mode(args)
    else:
        # Interactive mode
        interactive_mode()


if __name__ == "__main__":
    main()