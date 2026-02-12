# CLAWZENEGER FUNNEL 10X - FINAL VERSION
$ErrorActionPreference = "Continue"

Write-Host "Iniciando Activacion de Clawzeneger Funnel 10X..." -ForegroundColor Cyan

# 1. Kill Windows Ollama
Write-Host "Killing Windows Ollama..." -ForegroundColor Yellow
taskkill /F /IM ollama.exe 2>$null
Start-Sleep -Seconds 2

# 2. Check Gateway
Write-Host "Checking Gateway..." -ForegroundColor Cyan
try {
    $health = Invoke-WebRequest -Uri "http://localhost:18789/health" -UseBasicParsing -TimeoutSec 5
    Write-Host "Gateway Response: $($health.Content)" -ForegroundColor Green
}
catch {
    Write-Host "Restarting Clawzeneger Gateway..." -ForegroundColor Yellow
    wsl bash -c "echo 'Pataya@77/' | sudo -S systemctl --user restart clawdbot-gateway.service"
    Start-Sleep -Seconds 5
}

# 3. Create Skills
Write-Host "Creating Skills..." -ForegroundColor Cyan
if (!(Test-Path "D:\Neil Virtual Tests\NexoBot\skills")) { 
    New-Item -ItemType Directory -Path "D:\Neil Virtual Tests\NexoBot\skills" -Force 
}

# Skill 1: Intent Detector
$s1 = @'
module.exports = {
  name: "intent_detector_10x",
  description: "Detecta intencion de compra",
  async run(context, { mensaje }) {
    const text = (mensaje || "").toLowerCase();
    const highIntent = ["quiero", "comprar", "precio", "costo", "pago", "link", "ahora", "urgente"];
    const mediumIntent = ["como", "funciona", "sirve", "ejemplo", "demo", "planes"];
    const highScore = highIntent.filter(word => text.includes(word)).length;
    const mediumScore = mediumIntent.filter(word => text.includes(word)).length;
    let nivel = "bajo";
    let accion = "nutrir";
    if (highScore >= 1) { nivel = "alto"; accion = "enviar_link_pago"; }
    else if (mediumScore >= 2) { nivel = "medio"; accion = "enviar_demo"; }
    return { nivel, accion, confianza: Math.min(0.99, highScore * 0.5 + mediumScore * 0.2) };
  }
};
'@
$s1 | Set-Content -Path "D:\Neil Virtual Tests\NexoBot\skills\intent-detector-10x.js" -Force -Encoding ASCII

# Skill 2: Objection Killer
$s2 = @'
module.exports = {
  name: "objection_killer_10x",
  description: "Destruye objeciones",
  async run(context, { objecion }) {
    const o = (objecion || "").toLowerCase();
    if (o.includes("caro") || o.includes("precio")) {
      return "Te entiendo. La mayoria de clientes piensa igual, hasta que ven el retorno. Inviertes 49 USD y generas +500 USD en contenido. Sigue siendo caro?";
    }
    if (o.includes("tiempo") || o.includes("demora")) {
      return "47 segundos. Eso tarda en generarse tu primera imagen.";
    }
    if (o.includes("pensarlo") || o.includes("despues")) {
      return "Hoy es el ultimo dia del 20% OFF. Maniana pagas mas. Cerramos con el descuento?";
    }
    return "Cuentame mas, quiero entender tu duda.";
  }
};
'@
$s2 | Set-Content -Path "D:\Neil Virtual Tests\NexoBot\skills\objection-killer-10x.js" -Force -Encoding ASCII

# Skill 3: Closer
$s3 = @'
module.exports = {
  name: "closer_10x",
  description: "Cierra ventas con urgencia",
  async run(context, { lead, link }) {
    const frases = [
      (lead || "Compa") + ", tu link ya esta generado. Valido por 20 minutos: " + link,
      "Quedan 3 spots con este bono. Te guardo uno? " + link,
      "El sistema te espera. Dale clic y en 2 minutos estas adentro: " + link,
      "Hoy es el dia. Listo para despegar? " + link
    ];
    return { mensaje: frases[Math.floor(Math.random() * frases.length)], link_pago: link };
  }
};
'@
$s3 | Set-Content -Path "D:\Neil Virtual Tests\NexoBot\skills\closer-10x.js" -Force -Encoding ASCII

Write-Host "Skills created in disk." -ForegroundColor Green

# 4. Register Skills in OpenClaw
Write-Host "Registering Skills in OpenClaw..." -ForegroundColor Cyan
wsl openclaw skills install --file "/mnt/d/Neil Virtual Tests/NexoBot/skills/intent-detector-10x.js"
wsl openclaw skills install --file "/mnt/d/Neil Virtual Tests/NexoBot/skills/objection-killer-10x.js"
wsl openclaw skills install --file "/mnt/d/Neil Virtual Tests/NexoBot/skills/closer-10x.js"

# 5. Load Model in WSL
Write-Host "Loading Model in WSL..." -ForegroundColor Cyan
wsl ollama run qwen2.5-coder:7b "" 2>$null
Start-Sleep -Seconds 2

# 6. Verification
Write-Host "--- Verification ---" -ForegroundColor Cyan
wsl openclaw skills list

Write-Host ""
Write-Host "Clawzeneger 10X is active." -ForegroundColor Green
Write-Host "Modo Imperio Activado." -ForegroundColor Red
Write-Host ""
