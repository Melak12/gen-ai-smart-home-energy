from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from routes.auth import get_current_user
from utils.gemini import query_gemini
from typing import Optional, Dict, Any

router = APIRouter(prefix="/ai", tags=["conversational_ai"])

class QueryRequest(BaseModel):
    question: str
    device_id: Optional[int] = None
    time_range: Optional[str] = None  # e.g., 'last 7 days'

class QueryResponse(BaseModel):
    answer: str
    raw: Optional[Dict[str, Any]] = None

@router.post("/query", response_model=QueryResponse, summary="Conversational AI query", description="Ask a natural language question about your energy usage. Optionally filter by device or time range.")
async def ai_query(request: QueryRequest, user=Depends(get_current_user)):
    # Optionally: enrich prompt with user/device context
    prompt = f"User question: {request.question}\n"
    if request.device_id:
        prompt += f"Device ID: {request.device_id}\n"
    if request.time_range:
        prompt += f"Time range: {request.time_range}\n"
    try:
        answer = query_gemini(prompt)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Gemini API error: {e}")
    return QueryResponse(answer=answer)
