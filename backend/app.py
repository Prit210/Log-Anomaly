from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = "db.json"

def read_db():
    try:
        with open(DB_FILE) as f:
            return json.load(f)
    except:
        return []

@app.get("/")
def home():
    return {"message": "DeepLog API running"}

@app.get("/logs")
def get_logs():
    return read_db()[-100:]

@app.get("/stats")
def get_stats():
    data = read_db()
    total = len(data)
    abnormal = sum(1 for x in data if x["status"] == "ABNORMAL")
    normal = sum(1 for x in data if x["status"] == "NORMAL")

    return {
        "total": total,
        "abnormal": abnormal,
        "normal": normal
    }