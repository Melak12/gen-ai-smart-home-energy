from fastapi import APIRouter, HTTPException, Depends, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from prisma import Prisma
from pydantic import BaseModel
from typing import Optional, List
from utils.auth import verify_password, get_password_hash, create_access_token, decode_access_token

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

db = Prisma()

class UserCreate(BaseModel):
    email: str
    password: str
    role: Optional[str] = "user"

class UserOut(BaseModel):
    id: int
    email: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    user = await db.user.find_unique(where={"email": payload["sub"]})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

async def get_current_admin(user=Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return user

@router.on_event("startup")
async def startup():
    await db.connect()

@router.on_event("shutdown")
async def shutdown():
    await db.disconnect()

@router.post("/register", response_model=UserOut)
async def register(user: UserCreate):
    existing = await db.user.find_unique(where={"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = get_password_hash(user.password)
    db_user = await db.user.create({"email": user.email, "password": hashed, "role": user.role})
    return UserOut(id=db_user.id, email=db_user.email, role=db_user.role)

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await db.user.find_unique(where={"email": form_data.username})
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    token = create_access_token({"sub": user.email, "role": user.role})
    return Token(access_token=token)

@router.get("/me", response_model=UserOut)
async def me(user=Depends(get_current_user)):
    return UserOut(id=user.id, email=user.email, role=user.role)

@router.get("/roles", response_model=List[UserOut])
async def list_users(user=Depends(get_current_admin)):
    users = await db.user.find_many()
    return [UserOut(id=u.id, email=u.email, role=u.role) for u in users]

@router.patch("/roles/{user_id}", response_model=UserOut)
async def update_role(user_id: int, role: str, admin=Depends(get_current_admin)):
    user = await db.user.update(where={"id": user_id}, data={"role": role})
    return UserOut(id=user.id, email=user.email, role=user.role)
