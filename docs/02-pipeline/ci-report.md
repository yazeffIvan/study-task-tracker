# Отчёт об оптимизации конвейера

## Цель

Зафиксировать состояние инженерного конвейера ЛР2: стратегию ветвления, защиту основной ветки, непрерывную интеграцию (CI), контейнеризацию. Описать проблемы, возникшие при настройке, и решения.

## Что настроено

### Стратегия ветвления

- Основная ветка `main` защищена.
- Прямые пуши в `main` запрещены.
- Каждое изменение проходит через отдельную ветку и pull request.
- Формат имени ветки: `<type>/<issue-id>-<slug>` (например, `feature/2-create-course`).
- Merge выполняется через **squash merge** — все коммиты ветки сжимаются в один.

### Защита ветки main

В настройках репозитория для `main` включены:

- Require a pull request before merging (Required approvals: 1).
- Require status checks to pass before merging (проверка `CI / build`).
- Require conversation resolution before merging.
- Allow force pushes — **выключено**.
- Allow deletions — **выключено**.

### CI (GitHub Actions)

Файл `.github/workflows/ci.yml` содержит один job `build`, который выполняется на каждый `push` в `main` и на каждый `pull_request`. Шаги:

1. Checkout репозитория.
2. Установка Python 3.11.
3. Установка зависимостей из `requirements-dev.txt`.
4. Линтер (`ruff check .`).
5. Тесты (`pytest -v`).

### Docker

- `Dockerfile` на базе `python:3.11-slim`.
- `docker-compose.yml` — запуск сервиса одной командой `docker compose up`.
- `.dockerignore` исключает из образа `.venv`, `__pycache__`, `.pytest_cache`, `.ruff_cache`, `.git`, `tests`, `docs`.

### Шаблон PR и CODEOWNERS

- `.github/pull_request_template.md` — единый шаблон для всех PR.
- `.github/CODEOWNERS` — назначает владельца репозитория ответственным за изменения.

## Проблемы и решения

### Python 3.14 несовместим с `pydantic-core`

**Проблема:** при локальной установке зависимостей на Python 3.14 `pydantic-core==2.23.4` собирался из исходников и падал с ошибкой компиляции. Готовой колёски под 3.14 ещё нет.

**Решение:** установлен Python 3.11 через Homebrew, виртуальное окружение пересоздано. Это соответствует ТЗ (Python 3.11+) и `ci.yml` (`python-version: "3.11"`).

### Pytest не находил пакет `src`

**Проблема:** тесты падали с `ModuleNotFoundError: No module named 'src'`, потому что pytest не знал, где искать пакет.

**Решение:** в `pyproject.toml` добавлена настройка:

```
[tool.pytest.ini_options]
pythonpath = ["."]
```

### GitHub отказывался пушить `ci.yml`

**Проблема:** Personal Access Token без scope `workflow` не позволял пушить изменения в `.github/workflows/ci.yml`.

**Решение:** в настройках токена добавлен scope `workflow`.

### Branch protection требовал approvals = 1

**Проблема:** для команды из одного человека требование «1 approving review» невыполнимо — нельзя одобрить собственный PR.

**Решение:** используем административный обход: ставим галочку **Merge without waiting for requirements to be met (bypass rules)**. Правило включено для документирования процесса, обход — исключение для соло-проекта.

### `.DS_Store` и `study_tracker.db` попадали в Git

**Проблема:** macOS создаёт `.DS_Store` в каждой папке, SQLite создаёт `study_tracker.db`. Оба файла не должны попадать в репозиторий.

**Решение:** добавлены в `.gitignore`:

```text
.DS_Store
study_tracker.db