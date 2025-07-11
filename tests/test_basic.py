#!/usr/bin/env python3
"""
Basic tests for OBS Utils
"""

import pytest
import tempfile
import os
import json
from unittest.mock import Mock, patch


class TestConfig:
    """Test configuration functionality"""
    
    def test_config_import(self):
        """Test that config module can be imported"""
        from config import Config
        assert Config is not None
    
    def test_config_initialization(self):
        """Test config initialization with test file"""
        from config import Config
        
        test_config = {
            "access_key_id": "test_key",
            "secret_access_key": "test_secret", 
            "server": "https://test.example.com",
            "region": "test-region"
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_config, f)
            temp_file = f.name
        
        try:
            config = Config(temp_file)
            assert config.validate_credentials()
            assert config.get('access_key_id') == 'test_key'
            assert config.get('server') == 'https://test.example.com'
        finally:
            os.unlink(temp_file)
    
    def test_config_validation(self):
        """Test configuration validation"""
        from config import Config
        
        # Test invalid config
        invalid_config = {"access_key_id": "test"}
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(invalid_config, f)
            temp_file = f.name
        
        try:
            config = Config(temp_file)
            assert not config.validate_credentials()
        finally:
            os.unlink(temp_file)


class TestSecurity:
    """Test security functionality"""
    
    def test_security_import(self):
        """Test that security module can be imported"""
        from security import ConfigSecurity
        assert ConfigSecurity is not None
    
    def test_security_initialization(self):
        """Test security module initialization"""
        from security import ConfigSecurity
        
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            security = ConfigSecurity(temp_file)
            assert security is not None
            assert security.config_file == temp_file
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_password_hashing(self):
        """Test password hashing functionality"""
        from security import ConfigSecurity
        
        security = ConfigSecurity()
        
        # Test password hashing
        password = "test_password_123"
        hash1 = security._hash_password(password)
        hash2 = security._hash_password(password)
        
        # Same password should produce same hash
        assert hash1 == hash2
        
        # Different passwords should produce different hashes
        hash3 = security._hash_password("different_password")
        assert hash1 != hash3
        
        # Hash should be SHA-256 (64 characters)
        assert len(hash1) == 64
    
    def test_key_generation(self):
        """Test encryption key generation"""
        from security import ConfigSecurity
        
        security = ConfigSecurity()
        
        password = "test_password"
        key1, salt1 = security._generate_key(password)
        key2, salt2 = security._generate_key(password)
        
        # Different calls should generate different salts
        assert salt1 != salt2
        
        # Same password with same salt should generate same key
        key3, _ = security._generate_key(password, salt1)
        assert key1 == key3
        
        # Salt should be 16 bytes
        assert len(salt1) == 16


class TestSecurityLevels:
    """Test security levels functionality"""
    
    def test_security_levels_import(self):
        """Test that security levels module can be imported"""
        from security_levels import MultiLevelSecurity, SecurityLevel
        assert MultiLevelSecurity is not None
        assert SecurityLevel is not None
    
    def test_security_level_constants(self):
        """Test security level constants"""
        from security_levels import SecurityLevel
        
        assert SecurityLevel.READ_ONLY == "read_only"
        assert SecurityLevel.STANDARD == "standard"
        assert SecurityLevel.DESTRUCTIVE == "destructive"
        assert SecurityLevel.ADMIN == "admin"
    
    def test_operation_level_mapping(self):
        """Test operation to security level mapping"""
        from security_levels import MultiLevelSecurity, SecurityLevel
        
        security = MultiLevelSecurity()
        
        # Test READ_ONLY operations
        assert security.get_operation_level("list") == SecurityLevel.READ_ONLY
        assert security.get_operation_level("search") == SecurityLevel.READ_ONLY
        assert security.get_operation_level("download") == SecurityLevel.READ_ONLY
        
        # Test STANDARD operations
        assert security.get_operation_level("archive") == SecurityLevel.STANDARD
        assert security.get_operation_level("restore") == SecurityLevel.STANDARD
        assert security.get_operation_level("warm") == SecurityLevel.STANDARD
        
        # Test DESTRUCTIVE operations
        assert security.get_operation_level("delete") == SecurityLevel.DESTRUCTIVE
        assert security.get_operation_level("purge") == SecurityLevel.DESTRUCTIVE


