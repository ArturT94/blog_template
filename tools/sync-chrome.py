#!/usr/bin/env python3
"""Шапка, подвал и спрайт иконок — в одном месте.

Правит все .html в корне: находит блоки по маркерам @chrome:* и заменяет их.
Запускать из корня после правки этого файла:  python3 tools/sync-chrome.py
"""
import pathlib
import re
import sys

# --------------------------------------------------------------------------
# Иконки. Штриховые, 24×24, currentColor — значит наследуют тему страницы.
# --------------------------------------------------------------------------
ICONS = {
    "menu": '<path d="M3.5 7h17M3.5 12h17M3.5 17h17"/>',
    "close": '<path d="M6 6l12 12M18 6L6 18"/>',
    "arrow-right": '<path d="M4 12h15M13.5 6.5L19 12l-5.5 5.5"/>',
    "arrow-left": '<path d="M20 12H5M10.5 6.5L5 12l5.5 5.5"/>',
    "arrow-up": '<path d="M12 20V5M6.5 10.5L12 5l5.5 5.5"/>',
    "arrow-down": '<path d="M12 4v15M6.5 13.5L12 19l5.5-5.5"/>',
    "sun": ('<circle cx="12" cy="12" r="4.2"/><path d="M12 2.4v2.6M12 19v2.6M2.4 12h2.6M19 12h2.6'
            'M5.2 5.2l1.9 1.9M16.9 16.9l1.9 1.9M18.8 5.2l-1.9 1.9M7.1 16.9l-1.9 1.9"/>'),
    "moon": '<path d="M20.5 14.6A8.6 8.6 0 0 1 9.4 3.5a8.6 8.6 0 1 0 11.1 11.1z"/>',
    "clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.2V12l3.2 2"/>',
    "calendar": ('<rect x="3.5" y="5.5" width="17" height="15" rx="1.5"/>'
                 '<path d="M3.5 10h17M8 3.5v4M16 3.5v4"/>'),
    "mail": '<rect x="3" y="5.5" width="18" height="13" rx="1.5"/><path d="M3.6 7l8.4 6 8.4-6"/>',
    "send": '<path d="M21 3.5L10.5 14M21 3.5l-6.5 17-4-8-8-4z"/>',
    "rss": '<path d="M5 18.5a.5.5 0 1 0 0-1 .5.5 0 0 0 0 1z"/><path d="M4.5 11.5a8 8 0 0 1 8 8M4.5 5a14.5 14.5 0 0 1 14.5 14.5"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 6.5"/>',
    "book": ('<path d="M4 4.5h6a3 3 0 0 1 3 3v12a2.5 2.5 0 0 0-2.5-2.5H4z"/>'
             '<path d="M20 4.5h-6a3 3 0 0 0-3 3v12a2.5 2.5 0 0 1 2.5-2.5H20z"/>'),
    "link": ('<path d="M10 13.5a4 4 0 0 0 5.7 0l2.8-2.8a4 4 0 0 0-5.7-5.7l-1.4 1.4"/>'
             '<path d="M14 10.5a4 4 0 0 0-5.7 0l-2.8 2.8a4 4 0 0 0 5.7 5.7l1.4-1.4"/>'),
    "chevron-down": '<path d="M6 9.5l6 6 6-6"/>',
    "user": '<circle cx="12" cy="8.5" r="3.8"/><path d="M4.5 20.5a7.5 7.5 0 0 1 15 0"/>',
    "grid": ('<rect x="3.5" y="3.5" width="7" height="7" rx="1"/><rect x="13.5" y="3.5" width="7" height="7" rx="1"/>'
             '<rect x="3.5" y="13.5" width="7" height="7" rx="1"/><rect x="13.5" y="13.5" width="7" height="7" rx="1"/>'),
    "external": '<path d="M14 4.5h5.5V10M19.5 4.5L11 13"/><path d="M18 14.5v4a1.5 1.5 0 0 1-1.5 1.5h-11A1.5 1.5 0 0 1 4 18.5v-11A1.5 1.5 0 0 1 5.5 6h4"/>',
    "shield": '<path d="M12 3.5l7 2.6v6c0 4.2-2.9 7.4-7 8.4-4.1-1-7-4.2-7-8.4v-6z"/>',
    "list": '<path d="M9 6.5h11M9 12h11M9 17.5h11M4.5 6.5h.01M4.5 12h.01M4.5 17.5h.01"/>',
    "quote": '<path d="M9.5 6.5C6.7 8 5.5 10.4 5.5 13.8c0 2.3 1.2 3.7 3 3.7 1.6 0 2.8-1.2 2.8-2.8 0-1.5-1-2.6-2.5-2.6-.3 0-.6 0-.8.1.3-1.6 1.3-2.9 2.9-3.9zM19 6.5c-2.8 1.5-4 3.9-4 7.3 0 2.3 1.2 3.7 3 3.7 1.6 0 2.8-1.2 2.8-2.8 0-1.5-1-2.6-2.5-2.6-.3 0-.6 0-.8.1.3-1.6 1.3-2.9 2.9-3.9z"/>',
    "filter": '<path d="M3.5 5.5h17l-6.5 8v5.5l-4 2v-7.5z"/>',
    "search": '<circle cx="10.8" cy="10.8" r="6.6"/><path d="M15.6 15.6L21 21"/>',
}

