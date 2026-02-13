
# Placeholder for Funnel Backend Main
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Funnel Backend Active"}
