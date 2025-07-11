#!/usr/bin/env python3
"""
OBS Utils - Improved version
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
"""
import sys
import argparse
from typing import Optional
from obs_manager import OBSManager
from config import Config
from logger import get_logger


def get_user_input(prompt: str, required: bool = True, default: str = "") -> str:
    """
    Get user input with validation
    
    Args:
        prompt: Input prompt message
        required: Whether input is required
        default: Default value if empty input
        
    Returns:
        User input string
    """
    while True:
        try:
            value = input(prompt).strip()
            
            if not value and required and not default:
                print("This field is required. Please enter a value.")
                continue
            
            return value or default
            
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            sys.exit(0)
        except EOFError:
            print("\nUnexpected end of input.")
            sys.exit(1)


def interactive_mode():
    """Run in interactive mode with user prompts"""
    logger = get_logger(__name__)
    
    try:
        # Ask if user wants to enable security levels
        print("🔐 Security Options:")
        print("1. Standard mode (basic security)")
        print("2. Multi-level security mode (advanced)")
        
        security_choice = get_user_input("Choose security mode (1-2) [1]: ", required=False, default="1")
        
        # Initialize OBS Manager
        if security_choice == "2":
            try:
                from obs_manager_secure import SecureOBSManager
                obs_manager = SecureOBSManager(enable_security_levels=True)
                print("✅ Multi-level security enabled")
            except ImportError:
                print("⚠️  Security levels not available, using standard manager")
                from obs_manager import OBSManager
                obs_manager = OBSManager()
        else:
            from obs_manager import OBSManager
            obs_manager = OBSManager()
        
        print("=== OBS Utils - Interactive Mode ===")
        print("Available operations:")
        print("(l) List objects")
        print("(a) Archive objects (change to COLD storage)")
        print("(i) Infrequent access (change to WARM storage)")
        print("(r) Restore archived objects")
        print("(d) Download objects from path")
        print("(f) Download single file")
        print("(x) Search objects by name")
        print()
        
        operation = get_user_input(
            "Select operation [l/a/i/r/d/f/x]: ",
            required=True
        ).lower()
        
        if operation not in ['l', 'a', 'i', 'r', 'd', 'f', 'x']:
            print("Invalid operation selected.")
            return
        
        # Get bucket and route based on operation
        if operation == 'x':
            bucket = get_user_input(
                "Enter bucket name (press ENTER to search all buckets): ",
                required=False
            )
            route = get_user_input(
                "Enter path prefix (press ENTER for root): ",
                required=False
            )
            search_text = get_user_input(
                "Enter search text: ",
                required=True
            )
        else:
            bucket = get_user_input(
                "Enter bucket name: ",
                required=True
            )
            route = get_user_input(
                "Enter path prefix (press ENTER for root): ",
                required=False
            )
        
        # Execute operation
        count = 0
        
        if operation == 'l':
            count = obs_manager.list_objects(bucket, route)
            
        elif operation == 'a':
            count = obs_manager.change_storage_class(bucket, route, "COLD")
            
        elif operation == 'i':
            count = obs_manager.change_storage_class(bucket, route, "WARM")
            
        elif operation == 'r':
            days = get_user_input(
                "Enter restore days (default: 30): ",
                required=False,
                default="30"
            )
            tier = get_user_input(
                "Enter restore tier [Expedited/Standard/Bulk] (default: Expedited): ",
                required=False,
                default="Expedited"
            )
            
            try:
                days = int(days)
            except ValueError:
                print("Invalid number of days. Using default: 30")
                days = 30
            
            if tier not in ["Expedited", "Standard", "Bulk"]:
                print("Invalid tier. Using default: Expedited")
                tier = "Expedited"
            
            count = obs_manager.restore_objects(bucket, route, days, tier)
            
        elif operation == 'd':
            download_path = get_user_input(
                "Enter local download path (press ENTER for default): ",
                required=False
            )
            count = obs_manager.download_objects(bucket, route, download_path or None)
            
        elif operation == 'f':
            object_key = route or get_user_input("Enter object key: ", required=True)
            download_path = get_user_input(
                "Enter local download path (press ENTER for default): ",
                required=False
            )
            success = obs_manager.download_single_file(bucket, object_key, download_path or None)
            count = 1 if success else 0
            
        elif operation == 'x':
            count = obs_manager.search_objects(search_text, bucket, route)
        
        print(f"\nOperation completed. Items processed: {count}")
        
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        print(f"Configuration error: {e}")
        print("Please check your configuration file or environment variables.")
        
        # Offer to create sample config
        create_sample = get_user_input(
            "Would you like to create a sample configuration file? [y/N]: ",
            required=False,
            default="n"
        ).lower()
        
        if create_sample == 'y':
            Config().create_sample_config()
        
        sys.exit(1)
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
        
    finally:
        try:
            obs_manager.close()
        except:
            pass


