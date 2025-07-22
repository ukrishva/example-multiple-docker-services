## service-a/app/app.py (same for service-b, change name if needed)

from fastapi import FastAPI
import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
import requests
from .models.message import Message  # Use relative import

load_dotenv()

app = FastAPI()

@app.get("/")
def read_root():
    return {"service": os.getenv("SERVICE_NAME", "Unknown")}

@app.get("/ping-vector-db")
def ping_chroma():
    chroma_url = f"http://{os.getenv('CHROMA_HOST')}:{os.getenv('CHROMA_PORT')}/"
    try:
        r = requests.get(chroma_url)
        return {"status": r.status_code}
    except Exception as e:
        return {"error": str(e)}

@app.get("/ping-graph-db")
def ping_neo4j():
    try:
        uri = os.getenv("NEO4J_URI")
        user = os.getenv("NEO4J_USER")
        password = os.getenv("NEO4J_PASSWORD")
        driver = GraphDatabase.driver(uri, auth=(user, password))
        with driver.session() as session:
            result = session.run("RETURN 1 AS test")
            return {"neo4j_result": result.single()['test']}
    except Exception as e:
        return {"error": str(e)}

@app.get("/call-service-a")
def call_service_a():
    service_a_url = f"http://{os.getenv('SERVICE_A_HOST')}:{os.getenv('SERVICE_A_PORT')}/"
    try:
        r = requests.get(service_a_url)
        return {"service_a_response": r.json()}
    except Exception as e:
        return {"error": str(e)}

@app.post("/post-message")
def post_message(message: Message):
    # Here you can process the message as needed
    return {"received_message": message.content}