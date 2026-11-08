#!/usr/bin/env python3
"""Palette system (shipped with the 残光 / Zankō dusk palettes P1-P5 as a starting point) — writes machine-readable
palettes, 256x1 gradient-map LUT PNGs and a visual contact sheet that applies every palette to a procedural dusk scene
(or, with --plate, to one of your own backgrounds: judge daylight palettes on a daylight plate).
Edit PALETTES below for a new song's colour script, then re-run.

Usage:
  python tools/style_palette_sheet.py [--sheet docs/style_palettes.png] [--plate assets/bg/<plate>.png]

Outputs (under the project root):
  assets/style/palettes.json          (roles, gradient stops, duotone pairs, contrast)
  assets/style/luts/<id>.png          (256x1 RGB gradient-map LUT, OKLab-interpolated)
  assets/style/luts/<id>_duo.png      (256x1 duotone LUT)
  assets/style/dusk_scene_gray.png    (the grey test scene; used by tools/preview_style_fx.mjs)
  docs/style_palettes.png             (contact sheet)
Author: NikusonP -- vocaloid-style-mv-pipeline, MIT licence.
"""
import argparse, json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit_env  # noqa: E402

ROOT = str(kit_env.ROOT)
OUT_STYLE = os.path.join(ROOT, "assets", "style")
OUT_LUT = os.path.join(OUT_STYLE, "luts")
# label font for the contact sheet: project Noto Sans JP, else a system Japanese UI font
SHEET_FONTS = [os.path.join(ROOT, "engine", "fonts", "NotoSansJP_wght_.ttf"), "YuGothM.ttc", "meiryo.ttc",
               "ヒラギノ角ゴシック W3.ttc", "Hiragino Sans GB.ttc", "NotoSansCJK-Regular.ttc", "NotoSansCJKjp-Regular.otf",
               "NotoSansJP-Regular.otf", "DejaVuSans.ttf", "Arial.ttf", "arial.ttf"]

PALETTES = [  # 《秋風恋歌》 colour script (docs/CONCEPT.md); the 和紙 palette is typography only, no LUT
    {
        "id": "P1_ima", "name": "現在段 Ima (faded russet, present)",
        "use": "Verse 1/2, Chorus 1/2, 3D-A: faded maple, low saturation",
        "roles": {"c0": "#2A1C18", "c1": "#4A2A22", "c2": "#7A3B2A", "c3": "#A0603F", "c4": "#C9A487", "c5": "#EDE3D6"},
        "gradmap": [[0.00, "#2A1C18"], [0.20, "#4A2A22"], [0.40, "#7A3B2A"], [0.60, "#A0603F"], [0.80, "#C9A487"], [1.00, "#EDE3D6"]],
        "duotone": ["#2A1C18", "#EDE3D6"], "accent": "#B8322A", "afterimage": "#5E8FA0",
    },
    {
        "id": "P2_kaiso", "name": "回憶段 Kaisō (late-summer memory)",
        "use": "Pre-chorus 1 flashes, Interlude 1: warm gold + fresh green",
        "roles": {"c0": "#3A3A2A", "c1": "#5E8C3A", "c2": "#9DBF5A", "c3": "#F2D58A", "c4": "#FFF6DC"},
        "gradmap": [[0.00, "#3A3A2A"], [0.25, "#5E8C3A"], [0.50, "#9DBF5A"], [0.75, "#F2D58A"], [1.00, "#FFF6DC"]],
        "duotone": ["#3A3A2A", "#FFF6DC"], "accent": "#D9A441", "afterimage": "#7A5CC0",
    },
    {
        "id": "P3_shigure", "name": "時雨 Shigure (cold shower)",
        "use": "Pre-chorus 2, end of Chorus 2, Break: the greyest stretch",
        "roles": {"c0": "#1E2530", "c1": "#33404F", "c2": "#56677A", "c3": "#8698A8", "c4": "#B9C6CF", "c5": "#E8EDF0"},
        "gradmap": [[0.00, "#1E2530"], [0.20, "#33404F"], [0.40, "#56677A"], [0.60, "#8698A8"], [0.80, "#B9C6CF"], [1.00, "#E8EDF0"]],
        "duotone": ["#1E2530", "#E8EDF0"], "accent": "#B8322A", "afterimage": "#C08A5A",
    },
    {
        "id": "P4_momiji", "name": "紅楓 Momiji (full crimson)",
        "use": "second half of the Bridge, Last chorus, 3D-B",
        "roles": {"c0": "#3A1416", "c1": "#8E1B24", "c2": "#C7302A", "c3": "#E8662E", "c4": "#F6B04A", "c5": "#FFF1E0"},
        "gradmap": [[0.00, "#3A1416"], [0.20, "#8E1B24"], [0.40, "#C7302A"], [0.60, "#E8662E"], [0.80, "#F6B04A"], [1.00, "#FFF1E0"]],
        "duotone": ["#3A1416", "#FFF1E0"], "accent": "#9DBF5A", "afterimage": "#2FB7C0",
    },
    {
        "id": "P5_kazahana", "name": "風花 Kazahana (snow light)",
        "use": "Coda, Outro: white-out",
        "roles": {"c0": "#2B3440", "c1": "#8FA3B5", "c2": "#B7C6D4", "c3": "#D9E2EA", "c4": "#F2F5F8", "c5": "#FFFFFF"},
        "gradmap": [[0.00, "#2B3440"], [0.20, "#8FA3B5"], [0.40, "#B7C6D4"], [0.60, "#D9E2EA"], [0.80, "#F2F5F8"], [1.00, "#FFFFFF"]],
        "duotone": ["#2B3440", "#FFFFFF"], "accent": "#B8322A", "afterimage": "#D8B48A",
    }
]
GLOBAL = {"flash_white": "#FFFFFF", "sumi": "#111014", "paper": "#F4EFE6"}


