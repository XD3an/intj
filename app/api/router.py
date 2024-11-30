from fastapi import APIRouter, HTTPException
from service.langchain_pipeline import process_with_langchain
from models.query_request import QueryRequest
import time
import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
        handlers=[
        logging.FileHandler("./logs/router.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get(
    "/",
    response_description="Root Endpoint",
    status_code=200,
    summary="Welcome to INTJ IoT Security Assistant",
    description="Returns a welcome message and system status"
)
async def root():
    return {"message": "Welcome to INTJ: IoT Network Threat Journeyman"}

@router.post(
    "/ask",
    response_description="Process User Query",
    status_code=200,
    summary="IoT Security Query Processing",
    description="Submit a query for IoT network threat analysis"
)
async def ask(request: QueryRequest):
    if not request.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    current_time = time.time()

    try:
        # Performance tracking
        start_time = time.time()
        
        # Process the query
        response = process_with_langchain(request.query, request.context)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Structured logging
        logger.info(
            "Query processed successfully", 
            extra={
                "query_length": len(request.query),
                "context_length": len(request.context) if request.context else 0,
                "processing_time": processing_time
            }
        )
        
        return {
            "response": response,
            "metadata": {
                "processing_time": processing_time,
                "timestamp": current_time
            }
        }
    
    except ValueError as ve:
        logger.error(f"Input validation error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    
    except ConnectionError as ce:
        logger.error(f"Service connection error: {ce}")
        raise HTTPException(
            status_code=503, 
            detail="IoT analysis service is temporarily unavailable"
        )
    
    except Exception as e:
        logger.exception(f"Unexpected error during query processing: {e}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during IoT threat analysis"
        )

@router.get(
    "/health",
    status_code=200,
    summary="System Health Check",
    description="Check the operational status of the INTJ IoT Security Assistant"
)
async def health_check():
    return {
        "status": "healthy",
        "services": {
            "langchain": "operational",
            "ollama": "connected"
        },
        "timestamp": time.time()
    }
