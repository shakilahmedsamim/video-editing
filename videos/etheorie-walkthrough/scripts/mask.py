"""Copy the client screenshots into assets/shots/ and blur the few spots the brief forbids showing
(container / account IDs, dates). Everything else stays pixel-identical.
Usage: python3 scripts/mask.py <folder with 01_..17_ jpgs>
"""
import sys, glob, os
from PIL import Image, ImageFilter
GTM_TOP = [(1152, 56, 1242, 76)]
MASKS = {
    "01": [(1038, 240, 1135, 292)],
    "02": [(508, 126, 600, 145)],
    "03": GTM_TOP, "04": GTM_TOP, "05": GTM_TOP, "06": GTM_TOP,
    "07": [(508, 126, 600, 145)],
    "08": GTM_TOP,
    "09": [(496, 706, 578, 724)], "11": [(496, 706, 578, 724)],
    "12": [(1228, 104, 1362, 136)], "13": [(1228, 104, 1362, 136)], "14": [(1228, 104, 1362, 136)],
    "15": [(1350, 12, 1500, 32), (1284, 62, 1460, 82)],
    "16": [(397, 185, 462, 202)],
}
src = sys.argv[1]
os.makedirs("assets/shots", exist_ok=True)
for f in sorted(glob.glob(os.path.join(src, "*.jpg"))):
    name = os.path.basename(f); im = Image.open(f).convert("RGB")
    for box in MASKS.get(name[:2], []):
        region = im.crop(box).filter(ImageFilter.GaussianBlur(7))
        im.paste(region, box)
    im.save(os.path.join("assets/shots", name), quality=95)
    print(name, len(MASKS.get(name[:2], [])), "masked")
