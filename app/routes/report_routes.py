from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.models.report_model import Report
import shutil
from fastapi import Form


router = APIRouter()


VALID_STATUS = [
    "aberta",
    "em análise",
    "em andamento",
    "resolvida"
]


@router.post("/reports")
def create_report(
    title: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    image: UploadFile = File(None)
):

    db: Session = SessionLocal()

    image_path = None

    if image:

        image_path = f"uploads/{image.filename}"

        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

    new_report = Report(
        title=title,
        description=description,
        category=category,
        latitude=latitude,
        longitude=longitude,
        image_path=image_path
    )

    db.add(new_report)

    db.commit()

    db.refresh(new_report)

    return {
        "message": "Denúncia criada com sucesso",
        "report_id": new_report.id,
        "image_path": image_path
    }

@router.get("/reports")
def get_reports():

    db: Session = SessionLocal()

    reports = db.query(Report).all()

    return reports


@router.get("/reports/{report_id}")
def get_report(report_id: int):

    db: Session = SessionLocal()

    report = db.query(Report).filter(
        Report.id == report_id
    ).first()

    if not report:
        return {"error": "Denúncia não encontrada"}

    return report


@router.put("/reports/{report_id}")
def update_report_status(
    report_id: int,
    new_status: str
):

    if new_status not in VALID_STATUS:

        return {
            "error": "Status inválido",
            "valid_status": VALID_STATUS
        }

    db: Session = SessionLocal()

    report = db.query(Report).filter(
        Report.id == report_id
    ).first()

    if not report:
        return {"error": "Denúncia não encontrada"}

    report.status = new_status

    db.commit()

    db.refresh(report)

    return {
        "message": "Status atualizado",
        "new_status": report.status
    }