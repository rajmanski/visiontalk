"""Wrapper around the HuggingFace ViT-GPT2 image captioning model."""

from typing import Optional

from PIL import Image
from transformers import pipeline


MODEL_NAME = "nlpconnect/vit-gpt2-image-captioning"


class ImageCaptioner:
    """Lightweight wrapper for the ViT-GPT2 image-to-text model."""

    def __init__(self) -> None:
        """Initialize the captioner without loading the model yet."""
        self._captioner: Optional[pipeline] = None

    def load(self) -> None:
        """Load the HuggingFace image-to-text pipeline.

        The model is downloaded and cached on the first call. Subsequent calls
        are no-ops if the model is already loaded.
        """
        if self._captioner is None:
            self._captioner = pipeline(
                "image-to-text",
                model=MODEL_NAME,
            )

    def predict(self, image: Image.Image) -> str:
        """Generate a textual caption for the given image.

        Args:
            image: PIL Image in RGB mode.

        Returns:
            Generated caption string.

        Raises:
            RuntimeError: If the model has not been loaded.
        """
        if self._captioner is None:
            raise RuntimeError(
                "Model is not loaded. Call load() before predict()."
            )

        result = self._captioner(image)

        if isinstance(result, list) and len(result) > 0:
            return result[0].get("generated_text", "").strip()

        return ""

    def is_loaded(self) -> bool:
        """Return whether the model pipeline has been loaded."""
        return self._captioner is not None
