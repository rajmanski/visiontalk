# Plan wykonania projektu VisionTalk

## Wstęp

Projekt **VisionTalk** – generator opisów obrazów – ma być aplikacją webową skonteneryzowaną, wykorzystującą gotowy model ML `nlpconnect/vit-gpt2-image-captioning` (HuggingFace). Aplikacja wspiera osoby niedowidzące poprzez generowanie tekstowych opisów obrazów oraz syntezę mowy (TTS).

Projekt realizowany jest przez 3 osoby: **s28496**, **s27507**, **s26746**.

---

## Technologie

| Warstwa | Technologia | Uzasadnienie |
|---------|-------------|--------------|
| Język | Python 3.9+ | Wymagany w projekcie, łatwa integracja ML |
| Model ML | Transformers (HuggingFace) + PyTorch | Obsługa gotowego modelu ViT-GPT2 |
| Backend | FastAPI | Lekki, szybki, idealny do API obsługującego pliki |
| Frontend | Streamlit | Zgodnie z propozycją, szybkie UI z `st.camera_input`, `st.audio` |
| Preprocessing obrazów | Pillow | Standardowa obróbka obrazów przed modelem |
| TTS (mowa) | gTTS | Proste generowanie plików MP3 z tekstu angielskiego |
| Konteneryzacja | Docker + Docker Compose | Spełnia wymóg przenoszalności i dwóch kontenerów (BE + FE). `docker compose up` uruchamia całość |
| Jakość kodu | pylint, pytest, black | Spełnienie wymogu ≥ 8 pkt w pylint i czystego kodu (PEP8) |
| Kontrola wersji | Git + GitHub | Wymagane w kryteriach |

---

## Co to jest `venv` i dlaczego go używamy?

`venv` to **wirtualne środowisko Pythona** — czyli osobny, prywatny „pokój” na Twoim komputerze, w którym instalujesz tylko te biblioteki, które są potrzebne do tego projektu. Nie dotykasz przy tym reszty systemu.

### Dlaczego to ważne?
- Osoba 1 potrzebuje bibliotek do modelu ML (np. `torch`, `transformers`).
- Osoba 2 potrzebuje `fastapi`, `uvicorn`.
- Osoba 3 potrzebuje `streamlit`.

Jeśli wszyscy zainstalują wszystko na „pańskim” (systemowym) Pythonie, mogą sobie nawzajem psuć ustawienia. `venv` rozwiązuje ten problem — każdy ma swoje własne pudełko.

### Jak to wygląda w praktyce (dla każdej osoby osobno)?

1. **Tworzysz wirtualne środowisko** (raz na projekt):
   ```bash
   python -m venv venv
   ```
   Powstanie folder `venv/` w katalogu projektu.

2. **Aktywujesz** (musisz to robić za każdym razem, gdy otwierasz nowe okno terminala):
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

3. **Instalujesz biblioteki** z listy, którą przygotuje Osoba 3 w pliku `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

4. **Pracujesz i testujesz** w tym środowisku.

### A co z Dockerem?
Kontenery Dockera **nie potrzebują** `venv`, ponieważ sam kontener jest już izolowany. W kontenerze instalujesz biblioteki bezpośrednio przez `pip install` w `Dockerfile`. Plik `requirements.txt` jest wtedy używany przez Dockera jako „lista zakupów” do zbudowania obrazu.

---

## Struktura projektu

```
visiontalk/
├── README.md                 # Opis, instrukcja uruchomienia, format danych
├── docker-compose.yml        # Orchestracja BE + FE
├── requirements.txt          # Wspólne zależności (lub requirements.yaml)
├── .github/
│   └── workflows/            # (opcjonalnie) CI do pylint/pytest
├── data/
│   ├── __init__.py
│   ├── loader.py             # Ładowanie i walidacja obrazów
│   ├── preprocessor.py       # Resize, normalizacja, konwersja do tensorów
│   └── test_images/          # Katalog z obrazkami do weryfikacji modelu
├── model/
│   ├── __init__.py
│   ├── captioner.py          # Wrapper na ViT-GPT2 (load, predict)
│   └── evaluator.py          # Ewaluacja skuteczności na /test_images
├── app/
│   ├── backend/
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── main.py           # FastAPI: endpointy /predict, /tts, /health
│   │   └── api/
│   │       └── v1/
│   │           └── endpoints.py
│   └── frontend/
│       ├── Dockerfile
│       ├── requirements.txt
│       └── streamlit_app.py  # UI: upload, kamera, duża czcionka, audio
└── tests/
    ├── test_data.py
    ├── test_model.py
    └── test_api.py
