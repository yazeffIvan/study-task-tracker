import random

from locust import HttpUser, between, task


class TrackerUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        """При старте создаем тестовый курс для пользователя."""
        self.client.post("/courses", data={"title": "Нагрузочный тест"})

    @task(3)
    def view_courses(self):
        """Пользователь просматривает список курсов (часто)."""
        self.client.get("/courses")

    @task(2)
    def view_course_detail(self):
        """Пользователь открывает конкретный курс."""
        course_id = random.randint(1, 3)
        self.client.get(f"/courses/{course_id}")

    @task(1)
    def view_dashboard(self):
        """Пользователь смотрит главную страницу с дедлайнами."""
        self.client.get("/")