class TestOBSManager:
    """Test OBS Manager functionality"""
    
    def test_obs_manager_import(self):
        """Test that OBS manager can be imported"""
        from obs_manager import OBSManager
        assert OBSManager is not None
    
    @patch('obs_manager.ObsClient')
    def test_obs_manager_initialization(self, mock_obs_client):
        """Test OBS manager initialization with mocked client"""
        from obs_manager import OBSManager
        from config import Config
        
        # Create test config
        test_config = {
            "access_key_id": "test_key",
            "secret_access_key": "test_secret",
            "server": "https://test.example.com",
            "region": "test-region"
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_config, f)
            temp_file = f.name
        
        try:
            # Mock the OBS client
            mock_client_instance = Mock()
            mock_obs_client.return_value = mock_client_instance
            
            # Test initialization
            obs_manager = OBSManager(temp_file)
            assert obs_manager is not None
            
            # Verify OBS client was called with correct parameters
            mock_obs_client.assert_called_once_with(
                access_key_id="test_key",
                secret_access_key="test_secret",
                server="https://test.example.com",
                region="test-region"
            )
            
        finally:
            os.unlink(temp_file)
    
    def test_input_validation(self):
        """Test input validation methods"""
        from obs_manager import OBSManager
        
        # Create a mock OBS manager to test validation
        with patch('obs_manager.ObsClient'):
            test_config = {
                "access_key_id": "test",
                "secret_access_key": "test",
                "server": "https://test.com",
                "region": "test"
            }
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump(test_config, f)
                temp_file = f.name
            
            try:
                obs_manager = OBSManager(temp_file)
                
                # Test valid inputs
                bucket, route = obs_manager._validate_inputs("test-bucket", "path/")
                assert bucket == "test-bucket"
                assert route == "path/"
                
                # Test input cleaning
                bucket, route = obs_manager._validate_inputs("  test-bucket  ", "  path/  ")
                assert bucket == "test-bucket"
                assert route == "path/"
                
                # Test empty route
                bucket, route = obs_manager._validate_inputs("test-bucket", "")
                assert bucket == "test-bucket"
                assert route == ""
                
                # Test invalid bucket
                with pytest.raises(ValueError):
                    obs_manager._validate_inputs("", "path/")
                
                with pytest.raises(ValueError):
                    obs_manager._validate_inputs(None, "path/")
                    
            finally:
                os.unlink(temp_file)


class TestCLI:
    """Test CLI functionality"""
    
    def test_cli_help(self):
        """Test CLI help functionality"""
        import subprocess
        import sys
        
        # Test that help command works
        result = subprocess.run([
            sys.executable, 'obs_utils_improved.py', '--help'
        ], capture_output=True, text=True, cwd=os.path.dirname(os.path.dirname(__file__)))
        
        assert result.returncode == 0
        assert 'OBS Utils' in result.stdout
        assert '--operation' in result.stdout
    
    def test_config_creation(self):
        """Test configuration file creation"""
        import subprocess
        import sys
        
        # Test config creation
        result = subprocess.run([
            sys.executable, 'obs_utils_improved.py', '--create-config'
        ], capture_output=True, text=True, cwd=os.path.dirname(os.path.dirname(__file__)))
        
        assert result.returncode == 0
        
        # Check that sample config was created
        sample_config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'obs_config.json.sample')
        assert os.path.exists(sample_config_path)


@pytest.mark.integration
class TestIntegration:
    """Integration tests"""
    
    def test_full_import_chain(self):
        """Test that all modules can be imported together"""
        from config import Config
        from obs_manager import OBSManager
        from security import ConfigSecurity
        from security_levels import MultiLevelSecurity
        from logger import get_logger
        
        # All imports should work
        assert Config is not None
        assert OBSManager is not None
        assert ConfigSecurity is not None
        assert MultiLevelSecurity is not None
        assert get_logger is not None
    
    def test_logger_functionality(self):
        """Test logger functionality"""
        from logger import get_logger, setup_logger
        
        logger = get_logger("test_logger")
        assert logger is not None
        
        # Test that logger can log without errors
        logger.info("Test log message")
        logger.warning("Test warning message")
        logger.error("Test error message")


if __name__ == "__main__":
    pytest.main([__file__])
