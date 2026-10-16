from pathlib import Path

from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.db import Base, engine, get_db
from src.models import Course

BASE_DIR = Path(__file__).resolve().parent

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Трекер учебных задач")

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/health")
def health() -> dict[str, str]:
    """Проверка работоспособности сервиса."""
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    """Главная страница."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"title": "Трекер учебных задач"},
    )


@app.get("/courses", response_class=HTMLResponse)
def list_courses(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    """Страница со списком курсов и формой создания."""
    courses = db.query(Course).order_by(Course.created_at.desc()).all()
    return templates.TemplateResponse(
        request=request,
        name="courses.html",
        context={"title": "Курсы", "courses": courses, "error": None},
    )


@app.post("/courses")
def create_course(
    request: Request,
    title: str = Form(...),
    db: Session = Depends(get_db),
):
    """Создание курса. При пустом названии возвращается форма с ошибкой."""
    if not title.strip():
        courses = db.query(Course).order_by(Course.created_at.desc()).all()
        return templates.TemplateResponse(
            request=request,
            name="courses.html",
            context={
                "title": "Курсы",
                "courses": courses,
                "error": "Название обязательно",
            },
            status_code=400,
        )

    course = Course(title=title.strip())
    db.add(course)
    db.commit()
    return RedirectResponse(url="/courses", status_code=303)
