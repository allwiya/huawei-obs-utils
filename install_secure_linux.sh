#!/bin/bash

# OBS Utils - Secure Installation Script for Linux
# Instalador seguro con configuración encriptada y niveles de usuario
# 
# Copyright 2025 CCVASS - Lima, Peru
# Licensed under Apache License 2.0
# Contact: contact@ccvass.com

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funciones de utilidad
print_header() {
    echo -e "${BLUE}================================================${NC}"
    echo -e "${BLUE}  OBS Utils - Instalación Segura (Linux)${NC}"
    echo -e "${BLUE}  CCVASS - Lima, Peru (2025)${NC}"
    echo -e "${BLUE}================================================${NC}"
    echo
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Verificar requisitos del sistema
check_requirements() {
    print_info "Verificando requisitos del sistema..."
    
    # Verificar Python 3.9+
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 no está instalado"
        echo "Por favor instala Python 3.9 o superior:"
        echo "  Ubuntu/Debian: sudo apt update && sudo apt install python3 python3-pip python3-venv"
        echo "  CentOS/RHEL: sudo yum install python3 python3-pip"
        echo "  Fedora: sudo dnf install python3 python3-pip"
        exit 1
    fi
    
    # Verificar versión de Python
    python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    if [[ $(echo "$python_version < 3.9" | bc -l) -eq 1 ]]; then
        print_error "Se requiere Python 3.9 o superior (encontrado: $python_version)"
        exit 1
    fi
    
    print_success "Python $python_version encontrado"
    
    # Verificar pip
    if ! python3 -m pip --version &> /dev/null; then
        print_error "pip no está disponible"
        echo "Instala pip: sudo apt install python3-pip"
        exit 1
    fi
    
    print_success "pip disponible"
}

# Configurar entorno virtual
setup_virtual_environment() {
    print_info "Configurando entorno virtual..."
    
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        print_success "Entorno virtual creado"
    else
        print_info "Entorno virtual ya existe"
    fi
    
    # Activar entorno virtual
    source venv/bin/activate
    
    # Actualizar pip
    pip install --upgrade pip
    
    # Instalar dependencias
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        print_success "Dependencias instaladas"
    else
        # Instalar dependencias básicas
        pip install cryptography esdk-obs-python
        print_success "Dependencias básicas instaladas"
    fi
}

# Configurar permisos seguros
setup_secure_permissions() {
    print_info "Configurando permisos seguros..."
    
    # Crear directorio de logs con permisos seguros
    mkdir -p logs
    chmod 750 logs
    
    # Hacer ejecutables los scripts principales
    chmod +x obs_utils_improved.py 2>/dev/null || true
    chmod +x *.py 2>/dev/null || true
    
    print_success "Permisos configurados"
}

# Seleccionar tipo de usuario
select_user_type() {
    echo
    print_info "Selecciona el tipo de usuario para configurar los niveles de seguridad:"
    echo
    echo "1. 👤 Usuario Básico (READ_ONLY)"
    echo "   - Operaciones: listar, buscar, descargar"
    echo "   - Sin contraseña adicional requerida"
    echo
    echo "2. 👨‍💼 Usuario Estándar (STANDARD)"
    echo "   - Operaciones: archivar, restaurar, cambiar clase de almacenamiento"
    echo "   - Contraseña de nivel estándar requerida"
    echo
    echo "3. 🔧 Usuario Avanzado (DESTRUCTIVE)"
    echo "   - Operaciones: eliminar objetos, purgar buckets"
    echo "   - Contraseña de nivel destructivo requerida"
    echo
    echo "4. 👑 Administrador (ADMIN)"
    echo "   - Operaciones: gestión completa de buckets y permisos"
    echo "   - Contraseña de administrador requerida"
    echo
    echo "5. 🏢 Configuración Empresarial (Todos los niveles)"
    echo "   - Configurar todos los niveles de seguridad"
    echo "   - Múltiples contraseñas por nivel"
    echo
    
    while true; do
        read -p "Selecciona una opción (1-5): " user_choice
        case $user_choice in
            1|2|3|4|5) break ;;
            *) print_error "Opción inválida. Selecciona 1-5." ;;
        esac
    done
    
    echo
    return $user_choice
}

# Configurar credenciales OBS
setup_obs_credentials() {
    print_info "Configurando credenciales de Huawei Cloud OBS..."
    echo
    
    # Solicitar credenciales
    read -p "Access Key ID: " access_key_id
    echo
    read -s -p "Secret Access Key: " secret_access_key
    echo
    echo
    read -p "Servidor OBS [https://obs.sa-peru-1.myhuaweicloud.com/]: " obs_server
    obs_server=${obs_server:-"https://obs.sa-peru-1.myhuaweicloud.com/"}
    
    read -p "Región [sa-peru-1]: " obs_region
    obs_region=${obs_region:-"sa-peru-1"}
    
    # Validar credenciales
    if [[ -z "$access_key_id" || -z "$secret_access_key" ]]; then
        print_error "Las credenciales son obligatorias"
        return 1
    fi
    
    # Crear configuración temporal
    cat > temp_config.json << EOF
{
    "access_key_id": "$access_key_id",
    "secret_access_key": "$secret_access_key",
    "server": "$obs_server",
    "region": "$obs_region",
    "max_keys": 1000,
    "restore_days": 30,
    "restore_tier": "Expedited"
}
EOF
    
    print_success "Credenciales configuradas"
    return 0
}

