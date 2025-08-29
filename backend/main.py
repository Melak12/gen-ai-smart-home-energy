from fastapi import FastAPI
from routes.auth import router as auth_router
from routes.telemetry import router as telemetry_router
from routes.conversational_ai import router as ai_router

app = FastAPI(title="Smart Home Energy Backend")

app.include_router(auth_router)
app.include_router(telemetry_router)
app.include_router(ai_router)
