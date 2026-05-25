# Uzycie oficjalnego obrazu Pythona jako bazowego
FROM python:3.13.2-slim

# Ustawienie katalogu roboczego w kontenerze
WORKDIR /app

# Kopiowanie pliku requirements.txt do katalogu roboczego zgodnie z zasadą warstwowania Dockerfile
COPY requirements.txt .

# Instalacja zależności z pliku requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Kopiowanie reszty plików aplikacji do katalogu roboczego
COPY . .

# Eksponowanie portu, na którym będzie działać aplikacja
EXPOSE 8000

# Uruchomienie aplikacji FastAPI przez Uvicorn (przy docker run, nie przy build)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
