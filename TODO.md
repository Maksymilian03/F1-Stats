# F1-Stats — TODO

## 100 Days of Code Challenge

Start: 2026-05-16

### Tydzień 1 (Dzień 3-9): Roadmap + dokończenie testów

- [x] Dzień 3 (pon 18.05): Aktualizacja TODO.md + sekcja Roadmap w README + LeetCode
- [x] Dzień 4 (wt 19.05): Test happy path fetch_session_results + LeetCode
- [x] Dzień 5 (śr 20.05): "Test get_races_and_sprints (POMIJAM testy 404/502/503 fetch_session_results — duplikowałyby testy _fetch_openf1)" + LeetCode
- [x] Dzień 6 (czw 21.05): Test get_drivers_standings + LeetCode #345 Reverse Vowels 
- [x] Dzień 7 (pt 22.05): Refactor — fixtures do conftest.py + LeetCode
- [ ] Dzień 8 (sob 23.05): Docker teoria + notatki learning_notes.md + LeetCode
- [ ] Dzień 9 (niedz 24.05, LEKKO): Update README test count + przegląd tygodnia

### Tydzień 2 (Dzień 10-16): Docker + CI/CD

- [ ] Dzień 10 (pon 25.05): Dockerfile (zrozum każdą linię) + LeetCode
- [ ] Dzień 11 (wt 26.05): .dockerignore + build i uruchomienie lokalnie + LeetCode
- [ ] Dzień 12 (śr 27.05): docker-compose.yml (sam serwis app) + LeetCode
- [ ] Dzień 13 (czw 28.05): GitHub Actions — workflow pytest + LeetCode
- [ ] Dzień 14 (pt 29.05): CI badge + sekcja Docker w README + LeetCode
- [ ] Dzień 15 (sob 30.05): Lintery (ruff) + mypy w CI + LeetCode
- [ ] Dzień 16 (niedz 31.05, LEKKO): Refleksja tygodnia + learning_notes

### Tydzień 3 (Dzień 17-23): PostgreSQL — nauka + integracja

- [ ] Dzień 17 (pon 01.06): SQL podstawy (SELECT/WHERE/JOIN/normalizacja) + notatki + LeetCode
- [ ] Dzień 18 (wt 02.06): PostgreSQL w docker-compose + połączenie z app + LeetCode
- [ ] Dzień 19 (śr 03.06): SQLAlchemy teoria (engine/session/ORM) + notatki + LeetCode
- [ ] Dzień 20 (czw 04.06): Pierwszy model ORM (tabela standings) + LeetCode
- [ ] Dzień 21 (pt 05.06): Zapis standings do PostgreSQL zamiast JSON + LeetCode
- [ ] Dzień 22 (sob 06.06): Alembic — teoria + pierwsza migracja + LeetCode
- [ ] Dzień 23 (niedz 07.06, LEKKO): Refleksja + learning_notes

### Tydzień 4 (Dzień 24-30): PostgreSQL koniec + WOW feature (porównywarka kierowców)

- [ ] Dzień 24 (pon 08.06): Odczyt standings z DB w endpointach + testy + LeetCode
- [ ] Dzień 25 (wt 09.06): Usunięcie starego cache plikowego + sprzątanie + LeetCode
- [ ] Dzień 26 (śr 10.06): Design /compare/ endpoint + Pydantic schema + LeetCode
- [ ] Dzień 27 (czw 11.06): Implementacja logiki porównywarki + LeetCode
- [ ] Dzień 28 (pt 12.06): Testy porównywarki + przypadki brzegowe + LeetCode
- [ ] Dzień 29 (sob 13.06): Porównywarka w README + update Roadmap + LeetCode
- [ ] Dzień 30 (niedz 14.06, LEKKO): Refleksja + learning_notes

### Tydzień 5 (Dzień 31-37): Production patterns

- [ ] Dzień 31 (pon 15.06): Dependency Injection (Depends) + LeetCode
- [ ] Dzień 32 (wt 16.06): Strukturalne logowanie + LeetCode
- [ ] Dzień 33 (śr 17.06): Middleware (request ID + timing) + LeetCode
- [ ] Dzień 34 (czw 18.06): Error handling middleware + własne wyjątki + LeetCode
- [ ] Dzień 35 (pt 19.06): Env vars (pydantic-settings) + .env.example + LeetCode
- [ ] Dzień 36 (sob 20.06): Redis teoria + serwis w docker-compose + LeetCode
- [ ] Dzień 37 (niedz 21.06, LEKKO): Refleksja + learning_notes

### Tydzień 6 (Dzień 38-44): Redis + polish + interview prep

- [ ] Dzień 38 (pon 22.06): Redis jako warstwa cache + LeetCode
- [ ] Dzień 39 (wt 23.06): Rate limiting (slowapi) + CORS + LeetCode
- [ ] Dzień 40 (śr 24.06): Paginacja + filtrowanie /drivers/ + LeetCode
- [ ] Dzień 41 (czw 25.06): Integration testy (TestClient) + coverage badge + LeetCode
- [ ] Dzień 42 (pt 26.06): Finalny przegląd README + Roadmap + LeetCode
- [ ] Dzień 43 (sob 27.06): Interview prep — historia "tell me about F1-Stats" + powtórka
- [ ] Dzień 44 (niedz 28.06): Przegląd 6 tyg, GitHub before/after, intensyfikacja aplikacji

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
