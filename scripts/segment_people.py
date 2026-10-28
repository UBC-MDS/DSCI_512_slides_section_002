"""Cut the people out of a slide image with a pretrained segmentation model.

Saves a black and white mask next to the image (white = person), for the
"Remove the people" slide in lecture 8. The deck loads the mask, so torch is
only needed when the image changes, not when the slides render.

    uv run --with torch --with torchvision python scripts/segment_people.py \
        website/slides/images/lec08_english_bay_boats_people.png

The model is torchvision's Mask R-CNN trained on COCO (class 1 is "person").
The first run downloads its weights (about 170 MB) from download.pytorch.org.
"""

import sys
from pathlib import Path

import numpy as np
import torch
from PIL import Image
from scipy.ndimage import binary_dilation
from torchvision.models.detection import MaskRCNN_ResNet50_FPN_V2_Weights, maskrcnn_resnet50_fpn_v2

PERSON = 1          # COCO label for a person
MIN_SCORE = 0.7     # keep only confident detections
GROW = 4            # grow the mask a few pixels so no outline of the person is left behind


def person_mask(path):
    """True where a person is, for every confident person the model finds."""
    weights = MaskRCNN_ResNet50_FPN_V2_Weights.DEFAULT
    model = maskrcnn_resnet50_fpn_v2(weights=weights).eval()
    image = Image.open(path).convert("RGB")
    x = torch.from_numpy(np.asarray(image)).permute(2, 0, 1).float() / 255
    with torch.no_grad():
        out = model([x])[0]
    keep = (out["labels"] == PERSON) & (out["scores"] >= MIN_SCORE)
    print(f"{int(keep.sum())} people found, scores {out['scores'][keep].numpy().round(2).tolist()}")
    mask = (out["masks"][keep, 0] > 0.5).any(dim=0).numpy()
    return binary_dilation(mask, iterations=GROW)


if __name__ == "__main__":
    src = Path(sys.argv[1])
    out = src.with_name(src.stem + "_mask.png")
    Image.fromarray((person_mask(src) * 255).astype(np.uint8)).save(out)
    print(out)
