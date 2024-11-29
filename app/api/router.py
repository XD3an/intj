from fastapi import APIRouter, HTTPException
from service.langchain_pipeline import process_with_langchain
from models.query_request import QueryRequest
import logging

router = APIRouter()

@router.get(
    "/",
    response_description="Root Endpoint",
    status_code=200
)
async def root():
    return {"message": "Welcome to INTJ: IoT Network Threat Journeyman"}

@router.post(
    "/ask",
    response_description="Process User Query",
    status_code=200,
)
async def ask(request: QueryRequest):
    query = request.query
    context = request.context

    try:
        response = process_with_langchain(query, context)
        return {"response": response}
    except ValueError as ve:
        logging.error(f"Invalid input error: {ve}")
        raise HTTPException(status_code=400, detail="Invalid input format")
    except ConnectionError as ce:
        logging.error(f"Connection error: {ce}")
        raise HTTPException(status_code=503, detail="Service unavailable")
    except Exception as e:
        logging.error(f"Unexpected error during ask request: {e}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please try again later."
        )
