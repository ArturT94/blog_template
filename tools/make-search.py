#!/usr/bin/env python3
"""Поисковый индекс: search-index.js.

Запускать из корня:  python3 tools/make-search.py

Почему не fetch(): сайт открывается по file://, а fetch из file:// браузер
режет политикой CORS. Тег <script> этому не подвержен, поэтому индекс — это
JS-файл с одной переменной, а не JSON. main.js подгружает его лениво:
до первого открытия поиска файл не скачивается вообще.

Текст берётся из <main> — то есть без шапки, подвала и спрайта иконок,
которые на всех страницах одинаковы и только засоряли бы выдачу.
"""
import html
import json
import pathlib
import re
import sys
import unicodedata

OUT = "search-index.js"

# Служебные страницы в поиске не нужны: 404 — это тупик, а не ответ.
SKIP = {"404.html"}


def text_of(page: pathlib.Path) -> str:
    """Видимый текст <main>: без тегов, скриптов и стилей."""
    t = page.read_text()
    if "<main" not in t:
        return ""
    body = t[t.index("<main"):]
    body = body[:body.index("</main>")] if "</main>" in body else body
    # Шапка статьи (надзаголовок, заголовок, лид) из текста убирается:
    # в выдаче они уже стоят отдельными строками, и сниппет начинался бы
    # с их повтора вместо самой статьи.
    body = re.sub(r'<header class="article__head">.*?</header>', " ", body, flags=re.S)
    body = re.sub(r"<(script|style|svg)\b.*?</\1>", " ", body, flags=re.S)
    body = re.sub(r"<[^>]+>", " ", body)
    body = html.unescape(body)
    # Тире, кавычки и неразрывные пробелы — к обычным: иначе поиск
    # по «кэшбэк» не найдёт «кэшбэк» с другим дефисом.
    body = unicodedata.normalize("NFKC", body)
    body = body.replace(" ", " ").replace("‑", "-").replace("–", "-")
    return re.sub(r"\s+", " ", body).strip()


def field(text: str, pattern: str) -> str:
    m = re.search(pattern, text, re.S)
    if not m:
        return ""
    return re.sub(r"\s+", " ", html.unescape(m.group(1))).strip()


def build(root: pathlib.Path):
    pages = sorted(p for p in root.glob("*.html") if not p.name.startswith("_"))
    out = []
    for p in pages:
        if p.name in SKIP:
            continue
        raw = p.read_text()
        # <title> = <h1> + « — Понемногу» на всех страницах, кроме главной,
        # поэтому берём его: он написан вручную под каждую страницу.
        title = re.sub(r"\s*—\s*Понемногу\s*$", "", field(raw, r"<title>(.*?)</title>"))
        if p.name == "index.html":
            title = "Главная"      # иначе в выдаче «Понемногу — блог обо всём…»

        # Надзаголовок ищем только внутри <main> и предпочитаем kicker--accent:
        # без этого первым находился служебный «Дальше — § 02» из нижней
        # навигации, и у всех статей в выдаче стоял чужой номер.
        main = raw[raw.index("<main"):] if "<main" in raw else raw
        kicker = field(main, r'class="[^"]*kicker--accent[^"]*"[^>]*>(.*?)</p>')
        if not kicker:
            kicker = field(main, r'class="[^"]*\bkicker\b[^"]*"[^>]*>(.*?)</p>')
        dek = field(raw, r'<meta name="description" content="([^"]*)"')
        topic = re.search(r'<body[^>]*data-c="([^"]+)"', raw)
        body = text_of(p)
        if not body:
            continue
        out.append({
            "u": p.name,
            "t": title,
            "k": re.sub(r"<[^>]+>", "", kicker),
            "d": dek,
            "c": topic.group(1) if topic else "",
            "b": body,
        })
    return out


def main() -> int:
    root = pathlib.Path(".")
    pages = build(root)
    if not pages:
        print("не нашёл ни одной страницы", file=sys.stderr)
        return 1

    # ensure_ascii=False: кириллица в \\uXXXX раздувает файл вдвое,
    # а экономить тут нечего — он всё равно отдаётся сжатым.
    payload = json.dumps({"p": pages}, ensure_ascii=False, separators=(",", ":"))
    (root / OUT).write_text(
        "/* Собирается из страниц: python3 tools/make-search.py\n"
        "   Руками не править — перезапишется. */\n"
        f"window.PONY_SEARCH={payload};\n")

    size = len(payload.encode())
    print(f"  страниц в индексе: {len(pages)}")
    print(f"  {OUT}: {size // 1024} КБ (сжатым по сети ~{size // 1024 // 4} КБ)")
    for p in pages:
        print(f"    {p['u']:20} {len(p['b']):>5} знаков")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