# Фирменный знак. Не штриховой, поэтому лежит отдельно от ICONS.
# Три плашки: каждая выше шире и правее предыдущей — знак растёт вверх,
# «понемногу, слой за слоем». Верхняя красится в --mark-accent, если он
# задан; иначе в цвет текста.
# Плашек именно три, и они толстые: на четырёх тонких знак в шапке
# сливался в полоску и читался как значок меню.
MARK = ('<symbol id="i-mark" viewBox="0 0 32 32">'
        '<rect x="3.4" y="23.8" width="12.0" height="7.2" rx="3.6" fill="currentColor"/>'
        '<rect x="7.0" y="12.4" width="15.6" height="7.2" rx="3.6" fill="currentColor"/>'
        '<rect x="10.6" y="1.0" width="19.2" height="7.2" rx="3.6" fill="var(--mark-accent, currentColor)"/>'
        '</symbol>')

SPRITE_OPEN = '<!-- @chrome:sprite — правится в tools/sync-chrome.py -->'
SPRITE = SPRITE_OPEN + '''
<svg class="sprite" aria-hidden="true" focusable="false" width="0" height="0" style="position:absolute">
<defs>
''' + "\n".join(
    f'<symbol id="i-{n}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    f'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{p}</symbol>'
    for n, p in ICONS.items()) + "\n" + MARK + '''
</defs>
</svg>'''

# --------------------------------------------------------------------------
# Навигация. Один список — и для строки в шапке, и для мобильной панели.
# --------------------------------------------------------------------------
NAV = [
    ("blog.html", "Истории"),
    ("o-sebe.html", "Об авторе"),
    ("voprosy.html", "Вопросы"),
    ("chestno.html", "Честно о ссылках"),
    ("sotrudnichestvo.html", "Сотрудничество"),
]

# Разделы блога. Один список на подвал и на разводящую: цвета живут в styles.css
# под именами --c-<ключ>, поэтому здесь только ключ и название.
TOPICS = [
    ("dengi",    "Деньги"),
    ("biznes",   "Бизнес"),
    ("it",       "ИТ"),
    ("sport",    "Спорт"),
    ("zhizn",    "Жизнь"),
]

# какая страница подсвечивает какой пункт
ACTIVE = {
    "index.html": None, "blog.html": "blog.html",
    "perevody.html": "blog.html", "keshbek.html": "blog.html", "kopilka.html": "blog.html",
    "karty.html": "blog.html", "prilozheniya.html": "blog.html",
    "bezopasnost.html": "blog.html", "byudzhet.html": "blog.html",
    "biznes.html": "blog.html", "it.html": "blog.html",
    "sport.html": "blog.html", "zhizn.html": "blog.html",
    "o-sebe.html": "o-sebe.html", "voprosy.html": "voprosy.html",
    "chestno.html": "chestno.html",
    "sotrudnichestvo.html": "sotrudnichestvo.html", "404.html": None,
}

MASTHEAD_OPEN = '<!-- @chrome:masthead — правится в tools/sync-chrome.py -->'


