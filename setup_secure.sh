#!/bin/bash
# Enhanced setup script for OBS Utils with security features

set -e  # Exit on any error

echo "🔒 OBS Utils - Enhanced Setup with Security Features"
echo "=================================================="
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Check if Python is installed
check_python() {
    print_step "Checking Python installation..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
        PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
        print_status "Python $PYTHON_VERSION found"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
        PYTHON_VERSION=$(python --version 2>&1 | cut -d' ' -f2)
        print_status "Python $PYTHON_VERSION found"
    else
        print_error "Python not found. Please install Python 3.7 or higher."
        exit 1
    fi
    
    # Check Python version
    PYTHON_MAJOR=$($PYTHON_CMD -c "import sys; print(sys.version_info.major)")
    PYTHON_MINOR=$($PYTHON_CMD -c "import sys; print(sys.version_info.minor)")
    
    if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 7 ]); then
        print_error "Python 3.7 or higher is required. Found: $PYTHON_VERSION"
        exit 1
    fi
}

# Create virtual environment
create_venv() {
    print_step "Creating Python virtual environment..."
    
    if [ -d "venv" ]; then
        print_warning "Virtual environment already exists. Removing old one..."
        rm -rf venv
    fi
    
    $PYTHON_CMD -m venv venv
    print_status "Virtual environment created"
}

# Activate virtual environment
activate_venv() {
    print_step "Activating virtual environment..."
    source venv/bin/activate
    print_status "Virtual environment activated"
}

# Install dependencies
install_dependencies() {
    print_step "Installing Python dependencies..."
    
    # Upgrade pip first
    pip install --upgrade pip
    
    # Install requirements
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        print_status "Dependencies installed successfully"
    else
        print_error "requirements.txt not found"
        exit 1
    fi
}

# Create logs directory
create_logs_dir() {
    print_step "Creating logs directory..."
    
    if [ ! -d "logs" ]; then
        mkdir -p logs
        chmod 755 logs
        print_status "Logs directory created"
    else
        print_status "Logs directory already exists"
    fi
}

# Set secure permissions
set_secure_permissions() {
    print_step "Setting secure permissions..."
    
    # Make scripts executable
    chmod +x obs_utils_improved.py 2>/dev/null || true
    chmod +x security.py 2>/dev/null || true
    chmod +x setup_secure_config.py 2>/dev/null || true
    
    # Secure any existing config files
    if [ -f "obs_config.json" ]; then
        chmod 600 obs_config.json
        print_status "Secured obs_config.json permissions"
    fi
    
    if [ -f "obs_config.json.enc" ]; then
        chmod 600 obs_config.json.enc
        print_status "Secured encrypted config permissions"
    fi
    
    if [ -f "obs_config.json.salt" ]; then
        chmod 600 obs_config.json.salt
        print_status "Secured salt file permissions"
    fi
}

# Test installation
test_installation() {
    print_step "Testing installation..."
    
    # Test basic import
    if $PYTHON_CMD -c "from obs_manager import OBSManager; from config import Config; print('✅ Core modules imported successfully')" 2>/dev/null; then
        print_status "Core modules test passed"
    else
        print_error "Core modules test failed"
        return 1
    fi
    
    # Test security module
    if $PYTHON_CMD -c "from security import ConfigSecurity; print('✅ Security module imported successfully')" 2>/dev/null; then
        print_status "Security module test passed"
    else
        print_warning "Security module test failed - cryptography may not be installed properly"
    fi
    
    # Test help command
    if $PYTHON_CMD obs_utils_improved.py --help > /dev/null 2>&1; then
        print_status "CLI interface test passed"
    else
        print_error "CLI interface test failed"
        return 1
    fi
}

# Setup configuration
setup_configuration() {
    print_step "Configuration setup..."
    echo
    echo "Choose your preferred configuration method:"
    echo "1. Encrypted configuration (Most secure - recommended)"
    echo "2. Environment variables (Good for servers/CI/CD)"
    echo "3. Regular file with secure permissions (Basic)"
    echo "4. Skip configuration (set up manually later)"
    echo
    
    read -p "Enter your choice (1-4): " choice
    
    case $choice in
        1)
            print_status "Setting up encrypted configuration..."
            $PYTHON_CMD setup_secure_config.py
            ;;
        2)
            print_status "Environment variables setup..."
            echo
            echo "Add these lines to your ~/.bashrc or ~/.zshrc:"
            echo "export OBS_ACCESS_KEY_ID=\"your_access_key_here\""
            echo "export OBS_SECRET_ACCESS_KEY=\"your_secret_key_here\""
            echo "export OBS_SERVER=\"https://obs.sa-peru-1.myhuaweicloud.com/\""
            echo "export OBS_REGION=\"sa-peru-1\""
            echo
            echo "Then run: source ~/.bashrc"
            ;;
        3)
            print_status "Creating sample configuration file..."
            $PYTHON_CMD obs_utils_improved.py --create-config
            print_status "Edit obs_config.json with your credentials"
            ;;
        4)
            print_status "Skipping configuration setup"
            ;;
        *)
            print_warning "Invalid choice. Skipping configuration setup"
            ;;
    esac
}

# Create run script
create_run_script() {
    print_step "Creating run script..."
    
    cat > run.sh << 'EOF'
#!/bin/bash
# OBS Utils runner script with virtual environment activation

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo "Error: Virtual environment not found. Run setup.sh first."
    exit 1
fi

# Run OBS Utils with all passed arguments
python obs_utils_improved.py "$@"
EOF
    
    chmod +x run.sh
    print_status "Run script created: ./run.sh"
}

# Main installation process
main() {
    echo "Starting OBS Utils setup with security features..."
    echo
    
    # Check prerequisites
    check_python
    
    # Setup Python environment
    create_venv
    activate_venv
    install_dependencies
    
    # Setup directories and permissions
    create_logs_dir
    set_secure_permissions
    
    # Test installation
    if ! test_installation; then
        print_error "Installation test failed. Please check the errors above."
        exit 1
    fi
    
    # Create helper scripts
    create_run_script
    
    # Setup configuration
    echo
    setup_configuration
    
    echo
    print_status "🎉 Setup completed successfully!"
    echo
    echo "Next steps:"
    echo "1. Test your installation:"
    echo "   ./run.sh --operation list --bucket test-bucket"
    echo
    echo "2. Use the application:"
    echo "   ./run.sh                    # Interactive mode"
    echo "   ./run.sh --help            # See all options"
    echo
    echo "3. Security features:"
    echo "   ./run.sh --setup-secure-config     # Setup encrypted config"
    echo "   ./run.sh --encrypt-config          # Encrypt existing config"
    echo "   ./run.sh --secure-permissions      # Fix file permissions"
    echo
    echo "4. Read the security guide:"
    echo "   cat SECURITY.md"
    echo
    print_status "Installation complete! 🚀"
}

# Run main function
main "$@"
