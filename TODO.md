# F1-Stats — TODO

Projekt zacząłem 16.05.2026 jako 100 Days of Code Challenge.
Doszedłem do Dnia 30, potem zrobiłem chwile przerwy żeby przygotować się do rozmowy rekrutacyjnej. 100 dni już nie wyjdzie, ale projekt robię dalej.

Wracam do pracy nad projektem 29.06.2026.

---

## Co już zrobione

### Tydzień 1 (18-24.05)
- [x] Pierwsze testy do `fetch_session_results` i `get_races_and_sprints`
- [x] Testy do `get_driver_standings` (3 testy + cache hit)
- [x] Refactor — fixtures do `conftest.py`
- [x] Aktualizacja README z sekcją Roadmap
- [x] LeetCode codziennie

### Tydzień 2 (25-31.05)
- [x] Dockerfile + .dockerignore + split requirements prod/dev
- [x] docker-compose.yml z volumes i --reload dla dev
- [x] GitHub Actions CI — pytest, ruff, mypy
- [x] Bug fix `race_keys[-1]` IndexError w `get_driver_standings` i `get_constructor_standings`
- [x] Refactor `CURRENT_YEAR = datetime.now().year` zamiast hardcoded `le=2025`
- [x] CI badge w README

### Tydzień 3 (01-07.06)
- [x] Nauka SQL — SELECT, WHERE, JOIN, normalizacja
- [x] PostgreSQL w docker-compose + połączenie z aplikacją
- [x] SQLAlchemy teoria — engine, session, ORM
- [x] Pierwszy model ORM (tabela standings)
- [x] Zapis standings do PostgreSQL zamiast pliku JSON
- [x] Alembic teoria + pierwsza migracja

### Tydzień 4 (08-14.06)
- [x] Odczyt standings z DB w endpointach
- [x] Usunięcie starego cache plikowego
- [x] Zadanie rekrutacyjne MindPal — Solar Calculator (osobne repo, submitted 13.06)
- [x] Mid-fazy review

### Tydzień 5 — zaczęty (15-21.06)
- [x] 3 testy integracyjne dla `get_driver_standings` z TestClient
- [x] Wstęp do porównywarki — schema Pydantic i `calculate_comparison` (gołe szkice)
- [ ] Reszta tygodnia — nie zrobione, bo zacząłem przygotowania do rozmowy

### Tydzień 6 — pominięty (22-28.06)
Cały tydzień poszedł na przygotowania do rozmowy rekrutacyjnej. Bez commitów w F1-Stats.

---

## Do zrobienia teraz — porównywarka kierowców

Wracam do tego co zostało z Tygodnia 5.

### Tydzień 5 (29.06 – 05.07)

- [x] 29.06 (pon): Logika `calculate_comparison` + `load_comparison_data_from_db` + `get_comparison_drivers` skomitowana
- [ ] 30.06 (wt): Cache miss path w `get_comparison_drivers`
- [ ] 01.07 (śr): Walidacja `driver_number` w Path + endpoint w `main.py`
- [ ] 02.07 (czw): Testy do `calculate_comparison` z parametrize
- [ ] 03.07 (pt): Test integracyjny endpointu `/compare/`
- [ ] 04.07 (sob): Update README — dokumentacja `/compare/`
- [ ] 05.07 (niedz, LEKKO): Refleksja tygodnia + learning_notes.md

---

## Do zrobienia potem — to co miało być w Tygodniu 6

### Tydzień 6 (06-12.07)

- [ ] 06.07 (pon): Refactor DRY — wspólna funkcja dla `get_driver_standings` i `get_constructor_standings`
- [ ] 07.07 (wt): Strukturalne logowanie (structlog)
- [ ] 08.07 (śr): Middleware — request ID + timing
- [ ] 09.07 (czw): Error handling middleware + custom exceptions
- [ ] 10.07 (pt): Env vars — `pydantic-settings` + `.env.example`
- [ ] 11.07 (sob): Redis w docker-compose + warstwa cache
- [ ] 12.07 (niedz, LEKKO): Refleksja

### Tydzień 7 (13-19.07)

- [ ] Rate limiting (slowapi)
- [ ] CORS middleware
- [ ] Paginacja + filtrowanie dla `/drivers/`
- [ ] Coverage badge w README
- [ ] Finalny przegląd README + Roadmap

---

## Pomysły na później (bez deadline'u)

### Quality
- [ ] Property-based testing (Hypothesis) dla `calculate_comparison`
- [ ] Branch coverage zamiast line coverage w CI
- [ ] Alembic migrations zamiast `create_all` w lifespan
- [ ] Profile slow tests — `pytest --durations=10`

### Features
- [ ] JWT auth + user model + protected endpointy
- [ ] Endpoint `/teams/compare` — porównywanie konstruktorów
- [ ] Endpoint `/season/{year}/highlights` — najciekawsze statystyki sezonu
- [ ] Webhook dla powiadomień o nowym wyścigu

### Frontend (oddzielny projekt)
- [ ] Vue lub React tutorial
- [ ] Prosty frontend konsumujący F1-Stats API
- [ ] Deploy frontendu

### DevOps
- [ ] Multi-stage Dockerfile (mniejszy image)
- [ ] GitHub Actions matrix — testy na Python 3.11 i 3.12
- [ ] Deploy automation — fly.io lub Railway

### Observability
- [ ] OpenTelemetry tracing
- [ ] Prometheus metrics endpoint
- [ ] Sentry error reporting

---

## Tech debt — znane problemy

- [ ] DRY violation: `get_driver_standings` i `get_constructor_standings`. Plan: 06.07.
- [ ] Brak Alembic migrations w produkcji — używam `create_all` w lifespan. Plan: backlog.
- [ ] Brak testu edge case: rok bez sprintów. Plan: 02.07.
- [ ] `leader` jako Union[DriverStandingInfo, Literal["draw"]] — refactor gdy będzie więcej consumers.
- [ ] `asyncio.sleep(2)` w `fetch_session_with_semaphore` — zostaje, świadoma decyzja.
