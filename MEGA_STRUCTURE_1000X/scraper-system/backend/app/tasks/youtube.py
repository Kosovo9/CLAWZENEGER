
import asyncio
import yt_dlp
from celery import Celery
from ..config import settings
from ..models import SessionLocal, ScrapedVideo

celery = Celery(__name__, broker=settings.REDIS_URL, backend=settings.REDIS_URL)

@celery.task(name="scraper.extract_youtube")
def extract_youtube(url: str):
    """Extrae transcripción y metadatos de un video de YouTube"""
    # Simplified synchronous wrapper for example purposes
    # In prod, logic to extract subtitles would go here
    
    ydl_opts = {
        'skip_download': True,
        'quiet': True,
    }
    
    title = "Unknown"
    transcript = "No transcript available (Mock)"
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Unknown Title')
    except Exception as e:
        print(f"Error extracting info: {e}")

    # Save initial record
    db = SessionLocal()
    video = ScrapedVideo(url=url, title=title, transcript=transcript)
    try:
        db.add(video)
        db.commit()
        db.refresh(video)
    except Exception:
        db.rollback()
        video = db.query(ScrapedVideo).filter_by(url=url).first()
    
    db.close()
    
    # Normally we would daisy-chain tasks here:
    # analyze_video.delay(video.id)
    
    return {"video_id": video.id, "title": title}
