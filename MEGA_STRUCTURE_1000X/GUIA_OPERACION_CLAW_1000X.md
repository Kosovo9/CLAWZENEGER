# 🦅 GUÍA DE OPERACIÓN CLAWZENEGER OMEGA 1000X

## 🤖 1. NeilZenneger: El Supervisor Supremo
NeilZenneger es la inteligencia superior de la red. No solo ejecuta tareas, sino que **audita** y **planea** para maximizar ingresos.

*   **Auditoría (Cada 3 horas):** Verifica salud de agentes, leads y servidores.
*   **Plan Matutino (9:00 AM):** Lista de tareas prioritarias para generar dinero.
*   **Reporte Nocturno (9:00 PM):** Resumen de ingresos, logros y recomendaciones.
*   **Comandos Manuales:** Envía `{"action": "audit_now"}` a la cola Redis `queue:neilzenneger`.

---

## 🤝 2. Sistema de Afiliados
Sistema de crecimiento orgánico con 30% de comisión.
*   **Dashboard:** `http://localhost:9201`
*   **API Admin:** `http://localhost:9200/docs`
*   **Tracking:** Cookies de 30 días activas.

---

## 🎙️ 3. ClawVoice Pro
Generación de voz y avatares con IA hyper-realista.
*   **Portal:** Accede a la interfaz premium para clonar voces y crear videos de venta.
*   **Motores:** XTTS y Fish Speech activos en Docker.

---

## 🌐 4. Túnel & Conectividad (LIVE)
Para recibir pagos de Mercado Pago/PayPal en tu PC local, necesitas un túnel activo.
1.  **Registro:** Crea una cuenta en `https://dashboard.ngrok.com/signup`.
2.  **Auth:** Copia tu Token y ejecútalo en la terminal:
    `ngrok config add-authtoken TU_TOKEN_AQUI`
3.  **Encender:** Ejecuta `ngrok http 8002` para exponer la pasarela de pagos.
4.  **Webhooks:** Copia la URL de ngrok (ej: `https://abcd.ngrok-free.app`) y ponla en tu dashboard de Mercado Pago.

---

## 🚀 5. Lanzamiento del Sistema
1.  **God Mode Full:** `docker-compose -f docker-compose.god_mode.FINAL.yml up -d --build`
2.  **Verificar NeilZenneger:** `docker logs claw-neilzenneger -f`
3.  **Dashboard Afiliados:** `http://localhost:9201`

---

## 💳 5. Pasarela de Pagos
*   **Mercado Pago:** Integrado con redirección a Studio Nexora.
*   **PayPal:** Botón dinámico listo para cobros internacionales.
*   **Transferencia:** Datos bancarios visibles en el checkout.

**ESTADO DEL SISTEMA: 97% (READY FOR ASCENSION)**