```

---

## Etapy realizacji

### Etap 1: Infrastruktura i setup (Tydzień 1)

1. Utworzenie repozytorium na GitHub, dodanie kolaboratorów.
2. Ustalenie struktury katalogów (`data/`, `model/`, `app/`, `tests/`).
3. Przygotowanie wstępnych `Dockerfile` (BE i FE) oraz `docker-compose.yml`.
4. Szkielet `README.md` z opisem projektu i wstępną instrukcją uruchomienia.

### Etap 2: Moduł `data` (Tydzień 1–2)

1. Zebranie / wygenerowanie katalogu `/test_images` (różne kategorie obiektów).
2. Implementacja `loader.py` (walidacja formatów, obsługa błędnych plików).
3. Implementacja `preprocessor.py` (zmiana rozmiaru, normalizacja, konwersja do formatu wymaganego przez ViT).
4. Testy jednostkowe (`pytest`) dla modułu `data`.

### Etap 3: Moduł `model` (Tydzień 2)

1. Integracja modelu `nlpconnect/vit-gpt2-image-captioning` z HuggingFace.
2. Stworzenie klasy w `captioner.py` z metodami: `load()`, `predict(image)`, `generate_caption()`.
3. Implementacja `evaluator.py` – przetestowanie modelu na katalogu `/test_images` i zapisanie przykładowych wyników.
4. Pylint modułów `data` i `model` (cel: ≥ 8 pkt).

### Etap 4: Backend (`app/backend`) (Tydzień 2–3)

1. Stworzenie aplikacji FastAPI (`main.py`).
2. Endpoint `/predict`: przyjmuje obraz (multipart/form-data), zwraca wygenerowany opis tekstowy.
3. Integracja z modułem `model` (backend importuje i używa klasy z `model/captioner.py`).
4. Endpoint `/tts`: przyjmuje tekst, zwraca plik audio MP3 (np. za pomocą `gTTS`).
5. Endpoint `/health` do sprawdzania statusu.
6. Dockerfile dla backendu + testy API (`pytest`).

### Etap 5: Frontend (`app/frontend`) (Tydzień 3)

1. Aplikacja Streamlit (`streamlit_app.py`).
2. Upload obrazu (`st.file_uploader`) oraz obsługa kamery (`st.camera_input`).
3. Komunikacja z backendem (HTTP POST do `/predict` i `/tts`).
4. Wyświetlenie wyniku w **dużej czcionce** z **wysokim kontrastem** (dostosowanie CSS Streamlit lub użycie `st.markdown` z inline styles).
5. Odtwarzanie wygenerowanego audio (`st.audio`).
6. Responsywność – Streamlit domyślnie jest responsywny, ale wymaga przetestowania na telefonie.
7. Dockerfile dla frontendu.

### Etap 6: Integracja i przenoszalność (Tydzień 3–4)

1. Połączenie kontenerów przez `docker-compose.yml` (networking BE ↔ FE).
2. Upewnienie się, że **całość uruchamia się jednym poleceniem** (`docker compose up --build`) bez ręcznej konfiguracji OS.
3. Automatyczne pobieranie modelu przy pierwszym starcie (np. w entrypoint lub `Dockerfile`).
4. Uruchomienie `pylint` na całym projekcie i poprawki do osiągnięcia ≥ 8 pkt.
5. Testy end-to-end (upload obrazu → opis → audio).

### Etap 7: Dokumentacja i prezentacja (Tydzień 4)

1. Finalizacja `README.md`: szczegółowy opis, wymagania (`requirements.txt`), instrukcja `docker compose up`, format danych wejściowych (JPEG/PNG, max rozmiar), opis endpointów API.
2. Dopracowanie docstringów i komentarzy w kodzie.
3. Przygotowanie prezentacji (10 min + 5 min na pytania) – opis aplikacji, architektury, demo.

---

## Podział pracy na 3 osoby

### Osoba 1: Data & ML Engineer (s28496)

**Cel**: Przygotować moduły `data/` i `model/`, dane testowe i ewaluację.

| # | Task | Szczegóły / Kroki do wykonania |
|---|------|--------------------------------|
| 1.1 | **Setup venv i repozytorium** | Sklonować repo; otworzyć terminal w katalogu projektu; wpisać `python -m venv venv`; aktywować środowisko (`venv\Scripts\activate` na Windows); zainstalować zależności z `requirements.txt` (`pip install -r requirements.txt`) zawierające `torch`, `transformers`, `Pillow`, `pytest`; uruchomić `python -c "import transformers"` aby sprawdzić, czy działa. |
| 1.2 | **Zbudowanie struktury katalogów** | Utworzyć foldery: `data/`, `data/test_images/`, `model/`, `tests/`; w każdym utworzyć pusty plik `__init__.py` (wymagane, żeby Python widział te foldery jako moduły). |
| 1.3 | **Moduł `data/loader.py`** | Napisać funkcję `load_image(path)` która: otwiera obraz za pomocą `Pillow.Image.open`, sprawdza czy format to JPEG lub PNG, jeśli nie – rzuca wyjątek `ValueError`. Napisać funkcję `validate_image(image)` która sprawdza czy obraz nie jest uszkodzony (np. próba `.verify()` lub `.convert("RGB")`). |
| 1.4 | **Moduł `data/preprocessor.py`** | Napisać funkcję `preprocess(image)` która: zmienia rozmiar obrazu na 224x224 (lub inny wymagany przez ViT), normalizuje piksele do zakresu [0,1], konwertuje obraz do tensora PyTorch o wymiarach (1, 3, 224, 224) (batch, kanały, wysokość, szerokość). |
| 1.5 | **Katalog `data/test_images/`** | Znaleźć lub przygotować 10–15 różnorodnych obrazków (np. zdjęcia: kota, psa, krajobrazu, ulicy, jedzenia, człowieka); zapisać je w tym folderze jako `.jpg` lub `.png`; dodać do repozytorium (`git add data/test_images/`). |
| 1.6 | **Moduł `model/captioner.py`** | Stworzyć klasę `ImageCaptioner`: metoda `__init__(self)` ustawia `self.model = None`; metoda `load(self)` ładuje model i tokenizer z HuggingFace (`pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")`); metoda `predict(self, image)` przyjmuje obraz PIL, wywołuje pipeline i zwraca string z opisem. |
| 1.7 | **Moduł `model/evaluator.py`** | Napisać skrypt `evaluate.py` który: iteruje po plikach w `data/test_images/`, dla każdego wywołuje `ImageCaptioner.predict()`, zapisuje wyniki do pliku `results.json` (lista słowników: `{"image": "kot.jpg", "caption": "a cat sitting on a couch"}`). |
| 1.8 | **Testy jednostkowe** | W `tests/test_data.py` napisać testy: czy `load_image` poprawnie ładuje obraz, czy rzuca błąd dla złego formatu, czy `preprocess` zwraca tensor o dobrym kształcie. W `tests/test_model.py` napisać test: czy `ImageCaptioner` poprawnie generuje tekst dla testowego obrazka. Uruchomić `pytest tests/`. |
| 1.9 | **Jakość kodu** | W terminalu (z aktywnym venv) wpisać `pylint data/ model/ tests/`. Jeśli wynik < 8.0 – poprawić błędy: dodać docstringi do funkcji, skrócić za długie linie (< 79 znaków), usunąć nieużywane importy, zmienić nazwy zmiennych na opisowe (np. `img` → `input_image`). |

