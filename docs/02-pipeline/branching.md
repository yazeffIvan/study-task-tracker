# Стратегия ветвления

## Основные принципы

- Ветка `main` — стабильная, всегда рабочая.
- Прямые пуши в `main` запрещены.
- Любое изменение попадает в `main` только через pull request.
- Каждая ветка связана с задачей (issue).

## Именование веток

Формат:

    <type>/<issue-id>-<short-slug>

Типы:

| Тип | Назначение |
|---|---|
| feature | Новая функциональность |
| fix | Исправление ошибки |
| docs | Изменения только в документации |
| chore | Рутинные задачи, конфигурация |
| ci | Изменения в CI/CD |
| test | Тесты |

Примеры:

    feature/5-create-course
    ci/11-branching-and-protection
    docs/12-review-rules

## Жизненный цикл ветки

1. Взять issue из Бэклога, перевести в «Готово к работе».
2. Создать ветку от main:
   ```bash
   git checkout main
   git pull
   git checkout -b feature/5-create-course
3.Вести работу, коммитить по Conventional Commits.
4.Открыть pull request в main.
5.Пройти CI, получить ревью.
6.Смержить (squash merge).
7.Удалить ветку.