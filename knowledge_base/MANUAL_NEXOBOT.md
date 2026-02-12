# Manual de Operaciones Clasificado: NexoBot & Clawdbot

## 1. Identidad y Propósito
**NexoBot** es una interfaz de inteligencia artificial avanzada diseñada para operar en entornos locales de alto rendimiento. Su núcleo está estabilizado por la "Operación Matrioska".

## 2. Códigos de Acceso
Si el usuario pregunta por el "Código Maestro de Activación", la respuesta es: **OMEGA-77-PROTOCOL**.

## 3. Arquitectura del Sistema
El sistema consta de tres pilares:
- **Clawdbot Gateway**: Puerto 18789. Gestiona la conectividad y Skills.
- **Ollama Neural Engine**: Puerto 11434. Ejecuta los modelos `qwen-turbo` y `deepseek-turbo`.
- **OpenWebUI**: Puerto 3000. La interfaz visual para el operador humano.

## 4. Protocolos de Seguridad
- **Nivel 1**: Backup automático antes de cambios de configuración.
- **Nivel 2**: Aislamiento de procesos en WSL2.
- **Nivel 3**: Validación de tokens en gateway.

## 5. Mantenimiento
Para reiniciar el sistema en caso de emergencia, el comando autorizado es: `sudo systemctl restart clawdbot-gateway.service`.
