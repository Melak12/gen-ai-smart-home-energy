
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from prisma import Prisma
from routes.auth import get_current_user
from datetime import datetime

router = APIRouter(prefix="/telemetry", tags=["telemetry"])
db = Prisma()

class TelemetryIn(BaseModel):
    timestamp: datetime
    deviceId: int
    usage: float

class TelemetryOut(BaseModel):
    id: int
    timestamp: datetime
    usage: float
    deviceId: int

@router.on_event("startup")
async def startup():
    await db.connect()

@router.on_event("shutdown")
async def shutdown():
    await db.disconnect()

@router.post("/", response_model=TelemetryOut, summary="Submit telemetry data", description="Submit a telemetry record for a device you own.")
async def submit_telemetry(data: TelemetryIn, user=Depends(get_current_user)):
    device = await db.device.find_unique(where={"id": data.deviceId})
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    if device.userId != user.id:
        raise HTTPException(status_code=403, detail="Not your device")
    entry = await db.telemetry.create({
        "timestamp": data.timestamp,
        "usage": data.usage,
        "deviceId": data.deviceId
    })
    return TelemetryOut(id=entry.id, timestamp=entry.timestamp, usage=entry.usage, deviceId=entry.deviceId)

@router.get("/{device_id}", response_model=List[TelemetryOut], summary="Get telemetry for a device", description="Get all telemetry records for a device you own.")
async def get_telemetry(device_id: int, user=Depends(get_current_user)):
    device = await db.device.find_unique(where={"id": device_id})
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    if device.userId != user.id:
        raise HTTPException(status_code=403, detail="Not your device")
    entries = await db.telemetry.find_many(where={"deviceId": device_id})
    return [TelemetryOut(id=e.id, timestamp=e.timestamp, usage=e.usage, deviceId=e.deviceId) for e in entries]

@router.get("/", response_model=List[TelemetryOut], summary="Get all telemetry for user", description="Get all telemetry records for all devices you own.")
async def get_all_telemetry(user=Depends(get_current_user)):
    devices = await db.device.find_many(where={"userId": user.id})
    device_ids = [d.id for d in devices]
    if not device_ids:
        return []
    entries = await db.telemetry.find_many(where={"deviceId": {"in": device_ids}})
    return [TelemetryOut(id=e.id, timestamp=e.timestamp, usage=e.usage, deviceId=e.deviceId) for e in entries]
