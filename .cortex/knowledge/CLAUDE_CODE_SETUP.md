# 🚀 CortexMCP Setup Guide for Claude Code

## Paso 1: Configuración Automática (Recomendado)

El archivo `.mcp.json` ya está configurado en el proyecto. Claude Code debería detectarlo automáticamente.

## Paso 2: Configuración Manual (Si es necesario)

Si Claude Code no detecta automáticamente el servidor, ejecuta:

```bash
claude mcp add cortex-mcp -s project poetry run python server.py
```

O usando variables de entorno:

```bash
claude mcp add cortex-mcp -s project -e CORTEX_COLLABORATION_MODE=enabled -e STRATEGY_LOG_LEVEL=info poetry run python server.py
```

## Paso 3: Verificar la Configuración

1. **Ver servidores MCP configurados:**
   ```bash
   claude mcp list
   ```

2. **Ver el estado del servidor:**
   ```bash
   claude mcp status cortex-mcp
   ```

## Paso 4: Monitoreo de Logs en Tiempo Real

### Opción 1: Logs del Servidor MCP
Los logs aparecerán automáticamente en Claude Code cuando uses las herramientas MCP.

### Opción 2: Logs Detallados en Terminal Separada
Para ver logs más detallados, abre una terminal separada y ejecuta:

```bash
# Terminal 1: Logs en tiempo real
STRATEGY_LOG_LEVEL=debug poetry run python server.py

# Terminal 2: Claude Code (usar normalmente)
```

### Opción 3: Logs a Archivo
```bash
# Configurar logging a archivo
STRATEGY_LOG_LEVEL=debug poetry run python server.py 2> cortex_logs.txt

# En otra terminal, ver logs en tiempo real:
tail -f cortex_logs.txt
```

## Paso 5: Prueba de Funcionamiento

Una vez configurado, deberías poder usar:

```
Hey Claude, usa la herramienta strategy-architect para planificar un e-commerce con microservicios
```

## Troubleshooting

### Si el servidor no inicia:
```bash
# Verificar dependencias
poetry install

# Verificar que el servidor funciona standalone
timeout 3 poetry run python server.py
```

### Si Claude Code no encuentra el servidor:
```bash
# Re-configurar manualmente
claude mcp remove cortex-mcp
claude mcp add cortex-mcp -s project poetry run python server.py
```

### Para ver logs de debug detallados:
```bash
# En .mcp.json, cambiar:
"env": {
  "CORTEX_COLLABORATION_MODE": "enabled",
  "STRATEGY_LOG_LEVEL": "debug"
}
```

## Variables de Entorno Disponibles

- `CORTEX_COLLABORATION_MODE`: `enabled|disabled|auto` (default: auto)
- `STRATEGY_LOG_LEVEL`: `debug|info|warning|error` (default: info)

## Ejemplos de Uso

### Ejemplo 1: Proyecto Simple
```
Usa strategy-architect para: "Crear una aplicación de gestión de tareas con autenticación"
```

### Ejemplo 2: Proyecto Enterprise
```
Usa strategy-architect para: "Diseñar una plataforma de e-commerce escalable con microservicios, OAuth2, integración de pagos y ML para recomendaciones. Debe soportar multi-tenant y analytics en tiempo real"
```

### Ejemplo 3: Continuación de Workflow
```
Usa strategy-architect con el análisis previo para continuar con la descomposición de fases
```

¡Listo para la demostración en vivo! 🎉