def command_line_mode(args):
    """Run in command line mode with arguments"""
    logger = get_logger(__name__)
    
    try:
        # Use SecureOBSManager if security levels are enabled
        if hasattr(args, 'enable_security_levels') and args.enable_security_levels:
            try:
                from obs_manager_secure import SecureOBSManager
                obs_manager = SecureOBSManager(args.config, enable_security_levels=True)
                print("🔐 Multi-level security enabled")
            except ImportError:
                print("⚠️  Security levels not available, using standard manager")
                from obs_manager import OBSManager
                obs_manager = OBSManager(args.config)
        else:
            from obs_manager import OBSManager
            obs_manager = OBSManager(args.config)
        
        count = 0
        
        if args.operation == 'list':
            count = obs_manager.list_objects(args.bucket, args.prefix or "")
            
        elif args.operation == 'archive':
            count = obs_manager.change_storage_class(args.bucket, args.prefix or "", "COLD")
            
        elif args.operation == 'warm':
            count = obs_manager.change_storage_class(args.bucket, args.prefix or "", "WARM")
            
        elif args.operation == 'restore':
            count = obs_manager.restore_objects(
                args.bucket, 
                args.prefix or "", 
                args.days, 
                args.tier
            )
            
        elif args.operation == 'download':
            if args.object_key:
                success = obs_manager.download_single_file(
                    args.bucket, 
                    args.object_key, 
                    args.download_path
                )
                count = 1 if success else 0
            else:
                count = obs_manager.download_objects(
                    args.bucket, 
                    args.prefix or "", 
                    args.download_path
                )
                
        elif args.operation == 'search':
            count = obs_manager.search_objects(
                args.search_text, 
                args.bucket or "", 
                args.prefix or ""
            )
        
        print(f"Operation completed. Items processed: {count}")
        
    except Exception as e:
        logger.error(f"Error in command line mode: {e}")
        print(f"Error: {e}")
        sys.exit(1)
        
    finally:
        try:
            obs_manager.close()
        except:
            pass


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="OBS Utils - Huawei Cloud Object Storage utilities",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python obs_utils_improved.py
  
  # List objects
  python obs_utils_improved.py --operation list --bucket my-bucket
  
  # Archive objects with prefix
  python obs_utils_improved.py --operation archive --bucket my-bucket --prefix folder/
  
  # Search for files
  python obs_utils_improved.py --operation search --search-text "backup" --bucket my-bucket
  
  # Download single file
  python obs_utils_improved.py --operation download --bucket my-bucket --object-key file.txt
        """
    )
    
    parser.add_argument(
        '--config', 
        default='obs_config.json',
        help='Configuration file path (default: obs_config.json)'
    )
    
    parser.add_argument(
        '--operation',
        choices=['list', 'archive', 'warm', 'restore', 'download', 'search'],
        help='Operation to perform'
    )
    
    parser.add_argument(
        '--bucket',
        help='Bucket name'
    )
    
    parser.add_argument(
        '--prefix',
        help='Object prefix/path'
    )
    
    parser.add_argument(
        '--object-key',
        help='Specific object key (for single file operations)'
    )
    
    parser.add_argument(
        '--download-path',
        help='Local download path'
    )
    
    parser.add_argument(
        '--search-text',
        help='Text to search for in object names'
    )
    
    parser.add_argument(
        '--days',
        type=int,
        default=30,
        help='Number of days for restore operation (default: 30)'
    )
    
    parser.add_argument(
        '--tier',
        choices=['Expedited', 'Standard', 'Bulk'],
        default='Expedited',
        help='Restore tier (default: Expedited)'
    )
    
    parser.add_argument(
        '--create-config',
        action='store_true',
        help='Create sample configuration file and exit'
    )
    
    parser.add_argument(
        '--setup-secure-config',
        action='store_true',
        help='Run interactive secure configuration setup'
    )
    
    parser.add_argument(
        '--encrypt-config',
        action='store_true',
        help='Encrypt existing configuration file'
    )
    
    parser.add_argument(
        '--secure-permissions',
        action='store_true',
        help='Set secure permissions on configuration file'
    )
    
    parser.add_argument(
        '--setup-security-levels',
        action='store_true',
        help='Setup multi-level security system'
    )
    
    parser.add_argument(
        '--list-security-levels',
        action='store_true',
        help='List configured security levels'
    )
    
    parser.add_argument(
        '--enable-security-levels',
        action='store_true',
        help='Enable multi-level security for this session'
    )
    
    args = parser.parse_args()
    
    # Handle security operations first
    if args.setup_secure_config:
        try:
            from security import setup_secure_config
            setup_secure_config()
        except ImportError:
            print("❌ Security module not available. Install cryptography: pip install cryptography")
            sys.exit(1)
        return
    
    if args.setup_security_levels:
        try:
            from security_levels import setup_multi_level_security
            setup_multi_level_security()
        except ImportError:
            print("❌ Security levels module not available. Install cryptography: pip install cryptography")
            sys.exit(1)
        return
    
    if args.list_security_levels:
        try:
            from obs_manager_secure import SecureOBSManager
            obs_manager = SecureOBSManager(args.config, enable_security_levels=True)
            obs_manager.list_security_levels()
            obs_manager.close()
        except ImportError:
            print("❌ Security levels module not available")
            sys.exit(1)
        return
    
    if args.encrypt_config:
        try:
            config = Config(args.config)
            if config.encrypt_configuration():
                print("✅ Configuration encrypted successfully!")
            else:
                print("❌ Failed to encrypt configuration")
                sys.exit(1)
        except ImportError:
            print("❌ Security module not available. Install cryptography: pip install cryptography")
            sys.exit(1)
        return
    
    if args.secure_permissions:
        config = Config(args.config)
        if config.secure_file_permissions():
            print("✅ Secure permissions set on configuration file")
        else:
            print("❌ Could not set secure permissions (Windows or file not found)")
        return
    
    # Handle config creation
    if args.create_config:
        Config().create_sample_config()
        return
    
    # Run in appropriate mode
    if args.operation:
        # Command line mode
        if not args.bucket and args.operation != 'search':
            print("Error: --bucket is required for this operation")
            sys.exit(1)
        
        if args.operation == 'search' and not args.search_text:
            print("Error: --search-text is required for search operation")
            sys.exit(1)
        
        command_line_mode(args)
    else:
        # Interactive mode
        interactive_mode()


if __name__ == "__main__":
    main()
