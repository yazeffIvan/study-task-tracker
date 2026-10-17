import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db import Base, get_db
from src.main import app


@pytest.fixture
def client(tmp_path):
    """Тестовый клиент с изолированной БД."""
    db_path = tmp_path / "test.db"
    test_engine = create_engine(
        f"sqlite:///{db_path}", connect_args={"check_same_thread": False}
    )
    TestSession = sessionmaker(bind=test_engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def test_courses_page_opens(client):
    response = client.get("/courses")
    assert response.status_code == 200
    assert "Курсы" in response.text


def test_create_course_success(client):
    response = client.post(
        "/courses", data={"title": "Математический анализ"}, follow_redirects=False
    )
    assert response.status_code == 303

    response = client.get("/courses")
    assert "Математический анализ" in response.text


def test_create_course_empty_title_shows_error(client):
    response = client.post("/courses", data={"title": "   "})
    assert response.status_code == 400
    assert "Название обязательно" in response.text


def test_create_course_missing_title_shows_error(client):
    response = client.post("/courses", data={"title": ""})
    assert response.status_code == 400
    assert "Название обязательно" in response.text

def test_courses_page_shows_empty_state(client):
    response = client.get("/courses")
    assert response.status_code == 200
    assert "Курсов пока нет" in response.text
    assert "Создайте первый курс" in response.text


def test_courses_page_shows_task_count_column(client):
    client.post("/courses", data={"title": "История"})
    response = client.get("/courses")
    assert "Заданий" in response.text
    assert "История" in response.text