def masthead(page: str) -> str:
    cur = ACTIVE.get(page)
    CUR = ' aria-current="page"'
    links = "\n".join(
        f'          <a href="{h}"{CUR if h == cur else ""}>'
        f'<span class="nav__n">{i:02d}</span>{t}</a>'
        for i, (h, t) in enumerate(NAV, 1))
    return MASTHEAD_OPEN + f'''
<header class="masthead">
  <div class="wrap">
    <div class="masthead__meta">
      <span>Блог обо всём понемногу</span>
      <span>Выпуск № 12 — сентябрь 2026</span>
    </div>

    <div class="masthead__bar">
      <a class="wordmark" href="index.html">
        <svg class="mark" aria-hidden="true"><use href="#i-mark"></use></svg>
        <span>Понемногу</span>
      </a>

      <div class="masthead__tools">
        <nav class="nav" id="nav" aria-label="Основная навигация">
{links}
        </nav>

        <!-- Без JS это обычная ссылка на blog.html, где перечислены все
             истории с фильтром по разделам. С JS main.js перехватывает
             клик и открывает панель поиска. -->
        <a class="search-open" href="blog.html" aria-label="Поиск по сайту" title="Поиск — клавиша /">
          <svg class="icon" aria-hidden="true"><use href="#i-search"></use></svg>
        </a>

        <button class="theme" type="button" aria-pressed="false" aria-label="Переключить тему">
          <svg class="icon-sun" aria-hidden="true"><use href="#i-sun"></use></svg>
          <svg class="icon-moon" aria-hidden="true"><use href="#i-moon"></use></svg>
        </button>

        <button class="burger" type="button" id="burger"
                aria-expanded="false" aria-controls="nav" aria-label="Меню">
          <svg class="burger__open" aria-hidden="true"><use href="#i-menu"></use></svg>
          <svg class="burger__close" aria-hidden="true"><use href="#i-close"></use></svg>
        </button>
      </div>
    </div>
  </div>
</header>
<div class="drawer-scrim" id="scrim" hidden></div>

<div class="search" id="search" hidden>
  <div class="search__veil" data-search-close></div>
  <div class="search__panel" role="dialog" aria-modal="true" aria-label="Поиск по сайту">
    <div class="search__field">
      <svg class="search__icon" aria-hidden="true"><use href="#i-search"></use></svg>
      <input class="search__input" id="search-input" type="search" autocomplete="off"
             spellcheck="false" placeholder="Кэшбэк, переводы, бюджет…"
             aria-label="Поисковый запрос" aria-describedby="search-status">
      <button class="search__close" type="button" data-search-close aria-label="Закрыть поиск">
        <svg class="icon" aria-hidden="true"><use href="#i-close"></use></svg>
      </button>
    </div>
    <p class="search__status" id="search-status" role="status">Начните печатать — ищу по всем историям и страницам.</p>
    <ul class="search__list" id="search-list"></ul>
  </div>
</div>'''


