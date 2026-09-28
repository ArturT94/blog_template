#!/usr/bin/env python3
"""Canonical, Open Graph, микроразметка, sitemap, robots и счётчик — в одном месте.

Читает разметку страниц и blog.html, дописывает в <head> каждой страницы
блок @seo и заново собирает sitemap.xml, robots.txt и feed.xml.

Запускать из корня после правки статей:  python3 tools/make-seo.py

ПОЧЕМУ ТАК, А НЕ РУКАМИ: canonical, og:url, sitemap и RSS — это четыре копии
одного и того же списка адресов. Стоит добавить статью и забыть про одну из
копий, и поисковик получает противоречивые сигналы. Здесь список один —
blog.html, — а всё остальное из него выводится.
"""
import html
import pathlib
import re
import sys
import unicodedata

# --------------------------------------------------------------------------
# ЧТО ЗАПОЛНИТЬ ПЕРЕД ПУБЛИКАЦИЕЙ
# --------------------------------------------------------------------------
# Домен. Пока тут заглушка, инструмент считает сайт неопубликованным:
# в robots.txt он закроет его от индексации целиком. Это защита от
# конкретной ошибки — выложить папку на хостинг раньше, чем вписаны
# реферальные ссылки, и получить в индексе двадцать три заглушки.
# Впишете домен — робот откроется сам.
SITE = "https://REPLACE-DOMAIN"

# Номер счётчика Яндекс.Метрики. Пока заглушка — сниппет не вставляется
# вовсе (счётчик с несуществующим номером только сыпет ошибками в консоль).
METRIKA_ID = "REPLACE_METRIKA_ID"

AUTHOR = "Артур Тарасов"
LANG = "ru-RU"

# Разделы: ключ (он же data-c на <body>) → человеческое название и адрес.
TOPICS = {
    "dengi":  ("Деньги",  "blog.html#dengi"),
    "biznes": ("Бизнес",  "blog.html#biznes"),
    "it":     ("ИТ",      "blog.html#it"),
    "sport":  ("Спорт",   "blog.html#sport"),
    "zhizn":  ("Жизнь",   "blog.html#zhizn"),
}

# Страницы, которых в поиске быть не должно, и почему.
NOINDEX = {
    "404.html": "страница ошибки — в индексе ей делать нечего",
}

MONTHS = {
    "января": 1, "февраля": 2, "марта": 3, "апреля": 4, "мая": 5, "июня": 6,
    "июля": 7, "августа": 8, "сентября": 9, "октября": 10, "ноября": 11,
    "декабря": 12,
}

SEO_OPEN = "<!-- @seo — правится в tools/make-seo.py -->"
SEO_CLOSE = "<!-- /@seo -->"

# Заголовок страницы и её описание лежат в <head> и остаются рукописными:
# инструмент их только читает. Всё, что он пишет, — ниже.


def esc(s: str) -> str:
    """Для HTML-атрибутов."""
    return html.escape(s, quote=True)


def jesc(s: str) -> str:
    """Для JSON внутри <script type="application/ld+json">.

    Экранировать там по-html нельзя: <script> — raw text element, браузер
    не разбирает его содержимое как разметку, и &quot; попадёт в JSON как
    есть, сломав его. Зато '<' надо уводить в \\u003c: иначе строка,
    содержащая </script>, закроет блок раньше времени."""
    return (s.replace("\\", "\\\\").replace('"', '\\"')
             .replace("<", "\\u003c").replace(">", "\\u003e")
             .replace("\n", "\\n").replace("\r", "\\r"))


def clean_title(raw: str) -> str:
    """Заголовок карточки -> строка без разметки и неразрывных пробелов."""
    s = html.unescape(raw).replace(" ", " ")
    return re.sub(r"\s+", " ", s).strip()


def iso_date(ru: str) -> str:
    d, mon, y = ru.split()
    return f"{y}-{MONTHS[mon.lower()]:02d}-{int(d):02d}"


