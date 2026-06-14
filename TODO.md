# F1-Stats — TODO

## 100 Days of Code Challenge

Start: 2026-05-16

---

### Tydzień 1 (Dzień 3-9): Roadmap + dokończenie testów

- [x] Dzień 3 (pon 18.05): Aktualizacja TODO.md + sekcja Roadmap w README + LeetCode
- [x] Dzień 4 (wt 19.05): Test happy path fetch_session_results + LeetCode
- [x] Dzień 5 (śr 20.05): Test get_races_and_sprints + LeetCode
- [x] Dzień 6 (czw 21.05): Test get_driver_standings (3 focused + cache hit) + LeetCode #345
- [x] Dzień 7 (pt 22.05): Refactor — fixtures do conftest.py + LeetCode
- [x] Dzień 8 (sob 23.05): Docker teoria + learning_notes.md + LeetCode
- [x] Dzień 9 (niedz 24.05, LEKKO): Update README test count + przegląd tygodnia

---

### Tydzień 2 (Dzień 10-16): Docker + CI/CD

- [x] Dzień 10 (pon 25.05): Dockerfile + split requirements prod/dev + .dockerignore + LeetCode
- [x] Dzień 11 (wt 26.05): docker build lokalnie + docker run + LeetCode #334
- [x] Dzień 12 (śr 27.05): docker-compose.yml (dev: volumes + --reload) + LeetCode #443
- [x] Dzień 13 (czw 28.05): GitHub Actions CI workflow (pytest, on: push) + LeetCode
- [x] Dzień 14 (pt 29.05): Bug fix race_keys[-1] w get_driver_standings + test edge case + CI badge w README
- [x] Dzień 15 (sob 30.05): Bug fix race_keys[-1] w get_constructor_standings + 6 testów + CURRENT_YEAR → services.py + ruff + mypy w CI
- [x] Dzień 16 (niedz 31.05, LEKKO): Refleksja tygodnia + learning_notes.md

---

### Tydzień 3 (Dzień 17-23): PostgreSQL — nauka + integracja

- [x] Dzień 17 (pon 01.06): SQL podstawy (SELECT/WHERE/JOIN/normalizacja) + notatki
- [x] Dzień 18 (wt 02.06): PostgreSQL w docker-compose + połączenie z app
- [x] Dzień 19 (śr 03.06): SQLAlchemy teoria (engine/session/ORM) + notatki
- [x] Dzień 20 (czw 04.06): Pierwszy model ORM (tabela standings)
- [x] Dzień 21 (pt 05.06): Zapis standings do PostgreSQL zamiast JSON
- [x] Dzień 22 (sob 06.06): Alembic — teoria + pierwsza migracja
- [x] Dzień 23 (niedz 07.06, LEKKO): Refleksja + learning_notes.md

---

### Tydzień 4 (Dzień 24-30): Zadanie rekrutacyjne

- [x] Dzień 24 (pon 08.06): Odczyt standings z DB w endpointach
- [x] Dzień 25 (wt 09.06): Usunięcie starego cache plikowego + weryfikacja testów
- [x] Dzień 26 (śr 10.06): Zadanie rekrutacyjne — analiza i pierwsza wersja
- [x] Dzień 27 (czw 11.06): Zadanie rekrutacyjne — refactor na streaming + multi-search
- [x] Dzień 28 (pt 12.06): Zadanie rekrutacyjne — testowanie i optymalizacja
- [x] Dzień 29 (sob 13.06): Zadanie rekrutacyjne — finalna wersja + wysłanie
- [x] Dzień 30 (niedz 14.06, LEKKO): Mid-Fazy 1 review — gotowość vs plan

---

### Tydzień 5 (Dzień 31-37): WOW feature (porównywarka kierowców) + testy integracyjne

- [ ] Dzień 31 (pon 15.06):
  - [ ] Testy integracyjne dla endpointów ze standings z DB (TestClient)
  - [ ] LeetCode
- [ ] Dzień 32 (wt 16.06):
  - [ ] Design `/compare/` endpoint — Pydantic schema (input/output)
  - [ ] Szkic porównania kierowców — metryki i dane
  - [ ] LeetCode
- [ ] Dzień 33 (śr 17.06):
  - [ ] Implementacja logiki porównywarki w `services.py`
  - [ ] LeetCode
- [ ] Dzień 34 (czw 18.06):
  - [ ] Testy porównywarki + przypadki brzegowe (kierowca nie istnieje, różne sezony)
  - [ ] LeetCode
- [ ] Dzień 35 (pt 19.06):
  - [ ] Porównywarka w README + update Roadmap
  - [ ] LeetCode
- [ ] Dzień 36 (sob 20.06):
  - [ ] Dependency Injection (Depends) w FastAPI
  - [ ] Refactor get_driver_standings i get_constructor_standings — wspólna funkcja pomocnicza
  - [ ] LeetCode
- [ ] Dzień 37 (niedz 21.06, LEKKO):
  - [ ] Refleksja + learning_notes.md

---

### Tydzień 6 (Dzień 38-44): Production patterns + Redis + interview prep

- [ ] Dzień 38 (pon 22.06):
  - [ ] Strukturalne logowanie (structlog lub logging z JSON)
  - [ ] LeetCode
- [ ] Dzień 39 (wt 23.06):
  - [ ] Middleware (request ID + timing)
  - [ ] Error handling middleware + własne wyjątki
  - [ ] LeetCode
- [ ] Dzień 40 (śr 24.06):
  - [ ] Env vars (pydantic-settings) + .env.example
  - [ ] CACHE_DIR i CACHE_TTL_SECONDS → settings
  - [ ] LeetCode
- [ ] Dzień 41 (czw 25.06):
  - [ ] Redis w docker-compose + warstwa cache
  - [ ] Rate limiting (slowapi) + CORS
  - [ ] LeetCode
- [ ] Dzień 42 (pt 26.06):
  - [ ] Paginacja + filtrowanie `/drivers/`
  - [ ] Coverage badge w README
  - [ ] LeetCode
- [ ] Dzień 43 (sob 27.06):
  - [ ] Finalny przegląd README + Roadmap
  - [ ] Interview prep — historia "tell me about F1-Stats" (5 min)
  - [ ] Powtórka: Python async, pytest mockowanie, Docker, SQL
- [ ] Dzień 44 (niedz 28.06):
  - [ ] Przegląd 6 tyg, GitHub before/after, intensyfikacja aplikacji
  - [ ] Post na LinkedIn o F1-Stats
  - [ ] Cel: ~80% gotowości ✅ TARGET

---

### Znane bugi / tech debt do zaadresowania

- [ ] DRY violation: `get_driver_standings` i `get_constructor_standings` — wyciągnąć wspólną funkcję pomocniczą (Dzień 36)
- [ ] Brak testów edge case dla roku bez sprintów (sprint_keys = [])

---

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
- [ ] Dzień 100: GitHub "after" vs "before", podsumowanie, post LinkedIn/blog
