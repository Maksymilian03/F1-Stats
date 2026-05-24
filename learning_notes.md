# Learning Notes — F1-Stats journey

Notatki z nauki podczas 100 Days of Code Challenge.
Start: 16.05.2026

---

## Tydzień 1 (Dni 3-9, 18.05-24.05) — Testowanie + Roadmap

### Kod (F1-Stats)
- 4 testy z mockowaniem async dla `get_drivers_standings`:
  - Happy path rozbity na 3 focused testy (returns_correct_position, 
    calculates_total_points_correctly, does_not_count_sprint_wins_as_total_wins)
  - Cache hit test z tmp_path + pathlib
- Wyciągnięcie 6 fixtures do `tests/conftest.py` (fake_drivers, fake_race_keys,
  fake_sprint_keys, fake_races_results, fake_sprints_results, fake_cached_data)
- Refactor naming: `semphore` → `semaphore`, `get_standings` → `get_drivers_standings`
- Roadmap w README (sekcja Zrobione/W trakcie/Planowane)
- Odkrycie buga `race_keys[-1]` (IndexError dla pustego sezonu) przez testowanie 
  — do naprawy w Tygodniu 5 jako edge case test po dodaniu walidacji

### LeetCode (6 zadań)
- #1 Two Sum (hash map O(n))
- #1071 Greatest Common Divisor of Strings
- #1431 Kids With Greatest Number of Candies (O(n²) → O(n))
- #605 Can Place Flowers (refactor 25 linii → 10 linii z paddingiem)
- #345 Reverse Vowels (Easy, two pointers + set lookup — Beats 93% po refactorze z 53%)
- #151 Reverse Words in a String (Medium, two pointers → one-liner reversed(s.split()))

### Pojęcia poznane / utrwalone
- **pytest fixtures + conftest.py** — auto-discovery, fixture parametry w sygnaturze
- **monkeypatch.setattr** dla stałych modułu (`services.CACHE_DIR`)
- **tmp_path + pathlib** — `(tmp_path / 'plik.json').write_text(json.dumps(data))`
- **side_effect = list1 + list2** dla wielu wywołań różnych grup mocka
- **mock.assert_not_called()** vs `assert not mock.called` — opisowy traceback
- **Mock nie waliduje typów** — sprawdź podpis ORYGINALNEJ funkcji (dict vs list)
- **Eksperyment kontrolny** — po napisaniu testu zepsuj kluczową rzecz, sprawdź że pęka
- **Python: `x in collection`** złożoność: list/str O(n), set/dict O(1)
- **`{}` to pusty dict, NIE pusty set** — pusty set: `set()`
- **Two pointers pattern** — palce idą od końców do środka, O(n) czas O(1) extra space
- **Pythonic First zasada** — najpierw built-in (`reversed()`, `set()`, `sorted()`), 
  potem algorytm. LeetCode testuje TWOJE MYŚLENIE, nie algorytmy w izolacji.

### Docker fundamentals (Dz 8)
- **RUN vs CMD** — RUN przy `docker build` (raz), CMD przy `docker run` (każde uruchomienie)
- **Exec form `["cmd", "arg"]`** preferowane (sygnały, brak shell'a)
- **0.0.0.0 vs 127.0.0.1** — w Dockerze ZAWSZE 0.0.0.0 (inaczej port-mapping nie działa)
- **Image layers + cache** — kolejność: rzadko zmieniające → często zmieniające
  (COPY requirements.txt PRZED COPY .)
- **Image variants** — slim (Debian okrojony, 150MB), alpine (50MB, ale uwaga 
  na C-extensions z musl vs glibc)
- **Volumes (Docker zarządza, persystencja) vs bind mounts (user kontroluje, dev kod)**
- **EXPOSE** = dokumentacja, `-p host:container` faktycznie otwiera port
- **`docker run` / `docker exec -it ... bash` / `docker compose up`** — kiedy co

### Aplikacja ANSTA (sob 23.05)
- 3 zadania: generator kodów pocztowych, brakujące elementy 1-n, lista Decimal
- Lekcje: 
  - **Edge case `00-XXX`** w kodach pocztowych — `f"{i:05d}"` padding
  - **O(n²) → O(n)** przez set difference (zamiast list comp + `in`)
  - **Decimal od początku** — `Decimal("0.5")` ze stringa, nigdy `Decimal(0.5)` z floata
  - **`<` vs `<=`** złapane przez test "includes_start_and_end_values"
- 12 testów pytest jako "wbicie konkurencji w ziemię"
- Follow-up: sprawdzić odpowiedź do ~30.05

---

## Tydzień 2 — będzie wypełniony w toku