# F1-Stats — TODO

## 100 Days of Code Challenge

Start: 2026-05-16

### Tydzień 1 (Dzień 3-9): Roadmap + dokończenie testów

- [x] Dzień 3 (pon 18.05): Aktualizacja TODO.md + sekcja Roadmap w README + LeetCode
- [x] Dzień 4 (wt 19.05): Test happy path fetch_session_results + LeetCode
- [x] Dzień 5 (śr 20.05): Test get_races_and_sprints (POMIJAM testy 404/502/503 — duplikat) + LeetCode
- [x] Dzień 6 (czw 21.05): Test get_driver_standings (3 focused + cache hit) + LeetCode #345
- [x] Dzień 7 (pt 22.05): Refactor — fixtures do conftest.py + LeetCode
- [x] Dzień 8 (sob 23.05): Docker teoria + learning_notes.md + LeetCode
- [x] Dzień 9 (niedz 24.05, LEKKO): Update README test count + przegląd tygodnia

-----

### Tydzień 2 (Dzień 10-16): Docker + CI/CD

- [x] Dzień 10 (pon 25.05): Dockerfile + split requirements prod/dev + .dockerignore + LeetCode
- [x] Dzień 11 (wt 26.05): docker build lokalnie + docker run (Swagger UI w kontenerze) + LeetCode #334
- [x] Dzień 12 (śr 27.05): docker-compose.yml (dev: volumes + –reload) + LeetCode #443
- [x] Dzień 13 (czw 28.05): GitHub Actions CI workflow (pytest, on: push) + LeetCode
- [x] Dzień 14 (pt 29.05):
  - [x] CI badge w README
  - [x] Sekcja Docker w README (jak uruchomić lokalnie, jak przez docker-compose)
  - [x] Naprawa `race_keys[-1]` bug w `get_constructor_standings` (identyczna jak w get_driver_standings)
  - [x] Uproszczenie asercji w testach 422 (status_code zamiast pełnego JSON)
  - [x] Przemyślenie `CURRENT_YEAR` — przenieść do `services.py` lub `config.py`?
  - [x] LeetCode
- [x] Dzień 15 (sob 30.05):
  - [x] Lintery (ruff) + mypy w CI
  - [x] Testy dla `get_constructor_standings` (wzorzec znasz z get_driver_standings)
  - [x] LeetCode
- [x] Dzień 16 (niedz 31.05, LEKKO):
  - [x] Refleksja tygodnia + learning_notes.md (Tydzień 2 kondensaty)
  - [x] Update README — licznik testów

-----

### Tydzień 3 (Dzień 17-23): PostgreSQL — nauka + integracja

- [x] Dzień 17 (pon 01.06, odrobiony wt 02.06):
  - [x] SQL podstawy (SELECT/WHERE/JOIN/normalizacja) + notatki
- [x] Dzień 18 (wt 02.06, BEZ CZASU):
  - [x] Wszystkie zadania przesunięte na czw-sob
- [x] Dzień 19 (śr 03.06):
  - [x] Wszystkie zadania przesunięte na czw-sob
- [ ] Dzień 20 (czw 04.06, 5h):
  - [ ] Walidacja `year` w endpointach `/results/{year}/{country}/` i `/drivers/` — 2023 <= year <= CURRENT_YEAR, poza → 422
  - [ ] PostgreSQL w docker-compose 
  - [ ] Połączenie app z PostgreSQL 
  - [ ] SQLAlchemy teoria (engine/session/ORM)
  - [ ] LeetCode 1 zadanie
- [ ] Dzień 21 (pt 05.06, 5h):
  - [ ] Bugfix `asyncio.sleep(2)` w `fetch_session_with_semaphore` 
  - [ ] Pierwszy model ORM (tabela `standings`)
  - [ ] Start: zapis standings do Postgres 
  - [ ] LeetCode 1 zadanie
- [ ] Dzień 22 (sob 06.06, 5h):
  - [ ] Zapis standings do PostgreSQL zamiast cache plikowego JSON 
  - [ ] Alembic — teoria
  - [ ] Testy dla `get_races_and_sprints` edge case: rok bez sprintów (np. 2019) → sprint_keys = [] 
  - [ ] LeetCode 1 zadanie
- [ ] Dzień 23 (niedz 07.06, LEKKO):
  - [ ] Refleksja + learning_notes.md update
  - [ ] Bufor na rzeczy które się rozjechały z czw-sob
-----

### Tydzień 4 (Dzień 24-30): PostgreSQL koniec + WOW feature (porównywarka kierowców)

- [ ] Dzień 24 (pon 08.06):
  - [ ] Odczyt standings z DB w endpointach
  - [ ] Testy integracyjne dla nowych endpointów (TestClient)
  - [ ] LeetCode
- [ ] Dzień 25 (wt 09.06):
  - [ ] Usunięcie starego cache plikowego + sprzątanie
  - [ ] Upewnij się że wszystkie testy nadal zielone po usunięciu cache
  - [ ] LeetCode
- [ ] Dzień 26 (śr 10.06):
  - [ ] Design `/compare/` endpoint — Pydantic schema (co przyjmuje, co zwraca)
  - [ ] Narysuj na kartce: jak porównujesz dwóch kierowców? Jakie dane? Jakie metryki?
  - [ ] LeetCode