---

### Osoba 2: Backend Engineer (s27507)

**Cel**: Zbudować backend FastAPI jako osobny kontener, udostępniający API do predykcji i TTS.

| # | Task | Szczegóły / Kroki do wykonania |
|---|------|--------------------------------|
| 2.1 | **Setup venv i repozytorium** | Sklonować repo; otworzyć terminal; `python -m venv venv`; aktywować (`venv\Scripts\activate`); zainstalować zależności: `pip install fastapi uvicorn gTTS pytest`; uruchomić `python -c "import fastapi"` aby potwierdzić instalację. |
| 2.2 | **Struktura `app/backend/`** | Utworzyć foldery: `app/backend/`, `app/backend/api/v1/`; w każdym dodać `__init__.py`; utworzyć plik `app/backend/main.py`. |
| 2.3 | **Endpoint `/health`** | W `main.py` utworzyć aplikację FastAPI (`app = FastAPI()`); dodać dekorator `@app.get("/health")`; funkcja zwraca `{"status": "ok"}`. Uruchomić lokalnie: `uvicorn main:app --reload`; wejść w przeglądarkę na `http://localhost:8000/health` i sprawdzić czy widzi JSON. |
| 2.4 | **Endpoint `/predict`** | Dodać endpoint `@app.post("/predict")` przyjmujący plik (`file: UploadFile = File(...)`); w funkcji: przeczytać plik, przekonwertować na obraz PIL (`Image.open(BytesIO(...))`), wywołać klasę `ImageCaptioner` (z modułu `model/`) aby uzyskać opis, zwrócić JSON `{"caption": "..."}`. Dodać obsługę błędów (np. zły format pliku → 400 Bad Request). |
| 2.5 | **Endpoint `/tts`** | Dodać endpoint `@app.post("/tts")` przyjmujący tekst (`text: str = Form(...)`); w funkcji: wygenerować plik MP3 za pomocą `gTTS(text=text, lang='en')`, zapisać tymczasowo (np. w `/tmp/` lub `tempfile`), zwrócić plik jako `FileResponse` (lub jego zawartość binarną). |
| 2.6 | **Integracja z modelem** | W `main.py` (lub osobnym module) zaimportować `ImageCaptioner` z `model.captioner`; utworzyć instancję globalną przy starcie aplikacji (`captioner = ImageCaptioner(); captioner.load()`), aby model nie ładował się przy każdym zapytaniu. |
| 2.7 | **Dockerfile dla BE** | Utworzyć plik `app/backend/Dockerfile` z zawartością: obraz bazowy `FROM python:3.9-slim`, skopiować `requirements.txt`, zainstalować zależności (`pip install -r requirements.txt`), skopiować cały kod, wystawić port `EXPOSE 8000`, komenda startowa `CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]`. |
| 2.8 | **Testy API** | W `tests/test_api.py` użyć `from fastapi.testclient import TestClient`; napisać testy: `test_health` (sprawdza `/health`), `test_predict` (wysyła prawdziwy obraz testowy i sprawdza czy odpowiedź zawiera pole `caption`), `test_tts` (wysyła tekst i sprawdza czy odpowiedź ma nagłówek `audio/mpeg`). Uruchomić `pytest tests/test_api.py`. |
| 2.9 | **Jakość kodu** | W terminalu (venv aktywny): `pylint app/backend/ tests/test_api.py`. Jeśli wynik < 8.0 – poprawić błędy: dodać docstringi do endpointów, typy parametrów funkcji, skrócić linie, usunąć zbędne importy. |

