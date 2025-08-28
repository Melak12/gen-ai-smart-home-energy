from fastapi import FastAPI, APIRouter

app = FastAPI(title="Smart Home Energy Backend")

auth_router = APIRouter()
telemetry_router = APIRouter()
ai_router = APIRouter()

@auth_router.get("/auth/health")
def auth_health():
    return {"status": "ok", "service": "auth"}

@telemetry_router.get("/telemetry/health")
def telemetry_health():
    return {"status": "ok", "service": "telemetry"}

@ai_router.get("/ai/health")
def ai_health():
    return {"status": "ok", "service": "conversational_ai"}

app.include_router(auth_router)
app.include_router(telemetry_router)
app.include_router(ai_router)
