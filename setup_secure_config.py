#!/usr/bin/env python3
"""
Interactive setup for secure OBS Utils configuration
"""

import getpass
import json
import os
import sys

from security import setup_secure_config


def main():
    """Main setup function"""
    print("🔒 OBS Utils - Secure Configuration Setup")
    print("=" * 50)
    print()

    # Check if configuration already exists
    config_files = ["obs_config.json", "obs_config.json.enc", "obs_config.json.salt"]

    existing_configs = [f for f in config_files if os.path.exists(f)]

    if existing_configs:
        print("⚠️  Existing configuration files found:")
        for config in existing_configs:
            print(f"   - {config}")
        print()

        response = input("Continue and potentially overwrite? (y/N): ")
        if response.lower() != "y":
            print("Setup cancelled.")
            return
        print()

    # Run interactive setup
    try:
        setup_secure_config()
        print()
        print("✅ Secure configuration setup completed!")
        print()
        print("Next steps:")
        print("1. Test your configuration:")
        print("   python obs_utils_improved.py --operation list --bucket test-bucket")
        print("2. If using encrypted config, remember your password!")
        print("3. Consider backing up your configuration securely")

    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
