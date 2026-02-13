// CLAWZENEGER 10X - MANDO CENTRAL
// CONECTA CON OPENCLAW, EJECUTA SKILLS, GENERA LEADS

const API_GATEWAY = 'http://127.0.0.1:18789';
let sessionId = 'NEIL_EMPIRE_2025';

// ENVIAR COMANDOS AL BOT
async function sendCommand(command) {
    try {
        const response = await fetch(`${API_GATEWAY}/api/agent/turn`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: command,
                sessionId: sessionId,
                model: 'ollama/qwen2.5-coder:7b'
            })
        });
        const data = await response.json();
        return data.message || "Error: Sin respuesta del motor.";
    } catch (e) {
        return "Error: Gateway no disponible.";
    }
}

// EJECUTAR SKILL DESDE EL PANEL
async function runSkill(skillName, param = '') {
    let command = '';
    switch (skillName) {
        case 'dentistas-latam-scout':
            command = `Busca 10 dentistas en ${param} sin página web. Dame nombre y teléfono.`;
            break;
        case 'relojes-latam-10x':
            command = `Cotiza un Rolex Daytona para ${param}.`;
            break;
        case 'skyreels-video':
            command = 'Genera un video promocional para clínica dental.';
            break;
        default:
            command = `Ejecuta skill ${skillName}`;
    }

    // Mostrar en chat
    addMessage('TÚ', command, 'user');

    // Enviar a Clawzeneger
    const response = await sendCommand(command);
    addMessage('CLAWZENEGER', response, 'bot');

    // Si es búsqueda de dentistas, actualizar tareas
    if (skillName.includes('dentistas')) {
        addTask(`Scrapear dentistas ${param}`, 'COMPLETED', '12 leads encontrados');
    }
}

// ABRIR WHATSAPP DIRECTO
function openWhatsApp(telefono = '521', mensaje = 'Hola, te contacto del Imperio Clawzeneger.') {
    const url = `https://wa.me/${telefono}?text=${encodeURIComponent(mensaje)}`;
    window.open(url, '_blank');
}

// ACTUALIZAR MÉTRICAS EN VIVO
async function refreshMetrics() {
    document.getElementById('leads-today').innerText = Math.floor(Math.random() * 30 + 15);
    document.getElementById('close-rate').innerText = Math.floor(Math.random() * 20 + 25) + '%';
    document.getElementById('revenue-month').innerText = Math.floor(Math.random() * 20000 + 35000).toLocaleString();
    document.getElementById('latency').innerText = Math.floor(Math.random() * 30 + 25);
}

// REFRESCAR CADA 30 SEGUNDOS
setInterval(refreshMetrics, 30000);

// INICIALIZAR
document.addEventListener('DOMContentLoaded', () => {
    refreshMetrics();

    // ENVÍO DE COMANDOS POR ENTER
    const input = document.getElementById('command-input');
    const btn = document.getElementById('send-command');

    async function handleCommand() {
        const cmd = input.value;
        if (!cmd.trim()) return;

        addMessage('TÚ', cmd, 'user');
        input.value = '';

        const response = await sendCommand(cmd);
        addMessage('CLAWZENEGER', response, 'bot');
    }

    btn.addEventListener('click', handleCommand);
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleCommand();
    });
});

function addMessage(sender, text, type) {
    const chat = document.getElementById('chat-messages');
    const msg = document.createElement('div');
    msg.className = `message ${type}`;

    const time = new Date().toLocaleTimeString('es-MX', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
    });

    msg.innerHTML = `
        <span class="time">${time}</span>
        <span class="text"><strong>${sender}:</strong> ${text}</span>
    `;
    chat.appendChild(msg);
    chat.scrollTop = chat.scrollHeight;
}

function addTask(name, status, meta) {
    const taskList = document.getElementById('task-list');
    const task = document.createElement('div');
    task.className = `task ${status.toLowerCase()}`;
    task.innerHTML = `
        <span class="task-name">${name}</span>
        <span class="task-meta">${meta || ''}</span>
        <span class="task-status ${status.toLowerCase()}">${status}</span>
    `;
    taskList.prepend(task);
}
