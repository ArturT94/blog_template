#!/usr/bin/env python3
"""Рисует иллюстрации блога. Запускать из корня: python3 tools/make-art.py"""
import pathlib

OUT = pathlib.Path("img")
OUT.mkdir(exist_ok=True)

# Палитра развёрнута: раньше земля была почти чёрной, а штрих светлым.
# Теперь наоборот — светлая песочная земля и тёмный штрих. Прозрачности
# (stroke-opacity, opacity) при этом сохранили смысл: слабый штрих остаётся
# слабым, только читается как серая линия по бумаге, а не как серая по чёрному.
GROUND = "#FFF3E7"   # земля всех иллюстраций
INK    = "#1B1613"   # штрих и заливки нейтрального
SOFT   = "#E3D2B9"   # мягкая нейтральная заливка
MID    = "#6E6157"
PAPER  = "#FFFCF7"

# Цвета разделов — те же значения, что --c-*-fill в styles.css
C_DENGI, C_BIZNES, C_IT, C_SPORT, C_ZHIZN = "#FF6B3D", "#6E93FF", "#3FBF9A", "#F5B33C", "#A98BFF"
ACCENT = C_DENGI

HEAD = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        'width="{w}" height="{h}" role="img" aria-label="{alt}">\n'
        '<title>{alt}</title>\n')


def grain(w, h, seed=3, opacity=0.05):
    """Плёночное зерно — чтобы плашки не читались как плоский вектор.

    Рисуется ПОВЕРХ земли: раньше оно шло первым и его закрывала подложка,
    поэтому зерна не было видно вообще ни на одной иллюстрации.
    """
    return (f'<filter id="g{seed}" x="0" y="0" width="100%" height="100%">'
            f'<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" seed="{seed}"/>'
            f'<feColorMatrix type="saturate" values="0"/></filter>\n'
            f'<rect width="{w}" height="{h}" filter="url(#g{seed})" opacity="{opacity}"/>\n')


def ground(w, h, seed=3, opacity=0.05):
    """Подложка, а поверх неё зерно — в этом порядке, иначе зерно не видно."""
    return f'<rect width="{w}" height="{h}" fill="{GROUND}"/>\n' + grain(w, h, seed, opacity)


def cover_perevody(c=ACCENT):
    """Два счёта и линия между ними. Комиссия — волосок, а не клин."""
    w, h = 1200, 800
    s = HEAD.format(w=w, h=h, alt="Иллюстрация: два счёта, соединённые линией")
    s += ground(w, h, 3)
    # горизонт
    s += f'<path d="M0 400H1200" stroke="{INK}" stroke-opacity=".16"/>\n'
    # левый счёт — наливной
    s += f'<circle cx="360" cy="400" r="150" fill="{c}"/>\n'
    # правый счёт — контур
    s += f'<circle cx="840" cy="400" r="230" fill="none" stroke="{INK}" stroke-opacity=".34" stroke-width="1.5"/>\n'
    s += f'<circle cx="840" cy="400" r="150" fill="none" stroke="{INK}" stroke-opacity=".16"/>\n'
    # волосок комиссии: узкий клин в правом счёте
    s += f'<path d="M840 170 L 862 400 L 840 630 Z" fill="{c}" opacity=".9"/>\n'
    # перевод: линия слева направо, с разрывом на волоске
    s += f'<path d="M510 400H610" stroke="{INK}" stroke-opacity=".5" stroke-width="1.5"/>\n'
    s += f'<path d="M1070 400H1130" stroke="{INK}" stroke-opacity=".28" stroke-width="1.5"/>\n'
    s += f'<path d="M672 400H770" stroke="{c}" stroke-width="3"/>\n'
    s += f'<path d="M756 388l14 12-14 12" fill="none" stroke="{c}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>\n'
    s += '</svg>\n'
    return s


def cover_keshbek(c=ACCENT):
    """Категории: решётка квадратов, часть наливных."""
    w, h = 1200, 800
    s = HEAD.format(w=w, h=h, alt="Иллюстрация: категории покупок решёткой")
    s += ground(w, h, 7)
    cell, gap = 88, 22
    cols, rows = 8, 5
    x0 = (w - (cols * cell + (cols - 1) * gap)) / 2
    y0 = (h - (rows * cell + (rows - 1) * gap)) / 2
    # лесенка, а не шум: заливка спускается по диагонали
    filled = {(0, 0): c, (1, 0): c, (1, 1): c,
              (2, 1): SOFT, (2, 2): SOFT, (3, 2): MID,
              (4, 3): MID, (5, 3): SOFT, (6, 4): c, (7, 4): c}
    for r in range(rows):
        for c in range(cols):
            x = x0 + c * (cell + gap)
            y = y0 + r * (cell + gap)
            f = filled.get((c, r))
            if f:
                s += (f'<rect x="{x:.0f}" y="{y:.0f}" width="{cell}" height="{cell}" '
                      f'fill="{f}" opacity="{".7" if f == MID else "1"}"/>\n')
            else:
                s += (f'<rect x="{x:.0f}" y="{y:.0f}" width="{cell}" height="{cell}" '
                      f'fill="none" stroke="{INK}" stroke-opacity=".2"/>\n')
    s += '</svg>\n'
    return s


def cover_kopilka(c=ACCENT):
    """Сосуд: вложенные дуги и одна монета на дне."""
    w, h = 1200, 800
    s = HEAD.format(w=w, h=h, alt="Иллюстрация: вложенные дуги, похожие на сосуд")
    s += ground(w, h, 11)
    cx, base = 600, 640
    for i, r in enumerate((420, 330, 240, 150)):
        op = ".5" if i == 0 else ".3"
        s += (f'<path d="M{cx - r} {base} A {r} {r} 0 0 1 {cx + r} {base}" '
              f'fill="none" stroke="{INK}" stroke-opacity="{op}" stroke-width="1.5"/>\n')
    # тело сосуда — очень слабая заливка того же цвета, чтобы дуги не висели в воздухе
    s += f'<path d="M{cx - 240} {base} A 240 240 0 0 1 {cx + 240} {base}" fill="{c}" opacity=".14"/>\n'
    s += f'<path d="M{cx - 66} {base} A 66 66 0 0 1 {cx + 66} {base}" fill="{c}"/>\n'
    s += f'<path d="M{cx - 420} {base}H{cx + 420}" stroke="{INK}" stroke-opacity=".3"/>\n'
    # отвес — «на дне»
    s += f'<path d="M{cx} 180V{base - 66}" stroke="{INK}" stroke-opacity=".14" stroke-dasharray="2 7"/>\n'
    s += '</svg>\n'
    return s


def hero(c=ACCENT):
    """Семь месяцев — семь волосков на нулевой линии."""
    w, h = 1600, 700
    s = HEAD.format(w=w, h=h, alt="Иллюстрация: семь месяцев на нулевой линии")
    s += ground(w, h, 5, 0.04)
    accent, ink = c, INK
    s += f'<circle cx="1160" cy="330" r="290" fill="{accent}" opacity=".13"/>\n'
    s += f'<circle cx="1160" cy="330" r="290" fill="none" stroke="{ink}" stroke-opacity=".3" stroke-width="1.5"/>\n'
    s += f'<circle cx="1160" cy="330" r="205" fill="none" stroke="{ink}" stroke-opacity=".14"/>\n'
    base = 500
    n, step = 7, 118
    x0 = 150
    for i in range(n):
        x = x0 + i * step
        hgt = 26 + i * 9          # рост есть, но он в пределах погрешности
        last = i == n - 1
        col = accent if last else ink
        op = "1" if last else ".42"
        s += f'<rect x="{x}" y="{base - hgt}" width="4" height="{hgt}" fill="{col}" opacity="{op}"/>\n'
        s += f'<rect x="{x - 9}" y="{base + 4}" width="22" height="1.5" fill="{ink}" opacity=".45"/>\n'
    s += f'<path d="M{x0 - 46} {base + .75}H{x0 + (n - 1) * step + 46}" stroke="{ink}" stroke-opacity=".65" stroke-width="1.5"/>\n'
    s += '</svg>\n'
    return s


def wide_bank(c=ACCENT):
    """Широкая плашка для страницы «Об авторе»."""
    w, h = 1600, 600
    s = HEAD.format(w=w, h=h, alt="Иллюстрация: горизонтальные полосы выписки")
    s += ground(w, h, 13, 0.04)
    accent_rows = {3, 9}
    for i in range(16):
        y = 60 + i * 32
        long = 900 if i % 3 else 1180
        col = c if i in accent_rows else INK
        op = ".8" if i in accent_rows else ".18"
        s += f'<rect x="200" y="{y}" width="{long}" height="2" fill="{col}" opacity="{op}"/>\n'
    s += f'<path d="M200 40V560" stroke="{INK}" stroke-opacity=".3"/>\n'
    s += f'<circle cx="1380" cy="300" r="120" fill="none" stroke="{c}" stroke-opacity=".5" stroke-width="1.5"/>\n'
    s += '</svg>\n'
    return s


