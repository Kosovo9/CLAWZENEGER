import os
from datetime import datetime
from clawbot import Skill, command, on

class Archivist(Skill):
    """
    Un skill para gestionar una base de conocimiento activa,
    permitiendo guardar y catalogar información de forma proactiva.
    """
    KB_ROOT = "/mnt/d/Neil Virtual Tests/NexoBot/knowledge_base"

    @command
    def save_knowledge(self, category: str, *, content: str):
        """
        Guarda un fragmento de conocimiento en una categoría específica.
        Uso: /save_knowledge {categoría} {contenido del conocimiento}
        """
        category_path = os.path.join(self.KB_ROOT, category)
        if not os.path.exists(category_path):
            os.makedirs(category_path)
            self.reply(f"He creado una nueva categoría de conocimiento: '{category}'.")

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"knowledge_{timestamp}.md"
        file_path = os.path.join(category_path, filename)

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.reply(f"✅ Conocimiento guardado exitosamente en '{category}/{filename}'.")
            self.reply("Este nuevo conocimiento ya está disponible para consultas futuras a través de RAG en OpenWebUI.")
        except Exception as e:
            self.reply(f"🚨 Error al guardar el conocimiento: {e}")

    @on("after_reply")
    def prompt_for_knowledge(self, last_user_message: str, last_bot_reply: str):
        """
        Después de una interacción, sugiere guardar el conocimiento.
        Esta es una simulación de un comportamiento proactivo.
        """
        # Lógica simple: si la conversación es larga, pregunta.
        if len(last_user_message) > 100 and "proyecto" in last_user_message.lower():
            suggestion = (
                "Socio, esta parece una conversación importante. "
                "¿Hay algo de lo que hablamos que deba guardar en la base de conocimiento? "
                "Puedes usar: /save_knowledge {categoría} {resumen}"
            )
            # self.reply(suggestion) # Descomentar para activar
            pass
