#!/usr/bin/env python3
"""Generate the BBROSE org-profile banner + divider SVGs.

Brand tokens are lifted verbatim from the live site:
  static/css/main.css  -> --background #F5EEE4, --foreground #1A1714,
                          --primary #B07080, --muted-foreground #8C7B72,
                          --border #E0D5CF
  main.css:433         -> signature wine #7A2233
The wordmark is the real logo (static/images/logo_transparent.png) embedded as
a data URI so the SVG needs no external fetch (GitHub renders README SVGs
inside <img>, where external references are blocked).

Usage:
    python3 tools/build_banners.py [path/to/website-repo]

The wordmark is read from the website repo's static/images/logo_transparent.png.
Pass that repo's path as the first argument, or set BBROSE_SITE.
"""
import base64
import os
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent.parent

SRC = pathlib.Path(
    sys.argv[1] if len(sys.argv) > 1
    else os.environ.get("BBROSE_SITE", HERE.parent / "bbrose-website")
)
LOGO = SRC / "static/images/logo_transparent.png"
if not LOGO.is_file():
    sys.exit(f"Wordmark not found: {LOGO}\nPass the website repo path as the first argument.")

OUT = HERE / "assets"
OUT.mkdir(parents=True, exist_ok=True)

LOGO_B64 = base64.b64encode(LOGO.read_bytes()).decode()

W, H = 1600, 460


def rose(cx, cy, scale, color, opacity, rot=0):
    """Abstract bloom echoing the rose inside the logo's O: rotated petal ellipses."""
    petals = []
    for a in (0, 36, 72, 108, 144):
        petals.append(f'<ellipse rx="78" ry="31" transform="rotate({a})"/>')
    for a in (18, 54, 90, 126, 162):
        petals.append(f'<ellipse rx="45" ry="18" transform="rotate({a})"/>')
    body = "".join(petals)
    return (
        f'<g transform="translate({cx},{cy}) scale({scale}) rotate({rot})" '
        f'fill="none" stroke="{color}" stroke-width="2.4" opacity="{opacity}">'
        f'{body}<circle r="5.5" fill="{color}" stroke="none"/></g>'
    )


def banner(theme):
    if theme == "light":
        bg, wash = "#F5EEE4", "#FCF8F2"
        accent = "#7A2233"          # signature wine
        frame = "#E0D5CF"
        tagline_fill = "#7A2233"
        micro_fill = "#8C7B72"
        logo_filter = ""            # logo art is already near-black
        motif_op = "0.10"
        halo_op = "0.05"
    else:
        bg, wash = "#141110", "#221B18"
        accent = "#C08494"          # brand rose, lifted for dark contrast
        frame = "#332B27"
        tagline_fill = "#D3A3AF"
        micro_fill = "#9C8A80"
        logo_filter = ' filter="url(#toCream)"'
        motif_op = "0.16"
        halo_op = "0.10"

    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="BBROSE — Beauty and Colour, crafted">
  <defs>
    <radialGradient id="wash" cx="28%" cy="18%" r="82%">
      <stop offset="0%" stop-color="{wash}"/>
      <stop offset="100%" stop-color="{bg}"/>
    </radialGradient>
    <radialGradient id="halo" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{accent}" stop-opacity="{halo_op}"/>
      <stop offset="100%" stop-color="{accent}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{accent}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{accent}" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="{accent}" stop-opacity="0"/>
    </linearGradient>
    <!-- recolour the black wordmark to warm cream for the dark banner -->
    <filter id="toCream" color-interpolation-filters="sRGB">
      <feColorMatrix type="matrix" values="-1 0 0 0 0.961  0 -1 0 0 0.933  0 0 -1 0 0.894  0 0 0 1 0"/>
    </filter>
    <clipPath id="frameClip"><rect width="{W}" height="{H}"/></clipPath>
  </defs>

  <rect width="{W}" height="{H}" fill="url(#wash)"/>
  <g clip-path="url(#frameClip)">
    <ellipse cx="{W//2}" cy="205" rx="620" ry="300" fill="url(#halo)"/>
    {rose(118, 96, 1.05, accent, motif_op, rot=-12)}
    {rose(1486, 372, 1.25, accent, motif_op, rot=22)}
    {rose(1420, 78, 0.62, accent, motif_op, rot=8)}
    {rose(182, 400, 0.55, accent, motif_op, rot=-30)}
  </g>
  <rect x="26" y="26" width="{W-52}" height="{H-52}" rx="3" fill="none" stroke="{frame}" stroke-width="1.25"/>

  <image x="{(W-560)//2}" y="118" width="560" height="146"
         preserveAspectRatio="xMidYMid meet"{logo_filter}
         xlink:href="data:image/png;base64,{LOGO_B64}"/>

  <rect x="{W//2 - 200}" y="300" width="400" height="1.4" fill="url(#rule)"/>
  <g transform="translate({W//2},301) rotate(45)">
    <rect x="-4.2" y="-4.2" width="8.4" height="8.4" fill="{accent}" opacity="0.9"/>
  </g>

  <text x="{W//2}" y="352" text-anchor="middle" fill="{tagline_fill}"
        font-family="Georgia, 'Times New Roman', 'Playfair Display', serif"
        font-size="27" font-style="italic" letter-spacing="3.4">Beauty &amp; Colour, crafted</text>

  <text x="{W//2}" y="404" text-anchor="middle" fill="{micro_fill}"
        font-family="'Helvetica Neue', Helvetica, Arial, sans-serif"
        font-size="15.5" font-weight="500" letter-spacing="6.2">MAKEUP &#183; SKINCARE &#183; HAIR COLOUR &#183; NAILS &#183; PRIVATE LABEL</text>
</svg>
'''


def divider():
    """One theme-neutral rule. Brand rose sits legibly on both cream and near-black,
    so the page needs a single asset here rather than a <picture> swap."""
    accent = "#B07080"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="28" viewBox="0 0 1600 28" role="presentation">
  <defs>
    <linearGradient id="d" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{accent}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{accent}" stop-opacity="0.7"/>
      <stop offset="100%" stop-color="{accent}" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect x="0" y="13.4" width="1600" height="1.3" fill="url(#d)"/>
  <g transform="translate(800,14) rotate(45)">
    <rect x="-4.2" y="-4.2" width="8.4" height="8.4" fill="{accent}" opacity="0.9"/>
  </g>
  <g transform="translate(752,14) rotate(45)">
    <rect x="-2.4" y="-2.4" width="4.8" height="4.8" fill="{accent}" opacity="0.55"/>
  </g>
  <g transform="translate(848,14) rotate(45)">
    <rect x="-2.4" y="-2.4" width="4.8" height="4.8" fill="{accent}" opacity="0.55"/>
  </g>
</svg>
'''


for theme in ("light", "dark"):
    (OUT / f"banner-{theme}.svg").write_text(banner(theme))
    print(f"wrote banner-{theme}.svg")

(OUT / "divider.svg").write_text(divider())
print("wrote divider.svg")
print("logo base64 chars:", len(LOGO_B64))
