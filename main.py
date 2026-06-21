from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database.database import engine
from app.database.database import Base
from app.models.report_model import Report
from app.models.user_model import User
from app.routes.report_routes import router as report_router
from app.routes.auth_routes import router as auth_router
import os
from fastapi.middleware.cors import CORSMiddleware

print(os.path.abspath("database.db"))

Base.metadata.create_all(bind=engine)

print("TABLES CREATED")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)

app.include_router(report_router)
app.include_router(auth_router)

@app.get("/")
def home():
    return {"message": "Urban Reporting System Online"}
