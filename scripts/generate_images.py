"""Generate slide images with the OpenAI image API.

Two functions:

    generate_image(prompt, filename)   one image
    generate_from_csv(csv_path)        every row of a CSV with filename/prompt columns

By default both attach the lecture 1 otter images as style references, so the new
image keeps the same character and watercolour style. Pass `refs=None` to skip that
and do a plain text-to-image generation.

From the shell:

    uv run python scripts/generate_images.py "an otter holding a clock" otter_clock.png
    uv run python scripts/generate_images.py --csv website/slides/lec02_image_prompts.csv
"""

import base64
import csv
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

REPO_ROOT = Path(__file__).resolve().parents[1]
IMAGES_DIR = REPO_ROOT / "website" / "slides" / "images"

# Shown to the model so the otter and the style stay the same across lectures.
STYLE_REFS = [IMAGES_DIR / "example.png", IMAGES_DIR / "example2.png"]

# The written form of "same style as this one, same character".
STYLE_LOCK = (
    "Generate an image in the exact same illustration style as the attached reference "
    "image(s), using the exact same otter character. Then draw this scene:\n\n"
)

load_dotenv(REPO_ROOT / ".env")


def generate_image(prompt, filename, refs=STYLE_REFS, size="1536x1024", quality="high"):
    """Generate one image and save it to website/slides/images/<filename>."""
    client = OpenAI()

    if refs:
        files = [Path(ref).open("rb") for ref in refs]
        try:
            result = client.images.edit(
                model="gpt-image-1",
                image=files,
                prompt=STYLE_LOCK + prompt,
                size=size,
                quality=quality,
            )
        finally:
            for file in files:
                file.close()
    else:
        result = client.images.generate(
            model="gpt-image-1", prompt=prompt, size=size, quality=quality
        )

    out = IMAGES_DIR / filename
    out.write_bytes(base64.b64decode(result.data[0].b64_json))
    return out


def generate_from_csv(csv_path, refs=STYLE_REFS, overwrite=False):
    """Generate an image per row of a CSV with `filename` and `prompt` columns."""
    with open(csv_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    made = []
    for row in rows:
        filename, prompt = row["filename"], row["prompt"]
        if (IMAGES_DIR / filename).exists() and not overwrite:
            print(f"· {filename} exists, skipping")
            continue
        print(f"→ {filename}")
        made.append(generate_image(prompt, filename, refs=refs))
    return made


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prompt", nargs="?", help="prompt for a single image")
    parser.add_argument("filename", nargs="?", help="output filename, e.g. otter.png")
    parser.add_argument("--csv", help="generate every row of this CSV instead")
    parser.add_argument("--no-refs", action="store_true", help="skip the style references")
    parser.add_argument("--overwrite", action="store_true", help="redo images that exist")
    args = parser.parse_args()

    refs = None if args.no_refs else STYLE_REFS
    if args.csv:
        generate_from_csv(args.csv, refs=refs, overwrite=args.overwrite)
    elif args.prompt and args.filename:
        print(generate_image(args.prompt, args.filename, refs=refs))
    else:
        parser.error("give a prompt and a filename, or --csv")
