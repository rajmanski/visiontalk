"""Unit tests for the image captioning model wrapper."""

from pathlib import Path

import pytest
from PIL import Image

from model.captioner import ImageCaptioner


class TestImageCaptioner:
    """Tests for model.captioner module."""

    def test_is_loaded_before_load(self):
        """Fresh instance should report as not loaded."""
        captioner = ImageCaptioner()
        assert captioner.is_loaded() is False

    def test_predict_without_load_raises(self):
        """Calling predict before load should raise RuntimeError."""
        captioner = ImageCaptioner()
        dummy_image = Image.new("RGB", (100, 100), color="green")

        with pytest.raises(RuntimeError):
            captioner.predict(dummy_image)

    def test_load_and_predict(self):
        """Loading the model and predicting on a real image should work."""
        test_dir = Path("data/test_images")
        if not test_dir.exists():
            pytest.skip("Test images directory not available.")

        image_path = next(
            (p for p in test_dir.iterdir() if p.suffix.lower() in (".jpg", ".jpeg", ".png")),
            None,
        )
        if image_path is None:
            pytest.skip("No test images available.")

        captioner = ImageCaptioner()
        captioner.load()

        assert captioner.is_loaded() is True

        image = Image.open(image_path).convert("RGB")
        caption = captioner.predict(image)

        assert isinstance(caption, str)
        assert len(caption) > 0

    def test_load_idempotent(self):
        """Calling load() multiple times should be safe."""
        captioner = ImageCaptioner()
        captioner.load()
        captioner.load()
        assert captioner.is_loaded() is True
