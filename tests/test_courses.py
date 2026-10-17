
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


def test_create_task_success(client):
    # Сначала создаем курс
    client.post("/courses", data={"title": "Физика"})
    # Получаем ID (предполагаем, что это 1 в изолированной БД)
    response = client.get("/courses")
    assert "Физика" in response.text

    # Создаем задание
    response = client.post(
        "/courses/1/tasks",
        data={"title": "Лабораторная 1", "deadline": "2026-12-31T23:59"},
        follow_redirects=False
    )
    assert response.status_code == 303

    # Проверяем, что оно появилось в списке
    response = client.get("/courses/1")
    assert "Лабораторная 1" in response.text
    assert "31.12.2026 23:59" in response.text
    assert "К выполнению" in response.text
