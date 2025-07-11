# Guía de Seguridad

Esta guía proporciona información completa sobre las características de seguridad de OBS Utils y mejores prácticas para proteger tus credenciales y datos.

## 🔒 Características de Seguridad

### Encriptación AES-256
- **Algoritmo**: AES-256 en modo CBC
- **Protección**: Credenciales completamente encriptadas
- **Clave**: Derivada de contraseña usando PBKDF2
- **Salt**: Único para cada archivo de configuración

### Múltiples Métodos de Autenticación
1. **Configuración Encriptada** (Más Segura)
2. **Variables de Entorno** (Recomendado para Servidores)
3. **Archivo de Configuración** (Básico con permisos seguros)

### Detección de Configuración Insegura
- Verificación automática de permisos de archivos
- Alertas para configuraciones vulnerables
- Recomendaciones de seguridad automáticas

## 🛡️ Configuración Segura

### Método 1: Configuración Encriptada (Recomendado)

#### Configuración Inicial
```bash
python obs_utils_improved.py --setup-secure-config
```

#### Proceso Paso a Paso
1. **Ingreso de Credenciales**:
   ```
   Ingresa tu Access Key ID: AKIAIOSFODNN7EXAMPLE
   Ingresa tu Secret Access Key: [oculto]
   Ingresa el servidor OBS: https://obs.sa-peru-1.myhuaweicloud.com/
   Ingresa la región: sa-peru-1
   ```

2. **Creación de Contraseña de Encriptación**:
   ```
   Crea una contraseña de encriptación fuerte: [oculto]
   Confirma la contraseña: [oculto]
   ```

3. **Verificación de Seguridad**:
   ```
   ✅ Configuración encriptada guardada
   ✅ Permisos de archivo establecidos (600)
   ✅ Validación de seguridad completada
   ```

#### Cambiar Contraseña de Encriptación
```bash
python obs_utils_improved.py --change-password
```

### Método 2: Variables de Entorno

#### Configuración Segura
```bash
# Linux/macOS - Agregar a ~/.bashrc (solo lectura del usuario)
chmod 600 ~/.bashrc
echo 'export OBS_ACCESS_KEY_ID="tu_access_key"' >> ~/.bashrc
echo 'export OBS_SECRET_ACCESS_KEY="tu_secret_key"' >> ~/.bashrc
echo 'export OBS_SERVER="https://obs.sa-peru-1.myhuaweicloud.com/"' >> ~/.bashrc
echo 'export OBS_REGION="sa-peru-1"' >> ~/.bashrc
source ~/.bashrc
```

#### Variables Temporales (Sesión Única)
```bash
# Establecer para sesión actual solamente
export OBS_ACCESS_KEY_ID="tu_access_key"
export OBS_SECRET_ACCESS_KEY="tu_secret_key"
export OBS_SERVER="https://obs.sa-peru-1.myhuaweicloud.com/"
export OBS_REGION="sa-peru-1"
```

### Método 3: Archivo de Configuración con Permisos Seguros

#### Crear y Asegurar Archivo
```bash
# Crear configuración
python obs_utils_improved.py --create-config

# Establecer permisos seguros (solo propietario)
chmod 600 obs_config.json

# Verificar permisos
ls -la obs_config.json
# Debe mostrar: -rw------- 1 usuario grupo
```

#### Windows - Permisos Seguros
```powershell
# Ejecutar como Administrador
icacls obs_config.json /inheritance:r
icacls obs_config.json /grant:r "%USERNAME%:F"
icacls obs_config.json /remove "Everyone"
icacls obs_config.json /remove "Users"
```

## 🔐 Mejores Prácticas de Contraseñas

### Contraseñas de Encriptación Fuertes
- **Longitud**: Mínimo 12 caracteres
- **Complejidad**: Mayúsculas, minúsculas, números, símbolos
- **Unicidad**: Diferente a otras contraseñas
- **Almacenamiento**: Usar gestor de contraseñas

#### Ejemplos de Contraseñas Fuertes
```
✅ Buenas:
- MyS3cur3P@ssw0rd2025!
- Obs#Utils$Secure&2025
- CloudStorage!Safe#123

❌ Débiles:
- password123
- obs2025
- 12345678
```

### Rotación de Credenciales
```bash
# Cada 90 días, rotar claves de acceso
# 1. Crear nuevas claves en Huawei Cloud Console
# 2. Actualizar configuración
python obs_utils_improved.py --setup-secure-config

# 3. Probar nueva configuración
python obs_utils_improved.py --test-config

# 4. Eliminar claves antiguas de Huawei Cloud Console
```

## ⚠️ Detección de Vulnerabilidades

### Verificación Automática de Seguridad
OBS Utils verifica automáticamente:

#### Permisos de Archivos
```bash
# Verificación automática al iniciar
python obs_utils_improved.py --operation list --bucket mi-bucket

# Salida de ejemplo:
⚠️  ADVERTENCIA: obs_config.json tiene permisos inseguros (644)
🔧 Recomendación: chmod 600 obs_config.json
```