def hex2rgb(h):
    h = h.lstrip('#')
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], dtype=np.float64) / 255.0


def srgb2lin(c):
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def lin2srgb(c):
    c = np.clip(c, 0, 1)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * np.power(c, 1 / 2.4) - 0.055)


def lin2oklab(c):
    M1 = np.array([[0.4122214708, 0.5363325363, 0.0514459929],
                   [0.2119034982, 0.6806995451, 0.1073969566],
                   [0.0883024619, 0.2817188376, 0.6299787005]])
    M2 = np.array([[0.2104542553, 0.7936177850, -0.0040720468],
                   [1.9779984951, -2.4285922050, 0.4505937099],
                   [0.0259040371, 0.7827717662, -0.8086757660]])
    lms = np.cbrt(c @ M1.T)
    return lms @ M2.T


def oklab2lin(l):
    M2i = np.array([[1.0, 0.3963377774, 0.2158037573],
                    [1.0, -0.1055613458, -0.0638541728],
                    [1.0, -0.0894841775, -1.2914855480]])
    M1i = np.array([[4.0767416621, -3.3077115913, 0.2309699292],
                    [-1.2684380046, 2.6097574011, -0.3413193965],
                    [-0.0041960863, -0.7034186147, 1.7076147010]])
    lms = (l @ M2i.T) ** 3
    return lms @ M1i.T


def rel_lum(h):
    c = srgb2lin(hex2rgb(h))
    return float(0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2])