# Configurar encriptación
setup_encryption() {
    local user_type=$1
    
    print_info "Configurando encriptación de credenciales..."
    echo
    
    # Solicitar contraseña maestra
    while true; do
        read -s -p "Contraseña maestra para encriptar credenciales: " master_password
        echo
        read -s -p "Confirmar contraseña maestra: " master_password_confirm
        echo
        
        if [[ "$master_password" == "$master_password_confirm" ]]; then
            break
        else
            print_error "Las contraseñas no coinciden. Intenta nuevamente."
            echo
        fi
    done
    
    # Configurar contraseñas por nivel según el tipo de usuario
    case $user_type in
        1) # Usuario Básico
            setup_basic_user_passwords
            ;;
        2) # Usuario Estándar
            setup_standard_user_passwords
            ;;
        3) # Usuario Avanzado
            setup_advanced_user_passwords
            ;;
        4) # Administrador
            setup_admin_user_passwords
            ;;
        5) # Configuración Empresarial
            setup_enterprise_passwords
            ;;
    esac
    
    # Encriptar configuración
    python3 << EOF
import sys
import json
import os
from security import ConfigSecurity
from security_levels import MultiLevelSecurity

# Cargar configuración temporal
with open('temp_config.json', 'r') as f:
    config_data = json.load(f)

# Crear configuración encriptada
security = ConfigSecurity()
if security.create_encrypted_config(config_data, password='$master_password'):
    print("✅ Configuración encriptada creada exitosamente")
else:
    print("❌ Error al crear configuración encriptada")
    sys.exit(1)

# Limpiar archivo temporal
os.remove('temp_config.json')
EOF
    
    print_success "Configuración encriptada completada"
}

# Configurar contraseñas para usuario básico
setup_basic_user_passwords() {
    print_info "Configuración de Usuario Básico - Solo operaciones de lectura"
    echo "No se requieren contraseñas adicionales para operaciones básicas."
}

# Configurar contraseñas para usuario estándar
setup_standard_user_passwords() {
    print_info "Configuración de Usuario Estándar"
    echo
    read -s -p "Contraseña para operaciones estándar (archivo, restaurar): " standard_password
    echo
    
    # Guardar configuración de nivel estándar
    python3 << EOF
from security_levels import MultiLevelSecurity, SecurityLevel
import hashlib

security = MultiLevelSecurity()
password_hash = hashlib.sha256('$standard_password'.encode()).hexdigest()
security.set_level_password(SecurityLevel.STANDARD, password_hash)
security.save_security_config('$master_password')
EOF
}

# Configurar contraseñas para usuario avanzado
setup_advanced_user_passwords() {
    print_info "Configuración de Usuario Avanzado"
    echo
    read -s -p "Contraseña para operaciones estándar: " standard_password
    echo
    read -s -p "Contraseña para operaciones destructivas: " destructive_password
    echo
    
    python3 << EOF
from security_levels import MultiLevelSecurity, SecurityLevel
import hashlib

security = MultiLevelSecurity()
std_hash = hashlib.sha256('$standard_password'.encode()).hexdigest()
dest_hash = hashlib.sha256('$destructive_password'.encode()).hexdigest()

security.set_level_password(SecurityLevel.STANDARD, std_hash)
security.set_level_password(SecurityLevel.DESTRUCTIVE, dest_hash)
security.save_security_config('$master_password')
EOF
}

# Configurar contraseñas para administrador
setup_admin_user_passwords() {
    print_info "Configuración de Administrador"
    echo
    read -s -p "Contraseña para operaciones estándar: " standard_password
    echo
    read -s -p "Contraseña para operaciones destructivas: " destructive_password
    echo
    read -s -p "Contraseña de administrador: " admin_password
    echo
    
    python3 << EOF
from security_levels import MultiLevelSecurity, SecurityLevel
import hashlib

security = MultiLevelSecurity()
std_hash = hashlib.sha256('$standard_password'.encode()).hexdigest()
dest_hash = hashlib.sha256('$destructive_password'.encode()).hexdigest()
admin_hash = hashlib.sha256('$admin_password'.encode()).hexdigest()

security.set_level_password(SecurityLevel.STANDARD, std_hash)
security.set_level_password(SecurityLevel.DESTRUCTIVE, dest_hash)
security.set_level_password(SecurityLevel.ADMIN, admin_hash)
security.save_security_config('$master_password')
EOF
}

