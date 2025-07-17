#!/usr/bin/env python3
"""
Security Setup Helper for OBS Utils
Simplifica la configuración de niveles de seguridad y encriptación

Copyright 2025 CCVASS - Lima, Peru
Licensed under Apache License 2.0
Contact: contact@ccvass.com
"""

import getpass
import hashlib
import json
import os
import sys
from typing import Dict, Optional

try:
    from security import ConfigSecurity
    from security_levels import MultiLevelSecurity, SecurityLevel
except ImportError as e:
    print(f"❌ Error importing security modules: {e}")
    print("Asegúrate de que los módulos security.py y security_levels.py estén disponibles")
    sys.exit(1)


class SecuritySetupHelper:
    """Helper class for simplified security setup"""
    
    def __init__(self):
        self.config_security = ConfigSecurity()
        self.multi_level_security = MultiLevelSecurity()
        
    def setup_user_type(self, user_type: int, master_password: str, credentials: Dict) -> bool:
        """
        Configura el tipo de usuario con sus niveles de seguridad correspondientes
        
        Args:
            user_type: Tipo de usuario (1-5)
            master_password: Contraseña maestra para encriptación
            credentials: Diccionario con credenciales OBS
            
        Returns:
            bool: True si la configuración fue exitosa
        """
        try:
            # Crear configuración encriptada de credenciales
            if not self.config_security.create_encrypted_config(credentials, master_password):
                print("❌ Error al crear configuración encriptada de credenciales")
                return False
                
            # Configurar niveles de seguridad según el tipo de usuario
            if user_type == 1:
                return self._setup_basic_user(master_password)
            elif user_type == 2:
                return self._setup_standard_user(master_password)
            elif user_type == 3:
                return self._setup_advanced_user(master_password)
            elif user_type == 4:
                return self._setup_admin_user(master_password)
            elif user_type == 5:
                return self._setup_enterprise_user(master_password)
            else:
                print("❌ Tipo de usuario inválido")
                return False
                
        except Exception as e:
            print(f"❌ Error en configuración de seguridad: {e}")
            return False
    
    def _setup_basic_user(self, master_password: str) -> bool:
        """Configurar usuario básico (solo lectura)"""
        print("👤 Configurando Usuario Básico (READ_ONLY)")
        print("   - Solo operaciones de lectura permitidas")
        print("   - No se requieren contraseñas adicionales")
        
        # Para usuario básico, solo guardamos la configuración base
        return self.multi_level_security.save_security_config(master_password)
    
    def _setup_standard_user(self, master_password: str) -> bool:
        """Configurar usuario estándar"""
        print("👨‍💼 Configurando Usuario Estándar (STANDARD)")
        
        # Solicitar contraseña para operaciones estándar
        while True:
            std_password = getpass.getpass("Contraseña para operaciones estándar (archivo, restaurar): ")
            if std_password:
                break
            print("❌ La contraseña no puede estar vacía")
        
        # Configurar nivel estándar
        std_hash = hashlib.sha256(std_password.encode()).hexdigest()
        self.multi_level_security.set_level_password(SecurityLevel.STANDARD, std_hash)
        
        return self.multi_level_security.save_security_config(master_password)
    
    def _setup_advanced_user(self, master_password: str) -> bool:
        """Configurar usuario avanzado"""
        print("🔧 Configurando Usuario Avanzado (DESTRUCTIVE)")
        
        # Contraseña para operaciones estándar
        while True:
            std_password = getpass.getpass("Contraseña para operaciones estándar: ")
            if std_password:
                break
            print("❌ La contraseña no puede estar vacía")
        
        # Contraseña para operaciones destructivas
        while True:
            dest_password = getpass.getpass("Contraseña para operaciones destructivas: ")
            if dest_password:
                break
            print("❌ La contraseña no puede estar vacía")
        
        # Configurar niveles
        std_hash = hashlib.sha256(std_password.encode()).hexdigest()
        dest_hash = hashlib.sha256(dest_password.encode()).hexdigest()
        
        self.multi_level_security.set_level_password(SecurityLevel.STANDARD, std_hash)
        self.multi_level_security.set_level_password(SecurityLevel.DESTRUCTIVE, dest_hash)
        
        return self.multi_level_security.save_security_config(master_password)
    
    def _setup_admin_user(self, master_password: str) -> bool:
        """Configurar usuario administrador"""
        print("👑 Configurando Administrador (ADMIN)")
        
        # Contraseña para operaciones estándar
        while True:
            std_password = getpass.getpass("Contraseña para operaciones estándar: ")
            if std_password:
                break
            print("❌ La contraseña no puede estar vacía")
        
        # Contraseña para operaciones destructivas
        while True:
            dest_password = getpass.getpass("Contraseña para operaciones destructivas: ")
            if dest_password:
                break
            print("❌ La contraseña no puede estar vacía")
        
        # Contraseña de administrador
        while True:
            admin_password = getpass.getpass("Contraseña de administrador: ")
            if admin_password:
                break
            print("❌ La contraseña no puede estar vacía")
        
        # Configurar todos los niveles
        std_hash = hashlib.sha256(std_password.encode()).hexdigest()
        dest_hash = hashlib.sha256(dest_password.encode()).hexdigest()
        admin_hash = hashlib.sha256(admin_password.encode()).hexdigest()
        
        self.multi_level_security.set_level_password(SecurityLevel.STANDARD, std_hash)
        self.multi_level_security.set_level_password(SecurityLevel.DESTRUCTIVE, dest_hash)
        self.multi_level_security.set_level_password(SecurityLevel.ADMIN, admin_hash)
        
        return self.multi_level_security.save_security_config(master_password)
    
    def _setup_enterprise_user(self, master_password: str) -> bool:
        """Configurar usuario empresarial (todos los niveles)"""
        print("🏢 Configurando Configuración Empresarial (Todos los niveles)")
        
        # Contraseña para operaciones estándar
        while True:
            std_password = getpass.getpass("Contraseña para operaciones estándar: ")
            if std_password:
                break
            print("❌ La contraseña no puede estar vacía")
        
        # Contraseña para operaciones destructivas
        while True:
            dest_password = getpass.getpass("Contraseña para operaciones destructivas: ")
            if dest_password:
                break
            print("❌ La contraseña no puede estar vacía")
        
        # Contraseña de administrador
        while True:
            admin_password = getpass.getpass("Contraseña de administrador: ")
            if admin_password:
                break
            print("❌ La contraseña no puede estar vacía")
        
        # Configurar todos los niveles
        std_hash = hashlib.sha256(std_password.encode()).hexdigest()
        dest_hash = hashlib.sha256(dest_password.encode()).hexdigest()
        admin_hash = hashlib.sha256(admin_password.encode()).hexdigest()
        
        self.multi_level_security.set_level_password(SecurityLevel.STANDARD, std_hash)
        self.multi_level_security.set_level_password(SecurityLevel.DESTRUCTIVE, dest_hash)
        self.multi_level_security.set_level_password(SecurityLevel.ADMIN, admin_hash)
        
        print("✅ Configuración empresarial completada con todos los niveles de seguridad")
        return self.multi_level_security.save_security_config(master_password)
    
    def validate_credentials(self, credentials: Dict) -> bool:
        """Validar que las credenciales estén completas"""
        required_fields = ['access_key_id', 'secret_access_key', 'server', 'region']
        
        for field in required_fields:
            if not credentials.get(field):
                print(f"❌ Campo requerido faltante: {field}")
                return False
        
        return True
    
    def get_user_type_description(self, user_type: int) -> str:
        """Obtener descripción del tipo de usuario"""
        descriptions = {
            1: "👤 Usuario Básico (READ_ONLY) - Solo lectura",
            2: "👨‍💼 Usuario Estándar (STANDARD) - Operaciones de archivo",
            3: "🔧 Usuario Avanzado (DESTRUCTIVE) - Operaciones destructivas",
            4: "👑 Administrador (ADMIN) - Gestión completa",
            5: "🏢 Configuración Empresarial - Todos los niveles"
        }
        return descriptions.get(user_type, "❓ Tipo desconocido")


def main():
    """Función principal para testing del helper"""
    print("=== Security Setup Helper - Test Mode ===")
    print("Este script es un helper para los instaladores principales.")
    print("Usa install_secure_linux.sh o install_secure_windows.bat para instalación completa.")
    
    # Ejemplo de uso
    helper = SecuritySetupHelper()
    
    print("\nTipos de usuario disponibles:")
    for i in range(1, 6):
        print(f"{i}. {helper.get_user_type_description(i)}")


if __name__ == "__main__":
    main()
