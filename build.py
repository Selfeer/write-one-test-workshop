#!/usr/bin/env python3
"""Build workshop/index.html from src/deck.html.

Inlines the Metropolis fonts and the GeoSTQB logo so the deck is one file that
works offline. Edit src/deck.html, then run: python3 workshop/build.py
"""
import base64
import re
from pathlib import Path

here = Path(__file__).resolve().parent
src = here / "src"

fonts = {400: "Regular", 600: "SemiBold", 700: "Bold", 800: "ExtraBold"}
font_css = "\n".join(
    "@font-face{font-family:'Metropolis';font-weight:%d;font-style:normal;font-display:block;"
    "src:url(data:font/woff2;base64,%s) format('woff2')}"
    % (weight, base64.b64encode((src / "fonts" / f"Metropolis-{name}.woff2").read_bytes()).decode())
    for weight, name in fonts.items()
)

# The logo's blue square has a cut-out around the lettering, so the slide
# background shows through it. The lettering takes --logo-text, which is white
# on the dark theme and black on the light one, as in the brand book.
logo = (src / "brand" / "geostqb-logo.svg").read_text()
view_box = re.search(r'viewBox="([^"]+)"', logo).group(1)
paths = re.search(r"<svg[^>]*>(.*)</svg>", logo, re.S).group(1)
paths = paths.replace('class="lt"', 'style="fill:var(--logo-text)"')
symbol = f'<symbol id="geostqb" viewBox="{view_box}">{paths}</symbol>'

html = (src / "deck.html").read_text()
html = html.replace("/*FONTS*/", font_css).replace("<!--LOGO_SYMBOL-->", symbol)
(here / "index.html").write_text(html)
print(f"wrote {here / 'index.html'} ({len(html) // 1024} KiB)")
