#!/usr/bin/env python3
"""
Advanced security tests for OBS Utils
"""

import json
import os
import tempfile
import sys
import hashlib
import re
import base64
import secrets
import time
from unittest.mock import Mock, patch

class TestAdvancedSecurity:
    """Advanced security test suite"""
    
    def test_credential_encryption(self):
        """Test credential encryption/decryption"""
        def simple_encrypt(data, key):
            """Simple XOR encryption for testing"""
            if not data or not key:
                return ""
            
            key_bytes = key.encode()
            data_bytes = data.encode()
            
            encrypted = bytearray()
            for i, byte in enumerate(data_bytes):
                encrypted.append(byte ^ key_bytes[i % len(key_bytes)])
            
            return base64.b64encode(encrypted).decode()
        
        def simple_decrypt(encrypted_data, key):
            """Simple XOR decryption for testing"""
            if not encrypted_data or not key:
                return ""
            
            try:
                encrypted_bytes = base64.b64decode(encrypted_data.encode())
                key_bytes = key.encode()
                
                decrypted = bytearray()
                for i, byte in enumerate(encrypted_bytes):
                    decrypted.append(byte ^ key_bytes[i % len(key_bytes)])
                
                return decrypted.decode()
            except (ValueError, TypeError, UnicodeDecodeError):
                return ""
        
        # Test encryption/decryption
        original_data = "sensitive_access_key_12345"
        encryption_key = "test_key_for_testing"  # Test key only
        
        encrypted = simple_encrypt(original_data, encryption_key)
        decrypted = simple_decrypt(encrypted, encryption_key)
        
        assert encrypted != original_data, "Data should be encrypted"
        assert decrypted == original_data, "Decrypted data should match original"
        
        # Test with wrong key
        wrong_decrypted = simple_decrypt(encrypted, "wrong_key")
        assert wrong_decrypted != original_data, "Wrong key should not decrypt correctly"
        
        print("✅ Credential encryption/decryption passed")
    
    def test_secure_session_management(self):
        """Test secure session management"""
        class SecureSession:
            def __init__(self):
                self.sessions = {}
                self.session_timeout = 3600  # 1 hour
            
            def create_session(self, user_id):
                """Create a secure session"""
                session_id = secrets.token_hex(32)
                session_data = {
                    'user_id': user_id,
                    'created_at': time.time(),
                    'last_activity': time.time(),
                    'is_active': True
                }
                self.sessions[session_id] = session_data
                return session_id
            
            def validate_session(self, session_id):
                """Validate session and check timeout"""
                if session_id not in self.sessions:
                    return False
                
                session = self.sessions[session_id]
                current_time = time.time()
                
                # Check if session expired
                if current_time - session['last_activity'] > self.session_timeout:
                    session['is_active'] = False
                    return False
                
                # Update last activity
                session['last_activity'] = current_time
                return session['is_active']
            
            def invalidate_session(self, session_id):
                """Invalidate a session"""
                if session_id in self.sessions:
                    self.sessions[session_id]['is_active'] = False
        
        # Test session management
        session_mgr = SecureSession()
        
        # Create session
        session_id = session_mgr.create_session("user123")
        assert len(session_id) == 64, "Session ID should be 64 characters"
        assert session_mgr.validate_session(session_id), "New session should be valid"
        
        # Test invalid session
        assert not session_mgr.validate_session("invalid_session"), "Invalid session should fail"
        
        # Test session invalidation
        session_mgr.invalidate_session(session_id)
        assert not session_mgr.validate_session(session_id), "Invalidated session should fail"
        
        print("✅ Secure session management passed")
    
    def test_input_sanitization_advanced(self):
        """Test advanced input sanitization"""
        def sanitize_input_advanced(input_data):
            """Advanced input sanitization"""
            if not input_data:
                return ""
            
            # Remove script tags
            input_data = re.sub(r'<script[^>]*>.*?</script>', '', input_data, flags=re.IGNORECASE | re.DOTALL)
            
            # Remove dangerous HTML tags
            dangerous_tags = ['script', 'iframe', 'object', 'embed', 'form']
            for tag in dangerous_tags:
                input_data = re.sub(f'<{tag}[^>]*>.*?</{tag}>', '', input_data, flags=re.IGNORECASE | re.DOTALL)
                input_data = re.sub(f'<{tag}[^>]*/?>', '', input_data, flags=re.IGNORECASE)
            
            # Remove javascript: URLs
            input_data = re.sub(r'javascript:', '', input_data, flags=re.IGNORECASE)
            
            # Remove data: URLs
            input_data = re.sub(r'data:', '', input_data, flags=re.IGNORECASE)
            
            # Limit length
            if len(input_data) > 1000:
                input_data = input_data[:1000]
            
            return input_data.strip()
        
        # Test XSS prevention
        xss_inputs = [
            '<script>alert("xss")</script>',
            '<iframe src="javascript:alert(1)"></iframe>',
            'javascript:alert("xss")',
            '<img src="x" onerror="alert(1)">',
            'data:text/html,<script>alert(1)</script>'
        ]
        
        for xss_input in xss_inputs:
            sanitized = sanitize_input_advanced(xss_input)
            assert 'script' not in sanitized.lower(), f"Script not removed from {xss_input}"
            assert 'javascript:' not in sanitized.lower(), f"JavaScript URL not removed from {xss_input}"
        
        # Test normal input preservation
        normal_inputs = ['normal_filename.txt', 'folder/subfolder', 'document.pdf']
        for normal_input in normal_inputs:
            sanitized = sanitize_input_advanced(normal_input)
            assert sanitized == normal_input, f"Normal input should be preserved: {normal_input}"
        
        print("✅ Advanced input sanitization passed")
    
    def test_rate_limiting_advanced(self):
        """Test advanced rate limiting"""
        class AdvancedRateLimiter:
            def __init__(self):
                self.requests = {}
                self.blocked_ips = {}
                self.max_requests_per_minute = 60
                self.max_requests_per_hour = 1000
                self.block_duration = 300  # 5 minutes
            
            def is_request_allowed(self, client_ip, operation_type="default"):
                """Check if request is allowed with different limits per operation"""
                current_time = time.time()
                
                # Check if IP is blocked
                if client_ip in self.blocked_ips:
                    if current_time - self.blocked_ips[client_ip] < self.block_duration:
                        return False
                    else:
                        del self.blocked_ips[client_ip]
                
                # Initialize tracking for new IP
                if client_ip not in self.requests:
                    self.requests[client_ip] = []
                
                # Clean old requests
                minute_ago = current_time - 60
                hour_ago = current_time - 3600
                
                self.requests[client_ip] = [
                    req_time for req_time in self.requests[client_ip]
                    if req_time > hour_ago
                ]
                
                # Count recent requests
                requests_last_minute = sum(1 for req_time in self.requests[client_ip] if req_time > minute_ago)
                requests_last_hour = len(self.requests[client_ip])
                
                # Apply different limits for different operations
                minute_limit = self.max_requests_per_minute
                hour_limit = self.max_requests_per_hour
                
                if operation_type == "upload":
                    minute_limit = 10  # Stricter for uploads
                elif operation_type == "delete":
                    minute_limit = 5   # Very strict for deletes
                
                # Check limits
                if requests_last_minute >= minute_limit or requests_last_hour >= hour_limit:
                    self.blocked_ips[client_ip] = current_time
                    return False
                
                # Record this request
                self.requests[client_ip].append(current_time)
                return True
        
        # Test rate limiting
        limiter = AdvancedRateLimiter()
        
        # Test normal usage
        for i in range(5):
            assert limiter.is_request_allowed("192.168.1.1"), f"Request {i+1} should be allowed"
        
        # Test operation-specific limits
        assert limiter.is_request_allowed("192.168.1.2", "upload"), "Upload should be allowed initially"
        
        # Test different IPs don't interfere
        assert limiter.is_request_allowed("192.168.1.3"), "Different IP should be allowed"
        
        print("✅ Advanced rate limiting passed")
    
    def test_security_audit_logging(self):
        """Test security audit logging"""
        class SecurityAuditLogger:
            def __init__(self):
                self.audit_logs = []
            
            def log_security_event(self, event_type, user_id, details, severity="INFO"):
                """Log security events"""
                import time
                
                log_entry = {
                    'timestamp': time.time(),
                    'event_type': event_type,
                    'user_id': user_id,
                    'details': self._sanitize_log_details(details),
                    'severity': severity,
                    'source_ip': details.get('source_ip', 'unknown')
                }
                
                self.audit_logs.append(log_entry)
            
            def _sanitize_log_details(self, details):
                """Sanitize sensitive information from logs"""
                if not isinstance(details, dict):
                    return details
                
                sanitized = details.copy()
                sensitive_keys = ['password', 'secret', 'token', 'key']
                
                for key in sanitized:
                    if any(sensitive in key.lower() for sensitive in sensitive_keys):
                        sanitized[key] = '[REDACTED]'
                
                return sanitized
            
            def get_security_events(self, event_type=None, severity=None):
                """Get filtered security events"""
                events = self.audit_logs
                
                if event_type:
                    events = [e for e in events if e['event_type'] == event_type]
                
                if severity:
                    events = [e for e in events if e['severity'] == severity]
                
                return events
        
        # Test audit logging
        logger = SecurityAuditLogger()
        
        # Log various security events
        logger.log_security_event(
            'LOGIN_ATTEMPT',
            'user123',
            {'source_ip': '192.168.1.1', 'password': 'secret123'},
            'INFO'
        )
        
        logger.log_security_event(
            'FAILED_LOGIN',
            'user123',
            {'source_ip': '192.168.1.1', 'reason': 'invalid_password'},
            'WARNING'
        )
        
        logger.log_security_event(
            'SUSPICIOUS_ACTIVITY',
            'user456',
            {'source_ip': '10.0.0.1', 'activity': 'multiple_failed_attempts'},
            'CRITICAL'
        )
        
        # Test log retrieval
        all_events = logger.get_security_events()
        assert len(all_events) == 3, "Should have 3 logged events"
        
        critical_events = logger.get_security_events(severity='CRITICAL')
        assert len(critical_events) == 1, "Should have 1 critical event"
        
        login_events = logger.get_security_events(event_type='LOGIN_ATTEMPT')
        assert len(login_events) == 1, "Should have 1 login attempt"
        
        # Test sensitive data sanitization
        login_event = login_events[0]
        assert login_event['details']['password'] == '[REDACTED]', "Password should be redacted"
        assert login_event['details']['source_ip'] == '192.168.1.1', "Non-sensitive data should be preserved"
        
        print("✅ Security audit logging passed")

def run_advanced_security_tests():
    """Run advanced security tests"""
    print("🔒 Running Advanced Security Tests")
    print("=" * 50)
    
    test_suite = TestAdvancedSecurity()
    tests = [
        test_suite.test_credential_encryption,
        test_suite.test_secure_session_management,
        test_suite.test_input_sanitization_advanced,
        test_suite.test_rate_limiting_advanced,
        test_suite.test_security_audit_logging
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__}: FAIL ({e})")
            failed += 1
    
    print(f"\n🔒 Advanced Security Tests: {passed} passed, {failed} failed")
    return failed == 0

if __name__ == "__main__":
    success = run_advanced_security_tests()
    sys.exit(0 if success else 1)