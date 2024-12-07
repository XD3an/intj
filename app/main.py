from fastapi import FastAPI
# from contextlib import asynccontextmanager
import logging

from api.router import router
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler("./logs/main.log"),
        logging.StreamHandler()
    ]
)

app = FastAPI(
    title="INTJ: An LLM based IoT Network Threat Journeyman",
    version="1.0",
    description="INTJ is LLM based IoT Network Threat Journeyman that helps in detecting and mitigating IoT network threats."
)

app.include_router(router)
# Ensure the logs directory exists
os.makedirs("./logs", exist_ok=True)