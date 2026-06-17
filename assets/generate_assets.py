from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import math
import random


ROOT = Path(__file__).resolve().parent


def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def draw_cable_scene(path: Path):
    w, h = 1600, 1000
    img = Image.new("RGB", (w, h), "#eef3f7")
    draw = ImageDraw.Draw(img)

    for y in range(h):
        shade = int(238 - y * 18 / h)
        draw.line([(0, y), (w, y)], fill=(shade, shade + 5, shade + 10))

    random.seed(7)
    for x in range(120, w, 160):
        draw.line([(x, 0), (x + 220, h)], fill="#dde7ee", width=2)
    for y in range(120, h, 130):
        draw.line([(0, y), (w, y - 50)], fill="#e5edf3", width=2)

    rack_x = 160
    for i in range(4):
        x0 = rack_x + i * 310
        rounded(draw, (x0, 165, x0 + 230, 790), 12, "#1e2935", "#34465a", 3)
        for j in range(8):
            y0 = 210 + j * 62
            rounded(draw, (x0 + 28, y0, x0 + 202, y0 + 34), 6, "#2f4356", "#496174", 1)
            for k in range(5):
                px = x0 + 47 + k * 31
                rounded(draw, (px, y0 + 8, px + 18, y0 + 18), 3, "#86efac" if (j + k + i) % 3 == 0 else "#38bdf8")

    colors = ["#2dd4bf", "#60a5fa", "#f59e0b", "#a78bfa", "#34d399"]
    for i in range(38):
        x1 = 240 + (i % 7) * 45
        y1 = 725 + (i % 9) * 10
        x2 = 1180 + (i % 6) * 30
        y2 = 255 + (i % 10) * 42
        midx = (x1 + x2) / 2 + math.sin(i) * 120
        color = colors[i % len(colors)]
        draw.line([(x1, y1), (midx, 450 + math.sin(i) * 95), (x2, y2)], fill=color, width=5)

    panel = (680, 170, 1370, 430)
    rounded(draw, panel, 24, "#ffffff", "#d7e2ea", 2)
    rounded(draw, (730, 240, 1320, 330), 12, "#f7fafc", "#d8e4ec", 2)
    for i in range(16):
        px = 760 + i * 34
        rounded(draw, (px, 268, px + 20, 292), 4, "#0f172a", "#111827", 1)
        draw.rectangle((px + 5, 292, px + 15, 344), fill=colors[i % len(colors)])

    img = img.filter(ImageFilter.UnsharpMask(radius=1, percent=105))
    img.save(path, quality=92)


def draw_ceramic_scene(path: Path):
    w, h = 1600, 1000
    img = Image.new("RGB", (w, h), "#f5f7f8")
    draw = ImageDraw.Draw(img)

    for y in range(h):
        shade = 247 - int(y * 12 / h)
        draw.line([(0, y), (w, y)], fill=(shade, shade + 1, shade + 1))

    draw.ellipse((940, 130, 1500, 690), fill="#e4eef2")
    draw.ellipse((1000, 180, 1440, 620), fill="#d5e3e8")

    def board(cx, cy, bw, bh, angle_color, copper):
        rounded(draw, (cx, cy, cx + bw, cy + bh), 28, angle_color, "#d6dde2", 2)
        for i in range(6):
            x = cx + 55 + i * (bw - 120) / 5
            draw.line([(x, cy + 60), (x + 80, cy + bh - 60)], fill=copper, width=14)
            draw.ellipse((x - 12, cy + 45, x + 12, cy + 69), fill=copper)
            draw.ellipse((x + 68, cy + bh - 72, x + 92, cy + bh - 48), fill=copper)
        for j in range(3):
            y = cy + 95 + j * 72
            draw.line([(cx + 70, y), (cx + bw - 70, y)], fill=copper, width=10)

    board(170, 220, 520, 350, "#fbfcfc", "#b87333")
    board(455, 455, 520, 350, "#f3f7f8", "#c28a45")
    board(820, 290, 430, 290, "#fcfdfd", "#ad6b28")

    for x in [1040, 1120, 1200, 1280]:
        draw.rectangle((x, 650, x + 40, 820), fill="#fdfdfd", outline="#d5dde4", width=2)
        draw.rectangle((x + 7, 670, x + 33, 800), fill="#b87333")

    for i in range(34):
        x = 95 + i * 42
        y = 840 + math.sin(i / 2) * 12
        draw.ellipse((x, y, x + 15, y + 15), fill="#cbd5dc")

    img = img.filter(ImageFilter.UnsharpMask(radius=1, percent=105))
    img.save(path, quality=92)


if __name__ == "__main__":
    draw_cable_scene(ROOT / "ai-data-center-cabling.jpg")
    draw_ceramic_scene(ROOT / "ceramic-substrates.jpg")
