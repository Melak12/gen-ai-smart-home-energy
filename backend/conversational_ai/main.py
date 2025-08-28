from fastapi import FastAPI

app = FastAPI(title="Conversational AI Service")

@app.get("/health")
def health():
    return {"status": "ok"}