def contrast(a, b):
    la, lb = sorted((rel_lum(a), rel_lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def build_lut(stops, n=256):
    """OKLab-interpolated gradient map, returns (n,3) sRGB floats."""
    xs = np.array([s[0] for s in stops])
    labs = np.array([lin2oklab(srgb2lin(hex2rgb(s[1]))) for s in stops])
    t = np.linspace(0, 1, n)
    out = np.zeros((n, 3))
    for i, v in enumerate(t):
        j = np.searchsorted(xs, v, side='right') - 1
        j = int(np.clip(j, 0, len(xs) - 2))
        span = xs[j + 1] - xs[j]
        f = 0.0 if span <= 1e-9 else np.clip((v - xs[j]) / span, 0, 1)
        out[i] = labs[j] * (1 - f) + labs[j + 1] * f
    return lin2srgb(oklab2lin(out))


def dusk_scene(W=640, H=360, seed=7):
    """Procedural grayscale dusk: sky ramp, low sun, skyline, power lines, railway crossing, figure + long shadow."""
    rng = np.random.default_rng(seed)
    y, x = np.mgrid[0:H, 0:W].astype(np.float64)
    hz = 0.70 * H
    sunx, suny, sunr = 0.70 * W, 0.64 * H, 0.055 * H
    sky = 0.10 + 0.55 * np.clip(y / hz, 0, 1) ** 1.6
    d = np.hypot((x - sunx) / W, (y - suny) / H * 0.6)
    sky += 0.45 * np.exp(-d / 0.12) + 0.25 * np.exp(-np.abs(y - hz) / (0.03 * H)) * np.exp(-np.abs(x - sunx) / (0.5 * W))
    sky = np.clip(sky, 0, 0.97)
    sky[np.hypot(x - sunx, y - suny) < sunr] = 1.0
    img = Image.fromarray((sky * 255).astype(np.uint8), 'L')
    dr = ImageDraw.Draw(img)
    # far skyline (lighter = atmospheric perspective)
    xx = 0
    while xx < W:
        w = int(rng.integers(14, 46)); h = int(rng.integers(8, 52))
        dr.rectangle([xx, hz - h, xx + w, hz], fill=int(0.16 * 255)); xx += w
    # ground
    dr.rectangle([0, hz, W, H], fill=int(0.05 * 255))
    # rails converging
    for k in (-1, 1):
        dr.line([(0.52 * W + k * 6, hz), (0.52 * W + k * 170, H)], fill=int(0.35 * 255), width=3)
    # power poles + catenary wires
    poles = [0.12 * W, 0.47 * W, 0.93 * W]
    for px in poles:
        dr.rectangle([px - 3, 0.18 * H, px + 3, hz + 4], fill=6)
        dr.rectangle([px - 26, 0.22 * H, px + 26, 0.22 * H + 4], fill=6)
    for a, b in zip(poles[:-1], poles[1:]):
        for off in (-22, 0, 22):
            pts = [(a + off + (b - a) * s, 0.22 * H + 2 + 34 * np.sin(np.pi * s) + (off == 0) * 8 * np.sin(np.pi * s))
                   for s in np.linspace(0, 1, 40)]
            dr.line(pts, fill=6, width=1)
    # railway crossing: crossbuck, lamps, striped barrier arm
    cx, cy = 0.30 * W, 0.40 * H
    dr.rectangle([cx - 3, cy - 20, cx + 3, hz + 8], fill=6)
    for sgn in (1, -1):
        dr.line([(cx - 34, cy - 26 * sgn), (cx + 34, cy + 26 * sgn)], fill=int(0.92 * 255), width=9)
        dr.line([(cx - 34, cy - 26 * sgn), (cx + 34, cy + 26 * sgn)], fill=6, width=3)
    dr.ellipse([cx - 30, cy + 34, cx - 12, cy + 52], fill=int(0.98 * 255))   # lit lamp
    dr.ellipse([cx + 12, cy + 34, cx + 30, cy + 52], fill=int(0.12 * 255))   # dark lamp
    ax0, ay0 = cx + 6, hz - 30
    L = 250
    for i in range(10):
        s0, s1 = i / 10, (i + 1) / 10
        col = int(0.9 * 255) if i % 2 == 0 else 8
        dr.line([(ax0 + L * s0, ay0 + 6 * s0), (ax0 + L * s1, ay0 + 6 * s1)], fill=col, width=7)
    # figure silhouette + long shadow toward camera-left
    fx, fy = 0.60 * W, hz + 34
    dr.polygon([(fx, fy), (fx - 300, H), (fx - 250, H)], fill=2)
    dr.ellipse([fx - 7, fy - 62, fx + 7, fy - 48], fill=4)
    dr.polygon([(fx - 9, fy - 48), (fx + 9, fy - 48), (fx + 13, fy - 14), (fx - 13, fy - 14)], fill=4)
    dr.rectangle([fx - 6, fy - 14, fx - 2, fy], fill=4); dr.rectangle([fx + 2, fy - 14, fx + 6, fy], fill=4)
    for i in range(24):  # a few ember/firefly specks
        ex, ey = rng.uniform(0, W), rng.uniform(0.45 * H, 0.95 * H)
        r = rng.uniform(1, 2.4)
        dr.ellipse([ex - r, ey - r, ex + r, ey + r], fill=int(rng.uniform(0.75, 1.0) * 255))
    return np.asarray(img).astype(np.float64) / 255.0


def apply_lut(g, lut):
    idx = np.clip((g * 255).round().astype(int), 0, 255)
    return (lut[idx] * 255).round().astype(np.uint8)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sheet", default=os.path.join("docs", "style_palettes.png"),
                    help="contact sheet path, relative to the project root (default docs/style_palettes.png)")
    ap.add_argument("--plate", default=None,
                    help="preview image (greyscale, centre-cropped to 640x360) instead of the built-in dusk scene: "
                         "use one of your own backgrounds")
    for _s in (sys.stdout, sys.stderr):  # help texts contain 残光 / ō / ：; never crash on a cp1252 / cp932 console
        try:
            _s.reconfigure(errors="replace")
        except Exception:  # noqa: BLE001
            pass
    args = ap.parse_args()
    sheet_path = str(kit_env.resolve(args.sheet))
    plate = kit_env.resolve(args.plate) if args.plate else None
    if plate and not plate.is_file():
        sys.exit(f"--plate: {plate} not found")
    os.makedirs(OUT_LUT, exist_ok=True)
    os.makedirs(os.path.dirname(sheet_path), exist_ok=True)

    scene = dusk_scene()   # always refreshed: tools/preview_style_fx.mjs renders onto it
    Image.fromarray((scene * 255).round().astype(np.uint8), 'L').save(os.path.join(OUT_STYLE, "dusk_scene_gray.png"))
    if plate:   # Rec.601 luma of the plate, same 640x360 frame as the dusk scene
        grey = ImageOps.fit(Image.open(plate).convert("L"), (640, 360), Image.LANCZOS)
        scene = np.asarray(grey).astype(np.float64) / 255.0
        print("plate", kit_env.rel(plate))
    H, W = scene.shape
    font = None
    for name in SHEET_FONTS:
        fp = kit_env.find_font(name)
        if fp:
            try:
                font = ImageFont.truetype(fp, 20); break
            except Exception:
                pass
    font = font or ImageFont.load_default()
    rows = []
    meta = {"global": GLOBAL, "palettes": []}
    for p in PALETTES:
        lut = build_lut(p["gradmap"])
        lut_duo = build_lut([[0, p["duotone"][0]], [1, p["duotone"][1]]])
        Image.fromarray((lut[None] * 255).round().astype(np.uint8)).save(os.path.join(OUT_LUT, p["id"] + ".png"))
        Image.fromarray((lut_duo[None] * 255).round().astype(np.uint8)).save(os.path.join(OUT_LUT, p["id"] + "_duo.png"))
        a = apply_lut(scene, lut)
        b = apply_lut(scene, lut_duo)
        c = 255 - a  # sudden inversion preview
        sw_h = 64
        row = Image.new('RGB', (W * 3 + 40, H + sw_h + 44), (18, 18, 20))
        row.paste(Image.fromarray(a), (10, sw_h + 34))
        row.paste(Image.fromarray(b), (W + 20, sw_h + 34))
        row.paste(Image.fromarray(c), (2 * W + 30, sw_h + 34))
        d = ImageDraw.Draw(row)
        d.text((10, 6), f"{p['name']}   — gradient map | duotone {p['duotone'][0]}↔{p['duotone'][1]} "
                        f"({contrast(*p['duotone']):.1f}:1) | inversion", fill=(235, 235, 235), font=font)
        roles = list(p["roles"].items())
        sw = (W * 3 + 20) / len(roles)
        for i, (k, h) in enumerate(roles):
            x0 = 10 + i * sw
            d.rectangle([x0, 32, x0 + sw - 4, 32 + sw_h - 8], fill=h)
            txtc = (0, 0, 0) if rel_lum(h) > 0.3 else (255, 255, 255)
            d.text((x0 + 6, 36), f"{k}", fill=txtc, font=font)
            d.text((x0 + 6, 60), h, fill=txtc, font=font)
        rows.append(row)
        pm = dict(p)
        pm["luminance"] = {h: round(rel_lum(h), 4) for h in p["roles"].values()}
        pm["duotone_contrast"] = round(contrast(*p["duotone"]), 2)
        pm["lut"] = f"assets/style/luts/{p['id']}.png"
        pm["lut_duotone"] = f"assets/style/luts/{p['id']}_duo.png"
        lums = [rel_lum(s[1]) for s in p["gradmap"]]
        pm["gradmap_monotonic"] = all(b2 >= a2 - 1e-9 for a2, b2 in zip(lums, lums[1:]))
        meta["palettes"].append(pm)
    sheet = Image.new('RGB', (rows[0].width, sum(r.height for r in rows)), (18, 18, 20))
    y = 0
    for r in rows:
        sheet.paste(r, (0, y)); y += r.height
    sheet.save(sheet_path, optimize=True)
    with open(os.path.join(OUT_STYLE, "palettes.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    for pm in meta["palettes"]:
        print(pm["id"], "duotone", pm["duotone_contrast"], "monotonic", pm["gradmap_monotonic"])
    print("sheet", sheet.size)


if __name__ == "__main__":
    main()
