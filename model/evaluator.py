"""Evaluation script for the image captioning model on local test images."""

import json
from pathlib import Path

from data.loader import load_image
from model.captioner import ImageCaptioner


def evaluate_test_images(
    images_dir: str = "data/test_images",
    output_path: str = "data/test_results.json",
) -> None:
    """Run the captioner on all images in ``images_dir`` and save results.

    Args:
        images_dir: Directory containing test images.
        output_path: Path to the JSON file where results will be stored.
    """
    images_path = Path(images_dir)
    if not images_path.exists():
        raise FileNotFoundError(f"Test images directory not found: {images_dir}")

    captioner = ImageCaptioner()
    captioner.load()

    results = []
    for image_file in sorted(images_path.iterdir()):
        if image_file.suffix.upper().lstrip(".") not in {"JPEG", "JPG", "PNG"}:
            continue

        try:
            image = load_image(image_file)
            caption = captioner.predict(image)
            results.append({"image": image_file.name, "caption": caption})
            print(f"Processed {image_file.name}: {caption}")
        except (OSError, ValueError) as exc:
            print(f"Failed to process {image_file.name}: {exc}")
            results.append({"image": image_file.name, "caption": "", "error": str(exc)})

    output_file = Path(output_path)
    output_file.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nEvaluation complete. Results saved to {output_file.resolve()}")


if __name__ == "__main__":
    evaluate_test_images()
