
# 🔗 INSTRUCCIONES DE CONEXIÓN (CLUSTER 2 PCS)

## PASO 1: Preparar PC 2 (El Trabajador)
1.  Copia la carpeta `MEGA_STRUCTURE_1000X` a la PC 2.
2.  En PC 2, abre PowerShell y corre:
    `docker-compose -f docker-compose.worker.yml up -d`
3.  Averigua la IP de la PC 2 (comando `ipconfig`). Supongamos que es `192.168.1.50`.

## PASO 2: Configurar PC 1 (El Maestro)
1.  Edita el archivo `docker-compose.god_mode.yml` en PC 1.
2.  Busca la sección de `openwebui` o `n8n`.
3.  Añade la variable de entorno para conectar al cerebro remoto:
    `- OLLAMA_WORKER_URL=http://192.168.1.50:11434`

## PASO 3: Delegar Tareas
*   En **n8n (PC 1)**, cuando configures un nodo de IA pesado (ej. escribir código complejo), apunta al host `192.168.1.50` en lugar de `localhost`.
*   Esto libera a tu PC 1 para que maneje el chat y las ventas sin lag, mientras PC 2 suda la gota gorda generando el trabajo.

¡Listo! Tienes un Cluster de IA casero. 🚀
