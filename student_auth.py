from fastapi import APIRouter, HTTPException, Depends
from models import StudentRegister, StudentLogin
from database import student_collection
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

router = APIRouter(prefix="/auth", tags=["Authentication"])

SECRET_KEY = "mysecretkey123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/register")
def register_student(student: StudentRegister):
    existing = student_collection.find_one({"email": student.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = pwd_context.hash(student.password)
    student_dict = {
        "name": student.name,
        "email": student.email,
        "password": hashed_password,
    }
    student_collection.insert_one(student_dict)
    return {"message": "Student registered successfully"}


@router.post("/login")
def login_student(student: StudentLogin):
    existing = student_collection.find_one({"email": student.email})
    if not existing:
        raise HTTPException(status_code=404, detail="Student not found")

    if not pwd_context.verify(student.password, existing["password"]):
        raise HTTPException(status_code=401, detail="Invalid password")

    token = create_access_token({"sub": existing["email"]})
    return {"access_token": token, "token_type": "bearer"}




