"""VisionTalk backend API.

A small FastAPI application that wraps the ViT-GPT2 image captioning model
and Google Text-to-Speech (gTTS). It exposes three endpoints:

* ``GET  /health``  - simple liveness probe.
* ``POST /predict``  - upload an image, get a textual caption back.
* ``GET  /tts``      - send text, get an MP3 audio file back.

Interactive Swagger documentation is available at ``/docs`` and ReDoc at
``/redoc`` once the server is running.
"""

from io import BytesIO

from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.responses import Response
from gtts import gTTS
from PIL import Image, UnidentifiedImageError
from pydantic import BaseModel

from model.captioner import ImageCaptioner

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png"}

app = FastAPI(
    title="VisionTalk API",
    description=(
        "Generuje tekstowe opisy obrazów (image captioning) oraz syntezę "
        "mowy (TTS). Użyj zakładki **/docs** aby ręcznie przetestować "
        "endpointy."
    ),
    version="1.0.0",
)

# Single shared model instance. It is loaded lazily on the first /predict
# call so that the server (and Swagger UI) start instantly without having to
# download the model first.
_captioner = ImageCaptioner()


def _get_captioner() -> ImageCaptioner:
    """Return a loaded captioner instance, loading the model on first use."""
    if not _captioner.is_loaded():
        _captioner.load()
    return _captioner


class HealthResponse(BaseModel):
    """Response model for the health check endpoint."""

    status: str = "ok"


class CaptionResponse(BaseModel):
    """Response model for the prediction endpoint."""

    caption: str


@app.get("/health", response_model=HealthResponse, tags=["status"])
def health() -> HealthResponse:
    """Return a simple status payload to confirm the API is running."""
    return HealthResponse(status="ok")


@app.post("/predict", response_model=CaptionResponse, tags=["captioning"])
async def predict(file: UploadFile = File(...)) -> CaptionResponse:
    """Generate a textual caption for an uploaded image.

    Accepts a JPEG or PNG image as multipart/form-data and returns the
    caption produced by the ViT-GPT2 model.
    """
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file type. Please upload a JPEG or PNG image."
            ),
        )

    raw_bytes = await file.read()

    try:
        image = Image.open(BytesIO(raw_bytes)).convert("RGB")
    except (UnidentifiedImageError, OSError) as exc:
        raise HTTPException(
            status_code=400,
            detail="Could not read the uploaded file as an image.",
        ) from exc

    caption = _get_captioner().predict(image)
    return CaptionResponse(caption=caption)


@app.get("/tts", tags=["tts"])
def tts(text: str = Query(..., description="Text to convert to speech")):
    """Convert text to speech and return an MP3 file."""
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text must not be empty.")

    audio_buffer = BytesIO()
    gTTS(text=text, lang="en").write_to_fp(audio_buffer)

    return Response(
        content=audio_buffer.getvalue(),
        media_type="audio/mpeg",
        headers={"Content-Disposition": 'inline; filename="speech.mp3"'},
    )