# --------------------------------------------------------------------------
# Сбор статей. Источник — blog.html: он и так редактируется вручную,
# и дублировать список статей где-то ещё значит однажды их разойтись.
# --------------------------------------------------------------------------
def collect_articles(root: pathlib.Path):
    blog = (root / "blog.html").read_text()
    cards = re.findall(r'<li class="card"[^>]*>(.*?)</li>', blog, re.S)
    arts, need = [], False
    for body in cards:
        href = re.search(r'href="([^"]+\.html)"', body).group(1)
        page = root / href
        if not page.exists():
            print(f"  ! в blog.html есть {href}, а файла нет — пропускаю", file=sys.stderr)
            need = True
            continue
        text = page.read_text()
        topic = re.search(r'<body[^>]*data-c="([^"]+)"', text)
        desc = re.search(r'<meta name="description" content="([^"]*)"', text)
        arts.append({
            "file": href,
            "title": clean_title(re.search(r'card__title">([^<]*)<', body).group(1)),
            "kicker": clean_title(re.search(r'card__no">([^<]*)<', body).group(1)),
            "dek": clean_title(re.search(r'card__dek">([^<]*)<', body).group(1)),
            "cover": re.search(r'src="(img/[^"]+)"', body).group(1),
            "minutes": int(re.search(r'<span>(\d+) минут</span>', body).group(1)),
            "date": iso_date(re.search(r'<span>(\d{1,2} \w+ \d{4})</span>', body).group(1)),
            "topic": topic.group(1) if topic else "dengi",
            "desc": clean_title(desc.group(1)) if desc else "",
        })
    return arts


def head_meta(text: str):
    """title и description страницы — рукописные, только читаем."""
    t = re.search(r'<title>([^<]*)</title>', text)
    d = re.search(r'<meta name="description" content="([^"]*)"', text)
    return (clean_title(t.group(1)) if t else "Понемногу",
            clean_title(d.group(1)) if d else "")


# --------------------------------------------------------------------------
# Блок @seo: canonical, Open Graph, Twitter, микроразметка
# --------------------------------------------------------------------------
def seo_block(page: str, title: str, desc: str, art, is_index: bool, noindex: bool) -> str:
    url = f"{SITE}/{'' if page == 'index.html' else page}"
    img = f"{SITE}/{art['cover'].replace('.svg', '.png').replace('img/', 'img/og/')}" if art \
        else f"{SITE}/img/og/og-default.png"

    lines = [SEO_OPEN]
    # canonical: без него /index.html и / считаются двумя разными страницами
    lines.append(f'<link rel="canonical" href="{esc(url)}">')
    if noindex:
        lines.append(f'<meta name="robots" content="noindex, follow">')

    # Open Graph. og:image обязателен: без него Telegram и Дзен показывают
    # ссылку серой строкой, а это ровно те два канала, куда вы будете
    # выкладывать статьи.
    lines.append(f'<meta property="og:type" content="{"article" if art else "website"}">')
    lines.append(f'<meta property="og:site_name" content="Понемногу">')
    lines.append(f'<meta property="og:locale" content="ru_RU">')
    lines.append(f'<meta property="og:url" content="{esc(url)}">')
    lines.append(f'<meta property="og:title" content="{esc(title)}">')
    lines.append(f'<meta property="og:description" content="{esc(art["dek"] if art else desc)}">')
    lines.append(f'<meta property="og:image" content="{esc(img)}">')
    lines.append('<meta property="og:image:width" content="1200">')
    lines.append('<meta property="og:image:height" content="630">')
    lines.append('<meta property="og:image:alt" content="'
                 f'{esc(title)}">')
    if art:
        lines.append(f'<meta property="article:published_time" content="{art["date"]}">')
        lines.append(f'<meta property="article:section" content="{esc(TOPICS[art["topic"]][0])}">')

    # Twitter-карточка: своя, потому что og:image она читает, но тип и
    # заголовок берёт из twitter:*, если они есть.
    lines.append('<meta name="twitter:card" content="summary_large_image">')
    lines.append(f'<meta name="twitter:title" content="{esc(title)}">')
    lines.append(f'<meta name="twitter:description" content="{esc(art["dek"] if art else desc)}">')
    lines.append(f'<meta name="twitter:image" content="{esc(img)}">')

    # graph() уже вернул готовый JSON — здесь никакого экранирования быть не должно
    lines.append('<script type="application/ld+json">'
                 + graph(page, title, desc, art, url, img, is_index) + '</script>')
    lines.append(SEO_CLOSE)
    return "\n".join(lines) + "\n"