def cover_chestno(c=ACCENT):
    """Два сцепленных кольца — ссылка, которая связывает две стороны."""
    w, h = 1200, 800
    s = HEAD.format(w=w, h=h, alt="Иллюстрация: два сцепленных кольца")
    s += ground(w, h, 17)
    # Кольца толстые и с заливкой: на холсте 1200 px волосок в 1.5 px
    # в карточке становится половиной пикселя и пропадает совсем.
    # Залито правое — то, которое про ссылку; левое только контур.
    s += f'<circle cx="460" cy="400" r="232" fill="none" stroke="{INK}" stroke-opacity=".42" stroke-width="3"/>\n'
    s += f'<circle cx="740" cy="400" r="232" fill="{c}" fill-opacity=".12" stroke="{c}" stroke-width="4"/>\n'
    s += f'<path d="M600 187v426" stroke="{GROUND}" stroke-width="11"/>\n'
    s += f'<path d="M600 187v426" stroke="{INK}" stroke-opacity=".22" stroke-width="2"/>\n'
    s += f'<path d="M120 400H240M960 400H1080" stroke="{INK}" stroke-opacity=".22"/>\n'
    s += '</svg>\n'
    return s


def cover_karty(c=ACCENT):
    """Четыре карты стопкой. Три пустые, четвёртая рабочая."""
    w, h = 1200, 800
    s = HEAD.format(w=w, h=h, alt="Иллюстрация: четыре карты стопкой, три пустые")
    s += ground(w, h, 19)
    cw, ch, r = 460, 292, 26
    x0, y0, step = 268, 154, 78
    for i in range(4):
        front = i == 3
        x, y = x0 + i * step, y0 + i * step
        op = ".62" if front else f"{.2 + i * .07:.2f}"
        s += (f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="{r}" '
              f'fill="{GROUND}" stroke="{INK}" stroke-opacity="{op}" stroke-width="1.5"/>\n')
    fx, fy = x0 + 3 * step, y0 + 3 * step
    # чип и полоса — только у передней; три задние так и остаются пустыми
    s += f'<rect x="{fx + 48}" y="{fy + 94}" width="70" height="50" rx="8" fill="none" stroke="{c}" stroke-width="1.5"/>\n'
    s += (f'<path d="M{fx + 48} {fy + 119}h70M{fx + 83} {fy + 94}v50" '
          f'stroke="{c}" stroke-opacity=".55"/>\n')
    s += f'<rect x="{fx + 48}" y="{fy + 196}" width="252" height="4" fill="{c}" opacity=".85"/>\n'
    s += f'<rect x="{fx + 48}" y="{fy + 216}" width="140" height="3" fill="{INK}" opacity=".24"/>\n'
    s += '</svg>\n'
    return s


def cover_prilozheniya(c=ACCENT):
    """Экран телефона: одна ячейка пустая, остальные на месте."""
    w, h = 1200, 800
    s = HEAD.format(w=w, h=h, alt="Иллюстрация: экран телефона с пустой ячейкой")
    s += ground(w, h, 23)
    pw, ph = 470, 700
    px, py = (w - pw) / 2, (h - ph) / 2
    s += (f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="48" fill="none" '
          f'stroke="{INK}" stroke-opacity=".55" stroke-width="1.5"/>\n')
    cell, gap, cols, rows = 58, 28, 4, 6
    gx = px + (pw - (cols * cell + (cols - 1) * gap)) / 2
    gy = py + 84
    for r in range(rows):
        for c in range(cols):
            x = gx + c * (cell + gap)
            y = gy + r * (cell + gap)
            if r == 0 and c == 0:
                # пустая ячейка — приложение убрано с экрана
                s += (f'<rect x="{x:.0f}" y="{y:.0f}" width="{cell}" height="{cell}" rx="15" '
                      f'fill="none" stroke="{c}" stroke-width="1.5" stroke-dasharray="5 6"/>\n')
                continue
            op = ".3" if (r + c) % 5 else ".16"
            s += (f'<rect x="{x:.0f}" y="{y:.0f}" width="{cell}" height="{cell}" rx="15" '
                  f'fill="none" stroke="{INK}" stroke-opacity="{op}"/>\n')
    for i in range(3):
        s += (f'<rect x="{px + pw / 2 - 32 + i * 26:.0f}" y="{py + ph - 34}" width="16" height="3" '
              f'fill="{INK}" opacity=".3"/>\n')
    s += '</svg>\n'
    return s


def cover_bezopasnost(c=ACCENT):
    """Звонок: волны от точки и стена, до которой они доходят."""
    w, h = 1200, 800
    s = HEAD.format(w=w, h=h, alt="Иллюстрация: волны звонка и стена")
    s += ground(w, h, 29)
    cx, cy = 430, 400
    for i, r in enumerate((120, 200, 280, 360)):
        last = i == 3
        col = c if last else INK
        op = "1" if last else f"{.5 - i * .1:.2f}"
        sw = "2.5" if last else "1.5"
        s += (f'<path d="M{cx} {cy - r} A {r} {r} 0 0 1 {cx} {cy + r}" fill="none" '
              f'stroke="{col}" stroke-opacity="{op}" stroke-width="{sw}"/>\n')
    s += f'<path d="M{cx} 100V{cy - 360}" stroke="{INK}" stroke-opacity=".12" stroke-dasharray="2 8"/>\n'
    s += f'<path d="M{cx} {cy + 360}V700" stroke="{INK}" stroke-opacity=".12" stroke-dasharray="2 8"/>\n'
    s += f'<circle cx="{cx}" cy="{cy}" r="28" fill="{c}"/>\n'
    # стена ровно там, где кончается последняя волна
    s += f'<rect x="{cx + 368}" y="150" width="5" height="500" fill="{c}" opacity=".9"/>\n'
    s += f'<rect x="{cx + 394}" y="150" width="2" height="500" fill="{INK}" opacity=".2"/>\n'
    s += f'<path d="M{cx + 28} {cy}H{cx + 368}" stroke="{INK}" stroke-opacity=".28" stroke-dasharray="3 7"/>\n'
    s += '</svg>\n'
    return s


def cover_byudzhet(c=ACCENT):
    """Двенадцать месяцев: восемь столбиков и ровная линия вместо остальных."""
    w, h = 1200, 800
    s = HEAD.format(w=w, h=h, alt="Иллюстрация: столбики месяцев, обрывающиеся в линию")
    s += ground(w, h, 31)
    base = 620
    n, bw, gap = 12, 46, 30
    x0 = (w - (n * bw + (n - 1) * gap)) / 2
    heights = (300, 268, 236, 250, 206, 174, 150, 118)
    for i in range(n):
        x = x0 + i * (bw + gap)
        if i < len(heights):
            hgt = heights[i]
            col = c if i == len(heights) - 1 else INK
            op = ".9" if i == len(heights) - 1 else f"{.46 - i * .035:.2f}"
            s += f'<rect x="{x:.0f}" y="{base - hgt}" width="{bw}" height="{hgt}" fill="{col}" opacity="{op}"/>\n'
        else:
            s += f'<rect x="{x:.0f}" y="{base - 5}" width="{bw}" height="5" fill="{c}" opacity=".55"/>\n'
        s += f'<rect x="{x - 6:.0f}" y="{base + 9}" width="{bw + 12}" height="1.5" fill="{INK}" opacity=".3"/>\n'
    left = x0 - 46
    right = x0 + n * (bw + gap) - gap + 46
    s += f'<path d="M{left:.0f} {base + .75:.2f}H{right:.0f}" stroke="{INK}" stroke-opacity=".7" stroke-width="1.5"/>\n'
    mark = x0 + len(heights) * (bw + gap) - gap / 2
    s += f'<path d="M{mark:.0f} {base - 5:.0f}V150" stroke="{INK}" stroke-opacity=".12" stroke-dasharray="2 8"/>\n'
    s += '</svg>\n'
    return s



def cover_biznes(c=C_BIZNES):
    """Воронка: семь полос, каждая короче предыдущей. Деньги утекают в горло."""
    w, h = 1200, 800
    s = HEAD.format(w=w, h=h, alt="Иллюстрация: воронка из сужающихся полос")
    s += ground(w, h, 37)
    cx = 600
    n, bh, gap = 7, 54, 26
    top = (h - (n * bh + (n - 1) * gap)) / 2
    # Ширина падает линейно: 880 → 304. Полосы не гаснут книзу, а набирают
    # цвет раздела — сужение поддержано насыщенностью. Раньше они были
    # чернилами с убывающей прозрачностью: воронка бледнела ровно там, где
    # сужается, и картинка читалась серой.
    for i in range(n):
        bw = 880 - i * 96
        x = cx - bw / 2
        y = top + i * (bh + gap)
        op = f"{.22 + .78 * i / (n - 1):.2f}"
        s += (f'<rect x="{x:.0f}" y="{y:.0f}" width="{bw}" height="{bh}" rx="6" '
              f'fill="{c}" opacity="{op}"/>\n')
    # ось воронки — волосок: подчёркивает, что сужение ровное, а не случайное
    s += (f'<path d="M{cx} {top - 40}V{top + n * (bh + gap) + 20}" stroke="{INK}" '
          f'stroke-opacity=".14" stroke-dasharray="2 8"/>\n')
    s += f'<path d="M140 {top - 40}H1060" stroke="{INK}" stroke-opacity=".22"/>\n'
    s += f'<path d="M140 {top + n * (bh + gap) + 20}H1060" stroke="{INK}" stroke-opacity=".22"/>\n'
    s += '</svg>\n'
    return s


