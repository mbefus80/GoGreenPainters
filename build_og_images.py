#!/usr/bin/env python3
"""
Generate 1200x630 Open Graph / Twitter social-share card images.

One card per page: a darkened hero photo + green/gold brand treatment + the page
title. Output goes to /og/. Re-run with `python3 build_og_images.py` whenever
page titles or hero photos change.

OG image filenames are deterministic from the page slug so build_pages.py can
compute the same path without a config lookup:
  slug "services/exterior-painting/"  ->  /og/og-services-exterior-painting.jpg
"""
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
import os

W, H = 1200, 630
GREEN_DARK = (0, 79, 57)
GOLD = (238, 203, 48)
WHITE = (255, 255, 255)

POPPINS_BOLD = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
POPPINS_MED = "/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf"

os.makedirs("og", exist_ok=True)

# (output filename, background image, brand label, title)
SPECS = [
    ("og-home.jpg", "hero-bg.jpg", "GO GREEN COLLEGE PAINTERS",
     "Student-Owned House Painters in Greater Grand Rapids"),
    ("og-services-exterior-painting.jpg", "exterior-after.jpg", "GO GREEN COLLEGE PAINTERS",
     "Exterior House Painting in Grand Rapids, MI"),
    ("og-services-interior-painting.jpg", "interior-after.jpg", "GO GREEN COLLEGE PAINTERS",
     "Interior Painting in Grand Rapids, MI"),
    ("og-services-deck-staining.jpg", "stain-after.jpg", "GO GREEN COLLEGE PAINTERS",
     "Deck Staining & Restoration in Grand Rapids"),
    ("og-services-custom-murals.jpg", "custom-designs.jpg", "GO GREEN COLLEGE PAINTERS",
     "Custom Murals & Accent Walls in Grand Rapids"),
    ("og-grand-rapids-cascade.jpg", "exterior-after.jpg", "GO GREEN  ·  CASCADE, MI",
     "House Painters in Cascade — Cedar Siding Specialists"),
    ("og-grand-rapids-forest-hills.jpg", "exterior-after.jpg", "GO GREEN  ·  FOREST HILLS, MI",
     "House Painters in the Forest Hills Area"),
    ("og-grand-rapids-ada.jpg", "exterior-after.jpg", "GO GREEN  ·  ADA, MI",
     "House Painters in Ada — Cedar Siding Specialists"),
    ("og-grand-rapids-east-grand-rapids.jpg", "exterior-after.jpg", "GO GREEN  ·  EAST GRAND RAPIDS, MI",
     "House Painters in East Grand Rapids, Michigan"),
    ("og-blog.jpg", "hero-bg.jpg", "GO GREEN COLLEGE PAINTERS",
     "Painting Tips & Cost Guides for Grand Rapids Homeowners"),
    ("og-blog-cost-to-paint-a-house-in-grand-rapids.jpg", "exterior-after.jpg", "GO GREEN  ·  2026 GUIDE",
     "How Much Does It Cost to Paint a House in Grand Rapids?"),
    ("og-about.jpg", "exterior-after.jpg", "GO GREEN COLLEGE PAINTERS",
     "About Go Green — Student-Owned, Owner-Operated"),
    ("og-contact.jpg", "hero-bg.jpg", "GO GREEN COLLEGE PAINTERS",
     "Contact Go Green — Free Painting Estimates"),
]


def cover(img, w, h):
    """Resize + center-crop to exactly w x h."""
    img = ImageOps.exif_transpose(img)
    src_ratio = img.width / img.height
    dst_ratio = w / h
    if src_ratio > dst_ratio:
        new_h = h
        new_w = int(h * src_ratio)
    else:
        new_w = w
        new_h = int(w / src_ratio)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - w) // 2
    top = (new_h - h) // 2
    return img.crop((left, top, left + w, top + h))


def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        test = (cur + " " + word).strip()
        if draw.textlength(test, font=font) <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def make_card(out_name, bg_name, label, title):
    # background, covered + slightly blurred for text legibility
    bg = Image.open(bg_name).convert("RGB")
    bg = cover(bg, W, H)

    # green tint overlay
    tint = Image.new("RGB", (W, H), GREEN_DARK)
    canvas = Image.blend(bg, tint, 0.42)

    # bottom-up dark gradient for title legibility
    grad = Image.new("L", (1, H), 0)
    for y in range(H):
        # 0 at top -> ~225 at bottom
        grad.putpixel((0, y), int(235 * (y / H) ** 1.6))
    grad = grad.resize((W, H))
    dark = Image.new("RGB", (W, H), (0, 38, 27))
    canvas = Image.composite(dark, canvas, grad)

    draw = ImageDraw.Draw(canvas)

    margin = 70
    # gold accent bar above the title block
    title_font = ImageFont.truetype(POPPINS_BOLD, 58)
    label_font = ImageFont.truetype(POPPINS_MED, 26)

    # title wrapped, drawn from bottom
    max_text_w = W - 2 * margin
    lines = wrap(draw, title, title_font, max_text_w)
    line_h = int(58 * 1.16)
    title_block_h = line_h * len(lines)

    title_top = H - margin - title_block_h
    # gold bar
    bar_y = title_top - 28
    draw.rectangle([margin, bar_y, margin + 70, bar_y + 7], fill=GOLD)
    # brand label above the bar
    draw.text((margin, bar_y - 44), label, font=label_font, fill=GOLD)

    # title lines
    y = title_top
    for ln in lines:
        draw.text((margin, y), ln, font=title_font, fill=WHITE)
        y += line_h

    # logo, top-right
    try:
        logo = Image.open("logo.png").convert("RGBA")
        logo_w = 130
        logo_h = int(logo.height * logo_w / logo.width)
        logo = logo.resize((logo_w, logo_h), Image.LANCZOS)
        canvas.paste(logo, (W - margin - logo_w, margin - 20), logo)
    except Exception as e:
        print(f"  (logo skipped: {e})")

    out_path = os.path.join("og", out_name)
    canvas.save(out_path, "JPEG", quality=86, optimize=True, progressive=True)
    return os.path.getsize(out_path)


total = 0
for out_name, bg_name, label, title in SPECS:
    size = make_card(out_name, bg_name, label, title)
    total += size
    print(f"  og/{out_name}  ({size // 1024} KB)")
print(f"\nBuilt {len(SPECS)} OG cards, {total // 1024} KB total.")
