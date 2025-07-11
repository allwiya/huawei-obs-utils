#!/usr/bin/env python3
"""
Ejemplo de configuración y uso de niveles de seguridad
Demuestra cómo configurar y usar el sistema de seguridad multinivel
"""

import os
import sys
from security_levels import MultiLevelSecurity, SecurityLevel, setup_multi_level_security
from obs_manager_secure import SecureOBSManager


def demo_security_levels():
    """Demostración del sistema de niveles de seguridad"""
    print("🔐 Demo: Sistema de Niveles de Seguridad")
    print("=" * 50)

    # Verificar si ya existe configuración de seguridad
    security = MultiLevelSecurity()

    print("\n📋 Niveles de Seguridad Disponibles:")
    print("1. READ_ONLY    - Operaciones de solo lectura (list, search, download)")
    print("2. STANDARD     - Operaciones estándar (archive, restore, warm)")
    print("3. DESTRUCTIVE  - Operaciones destructivas (delete, purge)")
    print("4. ADMIN        - Operaciones administrativas (bucket management)")

    print("\n🎯 Ejemplo de Configuración:")
    print("- READ_ONLY: Sin contraseña (libre acceso)")
    print("- STANDARD: Contraseña 'standard123'")
    print("- DESTRUCTIVE: Contraseña 'delete456!'")
    print("- ADMIN: Contraseña 'admin789@'")

    return security


def demo_operations():
    """Demostrar operaciones con diferentes niveles de seguridad"""
    print("\n🧪 Probando Operaciones con Niveles de Seguridad")
    print("=" * 50)

    try:
        # Inicializar OBS Manager con seguridad
        obs_manager = SecureOBSManager(enable_security_levels=True)

        print("\n1. 📖 Operación READ_ONLY (sin contraseña)")
        print("   Intentando listar objetos...")
        # Esta operación debería funcionar sin contraseña si READ_ONLY no tiene contraseña

        print("\n2. 🔧 Operación STANDARD (requiere contraseña)")
        print("   Intentando cambiar clase de almacenamiento...")
        print("   Se te pedirá la contraseña para nivel STANDARD")

        print("\n3. ⚠️  Operación DESTRUCTIVE (requiere contraseña + confirmación)")
        print("   Intentando eliminar objetos...")
        print("   Se te pedirá la contraseña para nivel DESTRUCTIVE")
        print("   Y confirmación adicional por ser operación destructiva")

        obs_manager.close()

    except Exception as e:
        print(f"❌ Error en demo: {e}")


def create_example_config():
    """Crear configuración de ejemplo para testing"""
    print("\n🔧 Creando Configuración de Ejemplo")
    print("=" * 40)

    # Configuración de ejemplo (solo para demostración)
    example_config = {
        "levels": {
            SecurityLevel.READ_ONLY: {
                "password_hash": None,  # Sin contraseña
                "operations": ["list", "search", "download"],
                "description": "Read-only operations (list, search, download)",
            },
            SecurityLevel.STANDARD: {
                "password_hash": "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3",  # "hello"
                "operations": ["archive", "warm", "restore"],
                "description": "Standard operations (archive, restore, change storage class)",
            },
            SecurityLevel.DESTRUCTIVE: {
                "password_hash": "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f",  # "secret123"
                "operations": ["delete", "purge"],
                "description": "Destructive operations (delete objects, purge buckets)",
            },
            SecurityLevel.ADMIN: {
                "password_hash": "c1c224b03cd9bc7b6a86d77f5dace40191766c485cd55dc48caf9ac873335d6f",  # "admin456"
                "operations": ["create_bucket", "delete_bucket", "manage_permissions"],
                "description": "Administrative operations (bucket management)",
            },
        },
        "settings": {"require_confirmation": True, "log_all_operations": True, "session_timeout": 3600},
    }

    print("📝 Configuración de ejemplo:")
    print("- READ_ONLY: Sin contraseña")
    print("- STANDARD: Contraseña 'hello'")
    print("- DESTRUCTIVE: Contraseña 'secret123'")
    print("- ADMIN: Contraseña 'admin456'")

    return example_config


def interactive_security_demo():
    """Demo interactivo del sistema de seguridad"""
    print("\n🎮 Demo Interactivo")
    print("=" * 30)

    while True:
        print("\nOpciones disponibles:")
        print("1. Ver niveles de seguridad configurados")
        print("2. Configurar niveles de seguridad")
        print("3. Probar operación READ_ONLY")
        print("4. Probar operación STANDARD")
        print("5. Probar operación DESTRUCTIVE")
        print("6. Salir")

        try:
            choice = input("Selecciona opción (1-6): ").strip()

            if choice == "1":
                security = MultiLevelSecurity()
                security.list_security_levels()

            elif choice == "2":
                setup_multi_level_security()

            elif choice == "3":
                print("\n📖 Probando operación READ_ONLY...")
                try:
                    obs_manager = SecureOBSManager(enable_security_levels=True)
                    # Simular operación de listado
                    print("ℹ️  Esta operación requeriría credenciales válidas de OBS")
                    obs_manager.close()
                except Exception as e:
                    print(f"ℹ️  Demo: {e}")

            elif choice == "4":
                print("\n🔧 Probando operación STANDARD...")
                try:
                    obs_manager = SecureOBSManager(enable_security_levels=True)
                    # Simular operación de archivo
                    print("ℹ️  Esta operación requeriría credenciales válidas de OBS")
                    obs_manager.close()
                except Exception as e:
                    print(f"ℹ️  Demo: {e}")

            elif choice == "5":
                print("\n⚠️  Probando operación DESTRUCTIVE...")
                try:
                    obs_manager = SecureOBSManager(enable_security_levels=True)
                    # Simular operación destructiva
                    print("ℹ️  Esta operación requeriría credenciales válidas de OBS")
                    obs_manager.close()
                except Exception as e:
                    print(f"ℹ️  Demo: {e}")

            elif choice == "6":
                print("👋 ¡Hasta luego!")
                break

            else:
                print("❌ Opción inválida")

        except KeyboardInterrupt:
            print("\n👋 Demo cancelado")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


def main():
    """Función principal del ejemplo"""
    print("🔐 OBS Utils - Ejemplo de Niveles de Seguridad")
    print("=" * 60)

    # Verificar disponibilidad del módulo
    try:
        from security_levels import MultiLevelSecurity

        print("✅ Módulo de niveles de seguridad disponible")
    except ImportError:
        print("❌ Módulo de niveles de seguridad no disponible")
        print("   Instala: pip install cryptography")
        return

    # Demostración
    demo_security_levels()
    create_example_config()

    # Preguntar si quiere demo interactivo
    print("\n" + "=" * 60)
    response = input("¿Quieres probar el demo interactivo? (y/N): ").lower().strip()

    if response in ["y", "yes", "sí", "si"]:
        interactive_security_demo()

    print("\n📖 Para más información:")
    print("- Ejecuta: python obs_utils_improved.py --setup-security-levels")
    print("- Consulta: SECURITY.md")
    print("- Usa: python obs_utils_improved.py --list-security-levels")


if __name__ == "__main__":
    main()
