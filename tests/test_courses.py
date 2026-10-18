
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
    assert "У вас пока нет курсов" in response.text
    assert "Создайте первый курс" in response.text


def test_courses_page_shows_task_count_column(client):
    client.post("/courses", data={"title": "История"})
    response = client.get("/courses")
    assert "заданий" in response.text
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

def test_course_detail_404_for_missing_course(client):
    """Открытие несуществующего курса даёт 404."""
    response = client.get("/courses/999")
    assert response.status_code == 404


def test_create_task_for_missing_course(client):
    """Попытка добавить задание в несуществующий курс даёт 404."""
    response = client.post(
        "/courses/999/tasks",
        data={"title": "Задание"},
    )
    assert response.status_code == 404


def test_create_task_empty_title_shows_error(client):
    """Пустое название задания возвращает ошибку."""
    client.post("/courses", data={"title": "Биология"})
    response = client.post(
        "/courses/1/tasks",
        data={"title": "   ", "deadline": ""},
    )
    assert response.status_code == 400
    assert "Название задания обязательно" in response.text


def test_create_task_with_invalid_deadline(client):
    """Некорректный формат дедлайна не падает, а сохраняется как None."""
    client.post("/courses", data={"title": "Химия"})
    response = client.post(
        "/courses/1/tasks",
        data={"title": "Опыт", "deadline": "not-a-date"},
        follow_redirects=False,
    )
    # Мы не блокируем сохранение при некорректной дате, но ValueError перехватывается.
    assert response.status_code == 303


def test_update_task_status(client):
    client.post("/courses", data={"title": "Тест"})
    client.post("/courses/1/tasks", data={"title": "Задача"})

    # Меняем статус на in_progress
    response = client.post("/tasks/1/status", data={"status": "in_progress"}, follow_redirects=False)
    assert response.status_code == 303

    response = client.get("/courses/1")
    assert 'value="in_progress" selected' in response.text


def test_update_task_status_invalid(client):
    client.post("/courses", data={"title": "Тест"})
    client.post("/courses/1/tasks", data={"title": "Задача"})

    # Недопустимый статус
    response = client.post("/tasks/1/status", data={"status": "invalid"})
    assert response.status_code == 400


def test_delete_task(client):
    client.post("/courses", data={"title": "Удаление"})
    client.post("/courses/1/tasks", data={"title": "Задача"})
    response = client.post("/tasks/1/delete", follow_redirects=False)
    assert response.status_code == 303
    assert "Задача" not in client.get("/courses/1").text

def test_delete_course(client):
    client.post("/courses", data={"title": "Удаление курса"})
    response = client.post("/courses/1/delete", follow_redirects=False)
    assert response.status_code == 303
    assert "Удаление курса" not in client.get("/courses").text

def test_edit_task_page(client):
    client.post("/courses", data={"title": "Редактирование"})
    client.post("/courses/1/tasks", data={"title": "Старое"})
    response = client.get("/tasks/1/edit")
    assert response.status_code == 200
    assert "Старое" in response.text

def test_edit_task_success(client):
    client.post("/courses", data={"title": "Редактирование"})
    client.post("/courses/1/tasks", data={"title": "Старое"})
    response = client.post("/tasks/1/edit", data={"title": "Новое", "deadline": ""}, follow_redirects=False)
    assert response.status_code == 303
    assert "Новое" in client.get("/courses/1").text
