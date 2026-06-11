"""API tests for the FastAPI application."""

from io import BytesIO
import sys
import types

from fastapi.testclient import TestClient
from PIL import Image

fake_gtts_module = types.ModuleType("gtts")
fake_gtts_module.gTTS = object
sys.modules.setdefault("gtts", fake_gtts_module)

from app.backend import main


client = TestClient(main.app)


def _image_bytes(image_format: str = "PNG") -> bytes:
    """Create an in-memory test image."""
    image = Image.new("RGB", (64, 64), color="navy")
    buffer = BytesIO()
    image.save(buffer, format=image_format)
    return buffer.getvalue()


def test_health() -> None:
    """Health endpoint should report OK."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_index_serves_frontend() -> None:
    """Root path should return the frontend page."""
    response = client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "VisionTalk" in response.text


def test_predict_returns_caption(monkeypatch) -> None:
    """Predict endpoint should return caption JSON."""

    class FakeCaptioner:
        """Small test double for caption generation."""

        def predict(self, image) -> str:
            del image
            return "a test caption"

    monkeypatch.setattr(main, "_get_captioner", lambda: FakeCaptioner())

    response = client.post(
        "/predict",
        files={"file": ("sample.png", _image_bytes(), "image/png")},
    )

    assert response.status_code == 200
    assert response.json() == {"caption": "a test caption"}


def test_predict_rejects_invalid_type() -> None:
    """Predict endpoint should reject unsupported content types."""
    response = client.post(
        "/predict",
        files={"file": ("sample.gif", b"GIF89a", "image/gif")},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Unsupported file type. Please upload a JPEG or PNG image."
    )


def test_tts_returns_audio(monkeypatch) -> None:
    """TTS endpoint should return an MP3 response."""

    class FakeTTS:
        """Small test double for audio generation."""

        def __init__(self, text: str, lang: str) -> None:
            self.text = text
            self.lang = lang

        def write_to_fp(self, file_pointer) -> None:
            file_pointer.write(b"fake-mp3")

    monkeypatch.setattr(main, "gTTS", FakeTTS)

    response = client.get("/tts", params={"text": "hello world"})

    assert response.status_code == 200
    assert response.content == b"fake-mp3"
    assert response.headers["content-type"] == "audio/mpeg"
