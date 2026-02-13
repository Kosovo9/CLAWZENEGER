
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from .models import SessionLocal, ScrapedVideo
from .config import settings
from .tasks.youtube import extract_youtube

app = FastAPI(title=settings.PROJECT_NAME)

class ScrapeRequest(BaseModel):
    url: str

@app.post("/scrape/youtube")
async def scrape_youtube_endpoint(request: ScrapeRequest):
    # Encolar tarea en Celery
    task = extract_youtube.delay(request.url)
    return {"task_id": task.id, "status": "processing", "message": "Scraping job started"}

@app.get("/result/{video_id}")
def get_result(video_id: int):
    db = SessionLocal()
    video = db.query(ScrapedVideo).filter_by(id=video_id).first()
    db.close()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return {
        "id": video.id,
        "url": video.url,
        "title": video.title,
        "summary": video.summary,
        "entities": video.entities,
        "business_ideas": video.business_ideas
    }

@app.get("/health")
def health():
    return {"status": "ok", "service": "Scraper System"}
