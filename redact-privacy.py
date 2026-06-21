#!/usr/bin/env python3
"""Redact personal data (phones, emails, names) from portfolio screenshots."""

from PIL import Image, ImageDraw
import os

BASE = '/root/portfolio/images/projects'

# Absolute pixel boxes per image (x1, y1, x2, y2) — tuned per screenshot size.
REDACTIONS = {
    'ajwaa/settings-whatsapp.png': [
        (120, 55, 980, 115),   # status + instance URL
        (505, 105, 770, 145),  # test phone number
        (225, 218, 530, 258),  # login email
        (835, 218, 1015, 275), # password / right form values
        (250, 335, 900, 360),  # footer credit
    ],
    'ajwaa/command-center.png': [
        (200, 42, 900, 68),    # company name in subtitle
        (720, 342, 1024, 360), # footer
    ],
    'ajwaa/booking-detail.png': [
        (720, 342, 1024, 360), # footer
        (500, 268, 1010, 340), # pilgrims table (names / mobile)
        (60, 150, 250, 290),   # QR code (booking + client data)
    ],
    'ajwaa/purchases-bookings.png': [
        (650, 325, 1024, 360), # footer
        (390, 215, 760, 315),  # supplier names column
        (800, 215, 1015, 315), # booking / client IDs
    ],
    'ajwaa/booking-top-menu.png': [
        (720, 342, 1024, 360),
    ],
    'ajwaa/purchases-sidebar.png': [
        (720, 342, 1024, 360),
    ],
    'ajwaa/purchases.png': [
        (720, 342, 1024, 360),
    ],
    'bzone/user-management.png': [
        (678, 24, 1022, 318),  # user cards (names + emails)
    ],
    'poultry/farm-dashboard.png': [
        (200, 328, 824, 361),
    ],
    'poultry/accounting-center.png': [
        (200, 310, 824, 340),
    ],
    'poultry/inventory.png': [
        (200, 310, 824, 340),
    ],
}


def fill_region(img, box, color=(236, 239, 243)):
    draw = ImageDraw.Draw(img)
    draw.rectangle(box, fill=color)


FOOTER_BOX_RATIO = (0.62, -42, 1.0, 0)  # right sidebar footer strip


def redact_footer(img):
    w, h = img.size
    if h < 300:
        return
    box = (int(FOOTER_BOX_RATIO[0] * w), h + FOOTER_BOX_RATIO[1], w, h)
    fill_region(img, box)


def redact_image(path, boxes, strip_footer=True):
    img = Image.open(path).convert('RGB')
    for box in boxes:
        fill_region(img, box)
    if strip_footer:
        redact_footer(img)
    img.save(path, optimize=True)
    print(f'  {os.path.relpath(path, BASE)} — {len(boxes)} regions')


def redact_all_footers():
    for root, _, files in os.walk(BASE):
        for name in files:
            if name.endswith('.png'):
                path = os.path.join(root, name)
                img = Image.open(path).convert('RGB')
                redact_footer(img)
                img.save(path, optimize=True)


def main():
    print('Redacting personal data…')
    done = set()
    for rel, boxes in REDACTIONS.items():
        path = os.path.join(BASE, rel)
        if os.path.exists(path):
            redact_image(path, boxes)
            done.add(path)
        else:
            print(f'  MISSING: {rel}')

    print('Stripping sidebar footers on remaining images…')
    for root, _, files in os.walk(BASE):
        for name in files:
            if not name.endswith('.png'):
                continue
            path = os.path.join(root, name)
            if path in done:
                continue
            img = Image.open(path).convert('RGB')
            redact_footer(img)
            img.save(path, optimize=True)
            print(f'  footer only: {os.path.relpath(path, BASE)}')


if __name__ == '__main__':
    main()
