import os
import logging
from datetime import datetime

# Asegurarse de que el logging esté configurado
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

try:
    from clawbot import Skill, command, on
except ImportError:
    log.error("Error Crítico: No se pudo importar 'clawbot'. El skill no funcionará.")
    # Definir clases dummy para que el archivo al menos se pueda importar sin crashear
    class Skill: pass
    def command(func): return func
    def on(event): def decorator(func): return func; return decorator

class Archivist(Skill):
    """
    Un skill para gestionar una base de conocimiento activa,
    permitiendo guardar y catalogar información de forma proactiva.
    Versión robusta.
    """
    KB_ROOT = "/mnt/d/Neil Virtual Tests/NexoBot/knowledge_base"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        log.info("Skill 'Archivist' inicializado correctamente.")
        if not os.path.isdir(self.KB_ROOT):
            log.warning(f"El directorio base de conocimiento no existe: {self.KB_ROOT}")

    @command
    def save_knowledge(self, category: str, *, content: str):
        """
        Guarda un fragmento de conocimiento en una categoría específica.
        Uso: /save_knowledge {categoría} {contenido}
        """
        try:
            # Sanitizar nombre de categoría
            safe_category = "".join(c for c in category if c.isalnum() or c in ('_', '-')).rstrip()
            if not safe_category:
                self.reply("Categoría inválida. Por favor, usa solo letras y números.")
                return

            category_path = os.path.join(self.KB_ROOT, safe_category)
            os.makedirs(category_path, exist_ok=True)

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"knowledge_{timestamp}.md"
            file_path = os.path.join(category_path, filename)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"# Conocimiento guardado el {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
                f.write(content)

            self.reply(f"✅ Conocimiento guardado en '{safe_category}/{filename}'. Ya está disponible para RAG.")
            self.reply("Este nuevo conocimiento ya está disponible para consultas futuras a través de RAG en OpenWebUI.")

        except Exception as e:
            log.error(f"Error en save_knowledge: {e}")
            self.reply(f"🚨 Error al guardar el conocimiento: {e}")

    @on("after_reply")
    def prompt_for_knowledge(self, last_user_message: str, last_bot_reply: str):
        """
        Después de una interacción, sugiere guardar el conocimiento.
        """
        # Desactivado por defecto para evitar ruido hasta que se pruebe bien
        pass