def graph(page, title, desc, art, url, img, is_index) -> str:
    """JSON-LD. Собирается вручную, а не json.dumps всего словаря, чтобы
    порядок ключей был предсказуемым и файл не переписывался целиком
    при каждом запуске (иначе git показывает правку там, где её нет)."""
    site = (f'{{"@type":"WebSite","@id":"{SITE}/#site","url":"{SITE}/",'
            f'"name":"Понемногу","inLanguage":"ru-RU",'
            f'"description":"Блог обо всём понемногу: деньги, бизнес, техника, спорт, жизнь."}}')
    person = (f'{{"@type":"Person","@id":"{SITE}/#author","name":"{AUTHOR}",'
              f'"url":"{SITE}/o-sebe.html"}}')
    publisher = (f'{{"@type":"Organization","@id":"{SITE}/#publisher",'
                 f'"name":"Понемногу","url":"{SITE}/"}}')

    nodes = [site, person, publisher]
    if art:
        nodes.append(
            f'{{"@type":"BlogPosting","@id":"{url}#article",'
            f'"mainEntityOfPage":"{url}","headline":"{jesc(art["title"])}",'
            f'"description":"{jesc(art["dek"])}","image":"{img}",'
            f'"datePublished":"{art["date"]}","dateModified":"{art["date"]}",'
            f'"inLanguage":"ru-RU","articleSection":"{jesc(TOPICS[art["topic"]][0])}",'
            f'"author":{{"@id":"{SITE}/#author"}},'
            f'"publisher":{{"@id":"{SITE}/#publisher"}},'
            f'"isPartOf":{{"@id":"{SITE}/#site"}}}}')
        # Хлебные крошки: поисковик показывает их вместо голого адреса
        nodes.append(
            f'{{"@type":"BreadcrumbList","itemListElement":['
            f'{{"@type":"ListItem","position":1,"name":"Главная","item":"{SITE}/"}},'
            f'{{"@type":"ListItem","position":2,"name":"Истории","item":"{SITE}/blog.html"}},'
            f'{{"@type":"ListItem","position":3,"name":"{jesc(art["title"])}"}}]}}')
    return '{"@context":"https://schema.org","@graph":[' + ",".join(nodes) + ']}'


# --------------------------------------------------------------------------
# sitemap.xml, robots.txt, feed.xml
# --------------------------------------------------------------------------
def write_sitemap(root: pathlib.Path, pages, arts):
    by_file = {a["file"]: a for a in arts}
    # Главная — с максимальным приоритетом, статьи — по дате публикации.
    # Служебные страницы идут первыми в этом порядке, но список ими
    # не исчерпывается: всё, что не статья и не закрыто noindex,
    # дописывается следом. Раньше порядок был жёстким, и новая страница
    # просто не попадала в карту сайта — молча, без единой ошибки.
    urls = []
    lead = ["index.html", "blog.html", "o-sebe.html", "voprosy.html", "chestno.html"]
    order = [x for x in lead if x in pages] + [a["file"] for a in arts]
    order += sorted(x for x in pages if x not in order and x not in NOINDEX)
    for page in order:
        if page not in pages:
            continue
        art = by_file.get(page)
        loc = f"{SITE}/" if page == "index.html" else f"{SITE}/{page}"
        lastmod = art["date"] if art else "2026-09-27"
        prio = "1.0" if page == "index.html" else ("0.6" if art else "0.5")
        urls.append(f"  <url>\n    <loc>{esc(loc)}</loc>\n"
                    f"    <lastmod>{lastmod}</lastmod>\n"
                    f"    <changefreq>{'monthly' if art else 'weekly'}</changefreq>\n"
                    f"    <priority>{prio}</priority>\n  </url>")
    body = ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<!-- Собирается из blog.html: python3 tools/make-seo.py -->\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(urls) + "\n</urlset>\n")
    return body


