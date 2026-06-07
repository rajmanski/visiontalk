"""Unit tests for the data loading and preprocessing modules."""

import tempfile
from pathlib import Path

import pytest
import torch
from PIL import Image

from data.loader import load_image, validate_image
from data.preprocessor import preprocess


class TestLoader:
    """Tests for data.loader module."""

    def test_load_valid_image(self):
        """Loading a valid JPEG image should succeed."""
        test_dir = Path("data/test_images")
        if not test_dir.exists():
            pytest.skip("Test images directory not available.")

        image_path = next(
            (p for p in test_dir.iterdir() if p.suffix.lower() in (".jpg", ".jpeg", ".png")),
            None,
        )
        if image_path is None:
            pytest.skip("No test images available.")

        image = load_image(image_path)
        assert isinstance(image, Image.Image)
        assert image.mode == "RGB"

    def test_load_nonexistent_file(self):
        """Loading a nonexistent file should raise FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_image("data/test_images/nonexistent.jpg")

    def test_load_unsupported_format(self):
        """Loading an unsupported format should raise ValueError."""
        with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as tmp:
            tmp.write(b"GIF89a")
            tmp.flush()

            with pytest.raises(ValueError):
                load_image(tmp.name)

    def test_validate_image_success(self):
        """Validating a proper PIL Image should return True."""
        image = Image.new("RGB", (100, 100), color="red")
        assert validate_image(image) is True

    def test_validate_image_none(self):
        """Validating None should raise ValueError."""
        with pytest.raises(ValueError):
            validate_image(None)


class TestPreprocessor:
    """Tests for data.preprocessor module."""

    def test_preprocess_shape_and_type(self):
        """Preprocessed tensor should have correct shape and dtype."""
        image = Image.new("RGB", (300, 200), color="blue")
        tensor = preprocess(image, target_size=224)

        assert isinstance(tensor, torch.Tensor)
        assert tensor.shape == (1, 3, 224, 224)
        assert tensor.dtype == torch.float32

    def test_preprocess_value_range(self):
        """Preprocessed tensor values should be in [0, 1]."""
        image = Image.new("RGB", (100, 100), color="white")
        tensor = preprocess(image, target_size=224)

        assert tensor.min() >= 0.0
        assert tensor.max() <= 1.0

    def test_preprocess_different_mode(self):
        """Passing a non-RGB image should be handled gracefully."""
        image = Image.new("L", (100, 100), color=128)
        tensor = preprocess(image, target_size=224)

        assert tensor.shape == (1, 3, 224, 224)