- [ ] Dzień 27 (czw 11.06):
  - [ ] Implementacja logiki porównywarki w `services.py`
  - [ ] LeetCode
- [ ] Dzień 28 (pt 12.06):
  - [ ] Testy porównywarki + przypadki brzegowe (kierowca nie istnieje, różne sezony)
  - [ ] LeetCode
- [ ] Dzień 29 (sob 13.06):
  - [ ] Porównywarka w README + update Roadmap
  - [ ] LeetCode
- [ ] Dzień 30 (niedz 14.06, LEKKO):
  - [ ] Mid-Fazy 1 review — gotowość vs plan (cel: ~73%)
  - [ ] Refleksja + learning_notes.md

-----

### Tydzień 5 (Dzień 31-37): Production patterns

- [ ] Dzień 31 (pon 15.06):
  - [ ] Dependency Injection (Depends) w FastAPI
  - [ ] Refactor `get_driver_standings` i `get_constructor_standings` — DRY violation (50% kodu identyczne między tymi funkcjami, wyciągnąć wspólną logikę)
  - [ ] LeetCode
- [ ] Dzień 32 (wt 16.06):
  - [ ] Strukturalne logowanie (structlog lub logging z JSON)
  - [ ] LeetCode
- [ ] Dzień 33 (śr 17.06):
  - [ ] Middleware (request ID + timing)
  - [ ] LeetCode
- [ ] Dzień 34 (czw 18.06):
  - [ ] Error handling middleware + własne wyjątki
  - [ ] Refactor obsługi błędów w `_fetch_openf1` — ujednolicić komunikaty
  - [ ] LeetCode
- [ ] Dzień 35 (pt 19.06):
  - [ ] Env vars (pydantic-settings) + .env.example
  - [ ] `CACHE_DIR`, `CACHE_TTL_SECONDS` → przenieść do settings (pydantic-settings)
  - [ ] LeetCode
- [ ] Dzień 36 (sob 20.06):
  - [ ] Redis teoria + serwis w docker-compose
  - [ ] LeetCode
- [ ] Dzień 37 (niedz 21.06, LEKKO):
  - [ ] Refleksja + learning_notes.md

-----

### Tydzień 6 (Dzień 38-44): Redis + polish + interview prep

- [ ] Dzień 38 (pon 22.06):
  - [ ] Redis jako warstwa cache (zastąpić cache plikowy)
  - [ ] LeetCode
- [ ] Dzień 39 (wt 23.06):
  - [ ] Rate limiting (slowapi) + CORS
  - [ ] LeetCode
- [ ] Dzień 40 (śr 24.06):
  - [ ] Paginacja + filtrowanie `/drivers/`
  - [ ] LeetCode
- [ ] Dzień 41 (czw 25.06):
  - [ ] Integration testy (TestClient) — pełny coverage
  - [ ] Coverage badge w README
  - [ ] LeetCode
- [ ] Dzień 42 (pt 26.06):
  - [ ] Finalny przegląd README + Roadmap
  - [ ] LeetCode
- [ ] Dzień 43 (sob 27.06):
  - [ ] Interview prep — historia “tell me about F1-Stats” (5 min opowieść)
  - [ ] Powtórka: Python async, pytest mockowanie, Docker, SQL
- [ ] Dzień 44 (niedz 28.06):
  - [ ] Przegląd 6 tyg, GitHub before/after, intensyfikacja aplikacji
  - [ ] Post na LinkedIn o F1-Stats
  - [ ] Cel: ~80% gotowości ✅ TARGET

-----

### Znane bugi / tech debt do zaadresowania

- [ ] `race_keys[-1]` w `get_constructor_standings` — IndexError gdy pusty sezon (analogiczny fix jak w `get_driver_standings`)
- [ ] `asyncio.sleep(2)` PRZED requestem w `fetch_session_with_semaphore` — spowalnia niepotrzebnie, powinno być PO lub usunięte
- [ ] DRY violation: `get_driver_standings` i `get_constructor_standings` mają ~50% identycznego kodu (race_keys, sprint_keys, semaphore, gather, calculate_points, combined) — wyciągnąć do wspólnej funkcji pomocniczej
- [ ] `CURRENT_YEAR` w `main.py` importowany przez testy — przenieść do `services.py` lub `config.py`
- [ ] Brak testów dla `get_constructor_standings`
- [ ] Brak testów edge case dla roku bez sprintów (sprint_keys = [])

-----

### Tydzień 7-8: JWT Auth

- [ ] User model + rejestracja/login
- [ ] JWT tokeny + protected endpointy
- [ ] Testy autoryzacji

### Tydzień 9-10: Frontend basics

- [ ] Vue lub React tutorial
- [ ] Prosty frontend konsumujący F1-Stats API
- [ ] Deploy frontendu

### Tydzień 11-13: Drugi projekt LUB pogłębienie F1-Stats

- [ ] Decyzja: nowy mniejszy projekt czy F1-Stats v4
- [ ] Realizacja wybranego kierunku
- [ ] Deploy + dokumentacja + pin na GitHub

### Tydzień 14: Interview prep intensywny

- [ ] Mock interview (Pramp)
- [ ] Powtórka: Python, OOP, async, SQL, system design
- [ ] Dopracowanie historii projektowych
- [ ] Dzień 99: Refleksja — przegląd learning_notes.md
- [ ] Dzień 100: GitHub “after” vs “before”, podsumowanie, post LinkedIn/blog
