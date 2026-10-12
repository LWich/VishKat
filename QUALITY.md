# Отчёт о качестве

Проект прошёл расширенный аудит после реализации функциональных требований.

## Итоговые метрики

| Проверка | Результат |
|---|---|
| Unit/API/CLI-тесты | 21 passed |
| Branch coverage | 98,70% (порог 80%) |
| Mutation testing | 276/289 killed — 95,50% |
| Ruff, включая security rules | ошибок нет |
| Bandit (`app`, medium/high) | уязвимостей не найдено |
| mypy strict | ошибок нет |
| BasedPyright | 0 errors, 0 warnings |
| Vulture, confidence ≥80% | мёртвого кода не найдено |
| Pylint duplicate-code, 6+ строк | дублирования не найдено |
| Radon CC ≥ C (11+) | функций не найдено |
| Lizard CCN >15 | превышений нет; максимум 6 |
| Radon MI < B (65) | модулей не найдено |

## Что изменено после базового аудита

- Минимальное покрытие поднято с 60% до 80%.
- Добавлены тесты всех поддержанных типов транспорта и вещей, консольного сценария, OpenAPI-метаданных, граничных значений простоты и энергопотребления, доменных ошибок и запрета обхода техосмотра.
- Исключения получили единообразный суффикс `Error`.
- Подключены Ruff security rules, Bandit, BasedPyright, Vulture, Pylint, Radon, Lizard, Mutmut, Xenon и pre-commit.
- Целевая версия обновлена до Python 3.13+, зависимости зафиксированы в `uv.lock`.
- Добавлены локальные pre-commit-проверки и GitHub Actions workflow.

## Воспроизведение

```bash
uv sync --locked --dev
uv run ruff check .
uv run ruff format --check .
uv run mypy app tests
uv run basedpyright
uv run bandit -r app -ll
uv run vulture app tests --min-confidence 80
uv run radon cc app -n C -s
uv run lizard -l python -C 15 app
uv run pytest
uv run mutmut run
uv run mutmut results
```

Wily требует историю Git. В поставке есть готовые проверки и CI; после `git init` историю метрик можно включить командой `uv run wily build app`.