# Configurar contraseñas empresariales
setup_enterprise_passwords() {
    print_info "Configuración Empresarial - Todos los niveles de seguridad"
    echo
    read -s -p "Contraseña para operaciones estándar: " standard_password
    echo
    read -s -p "Contraseña para operaciones destructivas: " destructive_password
    echo
    read -s -p "Contraseña de administrador: " admin_password
    echo
    
    python3 << EOF
from security_levels import MultiLevelSecurity, SecurityLevel
import hashlib

security = MultiLevelSecurity()
std_hash = hashlib.sha256('$standard_password'.encode()).hexdigest()
dest_hash = hashlib.sha256('$destructive_password'.encode()).hexdigest()
admin_hash = hashlib.sha256('$admin_password'.encode()).hexdigest()

security.set_level_password(SecurityLevel.STANDARD, std_hash)
security.set_level_password(SecurityLevel.DESTRUCTIVE, dest_hash)
security.set_level_password(SecurityLevel.ADMIN, admin_hash)
security.save_security_config('$master_password')
EOF
    
    print_success "Configuración empresarial completada"
}

# Crear scripts de acceso rápido
create_launcher_scripts() {
    print_info "Creando scripts de acceso rápido..."
    
    # Script de activación del entorno
    cat > activate_obs.sh << 'EOF'
#!/bin/bash
# Script de activación para OBS Utils
cd "$(dirname "$0")"
source venv/bin/activate
echo "Entorno OBS Utils activado"
echo "Usa: python obs_utils_improved.py [opciones]"
EOF
    chmod +x activate_obs.sh
    
    # Script de ejecución directa
    cat > obs << 'EOF'
#!/bin/bash
# Launcher directo para OBS Utils
cd "$(dirname "$0")"
source venv/bin/activate
python obs_utils_improved.py "$@"
EOF
    chmod +x obs
    
    print_success "Scripts de acceso creados: ./activate_obs.sh y ./obs"
}

# Mostrar resumen de instalación
show_installation_summary() {
    local user_type=$1
    
    echo
    print_header
    print_success "¡Instalación completada exitosamente!"
    echo
    
    case $user_type in
        1) echo "👤 Configurado como: Usuario Básico (READ_ONLY)" ;;
        2) echo "👨‍💼 Configurado como: Usuario Estándar (STANDARD)" ;;
        3) echo "🔧 Configurado como: Usuario Avanzado (DESTRUCTIVE)" ;;
        4) echo "👑 Configurado como: Administrador (ADMIN)" ;;
        5) echo "🏢 Configurado como: Configuración Empresarial (Todos los niveles)" ;;
    esac
    
    echo
    print_info "Archivos de configuración creados:"
    echo "  📁 obs_config.json.enc (credenciales encriptadas)"
    echo "  🔑 obs_config.json.salt (salt de encriptación)"
    echo "  🛡️  obs_security_levels.json.enc (niveles de seguridad)"
    echo
    
    print_info "Formas de usar OBS Utils:"
    echo "  1. Modo interactivo: ./obs"
    echo "  2. Línea de comandos: ./obs --operation list --bucket mi-bucket"
    echo "  3. Activar entorno: ./activate_obs.sh"
    echo "  4. Manual: source venv/bin/activate && python obs_utils_improved.py"
    echo
    
    print_warning "IMPORTANTE:"
    echo "  • Guarda tu contraseña maestra de forma segura"
    echo "  • Las contraseñas no se pueden recuperar si se pierden"
    echo "  • Los archivos .enc y .salt son necesarios para el funcionamiento"
    echo
    
    print_info "Para obtener ayuda: ./obs --help"
    print_info "Documentación: docs/ directory"
    print_info "Soporte: contact@ccvass.com"
    echo
}

# Función principal
main() {
    print_header
    
    # Verificar si ya existe una instalación
    if [[ -f "obs_config.json.enc" ]]; then
        print_warning "Ya existe una configuración encriptada"
        read -p "¿Deseas reconfigurar? (s/N): " reconfigure
        if [[ ! "$reconfigure" =~ ^[Ss]$ ]]; then
            print_info "Instalación cancelada"
            exit 0
        fi
    fi
    
    # Ejecutar pasos de instalación
    check_requirements
    setup_virtual_environment
    setup_secure_permissions
    
    # Seleccionar tipo de usuario
    select_user_type
    user_type=$?
    
    # Configurar credenciales y encriptación
    if setup_obs_credentials; then
        setup_encryption $user_type
        create_launcher_scripts
        show_installation_summary $user_type
    else
        print_error "Error en la configuración de credenciales"
        exit 1
    fi
}

# Ejecutar instalación
main "$@"