def write_robots() -> str:
    draft = "REPLACE-DOMAIN" in SITE
    if draft:
        return ("# Домен ещё не вписан (tools/make-seo.py, константа SITE),\n"
                "# поэтому сайт закрыт от индексации целиком. Это не забывчивость,\n"
                "# а защита: пока в статьях стоят заглушки вместо реферальных\n"
                "# ссылок, в поиске им делать нечего. Впишете домен — откроется.\n"
                "User-agent: *\n"
                "Disallow: /\n")
    return ("User-agent: *\n"
            "Allow: /\n"
            "Disallow: /404.html\n"
            "\n"
            f"Sitemap: {SITE}/sitemap.xml\n")


def write_feed(root: pathlib.Path, arts) -> str:
    """RSS собирается из того же списка, что sitemap и og: — чтобы даты
    и описания не разъезжались. В ленте нужен именно дек карточки:
    он написан как самостоятельная фраза, а meta description — как
    продолжение заголовка."""
    items = []
    for a in sorted(arts, key=lambda x: x["date"], reverse=True):
        d = a["date"]
        rfc = f"{d}, 09:00:00 +0300"
        items.append(
            "    <item>\n"
            f"      <title>{esc(a['title'])}</title>\n"
            f"      <link>{SITE}/{a['file']}</link>\n"
            f"      <guid isPermaLink=\"true\">{SITE}/{a['file']}</guid>\n"
            f"      <pubDate>{rfc}</pubDate>\n"
            f"      <category>Про {TOPICS[a['topic']][0].lower()}</category>\n"
            f"      <description>{esc(a['dek'])}</description>\n"
            "    </item>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<!-- Собирается из blog.html: python3 tools/make-seo.py -->\n'
            '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
            '  <channel>\n'
            '    <title>Понемногу</title>\n'
            f'    <link>{SITE}/</link>\n'
            '    <description>Блог обо всём понемногу: деньги, бизнес, техника, '
            'спорт, жизнь. Истории с цифрами из собственных выписок. '
            'Партнёрские ссылки всегда помечены.</description>\n'
            '    <language>ru</language>\n'
            f'    <lastBuildDate>{sorted(a["date"] for a in arts)[-1]}, 09:00:00 +0300</lastBuildDate>\n'
            f'    <atom:link href="{SITE}/feed.xml" rel="self" type="application/rss+xml"/>\n'
            + "\n".join(items) + "\n  </channel>\n</rss>\n")


# --------------------------------------------------------------------------
# Счётчик
# --------------------------------------------------------------------------
def metrika() -> str:
    """Счётчик ставится перед </body>, а не в <head>: так он не задерживает
    отрисовку. Вебвизор выключен намеренно — он записывает сессии целиком,
    а это уже персональные данные, и для него нужно отдельное уведомление
    на сайте. Включите, когда это уведомление появится."""
    if "REPLACE" in METRIKA_ID:
        return ""
    return f'''
<!-- Яндекс.Метрика — правится в tools/make-seo.py -->
<script>
(function (m, e, t, r, i, k, a) {{
  m[i] = m[i] || function () {{ (m[i].a = m[i].a || []).push(arguments); }};
  m[i].l = 1 * new Date();
  for (var j = 0; j < document.scripts.length; j++) {{ if (document.scripts[j].src === r) {{ return; }} }}
  k = e.createElement(t); a = e.getElementsByTagName(t)[0]; k.async = 1; k.src = r;
  a.parentNode.insertBefore(k, a);
}})(window, document, 'script', 'https://mc.yandex.ru/metrika/tag.js', 'ym');
// номер кладём в атрибут: main.js читает его оттуда и не хранит
// собственную копию, которая однажды разойдётся с этой
document.documentElement.setAttribute('data-counter', '{METRIKA_ID}');
ym({METRIKA_ID}, 'init', {{ clickmap: true, trackLinks: true, accurateTrackBounce: true }});
</script>
<noscript><div><img src="https://mc.yandex.ru/watch/{METRIKA_ID}" style="position:absolute;left:-9999px" alt=""></div></noscript>'''


