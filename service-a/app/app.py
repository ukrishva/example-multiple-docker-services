## service-a/app/app.py (same for service-b, change name if needed)

from fastapi import FastAPI
import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
import requests

load_dotenv()

app = FastAPI()

@app.get("/")
def read_root():
    return {"service": os.getenv("SERVICE_NAME", "Unknown")}

@app.get("/service_info")
def service_info():
    return {
        "service_a": {
            "host": os.getenv("SERVICE_A_HOST"),
            "port": os.getenv("SERVICE_A_PORT")
        },
        "service_b": {
            "host": os.getenv("SERVICE_B_HOST"),
            "port": os.getenv("SERVICE_B_PORT")
        }
    }