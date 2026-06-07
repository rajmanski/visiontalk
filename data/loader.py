"""Module for loading and validating image files."""

from pathlib import Path
from typing import Union

from PIL import Image


SUPPORTED_FORMATS = {"JPEG", "JPG", "PNG"}


def load_image(image_path: Union[str, Path]) -> Image.Image:
    """Load an image from a given path and validate its format.

    Args:
        image_path: Path to the image file.

    Returns:
        Loaded PIL Image in RGB mode.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the image format is not supported or the file is
            corrupted.
    """
    image_path = Path(image_path)

    if not image_path.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")

    file_format = image_path.suffix.upper().lstrip(".")
    if file_format not in SUPPORTED_FORMATS:
        raise ValueError(
            f"Unsupported image format: {file_format}. "
            f"Supported formats are: {', '.join(SUPPORTED_FORMATS)}"
        )

    try:
        image = Image.open(image_path)
        image.verify()
    except Exception as exc:
        raise ValueError(f"Corrupted or unreadable image file: {image_path}") from exc

    # Re-open after verify() because it leaves the file pointer at the end
    image = Image.open(image_path)
    if image.mode != "RGB":
        image = image.convert("RGB")

    return image


def validate_image(image: Image.Image) -> bool:
    """Check if a PIL Image object is valid and not corrupted.

    Args:
        image: PIL Image instance.

    Returns:
        True if the image is valid.

    Raises:
        ValueError: If the image is invalid.
    """
    if image is None:
        raise ValueError("Image is None.")

    try:
        image.load()
    except Exception as exc:
        raise ValueError("Failed to load image data.") from exc

    return True
