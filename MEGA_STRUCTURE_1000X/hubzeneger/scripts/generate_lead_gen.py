
import os
import textwrap

BASE_DIR = r"c:\CLAWZENEGER\MEGA_STRUCTURE_1000X\clawzeneger-skills\lead-generation-automation"

def create_file(path, content):
    full_path = os.path.join(BASE_DIR, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"Created: {full_path}")

def main():
    print("🚀 Generating Lead Generation Automation System...")

    # --- SHARED ---
    create_file("shared/models.py", textwrap.dedent("""
    from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, JSON, Text
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
    from datetime import datetime

    Base = declarative_base()

    class Lead(Base):
        __tablename__ = 'leads'
        id = Column(Integer, primary_key=True)
        name = Column(String)
        email = Column(String)
        phone = Column(String)
        platform = Column(String)  # twitter, linkedin, etc.
        profile_url = Column(String)
        business_type = Column(String)
        pain_points = Column(JSON)  # lista de dolores
        survey_responses = Column(JSON)
        score = Column(Integer)  # lead score
        status = Column(String)  # new, contacted, surveyed, validated, closed
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    class Campaign(Base):
        __tablename__ = 'campaigns'
        id = Column(Integer, primary_key=True)
        name = Column(String)
        offer_a = Column(Text)
        offer_b = Column(Text)
        offer_c = Column(Text)
        winner = Column(String)  # oferta ganadora
        helpfull_test_id = Column(String)
        created_at = Column(DateTime, default=datetime.utcnow)

    class Audit(Base):
        __tablename__ = 'audits'
        id = Column(Integer, primary_key=True)
        lead_id = Column(Integer)
        maze_study_id = Column(String)
        report_path = Column(String)
        sent_at = Column(DateTime)
        converted = Column(Boolean, default=False)
    """))

    create_file("shared/database.py", textwrap.dedent("""
    import os
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from .models import Base

    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@postgres:5432/leadgen")

    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def init_db():
        Base.metadata.create_all(bind=engine)
    """))

    create_file("shared/redis_queue.py", textwrap.dedent("""
    import redis
    import json
    import os

    redis_client = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://redis:6379/0"))

    def publish(queue, message):
        redis_client.rpush(queue, json.dumps(message))

    def subscribe(queue, block=True):
        if block:
            _, msg = redis_client.blpop(queue)
        else:
            msg = redis_client.lpop(queue)
        if msg:
            return json.loads(msg)
        return None
    """))

    create_file("shared/chroma_client.py", textwrap.dedent("""
    import chromadb
    import os

    def get_client():
        host = os.getenv("CHROMA_HOST", "chromadb")
        return chromadb.HttpClient(host=host, port=8000)
    """))

    # --- AGENTS: Lead Hunter ---
    create_file("agents/lead_hunter/hunter.py", textwrap.dedent("""
    import asyncio
    from shared.redis_queue import publish
    from .platforms.twitter import search_twitter
    from .platforms.linkedin import search_linkedin
    from .platforms.facebook import search_facebook
    from shared.database import SessionLocal, Lead
    import logging

    logger = logging.getLogger(__name__)

    async def hunt():
        # Buscar en cada plataforma
        platforms = [
            ("twitter", search_twitter),
            ("linkedin", search_linkedin),
            ("facebook", search_facebook)
        ]
        for name, func in platforms:
            try:
                leads = await func()
                for lead_data in leads:
                    # Guardar en BD
                    db = SessionLocal()
                    # evitar duplicados por perfil
                    existing = db.query(Lead).filter_by(profile_url=lead_data["profile_url"]).first()
                    if not existing:
                        lead = Lead(**lead_data, status="new")
                        db.add(lead)
                        db.commit()
                        # Notificar al orquestador
                        publish("leads_queue", {"lead_id": lead.id, "action": "new_lead"})
                    db.close()
            except Exception as e:
                logger.error(f"Error en {name}: {e}")

    if __name__ == "__main__":
        asyncio.run(hunt())
    """))

    create_file("agents/lead_hunter/platforms/twitter.py", textwrap.dedent("""
    async def search_twitter():
        # Mock implementation
        return [{
            "name": "Jane Doe",
            "profile_url": "https://twitter.com/janedoe",
            "business_type": "Consulting",
            "pain_points": ["low leads", "bad website"]
        }]
    """))
    create_file("agents/lead_hunter/platforms/linkedin.py", textwrap.dedent("""
    async def search_linkedin():
        # Mock implementation
        return []
    """))
    create_file("agents/lead_hunter/platforms/facebook.py", textwrap.dedent("""
    async def search_facebook():
        # Mock implementation
        return []
    """))

    # --- AGENTS: Surveyor ---
    create_file("agents/surveyor/surveyor.py", textwrap.dedent("""
    import asyncio
    from shared.redis_queue import subscribe, publish
    from shared.database import SessionLocal, Lead
    from .zoho_api import send_survey, get_responses
    import logging

    logger = logging.getLogger(__name__)

    async def process_lead(lead_id):
        db = SessionLocal()
        lead = db.query(Lead).filter_by(id=lead_id).first()
        if not lead:
            db.close()
            return
        # Enviar encuesta (usando plantilla predefinida en Zoho)
        survey_link = await send_survey(lead.email, lead.name)
        lead.status = "survey_sent"
        db.commit()
        db.close()
        # Esperar respuestas (podría ser callback)
        # Aquí simulamos polling
        await asyncio.sleep(86400)  # 1 día después revisar
        responses = await get_responses(lead.email)
        if responses:
            db = SessionLocal()
            lead = db.query(Lead).filter_by(id=lead_id).first()
            lead.survey_responses = responses
            lead.status = "surveyed"
            db.commit()
            db.close()
            publish("leads_queue", {"lead_id": lead_id, "action": "survey_completed"})

    async def main():
        while True:
            msg = subscribe("surveyor_queue", block=True)
            if msg and msg["action"] == "send_survey":
                asyncio.create_task(process_lead(msg["lead_id"]))
            await asyncio.sleep(1)

    if __name__ == "__main__":
        asyncio.run(main())
    """))
    
    create_file("agents/surveyor/zoho_api.py", textwrap.dedent("""
    async def send_survey(email, name):
        # Mock implementation
        return "https://survey.zoho.com/s/12345"
    async def get_responses(email):
        # Mock implementation
        return {"budget": 500, "timeline": "urgent"}
    """))

    # --- AGENTS: Offer Validator ---
    create_file("agents/offer_validator/validator.py", textwrap.dedent("""
    import asyncio
    from shared.redis_queue import subscribe, publish
    from shared.database import SessionLocal, Campaign
    from .helpfull_api import create_test, get_results
    import logging

    logger = logging.getLogger(__name__)

    async def validate_offers(campaign_id):
        db = SessionLocal()
        campaign = db.query(Campaign).filter_by(id=campaign_id).first()
        if not campaign:
            db.close()
            return
        # Crear test en Helpfull con las 3 ofertas
        test_id = await create_test([
            campaign.offer_a,
            campaign.offer_b,
            campaign.offer_c
        ])
        campaign.helpfull_test_id = test_id
        db.commit()
        # Esperar resultados (polling)
        await asyncio.sleep(3600)  # 1 hora después
        results = await get_results(test_id)
        winner = max(results, key=lambda x: x["score"])["option"]
        campaign.winner = winner
        db.commit()
        db.close()
        publish("campaigns_queue", {"campaign_id": campaign_id, "action": "winner_selected", "winner": winner})

    async def main():
        while True:
            msg = subscribe("validator_queue", block=True)
            if msg and msg["action"] == "validate":
                asyncio.create_task(validate_offers(msg["campaign_id"]))
            await asyncio.sleep(1)

    if __name__ == "__main__":
        asyncio.run(main())
    """))

    create_file("agents/offer_validator/helpfull_api.py", textwrap.dedent("""
    async def create_test(options):
        # Mock implementation
        return "test_123"
    async def get_results(test_id):
        # Mock implementation
        return [{"option": "Safe Offer", "score": 90}, {"option": "Risky Offer", "score": 10}]
    """))

    # --- AGENTS: UX Auditor ---
    create_file("agents/ux_auditor/auditor.py", textwrap.dedent("""
    import asyncio
    from shared.redis_queue import subscribe, publish
    from shared.database import SessionLocal, Lead, Audit
    from .maze_api import create_study, get_report
    import logging

    logger = logging.getLogger(__name__)

    async def conduct_audit(lead_id):
        db = SessionLocal()
        lead = db.query(Lead).filter_by(id=lead_id).first()
        if not lead:
            db.close()
            return
        # Crear estudio en Maze (requiere prototipo, aquí lo simulamos con plantilla)
        # Idealmente, tendríamos un generador de prototipos basado en la web del lead
        study_id = await create_study(lead.business_type, lead.pain_points)
        # Esperar resultados
        await asyncio.sleep(7200)  # 2 horas después
        report_url = await get_report(study_id)
        audit = Audit(lead_id=lead_id, maze_study_id=study_id, report_path=report_url)
        db.add(audit)
        lead.status = "audited"
        db.commit()
        db.close()
        publish("leads_queue", {"lead_id": lead_id, "action": "audit_ready"})

    async def main():
        while True:
            msg = subscribe("auditor_queue", block=True)
            if msg and msg["action"] == "start_audit":
                asyncio.create_task(conduct_audit(msg["lead_id"]))
            await asyncio.sleep(1)

    if __name__ == "__main__":
        asyncio.run(main())
    """))

    create_file("agents/ux_auditor/maze_api.py", textwrap.dedent("""
    async def create_study(business_type, pain_points):
        # Mock implementation
        return "study_456"
    async def get_report(study_id):
        # Mock implementation
        return f"https://maze.co/reports/{study_id}"
    """))

    # --- AGENTS: Sales Closer ---
    create_file("agents/sales_closer/closer.py", textwrap.dedent("""
    import asyncio
    from shared.redis_queue import subscribe
    from shared.database import SessionLocal, Lead, Campaign, Audit
    from .email_sender import send_proposal
    from .whatsapp_sender import send_whatsapp
    import logging

    logger = logging.getLogger(__name__)

    async def close_lead(lead_id, winner_offer):
        db = SessionLocal()
        lead = db.query(Lead).filter_by(id=lead_id).first()
        audit = db.query(Audit).filter_by(lead_id=lead_id).first()
        if not lead or not audit:
            db.close()
            return
        # Preparar propuesta personalizada
        proposal = f"Hola {lead.name}, según nuestro análisis y la auditoría UX (ver {audit.report_path}), te recomiendo {winner_offer}. ¿Te gustaría agendar una llamada para implementarlo?"
        # Enviar por email y WhatsApp
        await send_proposal(lead.email, proposal)
        if lead.phone:
            await send_whatsapp(lead.phone, proposal)
        lead.status = "proposal_sent"
        db.commit()
        db.close()
        # Podríamos programar seguimiento

    async def main():
        while True:
            msg = subscribe("closer_queue", block=True)
            if msg and msg["action"] == "send_proposal":
                asyncio.create_task(close_lead(msg["lead_id"], msg["winner"]))
            await asyncio.sleep(1)

    if __name__ == "__main__":
        asyncio.run(main())
    """))

    create_file("agents/sales_closer/email_sender.py", textwrap.dedent("""
    async def send_proposal(email, content):
        print(f"Sending email to {email}: {content}")
        return True
    """))
    create_file("agents/sales_closer/whatsapp_sender.py", textwrap.dedent("""
    async def send_whatsapp(phone, content):
        print(f"Sending WA to {phone}: {content}")
        return True
    """))


    # --- ORCHESTRATOR ---
    create_file("orchestrator/orchestrator.py", textwrap.dedent("""
    import asyncio
    from shared.redis_queue import subscribe, publish
    from shared.database import SessionLocal, Lead, Campaign
    import logging

    logger = logging.getLogger(__name__)

    async def handle_new_lead(lead_id):
        # Enviar a surveyor
        publish("surveyor_queue", {"action": "send_survey", "lead_id": lead_id})

    async def handle_survey_completed(lead_id):
        # Una vez que tenemos respuestas, podemos decidir si es buen lead
        db = SessionLocal()
        lead = db.query(Lead).filter_by(id=lead_id).first()
        if lead and lead.survey_responses:
            # Si tiene presupuesto > 100 USD, procedemos
            budget = lead.survey_responses.get("budget", 0)
            if budget >= 100:
                # Agregar a campaña de validación (necesitamos una campaña activa)
                # Aquí simplificado: asumimos que hay una campaña ID 1
                publish("auditor_queue", {"action": "start_audit", "lead_id": lead_id})
            else:
                lead.status = "rejected_budget"
                db.commit()
        db.close()

    async def handle_audit_ready(lead_id):
        # La auditoría está lista, ahora necesitamos la oferta ganadora
        # Asumimos que la campaña ya tiene ganador
        db = SessionLocal()
        campaign = db.query(Campaign).first() # Tomar la primera campaña activa
        if campaign and campaign.winner:
            publish("closer_queue", {"action": "send_proposal", "lead_id": lead_id, "winner": campaign.winner})
        db.close()

    async def main():
        while True:
            # Escuchar cola de leads (eventos globales)
            msg = subscribe("leads_queue", block=False)
            if msg:
                if msg["action"] == "new_lead":
                    await handle_new_lead(msg["lead_id"])
                elif msg["action"] == "survey_completed":
                    await handle_survey_completed(msg["lead_id"])
                elif msg["action"] == "audit_ready":
                    await handle_audit_ready(msg["lead_id"])
            await asyncio.sleep(1)

    if __name__ == "__main__":
        asyncio.run(main())
    """))


    # --- INFRASTRUCTURE FILES ---
    
    # Dockerfiles (Simple Python Base)
    dockerfile_content = textwrap.dedent("""
    FROM python:3.9-slim
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    COPY . .
    CMD ["python", "app.py"] 
    # ^ Placeholder CMD, will be overridden by docker-compose or file specific naming
    """)
    
    # We need to copy 'shared' into each context or mount it. 
    # Best practice for monorepo is building from root, but here we generated inside folders.
    # We'll assume the build context is the root of lead-generation-automation
    
    dockerfile_template = textwrap.dedent("""
    FROM python:3.9-slim
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    COPY shared /app/shared
    COPY agents/{agent_name} /app/agents/{agent_name}
    ENV PYTHONPATH=/app
    CMD ["python", "agents/{agent_name}/{script_name}"]
    """)

    # Customize per agent
    create_file("agents/lead_hunter/Dockerfile", dockerfile_template.format(agent_name="lead_hunter", script_name="hunter.py"))
    create_file("agents/surveyor/Dockerfile", dockerfile_template.format(agent_name="surveyor", script_name="surveyor.py"))
    create_file("agents/offer_validator/Dockerfile", dockerfile_template.format(agent_name="offer_validator", script_name="validator.py"))
    create_file("agents/ux_auditor/Dockerfile", dockerfile_template.format(agent_name="ux_auditor", script_name="auditor.py"))
    create_file("agents/sales_closer/Dockerfile", dockerfile_template.format(agent_name="sales_closer", script_name="closer.py"))
    
    # Orchestrator Dockerfile
    create_file("orchestrator/Dockerfile", textwrap.dedent("""
    FROM python:3.9-slim
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    COPY shared /app/shared
    COPY orchestrator /app/orchestrator
    ENV PYTHONPATH=/app
    CMD ["python", "orchestrator/orchestrator.py"]
    """))

    # Requirements
    reqs = "redis\nsqlalchemy\npsycopg2-binary\nrequests\nchromadb"
    create_file("agents/lead_hunter/requirements.txt", reqs)
    create_file("agents/surveyor/requirements.txt", reqs)
    create_file("agents/offer_validator/requirements.txt", reqs)
    create_file("agents/ux_auditor/requirements.txt", reqs)
    create_file("agents/sales_closer/requirements.txt", reqs)
    create_file("orchestrator/requirements.txt", reqs)

    # Docker Compose
    create_file("docker-compose.leadgen.yml", textwrap.dedent("""
    version: '3.8'

    services:
      redis:
        image: redis:alpine
        networks:
          - leadgen-net

      postgres:
        image: postgres:15-alpine
        environment:
          POSTGRES_USER: user
          POSTGRES_PASSWORD: password
          POSTGRES_DB: leadgen
        networks:
          - leadgen-net
        volumes:
          - pg_data:/var/lib/postgresql/data

      lead_hunter:
        build:
          context: .
          dockerfile: agents/lead_hunter/Dockerfile
        environment:
          - REDIS_URL=redis://redis:6379/0
          - DATABASE_URL=postgresql://user:password@postgres:5432/leadgen
        depends_on:
          - redis
          - postgres
        networks:
          - leadgen-net

      surveyor:
        build:
          context: .
          dockerfile: agents/surveyor/Dockerfile
        environment:
          - REDIS_URL=redis://redis:6379/0
          - DATABASE_URL=postgresql://user:password@postgres:5432/leadgen
        depends_on:
          - redis
          - postgres
        networks:
          - leadgen-net

      offer_validator:
        build:
          context: .
          dockerfile: agents/offer_validator/Dockerfile
        environment:
          - REDIS_URL=redis://redis:6379/0
          - DATABASE_URL=postgresql://user:password@postgres:5432/leadgen
        depends_on:
          - redis
          - postgres
        networks:
          - leadgen-net

      ux_auditor:
        build:
          context: .
          dockerfile: agents/ux_auditor/Dockerfile
        environment:
          - REDIS_URL=redis://redis:6379/0
          - DATABASE_URL=postgresql://user:password@postgres:5432/leadgen
        depends_on:
          - redis
          - postgres
        networks:
          - leadgen-net

      sales_closer:
        build:
          context: .
          dockerfile: agents/sales_closer/Dockerfile
        environment:
          - REDIS_URL=redis://redis:6379/0
          - DATABASE_URL=postgresql://user:password@postgres:5432/leadgen
        depends_on:
          - redis
          - postgres
        networks:
          - leadgen-net

      orchestrator:
        build:
          context: .
          dockerfile: orchestrator/Dockerfile
        environment:
          - REDIS_URL=redis://redis:6379/0
          - DATABASE_URL=postgresql://user:password@postgres:5432/leadgen
        depends_on:
          - redis
          - postgres
        networks:
          - leadgen-net

    networks:
      leadgen-net:
        driver: bridge

    volumes:
      pg_data:
    """))

    # .env example
    create_file(".env.leadgen.example", textwrap.dedent("""
    ZOHO_API_KEY=your_zoho_key
    HELPFULL_API_KEY=your_helpfull_key
    MAZE_API_KEY=your_maze_key
    OPENAI_API_KEY=your_openai_key
    """))

    # Deploy script
    create_file("DEPLOY_LEADGEN.ps1", textwrap.dedent("""
    Write-Host "🔥 Desplegando Sistema de Automatización de Leads..." -ForegroundColor Cyan
    docker-compose -f docker-compose.leadgen.yml up -d --build
    Write-Host "✅ ¡Sistema LeadGen desplegado con éxito!" -ForegroundColor Green
    """))

if __name__ == "__main__":
    main()
