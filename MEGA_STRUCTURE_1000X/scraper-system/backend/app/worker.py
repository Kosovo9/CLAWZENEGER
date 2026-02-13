
from celery import Celery
from .tasks.youtube import celery as youtube_app
from .config import settings

# 🦅 CLAWZENEGER SCRAPER WORKER
# Centralizing all scraper tasks for 10x efficiency.

app = youtube_app

if __name__ == "__main__":
    app.start()
