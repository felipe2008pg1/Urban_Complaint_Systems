from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.models.user_model import User
from passlib.context import CryptContext

router = APIRouter()

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

@router.post("/register")
def register(
    username: str,
    email: str,
    password: str
):

    db: Session = SessionLocal()

    existing_user = db.query(User).filter(
        User.email == email
    ).first()

    if existing_user:
        return {"error": "Email já cadastrado"}

    hashed_password = pwd_context.hash(password)

    new_user = User(
        username=username,
        email=email,
        password=hashed_password
    )

    db.add(new_user)

    db.commit()

    return {
        "message": "Usuário criado com sucesso"
    }