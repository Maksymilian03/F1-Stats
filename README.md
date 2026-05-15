# F1-Stats 
Backend REST API zwracający aktualne klasyfikacje, wyniki wyścigów i informacje o kierowcach Formuły 1. Asynchroniczne pobieranie danych z OpenF1 API, cache'owanie, walidacja Pydantic oraz 23 testy jednostkowe z mockowaniem httpx.

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.136-009688?logo=fastapi&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-2.13-E92063?logo=pydantic&logoColor=white)
![Pytest](https://img.shields.io/badge/Tests-23%20passed-brightgreen?logo=pytest&logoColor=white)

## 🔗 Live Demo

**API dostępne pod:** [https://f1-stats-g283.onrender.com](https://f1-stats-g283.onrender.com)

**Interaktywna dokumentacja (Swagger UI):** [https://f1-stats-g283.onrender.com/docs](https://f1-stats-g283.onrender.com/docs)

> Aplikacja jest hostowana na darmowym planie Render — pierwsze wywołanie po dłuższej bezczynności może trwać ~30-50 sekund (cold start).

![Swagger UI](docs/screenshots/swagger-ui.png)

## Features

- **Asynchroniczność** — równoległe pobieranie ~25 sesji z OpenF1
- **Cache file-based** — pierwszy request ładuje sezon, kolejne natychmiastowe
- **Rate limiting** — Semaphore + sleep
- **Robust error handling** — 3-warstwowa obsługa błędów httpx (404 / 502 / 503)
- **Walidacja parametrów** — Pydantic + Path(ge/le)
- **23 testy jednostkowe** — z mockowaniem httpx
- **Clean architecture** — separacja services/routers/schemas


## Tech Stack

**Backend:** Python 3.13, FastAPI 0.136, Pydantic 2.13
**HTTP Client:** httpx 0.28 (async)
**Testing:** pytest 9.0, pytest-asyncio 1.3
**Server:** uvicorn 0.46
**External API:** OpenF1
**Deploy:** Render (Frankfurt EU)


## API Endpoints

| Metoda | Endpoint | Opis |
|--------|----------|------|
| GET | `/` | Root endpoint |
| GET | `/drivers/` | Lista aktualnych kierowców F1 |
| GET | `/results/{year}/{country}/` | Wyniki konkretnego wyścigu |
| GET | `/standings/{year}/` | Klasyfikacja kierowców |
| GET | `/standings/constructors/{year}/` | Klasyfikacja konstruktorów |

Parametr `year` przyjmuje wartości **2023-2025**.

### Przykład odpowiedzi: `GET /standings/2024/`

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

> Pełna interaktywna dokumentacja: [Swagger UI](https://f1-stats-g283.onrender.com/docs)


## Architecture

Aplikacja jest podzielona na trzy warstwy:

​```text
F1-Stats/
├── main.py                  # Routery FastAPI + walidacja parametrów (Path)
├── services.py              # Logika biznesowa, integracja z OpenF1, cache
├── schemas.py               # Modele Pydantic (response_model)
├── requirements.txt
├── cache/                   # File-based cache (gitignored)
└── tests/                   # 23 testy jednostkowe
    ├── __init__.py
    ├── test_calculate_points.py
    ├── test_aggregate_points_by_team.py
    ├── test_leaderboard.py
    ├── test_merge_driver_details.py
    └── test_fetch_drivers.py
​```

### Flow danych — przykład `GET /standings/2024/`

1. **Endpoint w `main.py`** waliduje parametr `year` (Path z `ge=2023, le=2025`)
2. **Service `get_standings(2024)`** sprawdza cache — jeśli istnieje i nie wygasł, zwraca natychmiast
3. **Cache miss:** funkcja pobiera listę sesji (~25: race + sprint) z OpenF1
4. **Równolegle (`asyncio.gather`)** pobiera wyniki każdej sesji — z **rate limitingiem** (`Semaphore(2)` + sleep)
5. **Agregacja punktów** per kierowca (czyste funkcje, łatwe do testowania)
6. **Merge** z danymi kierowców (full_name, team_name)
7. **Sortowanie** + dodanie pozycji (`leaderboard()` z tie-breakerem po wins)
8. **Cache save** + Pydantic validation (`response_model=List[StandingsEntry]`)
9. **Zwrot do klienta** w postaci JSON