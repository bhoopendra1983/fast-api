from fastapi import FastAPI
from routes import student_auth

app = FastAPI(title="Student Auth System")

app.include_router(student_auth.router)

@app.get("/")
def home():
    return {"message": "Welcome to Student Auth API"}
