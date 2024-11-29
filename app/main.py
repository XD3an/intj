from fastapi import FastAPI
# from contextlib import asynccontextmanager
import logging

from api.router import router


logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="INTJ: An LLM based IoT Network Threat Journeyman",
    version="1.0",
    description="INTJ is a tool that uses LLM to detect and respond to threats in IoT networks."
)

app.include_router(router)