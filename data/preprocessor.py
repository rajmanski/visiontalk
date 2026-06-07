"""Module for image preprocessing before feeding into the ML model."""

import numpy as np
import torch
from PIL import Image


def preprocess(image: Image.Image, target_size: int = 224) -> torch.Tensor:
    """Resize and normalize an image for the ViT-GPT2 model.

    The image is resized to ``target_size x target_size``, converted to RGB,
    scaled to the range [0, 1], and returned as a float32 tensor with shape
    ``(1, 3, target_size, target_size)`` (batch, channels, height, width).

    Args:
        image: PIL Image in any compatible mode.
        target_size: Desired spatial resolution. Default is 224, which is the
            input size expected by the ViT backbone.

    Returns:
        Preprocessed image tensor.
    """
    if image.mode != "RGB":
        image = image.convert("RGB")

    image = image.resize((target_size, target_size), Image.Resampling.LANCZOS)

    # Convert to numpy array and scale pixel values to [0, 1]
    image_array = np.array(image, dtype=np.float32) / 255.0

    # Convert to tensor and rearrange dimensions from HWC to CHW
    image_tensor = torch.from_numpy(image_array).permute(2, 0, 1)

    # Add batch dimension: (1, 3, target_size, target_size)
    return image_tensor.unsqueeze(0)
