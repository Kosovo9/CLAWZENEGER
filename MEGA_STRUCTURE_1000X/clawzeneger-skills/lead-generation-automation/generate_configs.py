import os

components = {
    "agents/lead_hunter": "agents/lead_hunter/hunter.py",
    "agents/surveyor": "agents/surveyor/surveyor.py",
    "agents/offer_validator": "agents/offer_validator/validator.py",
    "agents/ux_auditor": "agents/ux_auditor/auditor.py",
    "agents/sales_closer": "agents/sales_closer/closer.py",
    "orchestrator": "orchestrator/orchestrator.py"
}

dockerfile_template = """FROM python:3.11-slim
WORKDIR /app
COPY {path}/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY shared /app/shared
COPY {path} /app/{path}
ENV PYTHONPATH=/app
CMD ["python", "{cmd}"]
"""

requirements = "sqlalchemy\npsycopg2-binary\nredis\nrequests\nhttpx\n"

base_path = r"c:\CLAWZENEGER\MEGA_STRUCTURE_1000X\clawzeneger-skills\lead-generation-automation"

for path, cmd in components.items():
    # Requirements
    req_path = os.path.join(base_path, path, "requirements.txt")
    os.makedirs(os.path.dirname(req_path), exist_ok=True)
    with open(req_path, "w") as f:
        f.write(requirements)
    
    # Dockerfile
    df_path = os.path.join(base_path, path, "Dockerfile")
    with open(df_path, "w") as f:
        f.write(dockerfile_template.format(path=path, cmd=cmd))

print("Created Dockerfiles and requirements for leadgen components.")