#### Configuración Expuesta
```bash
# Detecta archivos de configuración en ubicaciones inseguras
⚠️  ADVERTENCIA: Archivo de configuración en directorio público
🔧 Recomendación: Mover a directorio privado del usuario
```

### Verificación Manual de Seguridad
```bash
# Verificar estado de seguridad
python obs_utils_improved.py --security-check

# Verificar permisos de archivos
ls -la obs_config.json*
ls -la logs/

# Verificar variables de entorno
env | grep OBS
```

## 🚨 Respuesta a Incidentes

### Si las Credenciales se Comprometen

#### Pasos Inmediatos
1. **Deshabilitar claves comprometidas**:
   - Ir a Huawei Cloud Console
   - "Mis Credenciales" > "Claves de Acceso"
   - Eliminar claves comprometidas

2. **Crear nuevas credenciales**:
   ```bash
   # Crear nuevas claves en la consola
   # Actualizar configuración inmediatamente
   python obs_utils_improved.py --setup-secure-config
   ```

3. **Verificar acceso no autorizado**:
   - Revisar logs de OBS en Huawei Cloud Console
   - Verificar actividad inusual en buckets
   - Cambiar contraseñas relacionadas

4. **Actualizar todas las instancias**:
   ```bash
   # Actualizar en todos los servidores/entornos
   # Verificar scripts automatizados
   # Actualizar documentación de equipo
   ```

### Monitoreo de Seguridad

#### Logs de Seguridad
```bash
# Revisar logs de autenticación
grep "Authentication" logs/obs_utils.log

# Revisar intentos fallidos
grep "FAILED\|ERROR" logs/obs_utils.log

# Monitorear accesos
tail -f logs/obs_utils.log | grep "Access"
```

#### Alertas Automáticas
```bash
# Configurar alertas para fallos de autenticación
# Agregar a crontab para verificación diaria
0 9 * * * /ruta/a/obs_utils/security_check.sh
```

## 🔧 Configuración de Entorno Seguro

### Desarrollo Local
```bash
# Usar configuración encriptada
python obs_utils_improved.py --setup-secure-config

# Establecer permisos de directorio
chmod 700 ~/obs_utils/
chmod 600 ~/obs_utils/obs_config.json.enc
```

### Entorno de Servidor
```bash
# Usar variables de entorno
export OBS_ACCESS_KEY_ID="clave_desde_vault"
export OBS_SECRET_ACCESS_KEY="secreto_desde_vault"

# Configurar en systemd service
[Service]
Environment=OBS_ACCESS_KEY_ID=clave_valor
Environment=OBS_SECRET_ACCESS_KEY=secreto_valor
```

### Contenedores Docker
```dockerfile
# Usar secrets de Docker
FROM python:3.9
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

# Usar secrets en runtime
# docker run --secret obs_access_key --secret obs_secret_key app
```

### CI/CD Pipelines
```yaml
# GitHub Actions ejemplo
env:
  OBS_ACCESS_KEY_ID: ${{ secrets.OBS_ACCESS_KEY_ID }}
  OBS_SECRET_ACCESS_KEY: ${{ secrets.OBS_SECRET_ACCESS_KEY }}
  OBS_SERVER: ${{ secrets.OBS_SERVER }}
  OBS_REGION: ${{ secrets.OBS_REGION }}
```

## 📋 Lista de Verificación de Seguridad

### ✅ Configuración Inicial
- [ ] Credenciales obtenidas de forma segura
- [ ] Método de configuración seguro elegido
- [ ] Permisos de archivo establecidos correctamente
- [ ] Contraseña de encriptación fuerte creada
- [ ] Configuración probada y funcionando

### ✅ Mantenimiento Regular
- [ ] Credenciales rotadas cada 90 días
- [ ] Logs de seguridad revisados mensualmente
- [ ] Permisos de archivo verificados
- [ ] Acceso no autorizado monitoreado
- [ ] Backups de configuración seguros

### ✅ Respuesta a Incidentes
- [ ] Plan de respuesta documentado
- [ ] Contactos de emergencia definidos
- [ ] Procedimiento de rotación de credenciales
- [ ] Logs de auditoría configurados
- [ ] Alertas automáticas establecidas

## 🆘 Soporte de Seguridad

### Reportar Vulnerabilidades
- **Email**: [security@ccvass.com](mailto:security@ccvass.com)
- **Asunto**: "OBS Utils Security - [Descripción Breve]"
- **Incluir**: Detalles técnicos, pasos para reproducir, impacto

### Recursos Adicionales
- [Guía de Configuración](CONFIGURACION.md)
- [Solución de Problemas](SOLUCION_PROBLEMAS.md)
- [Documentación de Huawei Cloud OBS Security](https://support.huaweicloud.com/obs/)

### Actualizaciones de Seguridad
- Suscribirse a notificaciones del repositorio
- Revisar regularmente las notas de versión
- Aplicar actualizaciones de seguridad promptamente

---

**🔒 La seguridad es responsabilidad compartida. Mantén tus credenciales seguras.**

**Desarrollado por CCVASS - Lima, Perú 🇵🇪**
