# Komendy do testowania i sprawdzania — Osoba 1 (s28496)

## Przed każdym uruchomieniem (aktywacja venv)

Otwórz PowerShell/terminal w folderze `SUML` i wpisz:

```powershell
cd C:\Users\Lenovo\Desktop\SUML
venv\Scripts\activate
```

Jeśli widzisz `(venv)` na początku linii — środowisko jest aktywne.

---

## 1. Testy jednostkowe

### Wszystkie testy naraz

```powershell
pytest tests/ -v
```

### Tylko moduł `data`

```powershell
pytest tests/test_data.py -v
```

### Tylko moduł `model`

```powershell
pytest tests/test_model.py -v
```

---

## 2. Szybki test modelu na jednym obrazku

```powershell
python -c "from model.captioner import ImageCaptioner; from data.loader import load_image; cap = ImageCaptioner(); cap.load(); img = load_image('data/test_images/animal.jpg'); print('>>>', cap.predict(img))"
```

> **Uwaga:** Pierwsze uruchomienie pobiera model z internetu i może trwać 1–2 minuty.

---

## 3. Ewaluacja modelu na wszystkich obrazkach testowych

```powershell
python -m model.evaluator
```

Wyniki zostaną zapisane do pliku `data/test_results.json`.

Aby podejrzeć wyniki:

```powershell
type data\test_results.json
```

---

## 4. Sprawdzenie jakości kodu (pylint)

```powershell
pylint data/ model/ tests/
```

Cel: wynik **≥ 8.00/10** (obecnie mamy **10.00/10**).

---

## 5. Formatowanie kodu (black) — opcjonalnie

Jeśli chcesz automatycznie sformatować kod do PEP8:

```powershell
black data/ model/ tests/
```

---

## 6. Sprawdzenie zainstalowanych bibliotek

```powershell
pip list
```

---

## 7. Wyjście z wirtualnego środowiska

```powershell
deactivate
```

---

## 8. Backend API w Dockerze

Uruchom z **katalogu głównego projektu** (`visiontalk/`):

```bash
docker build -f app/backend/Dockerfile -t visiontalk-backend .
docker run -p 8000:8000 visiontalk-backend
```

Sprawdzenie: http://localhost:8000/health → `{"status":"ok"}`  
Dokumentacja API: http://localhost:8000/docs

Zatrzymanie kontenera: `Ctrl+C`, potem `docker ps` i `docker stop <ID>`.

---

## Skrót — najczęstsze komendy

| Cel | Komenda |
|-----|---------|
| Aktywacja venv | `venv\Scripts\activate` |
| Wszystkie testy | `pytest tests/ -v` |
| Testy `data` | `pytest tests/test_data.py -v` |
| Testy `model` | `pytest tests/test_model.py -v` |
| Jeden obrazek | `python -c "from model.captioner ..."` |
| Ewaluacja wszystkich obrazków | `python -m model.evaluator` |
| Pylint | `pylint data/ model/ tests/` |
| Black (formatowanie) | `black data/ model/ tests/` |
| Wyjście z venv | `deactivate` |
| Backend w Dockerze (build) | `docker build -f app/backend/Dockerfile -t visiontalk-backend .` |
| Backend w Dockerze (run) | `docker run -p 8000:8000 visiontalk-backend` |
