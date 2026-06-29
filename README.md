# F1-Stats

Backend REST API zwracający aktualne klasyfikacje, wyniki wyścigów i informacje o kierowcach Formuły 1. Asynchroniczne pobieranie danych z OpenF1 API, cache w PostgreSQL, walidacja Pydantic oraz 40 testów (37 jednostkowych + 3 integracyjne).

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.136-009688?logo=fastapi&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-2.13-E92063?logo=pydantic&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql&logoColor=white)
![Pytest](https://img.shields.io/badge/Tests-40%20passed-brightgreen?logo=pytest&logoColor=white)
![CI](https://github.com/Maksymilian03/F1-Stats/actions/workflows/ci.yml/badge.svg)
![Ruff](https://img.shields.io/badge/Linting-ruff-261230?logo=ruff)
![Mypy](https://img.shields.io/badge/Type%20check-mypy-2A6DB2)

## Live Demo

API dostępne pod: [https://f1-stats-g283.onrender.com](https://f1-stats-g283.onrender.com)

Interaktywna dokumentacja (Swagger UI): [https://f1-stats-g283.onrender.com/docs](https://f1-stats-g283.onrender.com/docs)

> Aplikacja jest hostowana na darmowym planie Render — pierwsze wywołanie po dłuższej bezczynności może trwać ~30-50 sekund (cold start).

![Swagger UI](docs/screenshots/swagger-ui.png)

## Roadmap

### Zrobione
- Asynchroniczne REST API integrujące się z OpenF1 API
- Równoległe zapytania (asyncio.gather) z limitowaniem
- Walidacja danych przez Pydantic
- Cache w PostgreSQL z 3-poziomową logiką świeżości (no data / historical / current z TTL)
- 37 testów jednostkowych + 3 testy integracyjne (TestClient + PostgreSQL w Dockerze)
- Mockowanie async (AsyncMock, side_effect, patch)
- Podział na warstwy (main / schemas / services / database)
- Konteneryzacja aplikacji (Docker + docker-compose)
- CI/CD (GitHub Actions — pytest, ruff, mypy)
- Migracja z file-based cache do PostgreSQL
- SQLAlchemy 2.0 z Mapped typed annotations

### W trakcie
- Porównywarka kierowców (endpoint /compare/)
- Refactor wspólnej logiki get_driver_standings i get_constructor_standings (DRY)

### Planowane
- Redis — warstwa cache nad PostgreSQL
- Alembic migrations zamiast create_all
- Strukturalne logowanie (structlog)
- Middleware (request ID + timing)
- Rate limiting (slowapi)
- Paginacja + filtrowanie /drivers/
- Model użytkowników z rejestracją i logowaniem
- Autoryzacja JWT
- Prosty frontend konsumujący API

## Technologie

- Python 3.13
- FastAPI 0.136
- Pydantic 2.13
- SQLAlchemy 2.0 (async, Mapped)
- PostgreSQL 16
- httpx 0.28 (async)
- pytest 9.0, pytest-asyncio 1.3
- uvicorn 0.46
- OpenF1 API (zewnętrzne źródło danych)
- Render (deploy, Frankfurt EU)
- Docker + docker-compose (konteneryzacja)
- GitHub Actions (CI/CD)

## Funkcjonalności

- Asynchroniczne równoległe pobieranie ~25 sesji z OpenF1
- Cache w PostgreSQL z 3-poziomową logiką świeżości
- Rate limiting (Semaphore + sleep)
- Obsługa błędów HTTP (404 / 502 / 503) z fail-soft na pojedynczych rekordach
- Walidacja parametrów (Pydantic + Path z ge/le)
- 40 testów (pytest fixtures w conftest.py, AsyncMock, side_effect, TestClient dla integration)
- Clean architecture (separacja services/routers/schemas/database)

## Instalacja

```bash
git clone https://github.com/Maksymilian03/F1-Stats
cd F1-Stats
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
pip install -r requirements.txt
```

Wymagana baza PostgreSQL. Najprostszy setup przez Docker:

```bash
docker compose up
```

Aplikacja będzie dostępna pod `http://localhost:8000`. Dokumentacja Swagger pod `http://localhost:8000/docs`.

## Docker

Aplikację można uruchomić w kontenerze Docker. Dostępne są dwa tryby:

### Tryb produkcyjny (Dockerfile)

```bash
docker build -t f1stats:latest .
docker run -p 8000:8000 f1stats:latest
```

Image bazuje na `python:3.13.2-slim`. Aplikacja uruchamiana przez `uvicorn` bez `--reload`.

### Tryb deweloperski (docker-compose)

```bash
docker compose up
```

Konfiguracja deweloperska z `volumes` (bind mount), `--reload` i PostgreSQL — zmiany w kodzie są od razu widoczne w kontenerze bez ponownego buildu.

Aplikacja będzie dostępna pod `http://localhost:8000`.

## Endpointy API

| Metoda | Endpoint | Opis |
|--------|----------|------|
| GET | / | Root endpoint |
| GET | /drivers/ | Lista aktualnych kierowców F1 |
| GET | /results/{year}/{country}/ | Wyniki konkretnego wyścigu |
| GET | /standings/{year}/ | Klasyfikacja kierowców |
| GET | /standings/constructors/{year}/ | Klasyfikacja konstruktorów |

Parametr `year` przyjmuje wartości od 2023 do bieżącego roku.

### Przykład odpowiedzi: GET /standings/2024/

```json
[
  {
    "position": 1,
    "full_name": "Max VERSTAPPEN",
    "team": "Red Bull Racing",
    "points": 434,
    "wins": 9,
    "driver_number": 1
  },
  {
    "position": 2,
    "full_name": "Lando NORRIS",
    "team": "McLaren",
    "points": 368,
    "wins": 4,
    "driver_number": 4
  }
]
```

## Architektura

Aplikacja jest podzielona na warstwy:

- `main.py` — Routery FastAPI + walidacja parametrów (Path)
- `services.py` — Logika biznesowa, integracja z OpenF1, cache
- `schemas.py` — Modele Pydantic (response_model)
- `database.py` — SQLAlchemy async session, engine, get_db
- `models.py` — Modele ORM (DriverStanding, ConstructorStanding)
- `tests/` — 40 testów:
  - logika obliczeń: calculate_points, aggregate_points_by_team, leaderboard, merge_driver_details
  - integracja z OpenF1 (mock async): fetch_drivers, fetch_session_results, get_races_and_sprints
  - endpoint orchestracji: get_driver_standings (happy path + cache hit + cache miss)
  - integration tests dla get_driver_standings z PostgreSQL w Dockerze
  - `conftest.py` — fixtures z danymi testowymi i session DB

### Flow danych — przykład GET /standings/2024/

1. Endpoint w `main.py` waliduje parametr `year` (Path z `ge=2023, le=CURRENT_YEAR`)
2. FastAPI wstrzykuje async session przez `Depends(get_db)`
3. Service `get_driver_standings(2024)` sprawdza świeżość danych w PostgreSQL (3 przypadki: brak danych / historyczny rok / bieżący rok z TTL)
4. Cache hit: jedno SELECT, zwrot do klienta (~10 ms)
5. Cache miss: funkcja pobiera listę sesji (~25: race + sprint) z OpenF1
6. Równolegle (`asyncio.gather`) pobiera wyniki każdej sesji z rate limitingiem (`Semaphore(1)` + sleep)
7. Agregacja punktów per kierowca (czyste funkcje, łatwe do testowania)
8. Merge z danymi kierowców (full_name, team_name)
9. Sortowanie + dodanie pozycji (`leaderboard()` z tie-breakerem po wins)
10. Zapis do PostgreSQL + Pydantic validation (`response_model=List[StandingsEntry]`)
11. Zwrot do klienta w postaci JSON

## Uruchamianie testów

Testy jednostkowe (bez bazy):

```bash
pytest tests/unit/ -v
```

Testy integracyjne (wymagają PostgreSQL w Dockerze):

```bash
docker compose up -d
pytest tests/integration/ -v
```

Wszystkie testy:

```bash
docker compose up -d
pytest -v
```
