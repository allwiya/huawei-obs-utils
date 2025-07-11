#!/usr/bin/env python3
"""
Ejemplo de uso de OBS Utils con funciones de seguridad
Demuestra cómo usar las diferentes opciones de configuración segura
"""

import os
import sys
from config import Config
from obs_manager import OBSManager
from security import ConfigSecurity, setup_secure_config

def example_encrypted_config():
    """Ejemplo usando configuración cifrada"""
    print("=== Ejemplo: Configuración Cifrada ===")
    
    try:
        # Verificar si existe configuración cifrada
        security = ConfigSecurity()
        
        if not security.is_encrypted():
            print("No se encontró configuración cifrada.")
            print("Ejecuta: python obs_utils_improved.py --setup-secure-config")
            return
        
        # Cargar configuración cifrada
        config = Config(use_encryption=True)
        
        if config.validate_credentials():
            print("✅ Configuración cifrada cargada correctamente")
            
            # Usar OBS Manager con configuración cifrada
            obs_manager = OBSManager()
            
            # Ejemplo de operación
            print("Probando conexión...")
            # obs_manager.list_objects("test-bucket")  # Descomenta para probar
            
            obs_manager.close()
            print("✅ Conexión exitosa con configuración cifrada")
        else:
            print("❌ Credenciales inválidas en configuración cifrada")
            
    except Exception as e:
        print(f"❌ Error con configuración cifrada: {e}")

def example_env_variables():
    """Ejemplo usando variables de entorno"""
    print("\n=== Ejemplo: Variables de Entorno ===")
    
    # Verificar variables de entorno
    required_vars = ['OBS_ACCESS_KEY_ID', 'OBS_SECRET_ACCESS_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Variables de entorno faltantes: {missing_vars}")
        print("Configura las variables:")
        for var in missing_vars:
            print(f"  export {var}='tu_valor_aqui'")
        return
    
    try:
        # Cargar configuración desde variables de entorno
        config = Config()
        
        if config.validate_credentials():
            print("✅ Variables de entorno configuradas correctamente")
            print(f"Server: {config.get('server')}")
            print(f"Region: {config.get('region')}")
        else:
            print("❌ Variables de entorno incompletas")
            
    except Exception as e:
        print(f"❌ Error con variables de entorno: {e}")

def example_secure_file():
    """Ejemplo usando archivo con permisos seguros"""
    print("\n=== Ejemplo: Archivo con Permisos Seguros ===")
    
    config_file = "obs_config.json"
    
    if not os.path.exists(config_file):
        print(f"❌ Archivo {config_file} no encontrado")
        print("Crea uno con: python obs_utils_improved.py --create-config")
        return
    
    try:
        config = Config(config_file)
        
        # Verificar y corregir permisos
        if os.name != 'nt':  # No Windows
            file_stat = os.stat(config_file)
            if file_stat.st_mode & 0o077:
                print("⚠️  Archivo tiene permisos inseguros")
                config.secure_file_permissions()
            else:
                print("✅ Permisos de archivo seguros")
        
        if config.validate_credentials():
            print("✅ Configuración de archivo válida")
        else:
            print("❌ Credenciales inválidas en archivo")
            
    except Exception as e:
        print(f"❌ Error con archivo de configuración: {e}")

def example_security_operations():
    """Ejemplo de operaciones de seguridad"""
    print("\n=== Ejemplo: Operaciones de Seguridad ===")
    
    try:
        security = ConfigSecurity()
        
        # Verificar estado de cifrado
        if security.is_encrypted():
            print("✅ Configuración cifrada detectada")
            print(f"Archivos: {security.encrypted_file}, {security.salt_file}")
        else:
            print("ℹ️  No se detectó configuración cifrada")
        
        # Ejemplo de cambio de contraseña (comentado para evitar ejecución accidental)
        # print("Para cambiar contraseña:")
        # print("security.change_password()")
        
    except ImportError:
        print("❌ Módulo de seguridad no disponible")
        print("Instala: pip install cryptography")

def example_multiple_configs():
    """Ejemplo usando múltiples configuraciones"""
    print("\n=== Ejemplo: Múltiples Configuraciones ===")
    
    configs = {
        "Producción": "prod_config.json",
        "Desarrollo": "dev_config.json", 
        "Testing": "test_config.json"
    }
    
    for env_name, config_file in configs.items():
        if os.path.exists(config_file):
            try:
                config = Config(config_file)
                if config.validate_credentials():
                    print(f"✅ {env_name}: Configuración válida ({config_file})")
                else:
                    print(f"❌ {env_name}: Credenciales inválidas ({config_file})")
            except Exception as e:
                print(f"❌ {env_name}: Error cargando {config_file} - {e}")
        else:
            print(f"ℹ️  {env_name}: Archivo {config_file} no encontrado")

def interactive_security_setup():
    """Setup interactivo de seguridad"""
    print("\n=== Setup Interactivo de Seguridad ===")
    
    print("¿Quieres configurar seguridad ahora?")
    print("1. Sí, configurar cifrado")
    print("2. Sí, mostrar guía de variables de entorno")
    print("3. Sí, crear archivo con permisos seguros")
    print("4. No, salir")
    
    try:
        choice = input("Selecciona opción (1-4): ").strip()
        
        if choice == "1":
            setup_secure_config()
        elif choice == "2":
            print("\nConfigura estas variables de entorno:")
            print("export OBS_ACCESS_KEY_ID='tu_access_key'")
            print("export OBS_SECRET_ACCESS_KEY='tu_secret_key'")
            print("export OBS_SERVER='https://obs.sa-peru-1.myhuaweicloud.com/'")
            print("export OBS_REGION='sa-peru-1'")
            print("\nLuego ejecuta: source ~/.bashrc")
        elif choice == "3":
            config = Config()
            config.create_sample_config()
            config.secure_file_permissions()
        elif choice == "4":
            print("Setup cancelado")
        else:
            print("Opción inválida")
            
    except KeyboardInterrupt:
        print("\nSetup cancelado por el usuario")

def main():
    """Función principal de ejemplos"""
    print("🔒 OBS Utils - Ejemplos de Uso Seguro")
    print("=" * 50)
    
    # Ejecutar ejemplos
    example_encrypted_config()
    example_env_variables()
    example_secure_file()
    example_security_operations()
    example_multiple_configs()
    
    # Setup interactivo opcional
    interactive_security_setup()
    
    print("\n" + "=" * 50)
    print("✅ Ejemplos completados")
    print("\nPara más información:")
    print("- Consulta SECURITY.md")
    print("- Ejecuta: python obs_utils_improved.py --help")
    print("- Usa: python obs_utils_improved.py --setup-secure-config")

if __name__ == "__main__":
    main()
