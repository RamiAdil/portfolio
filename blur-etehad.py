#!/usr/bin/env python3
"""Blur sensitive data on Etihad / Oman shipping portfolio screenshots."""

from PIL import Image, ImageFilter
import os

BASE = '/root/portfolio/images/projects/etehad'

BLUR_REGIONS = {
    'shipments-portal.png': [
        (655, 0, 1024, 338),     # customer sidebar (name, phone, email, QR)
        (24, 118, 175, 330),     # tracking numbers column
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


def main():
    for name, boxes in BLUR_REGIONS.items():
        path = os.path.join(BASE, name)
        if not os.path.exists(path):
            print(f'MISSING {name}')
            continue
        img = Image.open(path).convert('RGB')
        for box in boxes:
            blur_region(img, box)
        img.save(path, optimize=True)
        print(f'blurred {name}')


if __name__ == '__main__':
    main()
