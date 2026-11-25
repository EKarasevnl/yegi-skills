#!/usr/bin/env python3
"""
Export an HTML deck built with this skill to a 16:9 PPTX.

Renders each slide at 1920x1080 via headless Chromium, then assembles
into a PPTX with one full-bleed image per slide. The PPTX is ready to
upload to Google Slides.

Requirements:
    pip install python-pptx --break-system-packages
    pip install playwright --break-system-packages
    playwright install chromium

Usage:
    python3 export_pptx.py --input deck.html --output deck.pptx
    python3 export_pptx.py -i deck.html -o deck.pptx

Trade-off note: images preserve visual fidelity exactly, but text isn't
editable in Google Slides after import. If editable native shapes are
required, that's a much larger rebuild (lose polish, not recommended).
"""

import argparse
import asyncio
import os
import sys
import tempfile

from playwright.async_api import async_playwright
from pptx import Presentation
from pptx.util import Inches


HIDE_CSS = """
.nav, #slideNum, .slide-num, .key-hint { display: none !important; }
body { background: #FBF9F4 !important; }
"""


async def render_slides(html_path: str, render_dir: str) -> int:
    """Render each slide of the HTML deck to a PNG in render_dir.
    Returns the number of slides rendered."""
    abs_path = os.path.abspath(html_path)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()

        await page.goto(f'file://{abs_path}')
        await page.add_style_tag(content=HIDE_CSS)
        await page.wait_for_timeout(500)  # let fonts load

        total = await page.evaluate('document.querySelectorAll(".slide").length')
        print(f'Rendering {total} slides at 1920x1080...')

        for i in range(total):
            await page.evaluate(f'window.show && window.show({i}, true)')
            await page.wait_for_timeout(1600)  # let reveals, line drawing and bars settle
            out = os.path.join(render_dir, f'slide-{i+1:02d}.png')
            await page.screenshot(path=out, full_page=False)
            print(f'  Wrote slide {i+1}/{total}')

        await browser.close()
        return total


def assemble_pptx(render_dir: str, output_path: str) -> None:
    """Build a 16:9 PPTX from rendered PNGs in render_dir."""
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]  # blank layout

    slide_files = sorted(
        f for f in os.listdir(render_dir)
        if f.startswith('slide-') and f.endswith('.png')
    )

    for fn in slide_files:
        slide = prs.slides.add_slide(blank_layout)
        img_path = os.path.join(render_dir, fn)
        slide.shapes.add_picture(img_path, 0, 0,
                                 width=prs.slide_width,
                                 height=prs.slide_height)

    prs.save(output_path)
    size_mb = os.path.getsize(output_path) / 1024 / 1024
    print(f'Wrote {output_path} ({size_mb:.2f} MB)')


async def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('-i', '--input', required=True,
                    help='Path to the HTML deck file')
    ap.add_argument('-o', '--output', required=True,
                    help='Output PPTX path')
    ap.add_argument('--render-dir', default=None,
                    help='Where to write intermediate PNGs (default: temp dir)')
    args = ap.parse_args()

    if not os.path.exists(args.input):
        print(f'Error: input not found: {args.input}', file=sys.stderr)
        sys.exit(1)

    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)

    render_dir = args.render_dir
    cleanup = False
    if render_dir is None:
        render_dir = tempfile.mkdtemp(prefix='deck-slides-')
        cleanup = True
    else:
        os.makedirs(render_dir, exist_ok=True)

    try:
        await render_slides(args.input, render_dir)
        assemble_pptx(render_dir, args.output)
    finally:
        if cleanup:
            import shutil
            shutil.rmtree(render_dir, ignore_errors=True)


if __name__ == '__main__':
    asyncio.run(main())