def cover_it(c=C_IT):
    """Стойка: блоки один на другом, у каждого свой огонёк. Четвёртый не горит."""
    w, h = 1200, 800
    s = HEAD.format(w=w, h=h, alt="Иллюстрация: стойка сервера с огоньками")
    s += ground(w, h, 41)
    uw, uh, gap = 540, 74, 16
    n = 7
    x0 = 250
    top = (h - (n * uh + (n - 1) * gap)) / 2
    for i in range(n):
        y = top + i * (uh + gap)
        dead = i == 3          # четвёртый — тот, который пришлось чинить
        op = ".78" if dead else ".46"
        dash = ' stroke-dasharray="6 7"' if dead else ''
        s += (f'<rect x="{x0}" y="{y:.0f}" width="{uw}" height="{uh}" rx="10" '
              f'fill="none" stroke="{INK}" stroke-opacity="{op}" stroke-width="2.2"{dash}/>\n')
        lit = i % 2 == 0
        s += (f'<circle cx="{x0 + 42}" cy="{y + uh / 2:.0f}" r="9" '
              f'fill="{c if lit else INK}" opacity="{1 if lit else .28}"/>\n')
        for k in range(3):
            s += (f'<rect x="{x0 + 84}" y="{y + 24 + k * 15:.0f}" width="{280 - k * 60}" '
                  f'height="4" fill="{INK}" opacity=".30"/>\n')
    # связь с малым блоком сбоку — «а ещё вот эта коробочка»
    ymid = top + 3 * (uh + gap) + uh / 2
    s += f'<path d="M{x0 + uw} {ymid:.0f}H950" stroke="{INK}" stroke-opacity=".3" stroke-dasharray="3 7"/>\n'
    s += (f'<rect x="950" y="{top + 2.4 * (uh + gap):.0f}" width="130" height="180" rx="10" '
          f'fill="none" stroke="{c}" stroke-width="3"/>\n')
    s += f'<path d="M250 {top - 46}H1080" stroke="{INK}" stroke-opacity=".22"/>\n'
    s += '</svg>\n'
    return s


def cover_sport(c=C_SPORT):
    """Год по неделям: ровная гряда, провал, возвращение."""
    w, h = 1200, 800
    s = HEAD.format(w=w, h=h, alt="Иллюстрация: год по неделям, с провалом посередине")
    s += ground(w, h, 43)
    base = 560
    n, bw, gap = 40, 16, 7
    x0 = (w - (n * bw + (n - 1) * gap)) / 2

    def height_at(i):
        if i < 12:
            return 250 + i * 4          # начало: ровно и с запасом
        if i < 22:
            return 300 - (i - 12) * 26  # провал: 300 → 40
        if i < 30:
            return 44 + (i - 22) * 30   # возвращение
        return 288 + (i - 30) * 2

    for i in range(n):
        hgt = max(height_at(i), 6)
        x = x0 + i * (bw + gap)
        last = i >= n - 4
        col = c if last else INK
        op = ".95" if last else f"{.34 + min(hgt, 300) / 300 * .3:.2f}"
        s += (f'<rect x="{x:.0f}" y="{base - hgt:.0f}" width="{bw}" height="{hgt:.0f}" '
              f'rx="4" fill="{col}" opacity="{op}"/>\n')
    s += (f'<path d="M{x0 - 40} {base + .75}H{x0 + n * (bw + gap) - gap + 40}" '
          f'stroke="{INK}" stroke-opacity=".65" stroke-width="1.5"/>\n')
    # отметка провала — на двадцать третьей неделе
    mx = x0 + 22 * (bw + gap)
    s += (f'<path d="M{mx:.0f} {base - 360}V{base + 30}" stroke="{INK}" '
          f'stroke-opacity=".14" stroke-dasharray="2 8"/>\n')
    s += '</svg>\n'
    return s


def cover_zhizn(c=C_ZHIZN):
    """Смета и факт: два столбика блоков. Справа на один больше — как всегда."""
    w, h = 1200, 800
    s = HEAD.format(w=w, h=h, alt="Иллюстрация: смета и факт двумя столбиками")
    s += ground(w, h, 47)
    base = 660
    bw, bh, gap = 230, 46, 20
    lx, rx = 300, 670
    plan, fact = 6, 7
    for i in range(max(plan, fact)):
        y = base - (i + 1) * (bh + gap)
        if i < plan:
            s += (f'<rect x="{lx}" y="{y:.0f}" width="{bw}" height="{bh}" rx="6" '
                  f'fill="{INK}" opacity="{.30 - i * .03:.2f}"/>\n')
        if i < fact:
            s += (f'<rect x="{rx}" y="{y:.0f}" width="{bw}" height="{bh}" rx="6" '
                  f'fill="{c}" opacity="{.9 if i == fact - 1 else .42}"/>\n')
    for x in (lx, rx):
        s += f'<rect x="{x}" y="{base + 20}" width="{bw}" height="2.5" fill="{INK}" opacity=".3"/>\n'
    s += f'<path d="M{lx + bw} 120H{rx}" stroke="{INK}" stroke-opacity=".2" stroke-dasharray="3 8"/>\n'
    s += (f'<path d="M{lx - 40} {base + 21}H{rx + bw + 40}" stroke="{INK}" '
          f'stroke-opacity=".5" stroke-width="1.5"/>\n')
    s += '</svg>\n'
    return s

# У каждой иллюстрации свой цвет раздела — раньше все десять были одного

# ---------------------------------------------------------------------------
# Иллюстрации внутри статей. Те же правила, что и у обложек: тёплая земля,
# тёмный штрих, один цвет раздела. Отличие одно — это не обложка, а схема:
# у каждой есть смысл, который можно пересказать словами, и этот смысл
# повторяет то, что сказано в тексте рядом. Ни одной ставки и ни одного
# процента: числа в подписях взяты из самого текста статьи.
#
# Форматы: wide — 1600x640, ставится на всю ширину колонки;
# float — 900x700, встаёт поплавком справа или слева.
# ---------------------------------------------------------------------------

WIDE_W, WIDE_H = 1600, 640
FLOAT_W, FLOAT_H = 900, 700


def _wide(alt, seed=21, tone=0.04):
    s = HEAD.format(w=WIDE_W, h=WIDE_H, alt=alt)
    return s + ground(WIDE_W, WIDE_H, seed, tone)


def _float(alt, seed=31, tone=0.05):
    s = HEAD.format(w=FLOAT_W, h=FLOAT_H, alt=alt)
    return s + ground(FLOAT_W, FLOAT_H, seed, tone)


def _bars(s, base, xs, heights, w, accent_i, c=None):
    """Столбики от общей基线. Акцентный — цветом раздела, остальные чернилами."""
    for i, (x, hgt) in enumerate(zip(xs, heights)):
        acc = i == accent_i
        col = (c or ACCENT) if acc else INK
        op = "1" if acc else ".22"
        s += f'<rect x="{x}" y="{base - hgt}" width="{w}" height="{hgt}" fill="{col}" opacity="{op}"/>\n'
    return s