METRIKA_OPEN = "<!-- @metrika — правится в tools/make-seo.py -->"
METRIKA_CLOSE = "<!-- /@metrika -->"


def strip(text: str) -> str:
    """Убирает всё, что инструмент писал в прошлый раз, и старые og-теги,
    набранные руками. Без этого повторный запуск дублировал бы метатеги."""
    text = re.sub(re.escape(SEO_OPEN) + r".*?" + re.escape(SEO_CLOSE) + r"\n?", "", text, flags=re.S)
    text = re.sub(re.escape(METRIKA_OPEN) + r".*?" + re.escape(METRIKA_CLOSE) + r"\n?", "", text, flags=re.S)
    # og:*/twitter:* вне блока — наследие первой версии страниц
    text = re.sub(r'[ \t]*<meta (?:property="og:[^"]*"|name="twitter:[^"]*")[^>]*>\n', "", text)
    return text


def insert_after_theme_color(text: str, block: str) -> str:
    m = re.search(r'<meta name="theme-color"[^>]*>\n', text)
    if not m:
        # запасной якорь для страниц без theme-color
        m = re.search(r"</title>\n", text)
    if not m:
        raise SystemExit("не нашёл, куда вставить @seo")
    return text[:m.end()] + block + text[m.end():]


def main() -> int:
    root = pathlib.Path(".")
    pages = sorted(p for p in root.glob("*.html") if not p.name.startswith("_"))
    if not pages:
        print("не нашёл ни одной страницы", file=sys.stderr)
        return 1

    arts = collect_articles(root)
    art_by_file = {a["file"]: a for a in arts}
    print(f"статей в blog.html: {len(arts)}")

    for p in pages:
        text = strip(p.read_text())
        title, desc = head_meta(text)
        art = art_by_file.get(p.name)
        block = seo_block(p.name, title, desc, art,
                          is_index=(p.name == "index.html"),
                          noindex=(p.name in NOINDEX))
        text = insert_after_theme_color(text, block)

        if p.name == "404.html":
            # canonical и og:url у страницы ошибки бессмысленны
            text = re.sub(r'<link rel="canonical"[^>]*>\n', "", text)
            text = re.sub(r'<meta property="og:url"[^>]*>\n', "", text)

        m = metrika()
        if m:
            text = text.replace("</body>", METRIKA_OPEN + m + "\n" + METRIKA_CLOSE + "\n</body>", 1)
        p.write_text(text)

    (root / "sitemap.xml").write_text(write_sitemap(root, {p.name for p in pages}, arts))
    (root / "robots.txt").write_text(write_robots())
    (root / "feed.xml").write_text(write_feed(root, arts))

    print(f"  @seo проставлен на {len(pages)} страницах")
    print("  sitemap.xml, robots.txt, feed.xml пересобраны")
    if "REPLACE-DOMAIN" in SITE:
        print("\n  ! SITE — заглушка. canonical и og:url указывают на "
              "несуществующий домен,\n    а robots.txt закрывает сайт от "
              "индексации. Впишите домен в tools/make-seo.py.")
    if "REPLACE" in METRIKA_ID:
        print("  ! METRIKA_ID — заглушка, счётчик не вставлен. "
              "Возьмите номер в metrika.yandex.ru.")
    if "REPLACE_REFERRAL_LINK" in " ".join(p.read_text() for p in pages):
        print("  ! в статьях всё ещё REPLACE_REFERRAL_LINK — "
              "сайт не зарабатывает, пока они там.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
