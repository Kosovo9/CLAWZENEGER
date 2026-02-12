set -euo pipefail

echo "==[0] Stop limpio (NO mezclar systemd + daemon al mismo tiempo) =="
systemctl --user stop clawdbot-gateway.service 2>/dev/null || true
clawdbot daemon stop 2>/dev/null || true
pkill -f 'clawdbot|clawd' 2>/dev/null || true

echo "==[1] Reset start-limit (si se quedó bloqueado por muchos crashes) =="
systemctl --user reset-failed clawdbot-gateway.service 2>/dev/null || true

echo "==[2] Permisos correctos (audit warning) =="
mkdir -p ~/.clawdbot/credentials ~/.clawdbot/agents/main/sessions
chmod 700 ~/.clawdbot ~/.clawdbot/credentials
[ -f ~/.clawdbot/clawdbot.json ] && chmod 600 ~/.clawdbot/clawdbot.json || true

echo "==[3] Backup config =="
ts="$(date +%F-%H%M%S)"
cp -a ~/.clawdbot/clawdbot.json ~/.clawdbot/clawdbot.json.bak.$ts

echo "==[4] Patch config: bind válido + modelo local + WA apagado por seguridad =="
python3 - <<'PY'
import json, pathlib
p = pathlib.Path.home()/".clawdbot"/"clawdbot.json"
cfg = json.loads(p.read_text())

# --- Gateway estable (bind debe ser modo, NO IP) ---
gw = cfg.setdefault("gateway", {})
gw["bind"] = "loopback"     # <- evita el error "gateway.bind: Invalid input"
gw.setdefault("port", 18789)

auth = gw.setdefault("auth", {})
auth.setdefault("mode", "token")
auth.setdefault("token", auth.get("token",""))  # NO lo cambia

control = gw.setdefault("controlUi", {})
control.setdefault("allowInsecureAuth", True)   # OK solo porque bind=loopback (local-only)

# --- Modelo: fuerza primary a Ollama (evita “claude-opus…” por default) ---
agents = cfg.setdefault("agents", {}).setdefault("defaults", {})
mdl = agents.setdefault("model", {})
mdl.setdefault("primary", "ollama/qwen3:8b-16k")
mdl["fallbacks"] = []  # <- no intentes cloud si estás offline

# --- Proveedor Ollama por OpenAI Chat Completions ---
models = cfg.setdefault("models", {})
models.setdefault("mode", "merge")
prov = models.setdefault("providers", {})
oll = prov.setdefault("ollama", {})
oll.setdefault("apiKey", "ollama-local")
oll["api"] = "openai-chat-completions"  # <- clave para que responda chat
# baseUrl se setea en el paso [5] según conectividad

# --- WhatsApp OFF por ahora (evitar que mande cosas mientras arreglamos core) ---
plugins = cfg.setdefault("plugins", {}).setdefault("entries", {})
plugins.setdefault("whatsapp", {})["enabled"] = False
wa = cfg.setdefault("channels", {}).setdefault("whatsapp", {})
wa["enabled"] = False
wa["dmPolicy"] = "allowlist"
wa["allowFrom"] = ["+5216143277218", "+5213331915253"]
wa["groupPolicy"] = "disabled"

p.write_text(json.dumps(cfg, indent=2, ensure_ascii=False))
print("patched:", p)
PY

echo "==[5] Detectar dónde vive Ollama (WSL vs Windows host) y setear baseUrl =="
HOST_IP="$(ip route | awk '/default/ {print $3; exit}')"
OLLAMA_HOST=""
for h in 127.0.0.1 localhost "$HOST_IP"; do
  if curl -s -m 1 "http://$h:11434/api/version" >/dev/null 2>&1; then
    OLLAMA_HOST="$h"
    break
  fi
done
if [ -z "$OLLAMA_HOST" ]; then
  echo "ERROR: No puedo ver Ollama en 11434 desde WSL. Arráncalo (Windows o WSL) y reintenta."
  exit 1
fi
export OLLAMA_HOST
python3 - <<'PY'
import json, pathlib, os
p = pathlib.Path.home()/".clawdbot"/"clawdbot.json"
cfg = json.loads(p.read_text())
cfg["models"]["providers"]["ollama"]["baseUrl"] = f"http://{os.environ['OLLAMA_HOST']}:11434/v1"
p.write_text(json.dumps(cfg, indent=2, ensure_ascii=False))
print("ollama baseUrl ->", cfg["models"]["providers"]["ollama"]["baseUrl"])
PY

echo "==[6] Start gateway (solo systemd) y esperar puerto =="
systemctl --user start clawdbot-gateway.service
for i in $(seq 1 40); do
  ss -lnt | grep -q ':18789' && break
  sleep 0.25
done

echo "== listener =="
ss -lntp | egrep ':18789|clawdbot' || true

echo "== curl =="
curl -I -m 2 "http://localhost:18789/" | head