---

### Osoba 3: Frontend Engineer & DevOps (s26746)

**Cel**: Zbudować frontend Streamlit, skonfigurować Docker Compose i napisać dokumentację.

| # | Task | Szczegóły / Kroki do wykonania |
|---|------|--------------------------------|
| 3.1 | **Setup venv i repozytorium** | Sklonować repo; terminal w katalogu projektu; `python -m venv venv`; aktywować; `pip install streamlit requests pytest`; sprawdzić: `streamlit hello` (otwiera przeglądarkę z demo). |
| 3.2 | **Struktura `app/frontend/`** | Utworzyć folder `app/frontend/`; wewnątrz plik `streamlit_app.py`. |
| 3.3 | **UI – Upload obrazu** | W `streamlit_app.py`: `import streamlit as st`; dodać `st.title("VisionTalk")`; dodać `uploaded_file = st.file_uploader("Wybierz obraz...", type=["jpg", "jpeg", "png"])`; sprawdzić czy plik nie jest `None`; wyświetlić podgląd: `st.image(uploaded_file, caption="Przesłany obraz")`. |
| 3.4 | **UI – Kamera** | Poniżej uploadu dodać: `camera_image = st.camera_input("Zrób zdjęcie")`; jeśli użytkownik zrobi zdjęcie, traktować `camera_image` tak samo jak `uploaded_file` (przesłać do backendu). |
| 3.5 | **UI – Dostępność** | Użyć `st.markdown()` z HTML/CSS, aby ustawić dużą czcionkę dla wyników: np. `st.markdown("<h1 style='font-size: 3em;'>{{ caption }}</h1>", unsafe_allow_html=True)`. Ustawić ciemne tło i jasny tekst przez `st.set_page_config(page_title="VisionTalk", layout="centered", initial_sidebar_state="collapsed")`. |
| 3.6 | **Komunikacja z BE** | Napisać funkcję `send_to_backend(image_bytes)` która: używa `requests.post("http://backend:8000/predict", files={"file": image_bytes})`, odbiera JSON, zwraca `caption`. Przycisk `st.button("Generuj opis")` wywołuje tę funkcję i wyświetla wynik. |
| 3.7 | **UI – Audio / TTS** | Pod wyświetlonym opisem dodać przycisk `st.button("Odczytaj na głos")`; funkcja `get_tts_audio(caption)` wysyła POST na `http://backend:8000/tts` z danymi `{"text": caption}`; odbiera plik audio; wyświetla przez `st.audio(audio_bytes, format="audio/mp3")`. |
| 3.8 | **Dockerfile dla FE** | Utworzyć `app/frontend/Dockerfile`: `FROM python:3.9-slim`, skopiować `requirements.txt`, `pip install -r requirements.txt`, skopiować `streamlit_app.py`, `EXPOSE 8501`, `CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]`. |
| 3.9 | **Docker Compose** | Utworzyć plik `docker-compose.yml` w katalogu głównym z dwoma usługami: `backend` (build: `app/backend/`, ports: `8000:8000`) i `frontend` (build: `app/frontend/`, ports: `8501:8501`, `depends_on: backend`). Uruchomić: `docker compose up --build` i sprawdzić czy oba kontenery startują bez błędów. |
| 3.10 | **README.md** | W katalogu głównym utworzyć `README.md` zawierający: nagłówek `# VisionTalk`, opis czego dotyczy aplikacja, listę technologii, instrukcję uruchomienia (`docker compose up --build`), format danych wejściowych (JPEG/PNG, max 5MB), opis endpointów API, link do modelu HuggingFace, wymagania systemowe (Docker, Docker Compose). |
| 3.11 | **Jakość kodu i prezentacja** | Uruchomić `pylint app/frontend/`; poprawić błędy do osiągnięcia ≥ 8 pkt. Przygotować 5–7 slajdów w PowerPoint/Google Slides: tytuł, problem (osoby niedowidzące), rozwiązanie (architektura), demo (zrzuty ekranu), podsumowanie. |

---

## Podsumowanie dopasowania do kryteriów zaliczeniowych

| Kryterium (PDF) | Jak jest spełnione |
|-----------------|--------------------|
| Rozdzielenie `data \| model \| app` | Osobne katalogi i moduły |
| Modularność | Funkcje, klasy, oddzielne pliki/katalogi |
| Przenoszalność | Docker Compose, GitHub, `docker compose up` |
| Dokumentacja | README.md, docstringi, komentarze |
| Czysty kod (PEP8, pylint ≥ 8) | pylint + black + nazewnictwo |
| Automatyczna instalacja | `requirements.txt` + Docker |
| Forma: web/API | FastAPI (API) + Streamlit (web) |
| Jakość modelu ML | Użycie sprawdzonego modelu HF + ewaluacja na `/test_images` |

---

*Plan sporządzony na podstawie kryteriów zaliczeniowych oraz propozycji projektu VisionTalk.*
