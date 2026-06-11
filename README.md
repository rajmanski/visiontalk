# VisionTalk

VisionTalk to aplikacja webowa do generowania opisu obrazu i odczytu audio.
Backend FastAPI udostępnia API, a ten sam proces serwuje frontend z
`app/backend/static/`.

## Uruchomienie lokalne

Instalacja zależności:

```bash
uv pip install -r requirements.txt
```

Start aplikacji:

```bash
uv run uvicorn app.backend.main:app --reload
```

Aplikacja będzie dostępna pod adresem `http://127.0.0.1:8000/`.

## Docker

Start całego projektu:

```bash
docker compose up --build
```

Serwis wystawia port `8000`.

## Przepływ użycia

1. Otwórz stronę główną.
2. Wgraj obraz `jpg`, `jpeg` albo `png`.
3. Kliknij `Generuj opis`.
4. Po otrzymaniu wyniku kliknij `Odczytaj opis`, aby pobrać audio z `/tts`.

## API

- `GET /health` zwraca `{"status": "ok"}`.
- `POST /predict` przyjmuje `multipart/form-data` z polem `file`.
- `GET /tts?text=...` zwraca `audio/mpeg`.

## Podział odpowiedzialności

- `data/` i `model/`: ładowanie obrazów, preprocessing, model captioningu.
- `app/backend/main.py`: API FastAPI, routing i serwowanie statycznego UI.
- `app/backend/static/`: frontend HTML/CSS/JS.
- `docker-compose.yml` i `app/backend/Dockerfile`: uruchamianie kontenerowe.
