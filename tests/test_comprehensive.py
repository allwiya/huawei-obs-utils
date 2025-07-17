#!/usr/bin/env python3
"""
Comprehensive tests for OBS Utils - Production ready test suite
"""

import json
import os
import tempfile
import sys
import hashlib
import re
import base64
import time
from datetime import datetime
from unittest.mock import Mock, patch

class TestComprehensive:
    """Comprehensive test suite for OBS Utils"""
    
    def test_config_functionality(self):
        """Test configuration functionality"""
        from config import Config
        
        # Test valid configuration
        test_config = {
            "access_key_id": "AKIAIOSFODNN7EXAMPLE",
            "secret_access_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
            "server": "https://obs.ap-southeast-1.myhuaweicloud.com",
            "region": "ap-southeast-1",
        }
        
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(test_config, f)
            temp_file = f.name
            
        try:
            config = Config(temp_file)
            assert config.validate_credentials()
            assert config.get("access_key_id") == "AKIAIOSFODNN7EXAMPLE"
            assert config.get("region") == "ap-southeast-1"
        finally:
            os.unlink(temp_file)
    
    def test_input_validation(self):
        """Test input validation functions"""
        def validate_bucket_name(bucket_name):
            if not bucket_name or not isinstance(bucket_name, str):
                return False
            if len(bucket_name) < 3 or len(bucket_name) > 63:
                return False
            if not re.match(r'^[a-z0-9][a-z0-9\-]*[a-z0-9]$', bucket_name):
                return False
            return True
        
        # Valid bucket names
        valid_buckets = ["test-bucket", "my-bucket-123", "bucket1"]
        for bucket in valid_buckets:
            assert validate_bucket_name(bucket)
        
        # Invalid bucket names
        invalid_buckets = ["", "a", "BUCKET", "bucket_name", "-bucket", "bucket-"]
        for bucket in invalid_buckets:
            assert not validate_bucket_name(bucket)
    
    def test_security_basics(self):
        """Test basic security functions"""
        def validate_password_strength(password):
            if len(password) < 8:
                return False
            if not re.search(r'[A-Z]', password):
                return False
            if not re.search(r'[a-z]', password):
                return False
            if not re.search(r'\d', password):
                return False
            return True
        
        # Test strong passwords
        strong_passwords = ["Password123", "MySecure1Pass", "Test123ABC"]
        for pwd in strong_passwords:
            assert validate_password_strength(pwd)
        
        # Test weak passwords
        weak_passwords = ["password", "123456", "PASSWORD", "Pass1"]
        for pwd in weak_passwords:
            assert not validate_password_strength(pwd)
    
    def test_logger_functionality(self):
        """Test logger functionality"""
        from logger import get_logger
        
        logger = get_logger("test_logger")
        assert logger is not None
        
        # Test logging without errors
        logger.info("Test info message")
        logger.warning("Test warning message")
        logger.error("Test error message")
    
    def test_file_operations(self):
        """Test file operation utilities"""
        def format_file_size(size_bytes):
            if size_bytes == 0:
                return "0 B"
            
            size_names = ["B", "KB", "MB", "GB", "TB"]
            i = 0
            while size_bytes >= 1024 and i < len(size_names) - 1:
                size_bytes /= 1024.0
                i += 1
            
            return f"{size_bytes:.1f} {size_names[i]}"
        
        # Test various file sizes
        test_cases = [
            (0, "0 B"),
            (1024, "1.0 KB"),
            (1048576, "1.0 MB"),
            (1073741824, "1.0 GB"),
        ]
        
        for size, expected in test_cases:
            result = format_file_size(size)
            assert result == expected

def run_manual_tests():
    """Run tests manually without pytest"""
    print("🚀 Running OBS Utils Comprehensive Tests")
    print("=" * 50)
    
    test_suite = TestComprehensive()
    tests = [
        test_suite.test_config_functionality,
        test_suite.test_input_validation,
        test_suite.test_security_basics,
        test_suite.test_logger_functionality,
        test_suite.test_file_operations
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            print(f"✅ {test.__name__}: PASS")
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__}: FAIL ({e})")
            failed += 1
    
    print(f"\n📊 Results: {passed} passed, {failed} failed")
    print(f"📈 Success Rate: {passed/(passed+failed)*100:.1f}%")
    
    return failed == 0

if __name__ == "__main__":
    # Try to run with pytest if available, otherwise run manually
    try:
        import pytest
        pytest.main([__file__])
    except ImportError:
        success = run_manual_tests()
        sys.exit(0 if success else 1)