FOOTER_OPEN = '<!-- @chrome:footer — правится в tools/sync-chrome.py -->'
FOOTER = FOOTER_OPEN + '''
<footer class="colophon">
  <div class="wrap">
    <div class="colophon__grid">

      <div>
        <h4>О блоге</h4>
        <p>
          «Понемногу» — блог обо всём понемногу: деньги, работа, техника,
          спорт, жизнь. Пишет один человек, без редакции. В части текстов
          есть партнёрские ссылки и помеченная реклама — и то и другое
          обозначено прямо в тексте.
        </p>
      </div>

      <div>
        <h4>Разделы</h4>
        <ul>
          <li><a href="blog.html#dengi">Деньги</a></li>
          <li><a href="blog.html#biznes">Бизнес</a></li>
          <li><a href="blog.html#it">ИТ</a></li>
          <li><a href="blog.html#sport">Спорт</a></li>
          <li><a href="blog.html#zhizn">Жизнь</a></li>
          <li><a href="blog.html">Все истории</a></li>
        </ul>
      </div>

      <div>
        <h4>Страницы</h4>
        <ul>
          <li><a href="o-sebe.html">Об авторе</a></li>
          <li><a href="voprosy.html">Вопросы и ответы</a></li>
          <li><a href="chestno.html">Честно о ссылках</a></li>
          <li><a href="sotrudnichestvo.html">Сотрудничество</a></li>
          <li><a href="feed.xml"><svg class="icon" aria-hidden="true"><use href="#i-rss"></use></svg>RSS-подписка</a></li>
        </ul>
      </div>

      <div>
        <h4>Связаться</h4>
        <ul>
          <li><a href="mailto:hi@example.com"><svg class="icon" aria-hidden="true"><use href="#i-mail"></use></svg>hi@example.com</a></li>
          <li><a href="REPLACE_TELEGRAM_LINK" rel="noopener" target="_blank"><svg class="icon" aria-hidden="true"><use href="#i-send"></use></svg>Телеграм-канал</a></li>
        </ul>
        <p class="colophon__note">
          Отвечаю сам, обычно в течение дня. По вопросам партнёрской
          программы — тоже сюда.
        </p>
      </div>

    </div>

    <div class="colophon__base">
      <span>© 2026 Понемногу</span>
      <span>Набрано Literata и JetBrains Mono</span>
      <span>Партнёрские ссылки помечены</span>
      <a class="colophon__top" href="#top"><svg class="icon" aria-hidden="true"><use href="#i-arrow-up"></use></svg>Наверх</a>
    </div>
  </div>
</footer>'''


def stamp(text: str, page: str) -> str:
    head = masthead(page)

    # Границы блоков привязаны к тому, что идёт СЛЕДУЮЩИМ за блоком,
    # а не к первому закрывающему тегу внутри: в шапке таких тегов десяток,
    # и нежадный шаблон обрывал её на середине.
    if SPRITE_OPEN in text:
        text = re.sub(re.escape(SPRITE_OPEN) + r'.*?</svg>', lambda m: SPRITE, text, flags=re.S)
    else:
        text = re.sub(r'(<body[^>]*>\s*)', lambda m: m.group(1) + SPRITE + "\n\n", text, count=1)

    if MASTHEAD_OPEN in text:
        text = re.sub(re.escape(MASTHEAD_OPEN) + r'.*?(?=<main)', lambda m: head + "\n\n", text, flags=re.S)
    elif '<header class="masthead">' in text:
        text = re.sub(r'<header class="masthead">.*?</header>\s*(?:<div class="drawer-scrim"[^>]*></div>)?',
                      lambda m: head, text, flags=re.S)
    else:
        # новая страница: шапки ещё нет — ставим перед <main>
        text = re.sub(r'(?=<main)', head + "\n\n", text, count=1)

    if FOOTER_OPEN in text:
        text = re.sub(re.escape(FOOTER_OPEN) + r'.*?(?=</body>)', lambda m: FOOTER + "\n", text, flags=re.S)
    elif '<footer class="colophon">' in text:
        text = re.sub(r'<footer class="colophon">.*?</footer>', lambda m: FOOTER, text, flags=re.S)
    else:
        text = re.sub(r'(?=</body>)', FOOTER + "\n\n", text, count=1)

    # Светлая тема — оформление по умолчанию, и оно должно работать даже
    # без JS. Ставим атрибут прямо в <html>; переключатель потом может
    # переопределить его на тёмную. Скрипт темы в <head> тоже читает
    # localStorage, но полагаться только на него нельзя.
    # re.search, а не re.match: файл начинается с <!doctype html>, и match
    # не находил тег вовсе — правка молча ничего не делала.
    m = re.search(r'<html\b[^>]*>', text)
    if m and 'data-theme=' not in m.group(0):
        text = text[:m.end() - 1] + ' data-theme="light"' + text[m.end() - 1:]

    if 'id="top"' not in text:
        text = re.sub(r'<body>', '<body id="top">', text, count=1)
    return text


def main():
    root = pathlib.Path(".")
    pages = sorted(p for p in root.glob("*.html") if not p.name.startswith("_"))
    if not pages:
        print("не нашёл ни одной страницы", file=sys.stderr)
        return 1
    for p in pages:
        src = p.read_text()
        out = stamp(src, p.name)
        if out != src:
            p.write_text(out)
            print(f"  обновлена {p.name}")
        else:
            print(f"  без изменений {p.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
