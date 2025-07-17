#!/usr/bin/env python3
"""
Comprehensive test report generator for OBS Utils
"""

import json
import os
import sys
import time
import subprocess
from datetime import datetime
from pathlib import Path

class TestReportGenerator:
    """Generate comprehensive test reports"""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.test_results = {
            "basic": [],
            "comprehensive": [],
            "obs_specific": [],
            "advanced_security": [],
            "integration": []
        }
        self.coverage_data = {}
        self.performance_metrics = {}
    
    def run_test_suite(self, test_file, suite_name):
        """Run a test suite and collect results"""
        print(f"🧪 Running {suite_name} tests...")
        
        try:
            start_time = time.time()
            result = subprocess.run([sys.executable, test_file], 
                                  capture_output=True, text=True, timeout=60)
            end_time = time.time()
            
            execution_time = end_time - start_time
            
            # Parse output for pass/fail counts
            output = result.stdout
            passed = output.count("✅") + output.count("PASS")
            failed = output.count("❌") + output.count("FAIL")
            
            self.test_results[suite_name] = {
                "passed": passed,
                "failed": failed,
                "execution_time": execution_time,
                "return_code": result.returncode,
                "output": output,
                "errors": result.stderr
            }
            
            self.performance_metrics[suite_name] = execution_time
            
            print(f"   ✅ {passed} passed, ❌ {failed} failed ({execution_time:.2f}s)")
            
        except subprocess.TimeoutExpired:
            print(f"   ⏰ Test suite {suite_name} timed out")
            self.test_results[suite_name] = {
                "passed": 0,
                "failed": 1,
                "execution_time": 60,
                "return_code": -1,
                "output": "Test timed out",
                "errors": "Timeout"
            }
        except Exception as e:
            print(f"   ❌ Error running {suite_name}: {e}")
            self.test_results[suite_name] = {
                "passed": 0,
                "failed": 1,
                "execution_time": 0,
                "return_code": -1,
                "output": "",
                "errors": str(e)
            }
    
    def analyze_code_coverage(self):
        """Analyze code coverage"""
        print("📊 Analyzing code coverage...")
        
        # Get list of Python files in the project
        python_files = []
        for root, dirs, files in os.walk("."):
            # Skip test directories and virtual environments
            if any(skip in root for skip in [".venv", "__pycache__", ".git", "tests"]):
                continue
            
            for file in files:
                if file.endswith(".py") and not file.startswith("test_"):
                    python_files.append(os.path.join(root, file))
        
        total_files = len(python_files)
        tested_files = 0
        
        # Check which files have corresponding tests
        for py_file in python_files:
            file_name = os.path.basename(py_file).replace(".py", "")
            test_file = f"tests/test_{file_name}.py"
            
            if os.path.exists(test_file):
                tested_files += 1
        
        coverage_percentage = (tested_files / total_files * 100) if total_files > 0 else 0
        
        self.coverage_data = {
            "total_files": total_files,
            "tested_files": tested_files,
            "coverage_percentage": coverage_percentage,
            "python_files": python_files
        }
        
        print(f"   📈 Coverage: {tested_files}/{total_files} files ({coverage_percentage:.1f}%)")
    
    def check_security_compliance(self):
        """Check security compliance"""
        print("🔒 Checking security compliance...")
        
        security_checks = {
            "https_endpoints": self._check_https_usage(),
            "password_validation": self._check_password_validation(),
            "input_sanitization": self._check_input_sanitization(),
            "credential_masking": self._check_credential_masking(),
            "secure_defaults": self._check_secure_defaults()
        }
        
        passed_checks = sum(1 for check in security_checks.values() if check)
        total_checks = len(security_checks)
        
        print(f"   🛡️ Security: {passed_checks}/{total_checks} checks passed")
        
        return security_checks
    
    def _check_https_usage(self):
        """Check if HTTPS is enforced"""
        try:
            # Check config files and code for HTTPS usage
            for root, dirs, files in os.walk("."):
                if ".git" in root or "__pycache__" in root:
                    continue
                
                for file in files:
                    if file.endswith((".py", ".json", ".md")):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                if "http://" in content and "obs." in content:
                                    return False  # Found insecure HTTP
                        except:
                            continue
            return True
        except:
            return False
    
    def _check_password_validation(self):
        """Check if password validation exists"""
        try:
            # Look for password validation patterns
            validation_patterns = ["password", "validate", "strength", "regex", "re.match"]
            
            for root, dirs, files in os.walk("."):
                if ".git" in root or "__pycache__" in root:
                    continue
                
                for file in files:
                    if file.endswith(".py"):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read().lower()
                                if any(pattern in content for pattern in validation_patterns):
                                    return True
                        except:
                            continue
            return False
        except:
            return False
    
    def _check_input_sanitization(self):
        """Check if input sanitization exists"""
        try:
            sanitization_patterns = ["sanitize", "validate", "escape", "clean"]
            
            for root, dirs, files in os.walk("."):
                if ".git" in root or "__pycache__" in root:
                    continue
                
                for file in files:
                    if file.endswith(".py"):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read().lower()
                                if any(pattern in content for pattern in sanitization_patterns):
                                    return True
                        except:
                            continue
            return False
        except:
            return False
    
    def _check_credential_masking(self):
        """Check if credential masking exists"""
        try:
            masking_patterns = ["mask", "redact", "hide", "***", "[REDACTED]"]
            
            for root, dirs, files in os.walk("."):
                if ".git" in root or "__pycache__" in root:
                    continue
                
                for file in files:
                    if file.endswith(".py"):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                if any(pattern in content for pattern in masking_patterns):
                                    return True
                        except:
                            continue
            return False
        except:
            return False
    
    def _check_secure_defaults(self):
        """Check if secure defaults are used"""
        try:
            # Check for HTTPS defaults, secure configurations
            secure_patterns = ["https://", "ssl", "tls", "secure"]
            
            config_files = ["config.py", "obs_config.json.sample"]
            for config_file in config_files:
                if os.path.exists(config_file):
                    try:
                        with open(config_file, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read().lower()
                            if any(pattern in content for pattern in secure_patterns):
                                return True
                    except:
                        continue
            return False
        except:
            return False
    
    def generate_html_report(self):
        """Generate HTML report"""
        end_time = datetime.now()
        total_duration = end_time - self.start_time
        
        # Calculate totals
        total_passed = sum(result["passed"] for result in self.test_results.values())
        total_failed = sum(result["failed"] for result in self.test_results.values())
        total_tests = total_passed + total_failed
        success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>OBS Utils - Test Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background: #f0f0f0; padding: 20px; border-radius: 5px; }}
        .summary {{ background: #e8f5e8; padding: 15px; margin: 20px 0; border-radius: 5px; }}
        .test-suite {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
        .pass {{ color: green; }}
        .fail {{ color: red; }}
        .metric {{ display: inline-block; margin: 10px; padding: 10px; background: #f9f9f9; border-radius: 3px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🧪 OBS Utils - Comprehensive Test Report</h1>
        <p><strong>Generated:</strong> {end_time.strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>Duration:</strong> {total_duration.total_seconds():.2f} seconds</p>
    </div>
    
    <div class="summary">
        <h2>📊 Summary</h2>
        <div class="metric">
            <strong>Total Tests:</strong> {total_tests}
        </div>
        <div class="metric">
            <strong class="pass">Passed:</strong> {total_passed}
        </div>
        <div class="metric">
            <strong class="fail">Failed:</strong> {total_failed}
        </div>
        <div class="metric">
            <strong>Success Rate:</strong> {success_rate:.1f}%
        </div>
    </div>
    
    <h2>🧪 Test Suites</h2>
"""
        
        for suite_name, results in self.test_results.items():
            if results:
                suite_success_rate = (results["passed"] / (results["passed"] + results["failed"]) * 100) if (results["passed"] + results["failed"]) > 0 else 0
                
                html_content += f"""
    <div class="test-suite">
        <h3>{suite_name.replace('_', ' ').title()}</h3>
        <p><strong class="pass">Passed:</strong> {results["passed"]} | 
           <strong class="fail">Failed:</strong> {results["failed"]} | 
           <strong>Success Rate:</strong> {suite_success_rate:.1f}% | 
           <strong>Duration:</strong> {results["execution_time"]:.2f}s</p>
        <details>
            <summary>View Output</summary>
            <pre>{results["output"]}</pre>
        </details>
    </div>
"""
        
        # Add coverage information
        if self.coverage_data:
            html_content += f"""
    <h2>📈 Code Coverage</h2>
    <div class="test-suite">
        <p><strong>Files Covered:</strong> {self.coverage_data["tested_files"]}/{self.coverage_data["total_files"]} ({self.coverage_data["coverage_percentage"]:.1f}%)</p>
        <table>
            <tr><th>File</th><th>Has Tests</th></tr>
"""
            for py_file in self.coverage_data["python_files"]:
                file_name = os.path.basename(py_file).replace(".py", "")
                test_file = f"tests/test_{file_name}.py"
                has_tests = "✅" if os.path.exists(test_file) else "❌"
                html_content += f"            <tr><td>{py_file}</td><td>{has_tests}</td></tr>\n"
            
            html_content += "        </table>\n    </div>\n"
        
        html_content += """
    <h2>⚡ Performance Metrics</h2>
    <div class="test-suite">
        <table>
            <tr><th>Test Suite</th><th>Execution Time (s)</th></tr>
"""
        
        for suite_name, exec_time in self.performance_metrics.items():
            html_content += f"            <tr><td>{suite_name}</td><td>{exec_time:.2f}</td></tr>\n"
        
        html_content += """
        </table>
    </div>
    
    <div class="summary">
        <h2>💡 Recommendations</h2>
"""
        
        if success_rate >= 90:
            html_content += "<p>🎉 <strong>Excellent!</strong> The application is in great shape with high test coverage and success rate.</p>"
        elif success_rate >= 70:
            html_content += "<p>👍 <strong>Good!</strong> The application is mostly functional. Consider addressing failing tests.</p>"
        else:
            html_content += "<p>⚠️ <strong>Needs Attention!</strong> Several critical issues found. Priority should be given to fixing failing tests.</p>"
        
        html_content += """
    </div>
</body>
</html>
"""
        
        # Write HTML report
        with open("test_report.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"📋 HTML report generated: test_report.html")
    
    def generate_json_report(self):
        """Generate JSON report for CI/CD integration"""
        end_time = datetime.now()
        
        report_data = {
            "timestamp": end_time.isoformat(),
            "duration": (end_time - self.start_time).total_seconds(),
            "summary": {
                "total_passed": sum(result["passed"] for result in self.test_results.values()),
                "total_failed": sum(result["failed"] for result in self.test_results.values()),
                "success_rate": 0
            },
            "test_suites": self.test_results,
            "coverage": self.coverage_data,
            "performance": self.performance_metrics
        }
        
        total_tests = report_data["summary"]["total_passed"] + report_data["summary"]["total_failed"]
        if total_tests > 0:
            report_data["summary"]["success_rate"] = report_data["summary"]["total_passed"] / total_tests * 100
        
        with open("test_report.json", "w") as f:
            json.dump(report_data, f, indent=2)
        
        print(f"📋 JSON report generated: test_report.json")

def run_comprehensive_test_report():
    """Run comprehensive test report generation"""
    print("📋 Generating Comprehensive Test Report")
    print("=" * 50)
    
    generator = TestReportGenerator()
    
    # Define test suites
    test_suites = [
        ("tests/test_basic.py", "basic"),
        ("tests/test_comprehensive.py", "comprehensive"),
        ("tests/test_obs_specific.py", "obs_specific"),
        ("tests/test_advanced_security.py", "advanced_security"),
        ("tests/test_integration.py", "integration")
    ]
    
    # Run each test suite
    for test_file, suite_name in test_suites:
        if os.path.exists(test_file):
            generator.run_test_suite(test_file, suite_name)
        else:
            print(f"⚠️ Test file not found: {test_file}")
    
    # Analyze coverage and security
    generator.analyze_code_coverage()
    security_checks = generator.check_security_compliance()
    
    # Generate reports
    generator.generate_html_report()
    generator.generate_json_report()
    
    print("\n🎯 Report Generation Complete!")
    print("📄 Files generated:")
    print("   - test_report.html (Human-readable report)")
    print("   - test_report.json (CI/CD integration)")

if __name__ == "__main__":
    run_comprehensive_test_report()