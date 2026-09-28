#!/usr/bin/env python3
"""Картинки для соцсетей: 1200×630 PNG на каждую статью.

Запускать из корня:  python3 tools/make-og.py

Зачем: og:image без картинки — это серая строка в Telegram и Дзене,
то есть ровно в тех двух каналах, куда статьи и выкладывают. SVG
для og:image не годится: ни Telegram, ни Дзен, ни Facebook его не
принимают. Поэтому картинки растрируются headless Chrome'ом.

Карточка собирается из тех же данных, что sitemap и RSS (blog.html),
и из тех же цветовых токенов, что сайт (styles.css), — чтобы не
завести третью палитру, которая разъедется с сайтом.
"""
import importlib.util
import pathlib
import re
import shutil
import subprocess
import sys

ROOT = pathlib.Path(".").resolve()
OUT = ROOT / "img" / "og"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

W, H = 1200, 630


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


seo = load("seo", ROOT / "tools" / "make-seo.py")
chrome_src = load("chrome", ROOT / "tools" / "sync-chrome.py")


def tokens():
    """Цвета берём из styles.css, а не задаём заново."""
    css = (ROOT / "styles.css").read_text()
    root = css[css.index(":root {"):]
    root = root[:root.index("\n}")]
    out = {}
    for name, val in re.findall(r'--([a-z-]+):\s*(#[0-9A-Fa-f]{6})', root):
        out.setdefault(name, val)
    return out


T = tokens()


def mark_svg(colour, size):
    """Тот же знак, что в шапке сайта: три плашки, верхняя — в цвет раздела."""
    inner = chrome_src.MARK[chrome_src.MARK.index('>') + 1:-len('</symbol>')]
    inner = inner.replace('var(--mark-accent, currentColor)', colour)
    return (f'<svg viewBox="0 0 32 32" width="{size}" height="{size}" '
            f'fill="{T["ink"]}" aria-hidden="true">{inner}</svg>')


def card(title, kicker, topic, cover=None, accent_bar=True):
    tc = T[f"c-{topic}"]
    fill = T[f"c-{topic}-fill"]
    return f"""<!doctype html>
<html lang="ru"><head><meta charset="utf-8">
<style>
@font-face {{ font-family: Literata; font-weight: 400;
  src: url("fonts/literata-normal-cyrillic.woff2") format("woff2"); }}
@font-face {{ font-family: Literata; font-weight: 400;
  src: url("fonts/literata-normal-latin.woff2") format("woff2"); }}
@font-face {{ font-family: "JB Mono"; font-weight: 400;
  src: url("fonts/jetbrains-mono-normal-cyrillic.woff2") format("woff2"); }}
@font-face {{ font-family: "JB Mono"; font-weight: 400;
  src: url("fonts/jetbrains-mono-normal-latin.woff2") format("woff2"); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: {W}px; height: {H}px; }}
body {{
  font-family: Literata, Georgia, serif;
  background: {T['surface']};
  color: {T['ink']};
  display: flex; flex-direction: column;
  overflow: hidden;
}}
/* Полоса раздела сверху — тот же приём, что у панелей в ленте на главной:
   цвет живёт в узкой полосе, а не разливается по всей площади. */
.bar {{ height: 10px; background: {tc}; flex: none; }}
.body {{ flex: 1; display: flex; align-items: center; gap: 48px; padding: 56px 72px; }}
.text {{ flex: 1 1 auto; min-width: 0; }}
.brand {{ display: flex; align-items: center; gap: 12px; margin-bottom: 34px; }}
.brand svg {{ width: 34px; height: 34px; }}
.brand span {{
  font-family: "JB Mono", monospace; font-size: 19px;
  letter-spacing: .14em; text-transform: uppercase; color: {T['ink-muted']};
}}
.kicker {{
  font-family: "JB Mono", monospace; font-size: 16px;
  letter-spacing: .16em; text-transform: uppercase;
  color: {tc}; margin-bottom: 20px;
}}
h1 {{
  font-size: 58px; line-height: 1.1; font-weight: 400;
  letter-spacing: -.02em; text-wrap: balance;
}}
/* Крупная геометрическая плашка справа: даёт карточке цвет раздела
   и не тащит сюда саму иллюстрацию — на 630 px она превращается в кашу. */
/* Цветная шапка панели и её тон — тот же приём, что у панелей ленты
   на главной: opacity на контейнере гасила бы и полосу внутри,
   поэтому тон задаётся через color-mix, а не прозрачностью. */
.plate {{
  flex: none; width: 300px; height: 300px; border-radius: 48px;
  position: relative; overflow: hidden;
  background: color-mix(in srgb, {fill} 15%, {T['surface-raised']});
  border: 1px solid color-mix(in srgb, {fill} 26%, {T['hairline']});
  display: flex; align-items: center; justify-content: center;
  padding: 26px;
}}
.plate::before {{
  content: ''; position: absolute; inset: 0 0 auto 0; height: 8px;
  background: {tc};
}}
.plate img {{ width: 100%; height: 100%; object-fit: contain; }}
.foot {{
  flex: none; padding: 0 72px 46px;
  font-family: "JB Mono", monospace; font-size: 17px;
  letter-spacing: .1em; text-transform: uppercase; color: {T['ink-subtle']};
}}
</style></head>
<body>
  {'<div class="bar"></div>' if accent_bar else ''}
  <div class="body">
    <div class="text">
      <div class="brand">
        <svg viewBox="0 0 32 32" aria-hidden="true">{chrome_src.MARK[chrome_src.MARK.index('>')+1:-len('</symbol>')].replace('var(--mark-accent, currentColor)', tc)}</svg>
        <span>Понемногу</span>
      </div>
      <p class="kicker">{seo.esc(kicker)}</p>
      <h1>{seo.esc(title)}</h1>
    </div>
    <div class="plate">{f'<img src="{cover}" alt="">' if cover else mark_svg(tc, 150)}</div>
  </div>
  <p class="foot">Блог обо всём понемногу</p>
</body></html>"""


def render(html_text, out_png):
    tmp = ROOT / "_og-tmp.html"
    tmp.write_text(html_text)
    try:
        subprocess.run(
            [CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
             "--allow-file-access-from-files",
             f"--window-size={W},{H}", f"--screenshot={out_png}",
             "--virtual-time-budget=3000", f"file://{tmp}"],
            check=True, capture_output=True)
    finally:
        tmp.unlink(missing_ok=True)


def main():
    if not pathlib.Path(CHROME).exists():
        print(f"не нашёл Chrome: {CHROME}", file=sys.stderr)
        return 1
    OUT.mkdir(parents=True, exist_ok=True)

    made = []
    for a in seo.collect_articles(ROOT):
        out = OUT / (a["cover"].split("/")[-1].replace(".svg", ".png"))
        render(card(a["title"], a["kicker"], a["topic"], cover=a["cover"]), out)
        made.append(out.name)
        print(f"  {out.name}")

    # общая карточка для главной и служебных страниц
    render(card("Блог обо всём понемногу",
                "Деньги · бизнес · техника · спорт · жизнь", "dengi", accent_bar=False),
           OUT / "og-default.png")
    made.append("og-default.png")
    print("  og-default.png")
    print(f"итого картинок: {len(made)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
