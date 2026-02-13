# Plan de Validación Manual – Clawzeneger Omega 1000X

Después de ejecutar el script de despliegue `DEPLOY_OMEGA_FINAL.ps1`, sigue estos pasos para garantizar que todo funciona correctamente y que puedes recibir pagos.

## Test 1: Conectar WhatsApp
1. Abre [http://localhost:8080](http://localhost:8080) (Evolution API).
2. Escanea el código QR con la aplicación WhatsApp de tu teléfono (modo multi-dispositivo).
3. Verifica que en la interfaz aparezca **"Conectado"** y tu número.
4. Desde otro teléfono, envía un mensaje a tu número y comprueba que aparece en el panel de Evolution.

## Test 2: Importar workflow de ventas en n8n
1. Abre [http://localhost:5678](http://localhost:5678) (n8n).
2. Ve a **"Settings"** → **"Import"** → selecciona el archivo `workflows_n8n/whatsapp_ai_responder.json`.
3. Una vez importado, actívalo (toggle en la esquina superior derecha).
4. Envía un mensaje de WhatsApp con texto como: *"Hola, quiero información sobre un micro-saas para mi negocio"*.
5. Verifica que recibes una respuesta automática inteligente (puede tardar unos segundos).

## Test 3: Probar funnel de pago
1. En el dashboard ([http://localhost:3000](http://localhost:3000)), crea un nuevo embudo con un producto de prueba (precio 1 USD).
2. Publica el embudo y obtén su enlace público.
3. Abre el enlace en una ventana de incógnito.
4. Selecciona un método de pago (**Mercado Pago**, **PayPal** o **Transferencia**).
5. Si eliges Mercado Pago o PayPal, serás redirigido al sandbox; completa la compra con tarjeta de prueba.
6. Después del pago, verifica que en el dashboard aparezca una nueva transacción con estado **"completado"**.
7. (*Si usaste transferencia, simula la confirmación manual con el botón "Ya transferí"*).

## Test 4: Verificar agentes autónomos
1. En el dashboard, ve a la sección **"Agentes"**.
2. Comprueba que los 20 agentes tienen un "corazón" (heartbeat) activo y la última actividad es reciente (< 5 min).
3. Haz clic en **"Ejecutar investigación"** del *Market Researcher*.
4. Espera 1 minuto y recarga la página; debe aparecer un nuevo reporte en la lista.
5. Revisa los logs del agente: `docker logs hub-agent-market` (debe mostrar líneas de actividad).

## Test 5: Probar scraper de YouTube
1. Abre la documentación de la API del scraper: [http://localhost:8001/docs](http://localhost:8001/docs).
2. Ejecuta el endpoint `POST /scrape/youtube` con una URL de un video de negocios.
3. Obtén el `task_id` y luego consulta `GET /result/{task_id}` hasta que esté listo.
4. Verifica que el resultado incluye transcripción, entidades y ideas de negocio.

## Test 6: Probar auto-reparación (Mecánico 24/7)
1. Abre una terminal y detén un agente manualmente: `docker stop hub-agent-coder`.
2. Espera 2 minutos y ejecuta `docker ps | findstr hub-agent-coder`.
3. Debería aparecer de nuevo en ejecución (reiniciado automáticamente).
4. Revisa los logs: `docker logs hub-agent-mechanic`.

## Test 7: Probar generación de leads automática
1. Asegúrate de que el workflow de n8n está activo.
2. Simula varios mensajes de WhatsApp desde diferentes números de prueba.
3. En el dashboard, verifica que aparecen nuevos leads en la tabla, con su puntuación (**score**) calculada.

## Test 8: Probar webhooks de pago (Requiere ngrok)
1. Realiza una compra real con tarjeta de prueba (Mercado Pago sandbox).
2. Verifica que el webhook llega a tu funnel backend (`docker logs hub-funnel-backend`).
3. La transacción debe pasar a **"completada"** automáticamente sin intervención manual.

---

### ✅ Checklist Final de Éxito
- [ ] WhatsApp conectado y respondiendo.
- [ ] n8n con workflow activo.
- [ ] Funnel de prueba genera pago completado.
- [ ] Agentes muestran heartbeats.
- [ ] Scraper devuelve resultados.
- [ ] Auto-reparación funciona.
- [ ] Leads se generan y puntúan.
- [ ] Webhooks de pago (si aplica) funcionan.

**¡Una vez superados estos tests, tu sistema está 100% listo para facturar!** 🚀