def banner():
    """Баннер на главной: живая картинка вместо видео.

    Настоящего видео здесь быть не может — сайт открывается по file://,
    без сборки и без зависимостей, а стоковые съёмки запрещены: всё, что
    нарисовано, должно быть нарисовано кодом. Поэтому баннер — SVG
    с анимацией внутри себя. Анимация живёт в <style> самого файла,
    а не в styles.css: SVG, подключённый через <img>, не видит внешних
    стилей, зато видит свои собственные.

    Устроено так, чтобы картинка НИКОГДА не была пустой: пять разделов
    поднимаются один раз при появлении, а дальше по кругу идёт только
    фоновое движение — волна света и падающие точки. Сброса в ноль
    в цикле нет: баннер, который раз в полминуты гаснет в пустоту,
    читается как сломанный, а не как живой.

    Естественное состояние каждого элемента — конечное. Поэтому
    при prefers-reduced-motion: reduce (все анимации выключены) баннер
    остаётся собранной статичной картинкой, а не пустым прямоугольником.
    """
    w, h = 1600, 520
    base = 452
    cols = [C_DENGI, C_BIZNES, C_IT, C_SPORT, C_ZHIZN]
    # Высоты подобраны так, чтобы самый высокий столбец почти доставал
    # до верхнего края: при прежних 312 над композицией висела пустая
    # четверть кадра, и баннер читался как недорисованный.
    heights = [252, 332, 284, 364, 300]
    bw, gap = 150, 96
    x0 = (w - (len(cols) * bw + (len(cols) - 1) * gap)) // 2

    s = HEAD.format(w=w, h=h, alt="Понемногу: пять разделов, которые поднимаются из общей линии")
    s += ground(w, h, 7, 0.045)

    # --- разметка: вертикали под каждым разделом и общая基线
    for i in range(len(cols)):
        x = x0 + i * (bw + gap)
        s += f'<rect x="{x + bw // 2}" y="58" width="1.5" height="{base - 58}" fill="{INK}" opacity=".1"/>\n'
    s += f'<path d="M{x0 - 90} {base}.75H{x0 + 5 * bw + 4 * gap + 90}" stroke="{INK}" stroke-opacity=".45" stroke-width="1.5"/>\n'

    # --- пять столбцов. Ширина столбца — единственное, что осталось
    #     от прежнего лендинга: одинаковые прямоугольники вместо «карточек».
    for i, (c, bh) in enumerate(zip(cols, heights)):
        x = x0 + i * (bw + gap)
        y = base - bh
        delay = 0.35 + i * 0.62
        s += (f'<g class="col" style="--d:{delay:.2f}s">'
              f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" fill="{c}" opacity=".9"/>'
              f'<rect x="{x}" y="{y}" width="{bw}" height="8" fill="{INK}" opacity=".14"/>'
              f'</g>\n')

    # --- профиль: ломаная поверх столбцов, прочерчивается слева направо
    pts = []
    for i, bh in enumerate(heights):
        pts.append((x0 + i * (bw + gap) + bw // 2, base - bh - 26))
    d = "M" + " L".join(f"{x} {y}" for x, y in pts)
    s += f'<path class="profile" d="{d}" fill="none" stroke="{INK}" stroke-opacity=".55" stroke-width="1.5"/>\n'
    for x, y in pts:
        s += f'<circle cx="{x}" cy="{y}" r="5" fill="{INK}" opacity=".5"/>\n'

    # --- точки: падают на столбцы и гаснут. Единственное, что живёт по кругу
    #     вместе с волной света, — поэтому картинка всё время дышит.
    dots = [(2, 40), (0, 120), (4, 18), (1, 66), (3, 96), (2, 132),
            (0, 26), (4, 110), (1, 148), (3, 30)]
    for k, (ci, dy) in enumerate(dots):
        x = x0 + ci * (bw + gap) + 30 + (k % 3) * 42
        y = base - heights[ci] - 34 - dy * 0.55
        delay = 0.9 + k * 0.42
        s += (f'<circle class="dot" style="--d:{delay:.2f}s" cx="{x}" cy="{y}" r="7" '
              f'fill="{cols[ci]}"/>\n')

    # --- волна света
    s += ('<defs><linearGradient id="sw" x1="0" y1="0" x2="1" y2="0">'
          f'<stop offset="0" stop-color="{PAPER}" stop-opacity="0"/>'
          f'<stop offset=".5" stop-color="{PAPER}" stop-opacity=".55"/>'
          f'<stop offset="1" stop-color="{PAPER}" stop-opacity="0"/>'
          '</linearGradient></defs>\n')
    s += f'<rect class="sweep" x="-380" y="0" width="380" height="{h}" fill="url(#sw)"/>\n'

    s += f'''<style>
    .col {{ transform-box: fill-box; transform-origin: 50% 100%;
            animation: rise 1.2s var(--ease, cubic-bezier(.22,1,.36,1)) var(--d) both; }}
    /* Колонка входит из тонкой полоски на линии, а не из нуля:
       кадр не должен пустовать ни в одну миллисекунду. */
    @keyframes rise {{ from {{ transform: scaleY(0.05); }} to {{ transform: scaleY(1); }} }}

    .profile {{ stroke-dasharray: 1500; stroke-dashoffset: 1500;
                animation: draw 1.6s cubic-bezier(.22,1,.36,1) 3.4s both; }}
    @keyframes draw {{ to {{ stroke-dashoffset: 0; }} }}

    .dot {{ opacity: 0; transform-box: fill-box; transform-origin: 50% 50%;
            animation: fall 7s linear var(--d) infinite; }}
    @keyframes fall {{
      0%   {{ opacity: 0; transform: translateY(-26px); }}
      6%   {{ opacity: .85; }}
      22%  {{ opacity: .85; transform: translateY(0); }}
      34%  {{ opacity: 0; transform: translateY(0); }}
      100% {{ opacity: 0; transform: translateY(-26px); }}
    }}

    .sweep {{ animation: sweep 9s cubic-bezier(.4,0,.6,1) 2.4s infinite; }}
    @keyframes sweep {{
      0%   {{ transform: translateX(0); opacity: 0; }}
      12%  {{ opacity: 1; }}
      70%  {{ opacity: 1; }}
      100% {{ transform: translateX({w + 380}px); opacity: 0; }}
    }}

    /* Анимации выключены — картинка остаётся собранной: каждый элемент
       в своём конечном состоянии, а не в начальном. */
    @media (prefers-reduced-motion: reduce) {{
      .col, .profile, .dot, .sweep {{ animation: none; }}
      .profile {{ stroke-dashoffset: 0; }}
      .dot {{ opacity: 0; }}
      .sweep {{ opacity: 0; }}
    }}
    </style>
    </svg>
    '''
    return s


def lead_perevody(c=ACCENT):
    """Картинка главной: два счёта и перевод между ними.

    Стоит СЗАДИ текста ведущего материала, а не над ним: полотно лежит
    под заголовком, лидом и фигурой «0 ₽». Поэтому всё плотное собрано
    в правой верхней четверти — там, где текста нет, — а к левому и
    нижнему краю картинка сходит на бумагу: мелкая mono-подпись фигуры
    должна читаться по чистому фону, а не по рисунку.

    1600×1000, обрезка `object-fit: cover` с прижатием к правому верхнему
    углу: полотно растёт вместе с окном, а режется левый и нижний край —
    там пусто. Крупные круги нарочно уходят за правый и верхний край:
    кадр читается окном в картинку, а не схемой, нарисованной по центру.

    Ни одной оси, ни одного столбика и ни одной сетки: прежний баннер
    главной читался графиком, и это первое, что здесь запрещено.

    Движение одно и то же по смыслу: монеты летят по дуге перевода от
    наливного счёта к контурному. Оно живёт в <style> самого файла —
    SVG, подключённый через <img>, внешних стилей не видит. Естественное
    состояние конечное: при prefers-reduced-motion монеты остаются лежать
    на дуге, а не пропадают.
    """
    w, h = 1600, 1000
    # Правее 1080 — сюжет; левее и ниже — только воздух: там заголовок,
    # лид, подпись фигуры и её число.
    ax, ay, ar = 1150, 445, 125        # счёт, с которого уходит: наливной
    bx, by, br = 1425, 145, 110        # счёт, на который приходит: контурный
    qx, qy = 1560, 420                 # выгиб дуги перевода
    sun = (1345, 285, 265)             # «день» за счетами, чуть за край

    s = HEAD.format(w=w, h=h, alt="Понемногу: два счёта и перевод между ними")
    s += (f'<defs>'
          f'<linearGradient id="pw" x1="0" y1="0" x2="1" y2="0">'
          f'<stop offset="0" stop-color="{PAPER}"/>'
          f'<stop offset=".55" stop-color="{PAPER}"/>'
          f'<stop offset="1" stop-color="{GROUND}"/></linearGradient>'
          f'<radialGradient id="gl" cx=".5" cy=".5" r=".5">'
          f'<stop offset="0" stop-color="{c}" stop-opacity=".26"/>'
          f'<stop offset=".5" stop-color="{c}" stop-opacity=".1"/>'
          f'<stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient>'
          f'<radialGradient id="gd" cx=".5" cy=".5" r=".5">'
          f'<stop offset="0" stop-color="{GROUND}" stop-opacity=".95"/>'
          f'<stop offset=".62" stop-color="{GROUND}" stop-opacity=".8"/>'
          f'<stop offset="1" stop-color="{GROUND}" stop-opacity="0"/></radialGradient>'
          f'<radialGradient id="cg" cx=".5" cy=".5" r=".5">'
          f'<stop offset="0" stop-color="{c}" stop-opacity=".34"/>'
          f'<stop offset=".55" stop-color="{c}" stop-opacity=".14"/>'
          f'<stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient>'
          f'<radialGradient id="bl" cx=".5" cy=".5" r=".5">'
          f'<stop offset="0" stop-color="{c}" stop-opacity=".07"/>'
          f'<stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient>'
          f'<linearGradient id="ft" x1="0" y1="0" x2="0" y2="1">'
          f'<stop offset="0" stop-color="{PAPER}" stop-opacity="1"/>'
          f'<stop offset="1" stop-color="{PAPER}" stop-opacity="0"/></linearGradient>'
          f'<linearGradient id="fb" x1="0" y1="0" x2="0" y2="1">'
          f'<stop offset="0" stop-color="{PAPER}" stop-opacity="0"/>'
          f'<stop offset=".4" stop-color="{PAPER}" stop-opacity=".3"/>'
          f'<stop offset=".8" stop-color="{PAPER}" stop-opacity=".75"/>'
          f'<stop offset="1" stop-color="{PAPER}" stop-opacity=".95"/></linearGradient>'
          f'<linearGradient id="sw" x1="0" y1="0" x2="1" y2="0">'
          f'<stop offset="0" stop-color="{PAPER}" stop-opacity="0"/>'
          f'<stop offset=".5" stop-color="{PAPER}" stop-opacity=".55"/>'
          f'<stop offset="1" stop-color="{PAPER}" stop-opacity="0"/></linearGradient>'
          f'</defs>\n')
    # бумага: у левого края — цвет страницы, правее — тёплая земля сайта
    s += f'<rect width="{w}" height="{h}" fill="url(#pw)"/>\n'
    s += grain(w, h, 41, 0.045)

    # воздух: мягкие пятна вместо колец — картинка, а не построение
    for cx, cy, r in ((1180, 250, 620), (700, 240, 340), (350, 660, 380), (1150, 720, 330)):
        s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#bl)"/>\n'

    # круг за счетами — уходит за правый край кадра
    s += f'<circle cx="{sun[0]}" cy="{sun[1]}" r="{sun[2]}" fill="{c}" opacity=".2"/>\n'
    s += f'<circle cx="{sun[0]}" cy="{sun[1]}" r="{sun[2]}" fill="none" stroke="{INK}" stroke-opacity=".2"/>\n'
    s += f'<circle cx="{sun[0]}" cy="{sun[1]}" r="{sun[2] - 86}" fill="none" stroke="{INK}" stroke-opacity=".09"/>\n'
    # кольцо сверху — тоже за краем
    s += f'<circle cx="1300" cy="-20" r="230" fill="none" stroke="{INK}" stroke-opacity=".15" stroke-width="1.5"/>\n'

    # земля под счетами: мягкое пятно вместо линии горизонта —
    # линия читалась бы осью, а пятно читается пейзажем
    s += f'<ellipse cx="1330" cy="700" rx="470" ry="215" fill="url(#gd)"/>\n'
    # глубина круга: ядро плотнее, чем само пятно
    s += f'<circle cx="{sun[0] - 60}" cy="{sun[1] + 30}" r="{sun[2] - 120}" fill="{c}" opacity=".1"/>\n'

    # счёт, на который приходит: контурный, выше и дальше
    s += (f'<circle cx="{bx}" cy="{by}" r="{br}" fill="{PAPER}" fill-opacity=".8" '
          f'stroke="{INK}" stroke-opacity=".5" stroke-width="1.5"/>\n')
    s += f'<circle cx="{bx}" cy="{by}" r="{br - 40}" fill="none" stroke="{INK}" stroke-opacity=".15"/>\n'
    # счёт, с которого уходит: наливной, ближе и ниже
    s += (f'<g class="acc">'
          f'<circle cx="{ax}" cy="{ay}" r="{ar}" fill="{c}"/>'
          f'<circle cx="{ax}" cy="{ay}" r="{ar}" fill="none" stroke="{INK}" stroke-opacity=".26"/>'
          f'</g>\n')
    s += f'<circle cx="{ax}" cy="{ay}" r="{ar + 52}" fill="none" stroke="{INK}" stroke-opacity=".12" stroke-dasharray="2 10" class="route"/>\n'
    # кольцо перевода: расходится от счёта и гаснет — движение, которое
    # видно даже краем глаза и не требует следить за монетой
    s += f'<circle class="pulse" cx="{ax}" cy="{ay}" r="{ar}" fill="none" stroke="{c}" stroke-width="2"/>\n'

    # дуга перевода и её след
    s += (f'<path d="M{ax} {ay} Q{qx} {qy} {bx} {by}" fill="none" stroke="{c}" '
          f'stroke-opacity=".22" stroke-width="26" stroke-linecap="round"/>\n')
    s += f'<path d="M{ax} {ay} Q{qx} {qy} {bx} {by}" fill="none" stroke="{INK}" stroke-opacity=".38" stroke-width="1.5"/>\n'
    for i in range(1, 8):
        t = i / 8
        px = (1 - t) ** 2 * ax + 2 * (1 - t) * t * qx + t ** 2 * bx
        py = (1 - t) ** 2 * ay + 2 * (1 - t) * t * qy + t ** 2 * by
        s += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="3" fill="{INK}" opacity="{.08 + .14 * t:.2f}"/>\n'

    # монеты: летят по дуге от счёта к счёту. Задержки отрицательные и равны
    # пройденной доле пути: к нулевой секунде монеты уже разошлись по дуге,
    # первый же кадр живой, и ни одна не прыгает — она продолжает движение
    # ровно с того места, где нарисована её cx/cy.
    for k, t in enumerate((0.1, 0.3, 0.5, 0.7, 0.9)):
        px = (1 - t) ** 2 * ax + 2 * (1 - t) * t * qx + t ** 2 * bx
        py = (1 - t) ** 2 * ay + 2 * (1 - t) * t * qy + t ** 2 * by
        s += (f'<g class="coin" style="--d:{-t * 6:.1f}s">'
              f'<circle cx="{px:.0f}" cy="{py:.0f}" r="72" fill="url(#cg)"/>'
              f'<circle cx="{px:.0f}" cy="{py:.0f}" r="30" fill="{c}"/>'
              f'<circle cx="{px:.0f}" cy="{py:.0f}" r="30" fill="none" stroke="{INK}" stroke-opacity=".34"/>'
              f'<circle cx="{px:.0f}" cy="{py:.0f}" r="14" fill="none" stroke="{INK}" stroke-opacity=".22"/>'
              f'</g>\n')

    # след уходит влево, под заголовок: точки на бумаге, а не рисунок
    for i in range(8):
        x = 1010 - i * 54
        s += (f'<circle cx="{x}" cy="{512 + (i % 3) * 6}" r="{4.4 - i * .3:.1f}" '
              f'fill="{INK}" opacity="{.18 - i * .018:.2f}"/>\n')

    # редкие точки в верхней полосе — воздух, а не сюжет
    for x, y, r, o in ((430, 62, 6, .5), (742, 34, 4, .34), (296, 132, 5, .3), (1030, 66, 5, .38)):
        s += f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" opacity="{o}"/>\n'

    # края сходят на бумагу: полоса над картинкой и подпись под ней
    s += f'<rect x="0" y="0" width="{w}" height="110" fill="url(#ft)"/>\n'
    s += f'<rect x="0" y="620" width="{w}" height="380" fill="url(#fb)"/>\n'

    # блик, проходящий по картинке раз в двенадцать секунд
    s += f'<rect class="sweep" x="-380" y="0" width="380" height="{h}" fill="url(#sw)"/>\n'

    s += f'''<style>
    /* Монета летит по той же дуге, что нарисована в разметке. Своё место
       она помнит через cx/cy: если offset-path не поддержан или анимации
       выключены, монета просто лежит на дуге — кадр не пустеет. */
    /* transform-box: fill-box обязателен: без него offset-anchor берётся
       от начала системы координат SVG (центр viewBox), и монета улетает
       далеко за кадр — движение есть, а видеть нечего. */
    .coin {{ transform-box: fill-box; transform-origin: 50% 50%;
             offset-path: path("M{ax} {ay} Q{qx} {qy} {bx} {by}");
             offset-rotate: 0deg;
             animation: fly 6s linear var(--d) infinite; }}
    @keyframes fly {{ from {{ offset-distance: 0%; }} to {{ offset-distance: 100%; }} }}

    /* Счёт дышит, от него расходится кольцо перевода, пунктирный
       обод медленно поворачивается. Это фон, а не аттракцион: движение
       идёт само, пока читатель читает заголовок. */
    .acc {{ transform-box: fill-box; transform-origin: 50% 50%;
            animation: breathe 6s ease-in-out infinite; }}
    @keyframes breathe {{
      0%, 100% {{ transform: scale(1); }}
      50%      {{ transform: scale(1.035); }}
    }}

    .pulse {{ transform-box: fill-box; transform-origin: 50% 50%;
              animation: pulse 6s ease-out infinite; }}
    @keyframes pulse {{
      0%   {{ transform: scale(1); opacity: .5; }}
      70%  {{ opacity: .1; }}
      100% {{ transform: scale(2.4); opacity: 0; }}
    }}

    .route {{ transform-box: fill-box; transform-origin: 50% 50%;
              animation: spin 90s linear infinite; }}
    @keyframes spin {{ to {{ transform: rotate(360deg); }} }}

    .sweep {{ animation: sweep 12s cubic-bezier(.4,0,.6,1) 3s infinite; }}
    @keyframes sweep {{
      0%   {{ transform: translateX(0); opacity: 0; }}
      10%  {{ opacity: .9; }}
      80%  {{ opacity: .9; }}
      100% {{ transform: translateX({w + 380}px); opacity: 0; }}
    }}

    /* Анимации выключены — монеты лежат на дуге, блик погашен:
       конечное состояние, а не пустой кадр. */
    @media (prefers-reduced-motion: reduce) {{
      .coin {{ animation: none; offset-path: none; }}
      .acc, .route {{ animation: none; }}
      .pulse {{ animation: none; opacity: 0; }}
      .sweep {{ animation: none; opacity: 0; }}
    }}
    </style>
    </svg>
    '''
    return s


def art_perevody_scheta(c=ACCENT):
    """Два счёта и перевод между ними. Внизу — семь месяцев на нулевой линии."""
    s = _wide("Схема: два счёта, перевод между ними и ноль комиссий за семь месяцев", 21)
    s += f'<circle cx="390" cy="250" r="168" fill="{c}"/>\n'
    s += f'<circle cx="390" cy="250" r="232" fill="none" stroke="{INK}" stroke-opacity=".14"/>\n'
    s += f'<circle cx="1180" cy="250" r="232" fill="none" stroke="{INK}" stroke-opacity=".34" stroke-width="1.5"/>\n'
    s += f'<circle cx="1180" cy="250" r="168" fill="none" stroke="{INK}" stroke-opacity=".16"/>\n'
    s += f'<path d="M596 250H974" stroke="{INK}" stroke-opacity=".5" stroke-width="1.5"/>\n'
    s += f'<path d="M974 250l-18-11v22z" fill="{INK}" opacity=".5"/>\n'
    base = 560
    s += f'<path d="M120 {base}.75H1480" stroke="{INK}" stroke-opacity=".55" stroke-width="1.5"/>\n'
    for i in range(7):
        x = 160 + i * 200
        s += f'<rect x="{x}" y="{base - 6}" width="4" height="6" fill="{c}"/>\n'
        s += f'<rect x="{x - 14}" y="{base + 14}" width="32" height="1.5" fill="{INK}" opacity=".38"/>\n'
    s += f'<rect x="1440" y="{base + 12}" width="40" height="1.5" fill="{INK}" opacity=".2"/>\n'
    return s + "</svg>\n"


def art_perevody_dva(c=ACCENT):
    """Поплавок: счёт наливной, счёт контурный, между ними — волосок комиссии."""
    s = _float("Схема: два счёта, соединённые линией перевода", 22)
    s += f'<path d="M110 350H790" stroke="{INK}" stroke-opacity=".14"/>\n'
    s += f'<circle cx="290" cy="350" r="140" fill="{c}"/>\n'
    s += f'<circle cx="290" cy="350" r="196" fill="none" stroke="{INK}" stroke-opacity=".12"/>\n'
    s += f'<circle cx="640" cy="350" r="196" fill="none" stroke="{INK}" stroke-opacity=".34" stroke-width="1.5"/>\n'
    s += f'<circle cx="640" cy="350" r="140" fill="none" stroke="{INK}" stroke-opacity=".16"/>\n'
    s += f'<path d="M436 350H486" stroke="{INK}" stroke-opacity=".55" stroke-width="1.5"/>\n'
    s += f'<path d="M486 350l-16-10v20z" fill="{INK}" opacity=".55"/>\n'
    # волосок: узкий клин ровно по центру правого счёта
    s += f'<path d="M640 214 L652 350 L640 486 Z" fill="{c}"/>\n'
    return s + "</svg>\n"


def art_keshbek_kategorii(c=ACCENT):
    """Двенадцать категорий, из которых окупилась одна."""
    s = _wide("Схема: столбики категорий кэшбэка, один из них заметно выше остальных", 23)
    base = 540
    xs = [140 + i * 118 for i in range(11)]
    hs = [46, 34, 28, 40, 22, 30, 36, 24, 38, 26, 32]
    hs[4] = 348
    s = _bars(s, base, xs, hs, 46, 4, c)
    s += f'<path d="M110 {base}.75H1500" stroke="{INK}" stroke-opacity=".55" stroke-width="1.5"/>\n'
    s += f'<path d="M{140 + 4 * 118 - 30} 168V{base}" stroke="{c}" stroke-opacity=".35" stroke-dasharray="4 6"/>\n'
    return s + "</svg>\n"


def art_keshbek_tablica(c=ACCENT):
    """Поплавок: таблица, в которой заполнены немногие клетки."""
    s = _float("Схема: таблица покупок, где заполнена лишь часть клеток", 24)
    on = {1, 3, 8, 11, 12, 19, 22, 27, 33, 34, 40}
    for i in range(48):
        x = 130 + (i % 8) * 82
        y = 160 + (i // 8) * 74
        if i in on:
            s += f'<rect x="{x}" y="{y}" width="58" height="44" fill="{c}"/>\n'
        else:
            s += (f'<rect x="{x}" y="{y}" width="58" height="44" fill="none" '
                  f'stroke="{INK}" stroke-opacity=".26"/>\n')
    return s + "</svg>\n"


def art_kopilka_stupeni(c=ACCENT):
    """Ступени: каждый месяц на ступеньку выше, и ни одной пропущенной."""
    s = _wide("Схема: двенадцать ступеней, поднимающихся слева направо", 25)
    x, y = 150, 540
    for i in range(12):
        w_, h_ = 96, 34
        s += (f'<rect x="{x + i * w_}" y="{y - (i + 1) * h_}" width="{w_}" height="{(i + 1) * h_}" '
              f'fill="{c}" opacity="{0.24 + i * 0.06:.2f}"/>\n')
    s += f'<path d="M110 540.75H1480" stroke="{INK}" stroke-opacity=".55" stroke-width="1.5"/>\n'
    s += f'<path d="M150 {y - 34} L1302 {y - 408}" stroke="{INK}" stroke-opacity=".3" stroke-dasharray="5 7"/>\n'
    return s + "</svg>\n"


def art_kopilka_sosud(c=ACCENT):
    """Поплавок: сосуд, который наполняется снизу, а не сверху."""
    s = _float("Схема: уровень в сосуде, который поднимается снизу", 26)
    s += f'<path d="M250 170V500a200 200 0 0 0 400 0V170" fill="none" stroke="{INK}" stroke-opacity=".34" stroke-width="1.5"/>\n'
    s += f'<path d="M250 380V500a200 200 0 0 0 400 0V380z" fill="{c}" opacity=".8"/>\n'
    s += f'<path d="M222 380H678" stroke="{INK}" stroke-opacity=".55" stroke-width="1.5"/>\n'
    s += f'<path d="M222 170H678" stroke="{INK}" stroke-opacity=".55" stroke-width="1.5"/>\n'
    for i in range(4):
        s += f'<rect x="200" y="{430 + i * 40}" width="14" height="1.5" fill="{INK}" opacity=".3"/>\n'
    return s + "</svg>\n"


def art_karty_chetyre(c=ACCENT):
    """Четыре карты, три из которых зачёркнуты."""
    s = _wide("Схема: четыре карты, три перечёркнуты тонкой линией", 27)
    for i in range(4):
        x = 150 + i * 330
        live = i == 0
        s += (f'<rect x="{x}" y="180" width="280" height="176" rx="20" '
              f'fill="{c}" opacity="{".9" if live else ".1"}"/>\n')
        s += (f'<rect x="{x}" y="180" width="280" height="176" rx="20" fill="none" '
              f'stroke="{INK}" stroke-opacity="{".4" if live else ".22"}"/>\n')
        s += f'<rect x="{x + 28}" y="228" width="80" height="14" rx="7" fill="{INK}" opacity="{".5" if live else ".22"}"/>\n'
        s += f'<rect x="{x + 28}" y="286" width="180" height="8" rx="4" fill="{INK}" opacity="{".34" if live else ".14"}"/>\n'
        if not live:
            s += f'<path d="M{x + 40} 336L{x + 240} 196" stroke="{INK}" stroke-opacity=".5" stroke-width="1.5"/>\n'
    return s + "</svg>\n"


def art_karty_yashchik(c=ACCENT):
    """Поплавок: стопка карт, из которой достают одну."""
    s = _float("Схема: стопка карт в ящике, одна выдвинута вперёд", 28)
    for i in range(4):
        y = 220 + i * 34
        s += f'<rect x="170" y="{y}" width="440" height="120" rx="16" fill="{INK}" opacity=".08"/>\n'
        s += f'<rect x="170" y="{y}" width="440" height="120" rx="16" fill="none" stroke="{INK}" stroke-opacity=".2"/>\n'
    s += f'<rect x="170" y="180" width="440" height="120" rx="16" fill="{c}" opacity=".9"/>\n'
    s += f'<rect x="204" y="216" width="90" height="12" rx="6" fill="{INK}" opacity=".4"/>\n'
    s += f'<rect x="204" y="256" width="220" height="8" rx="4" fill="{INK}" opacity=".3"/>\n'
    return s + "</svg>\n"


def art_prilozheniya_ekran(c=ACCENT):
    """Три экрана: иконка уезжает на третий, число открытий падает."""
    s = _wide("Схема: три экрана телефона, иконка приложения уезжает на третий", 29)
    for i in range(3):
        x = 130 + i * 300
        s += (f'<rect x="{x}" y="110" width="230" height="430" rx="28" fill="none" '
              f'stroke="{INK}" stroke-opacity=".3" stroke-width="1.5"/>\n')
        for r in range(4):
            for k in range(3):
                cx = x + 42 + k * 66
                cy = 176 + r * 92
                filled = (i == 0 and r == 0 and k == 0)
                s += (f'<rect x="{cx}" y="{cy}" width="50" height="50" rx="15" '
                      f'fill="{c}" opacity="{".9" if filled else ".1"}"/>\n')
        if i < 2:
            s += (f'<path d="M{x + 246} 325h44" stroke="{INK}" stroke-opacity=".3" '
                  f'stroke-width="1.5"/>\n')
    # кривая открытий: падает и выходит на полку
    pts = [(1090, 180), (1200, 180), (1200, 268), (1310, 268), (1310, 356),
           (1420, 356), (1420, 444), (1520, 444)]
    d = "M" + " L".join(f"{x} {y}" for x, y in pts)
    s += f'<path d="M1050 500H1540" stroke="{INK}" stroke-opacity=".3" stroke-width="1.5"/>\n'
    s += f'<path d="{d}" fill="none" stroke="{c}" stroke-width="2.5"/>\n'
    for x, y in pts[1:]:
        s += f'<circle cx="{x}" cy="{y}" r="6" fill="{INK}" opacity=".4"/>\n'
    return s + "</svg>\n"


def art_prilozheniya_chastota(c=ACCENT):
    """Поплавок: ступенчатая кривая, которая падает и выравнивается."""
    s = _float("Схема: ломаная линия, которая падает и выходит на ровную полку", 30)
    pts = [(140, 200), (280, 200), (280, 320), (420, 320), (420, 430), (560, 430), (560, 500), (760, 500)]
    d = "M" + " L".join(f"{x} {y}" for x, y in pts)
    s += f'<path d="{d}" fill="none" stroke="{c}" stroke-width="2.5"/>\n'
    s += f'<path d="M110 540H790" stroke="{INK}" stroke-opacity=".4" stroke-width="1.5"/>\n'
    s += f'<path d="M110 160H790" stroke="{INK}" stroke-opacity=".14"/>\n'
    for x, y in pts:
        s += f'<circle cx="{x}" cy="{y}" r="6" fill="{INK}" opacity=".45"/>\n'
    return s + "</svg>\n"


def art_bezopasnost_zvonok(c=ACCENT):
    """Трубка, щит и список: что звонящий знал и чего он не знал."""
    s = _wide("Схема: звонок, щит и список того, что знал звонящий", 31)
    s += f'<rect x="130" y="150" width="210" height="380" rx="40" fill="{INK}" opacity=".12"/>\n'
    s += (f'<rect x="130" y="150" width="210" height="380" rx="40" fill="none" '
          f'stroke="{INK}" stroke-opacity=".34" stroke-width="1.5"/>\n')
    s += f'<rect x="190" y="215" width="90" height="14" rx="7" fill="{INK}" opacity=".35"/>\n'
    s += f'<circle cx="235" cy="478" r="14" fill="none" stroke="{INK}" stroke-opacity=".34" stroke-width="1.5"/>\n'
    s += f'<path d="M390 280q56-56 112 0M390 348q56-56 112 0M390 416q56-56 112 0" fill="none" stroke="{c}" stroke-width="2.5"/>\n'
    s += (f'<path d="M620 168l172-70 172 70v186q0 172-172 248-172-76-172-248z" '
          f'fill="{c}" opacity=".1"/>\n')
    s += (f'<path d="M620 168l172-70 172 70v186q0 172-172 248-172-76-172-248z" '
          f'fill="none" stroke="{INK}" stroke-opacity=".38" stroke-width="1.5"/>\n')
    s += f'<path d="M770 250l34 52-26 18 42 62-34 24" fill="none" stroke="{c}" stroke-width="2.5"/>\n'
    for i in range(5):
        y = 175 + i * 74
        known = i < 3
        s += (f'<rect x="1120" y="{y}" width="48" height="48" rx="14" '
              f'fill="{c}" opacity="{".9" if known else ".07"}"/>\n')
        if not known:
            s += (f'<rect x="1120" y="{y}" width="48" height="48" rx="14" fill="none" '
                  f'stroke="{INK}" stroke-opacity=".3"/>\n')
        s += (f'<rect x="1200" y="{y + 18}" width="{330 - i * 42}" height="12" rx="6" '
              f'fill="{INK}" opacity="{".34" if known else ".16"}"/>\n')
    return s + "</svg>\n"


def art_bezopasnost_shchit(c=ACCENT):
    """Поплавок: щит, который выдержал."""
    s = _float("Схема: щит с волосяной трещиной, оставшийся целым", 32)
    s += f'<path d="M450 120l224-88 224 88v240q0 224-224 320-224-96-224-320z" fill="{c}" opacity=".14"/>\n'
    s += f'<path d="M450 120l224-88 224 88v240q0 224-224 320-224-96-224-320z" fill="none" stroke="{INK}" stroke-opacity=".38" stroke-width="1.5"/>\n'
    s += f'<path d="M470 250l60 40-40 34 74 60-30 40" fill="none" stroke="{c}" stroke-width="2.5"/>\n'
    return s + "</svg>\n"


def art_byudzhet_kategorii(c=ACCENT):
    """Двадцать две категории в начале года и одна, которая осталась."""
    s = _wide("Схема: двадцать две клетки категорий, из которых заполнена одна", 33)
    for i in range(22):
        x = 150 + (i % 11) * 108
        y = 190 + (i // 11) * 116
        s += (f'<rect x="{x}" y="{y}" width="84" height="84" rx="14" fill="none" '
              f'stroke="{INK}" stroke-opacity=".26"/>\n')
    s += f'<rect x="150" y="190" width="84" height="84" rx="14" fill="{c}" opacity=".9"/>\n'
    s += f'<path d="M1420 190v232" stroke="{INK}" stroke-opacity=".3" stroke-width="1.5"/>\n'
    s += f'<rect x="1470" y="250" width="80" height="112" rx="14" fill="{c}"/>\n'
    s += f'<rect x="1470" y="250" width="80" height="112" rx="14" fill="none" stroke="{INK}" stroke-opacity=".3"/>\n'
    return s + "</svg>\n"


def art_byudzhet_odin(c=ACCENT):
    """Поплавок: одно число, до которого всё свелось."""
    s = _float("Схема: одна заполненная клетка из двадцати двух", 34)
    for i in range(22):
        x = 120 + (i % 5) * 132
        y = 180 + (i // 5) * 100
        s += (f'<rect x="{x}" y="{y}" width="100" height="72" rx="12" fill="none" '
              f'stroke="{INK}" stroke-opacity=".2"/>\n')
    s += f'<rect x="120" y="180" width="100" height="72" rx="12" fill="{c}" opacity=".9"/>\n'
    s += f'<path d="M120 640H780" stroke="{INK}" stroke-opacity=".4" stroke-width="1.5"/>\n'
    s += f'<rect x="120" y="600" width="180" height="10" rx="5" fill="{INK}" opacity=".3"/>\n'
    return s + "</svg>\n"


def art_biznes_vorot(c=ACCENT):
    """Сорок тысяч на входе, восемьдесят четыре на выходе и вопрос посередине."""
    s = _wide("Схема: сорок тысяч входят, восемьдесят четыре выходят, между ними вопрос", 35)
    s += f'<path d="M150 230h360l120 90-120 90H150z" fill="{INK}" opacity=".12"/>\n'
    s += f'<path d="M150 230h360l120 90-120 90H150z" fill="none" stroke="{INK}" stroke-opacity=".3" stroke-width="1.5"/>\n'
    s += f'<rect x="190" y="304" width="120" height="12" rx="6" fill="{c}"/>\n'
    s += f'<rect x="190" y="336" width="200" height="8" rx="4" fill="{INK}" opacity=".28"/>\n'
    s += f'<circle cx="800" cy="320" r="86" fill="none" stroke="{c}" stroke-width="2.5"/>\n'
    s += f'<path d="M780 288q0-26 22-26t22 24q0 20-20 26v16" fill="none" stroke="{c}" stroke-width="2.5"/>\n'
    s += f'<circle cx="804" cy="356" r="5" fill="{c}"/>\n'
    s += f'<path d="M920 320h180" stroke="{INK}" stroke-opacity=".45" stroke-width="1.5"/>\n'
    s += f'<path d="M1100 320l-18-11v22z" fill="{INK}" opacity=".45"/>\n'
    s += f'<path d="M1180 230h280l96 90-96 90h-280z" fill="{c}" opacity=".85"/>\n'
    return s + "</svg>\n"


def art_biznes_vopros(c=ACCENT):
    """Поплавок: выручка и деньги — два разных числа."""
    s = _float("Схема: две полосы разной длины — выручка и то, что осталось", 36)
    base = 470
    s += f'<rect x="150" y="{base - 220}" width="600" height="60" rx="12" fill="{c}" opacity=".9"/>\n'
    s += f'<rect x="150" y="{base - 90}" width="270" height="60" rx="12" fill="{INK}" opacity=".22"/>\n'
    s += f'<path d="M110 {base}.75H790" stroke="{INK}" stroke-opacity=".5" stroke-width="1.5"/>\n'
    for i in range(4):
        s += f'<rect x="110" y="{base - 40 - i * 60}" width="12" height="1.5" fill="{INK}" opacity=".22"/>\n'
    return s + "</svg>\n"


def art_it_server(c=ACCENT):
    """Стойка, четыре сервиса и диск, который умер на четвёртом месяце."""
    s = _wide("Схема: стойка сервера, четыре сервиса и отказ диска на четвёртом месяце", 37)
    for i in range(4):
        y = 150 + i * 78
        s += f'<rect x="170" y="{y}" width="300" height="58" rx="12" fill="{INK}" opacity=".1"/>\n'
        s += f'<rect x="170" y="{y}" width="300" height="58" rx="12" fill="none" stroke="{INK}" stroke-opacity=".28"/>\n'
        s += f'<circle cx="206" cy="{y + 29}" r="7" fill="{c}" opacity=".9"/>\n'
        s += f'<rect x="234" y="{y + 24}" width="150" height="9" rx="4" fill="{INK}" opacity=".28"/>\n'
    s += f'<path d="M180 470H520" stroke="{INK}" stroke-opacity=".14"/>\n'
    base = 560
    s += f'<path d="M700 {base}.75H1470" stroke="{INK}" stroke-opacity=".55" stroke-width="1.5"/>\n'
    for i in range(6):
        x = 720 + i * 150
        dead = i >= 3
        s += (f'<rect x="{x}" y="{base - 120}" width="90" height="120" rx="10" '
              f'fill="{c}" opacity="{".12" if dead else ".7"}"/>\n')
        s += (f'<rect x="{x}" y="{base - 120}" width="90" height="120" rx="10" fill="none" '
              f'stroke="{INK}" stroke-opacity="{".34" if dead else ".24"}"/>\n')
    s += f'<path d="M1170 380l120 180M1290 380l-120 180" stroke="{c}" stroke-width="2.5"/>\n'
    return s + "</svg>\n"


def art_it_disk(c=ACCENT):
    """Поплавок: пластина с одним мёртвым сектором."""
    s = _float("Схема: диск с одним нерабочим сектором", 38)
    s += f'<circle cx="450" cy="340" r="230" fill="none" stroke="{INK}" stroke-opacity=".3" stroke-width="1.5"/>\n'
    s += f'<circle cx="450" cy="340" r="188" fill="none" stroke="{INK}" stroke-opacity=".16"/>\n'
    s += f'<circle cx="450" cy="340" r="60" fill="none" stroke="{INK}" stroke-opacity=".3"/>\n'
    s += f'<path d="M450 340 L450 110 A230 230 0 0 1 613 178 Z" fill="{c}" opacity=".85"/>\n'
    s += f'<path d="M450 340 L613 178" stroke="{INK}" stroke-opacity=".2"/>\n'
    return s + "</svg>\n"


def art_sport_dni(c=ACCENT):
    """Сорок один поход за год — и двенадцать недель, о которых не пишут."""
    s = _wide("Схема: сорок одна отметка походов за год и четыре пустые недели", 39)
    base = 540
    # Плашка «тихих» недель идёт ПОД точки: поверх они читались как
    # выцветшие, а сама плашка — как серый прямоугольник, наклеенный сверху.
    s += (f'<rect x="{150 + 8 * 110 - 14}" y="150" width="{4 * 110 + 14}" '
          f'height="{base - 150}" fill="{INK}" opacity=".05"/>\n')
    for w in range(12):
        x = 150 + w * 110
        quiet = w >= 8
        s += f'<rect x="{x}" y="150" width="1.5" height="{base - 150}" fill="{INK}" opacity=".12"/>\n'
        for d in range(4):
            cx = x + 22 + (d % 2) * 50
            cy = base - 66 - (d // 2) * 80
            filled = (w * 4 + d) % 7 < 3 and not quiet
            s += (f'<circle cx="{cx}" cy="{cy}" r="17" fill="{c}" '
                  f'opacity="{".85" if filled else ".14"}"/>\n')
            if not filled:
                s += (f'<circle cx="{cx}" cy="{cy}" r="17" fill="none" '
                      f'stroke="{INK}" stroke-opacity=".22"/>\n')
    s += f'<path d="M120 {base + 40}.75H1480" stroke="{INK}" stroke-opacity=".4" stroke-width="1.5"/>\n'
    return s + "</svg>\n"


def art_sport_nedeli(c=ACCENT):
    """Поплавок: двенадцать недель, из которых четыре пустые."""
    s = _float("Схема: двенадцать недель подряд, четыре из них пустые", 40)
    for w in range(12):
        x = 130 + (w % 4) * 168
        y = 190 + (w // 4) * 168
        quiet = w >= 8
        s += (f'<rect x="{x}" y="{y}" width="132" height="132" rx="18" '
              f'fill="{c}" opacity="{".1" if quiet else ".8"}"/>\n')
        if quiet:
            s += (f'<rect x="{x}" y="{y}" width="132" height="132" rx="18" fill="none" '
                  f'stroke="{INK}" stroke-opacity=".26" stroke-dasharray="5 7"/>\n')
    return s + "</svg>\n"


def art_zhizn_smeta(c=ACCENT):
    """Смета и факт: короткая серая полоса и длинная цветная, между концами — разрыв."""
    s = _wide("Схема: две полосы — смета переезда и то, во что он обошёлся на самом деле", 41)
    left, gap = 200, 150
    short_w, long_w = 640, 1120
    s += f'<path d="M{left} 150V520" stroke="{INK}" stroke-opacity=".3"/>\n'
    # смета — контур, факт — заливка: контур читается как «предположение»,
    # заливка — как «сколько вышло на самом деле».
    s += (f'<rect x="{left}" y="190" width="{short_w}" height="104" rx="16" fill="{INK}" opacity=".16"/>\n')
    s += (f'<rect x="{left}" y="{190 + gap}" width="{long_w}" height="104" rx="16" fill="{c}" opacity=".9"/>\n')
    # разрыв: от конца сметы до конца факта
    xe = left + short_w
    s += (f'<path d="M{xe} 294V{190 + gap}" stroke="{INK}" stroke-opacity=".35" '
          f'stroke-dasharray="5 7"/>\n')
    s += (f'<path d="M{left + long_w} {294 + gap}V{190 + gap}" stroke="{c}" '
          f'stroke-opacity=".45" stroke-dasharray="5 7"/>\n')
    s += f'<path d="M{left} 550H{left + long_w}" stroke="{INK}" stroke-opacity=".45" stroke-width="1.5"/>\n'
    for i in range(6):
        s += f'<rect x="{left + i * 200}" y="558" width="1.5" height="14" fill="{INK}" opacity=".22"/>\n'
    return s + "</svg>\n"


def art_zhizn_raznica(c=ACCENT):
    """Поплавок: смета идёт ровно, факт загибается вверх, между ними — разрыв."""
    s = _float("Схема: разрыв между сметой и фактом растёт слева направо", 42)
    y0 = 470
    # Заливка разрыва — между прямой ожидания и кривой факта.
    s += f'<path d="M120 {y0}C420 {y0} 560 300 780 150L780 {y0}z" fill="{c}" opacity=".12"/>\n'
    s += f'<path d="M120 {y0}H780" stroke="{INK}" stroke-opacity=".4" stroke-width="1.5"/>\n'
    s += f'<path d="M120 {y0}C420 {y0} 560 300 780 150" fill="none" stroke="{c}" stroke-width="2.5"/>\n'
    for i, x in enumerate([200, 350, 500, 650]):
        y = y0 - [0, 26, 118, 244][i]
        s += (f'<path d="M{x} {y0}V{y}" stroke="{INK}" stroke-opacity=".22" '
              f'stroke-dasharray="4 6"/>\n')
    s += f'<path d="M120 130V630" stroke="{INK}" stroke-opacity=".3"/>\n'
    return s + "</svg>\n"


for name, fn, col in [("cover-perevody.svg",    cover_perevody,    C_DENGI),
                      ("cover-keshbek.svg",     cover_keshbek,     C_DENGI),
                      ("cover-kopilka.svg",     cover_kopilka,     C_DENGI),
                      ("cover-karty.svg",       cover_karty,       C_DENGI),
                      ("cover-prilozheniya.svg", cover_prilozheniya, C_DENGI),
                      ("cover-bezopasnost.svg", cover_bezopasnost, C_DENGI),
                      ("cover-byudzhet.svg",    cover_byudzhet,    C_DENGI),
                      ("cover-biznes.svg",      cover_biznes,      C_BIZNES),
                      ("cover-it.svg",          cover_it,          C_IT),
                      ("cover-sport.svg",       cover_sport,       C_SPORT),
                      ("cover-zhizn.svg",       cover_zhizn,       C_ZHIZN),
                      ("cover-chestno.svg",     cover_chestno,     C_DENGI),
                      ("hero.svg",              hero,              C_DENGI),
                      ("wide-vypiska.svg",      wide_bank,         C_DENGI),
                      ("banner.svg",            lambda c: banner(), C_DENGI),
                      ("lead-perevody.svg",    lead_perevody,     C_DENGI),
                      # Иллюстрации внутри статей: по одной широкой и по одной
                      # поплавковой на историю.
                      ("art-perevody-scheta.svg",      art_perevody_scheta,      C_DENGI),
                      ("art-perevody-dva.svg",         art_perevody_dva,         C_DENGI),
                      ("art-keshbek-kategorii.svg",    art_keshbek_kategorii,    C_DENGI),
                      ("art-keshbek-tablica.svg",      art_keshbek_tablica,      C_DENGI),
                      ("art-kopilka-stupeni.svg",      art_kopilka_stupeni,      C_DENGI),
                      ("art-kopilka-sosud.svg",        art_kopilka_sosud,        C_DENGI),
                      ("art-karty-chetyre.svg",        art_karty_chetyre,        C_DENGI),
                      ("art-karty-yashchik.svg",       art_karty_yashchik,       C_DENGI),
                      ("art-prilozheniya-ekran.svg",   art_prilozheniya_ekran,   C_DENGI),
                      ("art-prilozheniya-chastota.svg", art_prilozheniya_chastota, C_DENGI),
                      ("art-bezopasnost-zvonok.svg",   art_bezopasnost_zvonok,   C_DENGI),
                      ("art-bezopasnost-shchit.svg",   art_bezopasnost_shchit,   C_DENGI),
                      ("art-byudzhet-kategorii.svg",   art_byudzhet_kategorii,   C_DENGI),
                      ("art-byudzhet-odin.svg",        art_byudzhet_odin,        C_DENGI),
                      ("art-biznes-vorot.svg",         art_biznes_vorot,         C_BIZNES),
                      ("art-biznes-vopros.svg",        art_biznes_vopros,        C_BIZNES),
                      ("art-it-server.svg",            art_it_server,            C_IT),
                      ("art-it-disk.svg",              art_it_disk,              C_IT),
                      ("art-sport-dni.svg",            art_sport_dni,            C_SPORT),
                      ("art-sport-nedeli.svg",         art_sport_nedeli,         C_SPORT),
                      ("art-zhizn-smeta.svg",          art_zhizn_smeta,          C_ZHIZN),
                      ("art-zhizn-raznica.svg",        art_zhizn_raznica,        C_ZHIZN)]:
    (OUT / name).write_text(fn(col))
    print(f"  {name:24} {(OUT / name).stat().st_size:>6} байт")
