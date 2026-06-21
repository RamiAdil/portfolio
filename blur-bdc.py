#!/usr/bin/env python3
"""Apply blur (not solid masks) to sensitive BDC portfolio screenshots."""

from PIL import Image, ImageFilter
import os

BASE = '/root/portfolio/images/projects/bdc'

# (x1, y1, x2, y2) tuned for 1440x900 captures
BLUR_REGIONS = {
    'executive-dashboard.png': [
        (900, 88, 1380, 135),      # company subtitle line
        (880, 700, 1400, 870),     # consultant table data rows
    ],
    'charts-analytics.png': [
        (900, 88, 1380, 135),
        (160, 545, 1280, 655),     # bar chart x-axis consultant labels
    ],
    'delays-penalties.png': [
        (900, 88, 1380, 135),
        (120, 248, 1180, 540),     # delay table sensitive columns
        (120, 600, 1320, 860),     # delayed projects summary names
    ],
    'consultants-performance.png': [
        (900, 88, 1380, 135),
        (100, 155, 440, 225),
        (480, 155, 820, 225),
        (860, 155, 1200, 225),
        (100, 415, 440, 485),
        (480, 415, 820, 485),
        (860, 415, 1200, 485),
        (100, 675, 440, 755),
        (480, 675, 820, 755),
        (860, 675, 1200, 755),
    ],
    'projects-works.png': [
        (1240, 8, 1435, 58),       # user / company in systray
        (455, 128, 760, 880),      # consultant column
    ],
    'metrics.png': [
        (1240, 8, 1435, 58),
        (70, 128, 290, 880),       # metric numbers
        (455, 128, 660, 880),      # consultant column
        (655, 128, 860, 880),      # contractor column
        (855, 128, 1000, 880),     # metric values
    ],
}


def blur_region(img, box, pixel_scale=5, blur_radius=11):
    x1, y1, x2, y2 = box
    w, h = img.size
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(w, x2), min(h, y2)
    if x2 - x1 < 4 or y2 - y1 < 4:
        return
    region = img.crop((x1, y1, x2, y2))
    small = region.resize(
        (max(1, region.width // pixel_scale), max(1, region.height // pixel_scale)),
        Image.Resampling.BILINEAR,
    )
    blurred = small.resize(region.size, Image.Resampling.NEAREST)
    blurred = blurred.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    img.paste(blurred, (x1, y1))


def process_image(path, boxes):
    img = Image.open(path).convert('RGB')
    for box in boxes:
        blur_region(img, box)
    img.save(path, optimize=True)
    print(f'  blurred {os.path.basename(path)} ({len(boxes)} regions)')


def main():
    print('Blurring BDC sensitive data…')
    for name, boxes in BLUR_REGIONS.items():
        path = os.path.join(BASE, name)
        if os.path.exists(path):
            process_image(path, boxes)
        else:
            print(f'  MISSING {name}')


if __name__ == '__main__':
    main()
