/* Понемногу — весь скрипт сайта.
   Ничего не скрывает насовсем: если он не выполнится, страница остаётся
   читаемой, потому что скрытие включается только классом .js. */
(function () {
  'use strict';

  var root = document.documentElement;

  function each(list, fn) { Array.prototype.forEach.call(list, fn); }
  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function $$(sel, ctx) { return (ctx || document).querySelectorAll(sel); }

  function throttle(fn) {
    var queued = false;
    return function () {
      if (queued) return;
      queued = true;
      requestAnimationFrame(function () { queued = false; fn(); });
    };
  }

  var calm = window.matchMedia('(prefers-reduced-motion: reduce)');

  /* ---------------------------------------------------------------- тема */
  /* Оформление по умолчанию светлое: data-theme="light" стоит прямо
     в <html>, поэтому система на вид сайта не влияет. Тёмная включается
     только этой кнопкой и запоминается. */
  (function theme() {
    var buttons = $$('.theme');
    if (!buttons.length) return;

    function paint(next) {
      each(buttons, function (b) { b.setAttribute('aria-pressed', String(next === 'dark')); });
      // theme-color красит полосу браузера на телефоне — держим её в тон
      var meta = $('meta[name="theme-color"]');
      if (meta) meta.setAttribute('content', next === 'dark' ? '#14110E' : '#FFFCF7');
    }

    paint(root.getAttribute('data-theme') === 'dark');

    each(buttons, function (btn) {
      btn.addEventListener('click', function () {
        var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
        root.setAttribute('data-theme', next);
        paint(next);
        try { localStorage.setItem('theme', next); } catch (e) { /* приватный режим */ }
      });
    });
  }());

  /* --------------------------------------------------------------- меню */
  (function menu() {
    var burger = $('#burger');
    var nav = $('#nav');
    var scrim = $('#scrim');
    if (!burger || !nav) return;

    var lastFocus = null;

    function open() {
      lastFocus = document.activeElement;
      root.setAttribute('data-menu', 'open');
      burger.setAttribute('aria-expanded', 'true');
      if (scrim) scrim.hidden = false;
      requestAnimationFrame(function () { if (scrim) scrim.style.opacity = '1'; });
      root.style.overflow = 'hidden';
      var first = $('a', nav);
      if (first) first.focus();
    }

    function close(returnFocus) {
      root.removeAttribute('data-menu');
      burger.setAttribute('aria-expanded', 'false');
      root.style.overflow = '';
      if (scrim) {
        scrim.style.opacity = '0';
        window.setTimeout(function () { scrim.hidden = true; }, 320);
      }
      if (returnFocus !== false && lastFocus) lastFocus.focus();
    }

    burger.addEventListener('click', function () {
      if (root.getAttribute('data-menu') === 'open') close(); else open();
    });

    if (scrim) scrim.addEventListener('click', function () { close(); });

    each($$('a', nav), function (a) {
      a.addEventListener('click', function () { close(false); });
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && root.getAttribute('data-menu') === 'open') close();
      if (e.key !== 'Tab' || root.getAttribute('data-menu') !== 'open') return;
      // фокус не должен уходить за пределы открытой панели
      var items = $$('a, button', nav);
      if (!items.length) return;
      var first = items[0];
      var last = items[items.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });

    window.addEventListener('resize', throttle(function () {
      // порог тот же, что у панели в styles.css: шапка держит строку
      // до 1024px, поэтому и закрывать панель нужно начиная с него
      if (window.innerWidth > 1024 && root.getAttribute('data-menu') === 'open') close(false);
    }));
  }());

  /* ------------------------------------------- появление блоков при скролле */
  var reveal = (function () {
    var targets = $$('.reveal, .cascade, .plate--reveal, .tried');
    if (!targets.length) return { sweep: function () {} };

    // Каскад: каждому ребёнку — свой порядковый номер для задержки
    each($$('.cascade'), function (box) {
      each(box.children, function (child, i) { child.style.setProperty('--i', i); });
    });

    function show(el) {
      if (el.classList.contains('is-in')) return;
      el.classList.add('is-in');
    }

    function sweep() {
      var h = window.innerHeight || root.clientHeight;
      each(targets, function (el) {
        var r = el.getBoundingClientRect();
        if (r.top < h * 0.92 && r.bottom > 0) show(el);
      });
    }

    // Первый проход — сразу, ещё до отрисовки следующего кадра.
    // Он один уже гарантирует, что видимое при загрузке не пропадёт.
    requestAnimationFrame(sweep);

    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) { show(entry.target); io.unobserve(entry.target); }
        });
      }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
      each(targets, function (el) { io.observe(el); });
    } else {
      window.addEventListener('scroll', throttle(sweep), { passive: true });
    }

    // Страховка: если что-то осталось скрытым после полной загрузки
    window.addEventListener('load', function () { window.setTimeout(sweep, 400); });

    return { sweep: sweep };
  }());

  /* ------------------------------------------------- разъезд иллюстраций */
  (function parallax() {
    var plates = $$('.plate--parallax');
    if (!plates.length || calm.matches) return;

    var ticking = false;

    function frame() {
      ticking = false;
      var h = window.innerHeight;
      each(plates, function (plate) {
        var r = plate.getBoundingClientRect();
        if (r.bottom < -200 || r.top > h + 200) return;   // вне экрана — не считаем
        // −1 … 1 по мере прохождения через экран
        var t = (r.top + r.height / 2 - h / 2) / (h / 2 + r.height / 2);
        t = Math.max(-1, Math.min(1, t));
        var img = plate.firstElementChild;
        // в переменную, а не в transform: transform занят шторкой (.plate--reveal)
        if (img) img.style.setProperty('--py', (t * r.height * 0.12).toFixed(2) + 'px');
      });
    }

    function onScroll() {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(frame);
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', throttle(frame));
    frame();
  }());

  /* -------------------------------------------------------------- слайдер */
  (function sliders() {
    each($$('[data-slider]'), function (box) {
      var track = $('.slider__track', box);
      if (!track) return;
      var prev = $('[data-prev]', box);
      var next = $('[data-next]', box);
      var count = $('[data-count]', box);

      function step() {
        var first = track.firstElementChild;
        if (!first) return track.clientWidth;
        var gap = parseFloat(getComputedStyle(track).columnGap) || 0;
        return first.getBoundingClientRect().width + gap;
      }

      function update() {
        var max = track.scrollWidth - track.clientWidth;
        var total = track.children.length;
        var i = Math.round(track.scrollLeft / Math.max(step(), 1));
        // У правого края прокрутка упирается в максимум, а он не кратен шагу
        // карточки: последняя снап-точка за ним недостижима, и счётчик
        // показывал «06 / 08» на самом конце. Дошли до края — значит последняя.
        if (max > 0 && track.scrollLeft >= max - 2) i = total - 1;
        if (count) {
          count.textContent = ('0' + Math.min(i + 1, total)).slice(-2) + ' / ' + ('0' + total).slice(-2);
        }
        if (prev) prev.disabled = track.scrollLeft <= 2;
        if (next) next.disabled = track.scrollLeft >= max - 2;
      }

      function go(dir) {
        track.scrollBy({ left: dir * step(), behavior: calm.matches ? 'auto' : 'smooth' });
      }

      if (prev) prev.addEventListener('click', function () { go(-1); });
      if (next) next.addEventListener('click', function () { go(1); });

      track.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowRight') { e.preventDefault(); go(1); }
        if (e.key === 'ArrowLeft') { e.preventDefault(); go(-1); }
      });

      track.addEventListener('scroll', throttle(update), { passive: true });
      window.addEventListener('resize', throttle(update));
      update();
    });
  }());

  /* --------------------------------------------- фильтр историй по разделам */
  (function filters() {
    var chips = $$('[data-filter]');
    if (!chips.length) return;
    var items = $$('[data-topic]');

    each(chips, function (chip) {
      chip.addEventListener('click', function () {
        var want = chip.getAttribute('data-filter');
        each(chips, function (c) {
          c.setAttribute('aria-pressed', String(c === chip));
        });
        each(items, function (item) {
          item.hidden = !(want === 'all' || item.getAttribute('data-topic') === want);
        });
        reveal.sweep();
      });
    });
  }());

  /* -------------------------------------------------------- поиск по сайту */
  /* Индекс — отдельный файл search-index.js, собранный tools/make-search.py,
     и до первого открытия поиска он не скачивается: 113 КБ на каждой
     странице не нужны никому. Подгружается тегом <script>, а не fetch:
     сайт открывается по file://, и fetch там режется политикой CORS. */
  (function search() {
    var box = $('#search');
    var opener = $('.search-open');
    if (!box || !opener) return;

    var input = $('#search-input', box);
    var list = $('#search-list', box);
    var status = $('#search-status', box);
    var idle = status ? status.textContent : '';

    var index = null;
    var loading = false;
    var waiting = [];
    var results = [];
    var active = -1;
    var lastFocus = null;

    function load(done) {
      if (index) return done();
      waiting.push(done);
      if (loading) return;   // набранное во время загрузки выполнится
      loading = true;        // в onload — иначе первый же запрос пропал бы
      var el = document.createElement('script');
      el.src = 'search-index.js';
      el.onload = function () {
        index = (window.PONY_SEARCH && window.PONY_SEARCH.p) || [];
        each(index, prepare);
        var queue = waiting; waiting = [];
        each(queue, function (fn) { fn(); });
      };
      el.onerror = function () {
        loading = false; waiting = [];
        if (status) status.textContent = 'Не удалось загрузить поисковый индекс.';
      };
      document.head.appendChild(el);
    }

    /* Русский поиск без морфологии: у слова отрезается хвост, и остаются
       первые пять букв. «Переводами» и «переводы» дают «перев» и находят
       друг друга. Грубо, но для шестнадцати страниц этого достаточно,
       а словарь и стеммер весили бы больше самого сайта. */
    var STEM = 5;
    function fold(text) { return text.toLowerCase().replace(/ё/g, 'е'); }
    function stem(word) { return word.length > STEM ? word.slice(0, STEM) : word; }
    function words(q) {
      return fold(q).split(/[^0-9a-zа-я]+/)
        .filter(function (w) { return w.length > 1; });
    }
    function count(hay, needle) {
      if (!hay || !needle) return 0;
      var n = 0, i = hay.indexOf(needle);
      while (i !== -1) { n++; i = hay.indexOf(needle, i + needle.length); }
      return n;
    }
    function prepare(page) {
      page._t = fold(page.t); page._k = fold(page.k);
      page._d = fold(page.d); page._b = fold(page.b);
    }

    function rank(q) {
      var stems = words(q).map(stem);
      if (!stems.length) return [];
      var out = [];
      each(index, function (page) {
        var sum = 0, all = true;
        each(stems, function (st) {
          var hit = count(page._t, st) * 10 + count(page._k, st) * 6 +
                    count(page._d, st) * 4 + count(page._b, st);
          if (!hit) all = false;
          sum += hit;
        });
        // Совпало всё — сильно выше тех, где совпало одно слово. Страницы
        // с частичным совпадением не выбрасываются: иначе запрос из двух
        // слов давал бы пустоту там, где есть что показать.
        if (all) sum += 40;
        if (sum > 0) out.push({ page: page, score: sum });
      });
      out.sort(function (a, b) {
        return b.score - a.score || a.page.t.length - b.page.t.length;
      });
      return out.slice(0, 12);
    }

    function esc(text) {
      return text.replace(/[&<>"]/g, function (c) {
        return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
      });
    }
    function escRe(text) { return text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }

    /* Подсвечиваем слово целиком, а не основу: к найденным пяти буквам
       дописывается хвост слова, иначе в «переводами» подсветились бы
       только «перев», и это читалось бы как обрыв. */
    function pattern(stems) {
      return new RegExp('(' + stems.map(function (s) {
        return escRe(s) + '[а-яёa-z]*';
      }).join('|') + ')', 'gi');
    }

    var OPEN = String.fromCharCode(1), SHUT = String.fromCharCode(2);

    function mark(text, stems) {
      if (!text) return '';
      // Сначала метим совпадения непечатаемыми символами, потом экранируем
      // разметку, и только потом меняем метки на <mark>: экранирование
      // сдвигает индексы, поэтому резать строку по ним нельзя.
      var marked = text.replace(pattern(stems), OPEN + '$1' + SHUT);
      return esc(marked).split(OPEN).join('<mark>').split(SHUT).join('</mark>');
    }

    function snippet(page, stems) {
      var at = page._b.search(pattern(stems));
      if (at < 0) {
        // Совпало только в заголовке — показываем описание.
        var d = page.d || page.b.slice(0, 170);
        return mark(d.length > 170 ? d.slice(0, 167).replace(/\s\S*$/, '') + '…' : d, stems);
      }
      var from = Math.max(0, at - 70);
      var to = Math.min(page.b.length, at + 150);
      var text = page.b.slice(from, to);
      if (from > 0) text = text.replace(/^\S*\s+/, '');
      if (to < page.b.length) text = text.replace(/\s+\S*$/, '');
      return (from > 0 ? '…' : '') + mark(text, stems) +
             (to < page.b.length ? '…' : '');
    }

    function plural(n, forms) {
      var a = n % 10, b = n % 100;
      if (a === 1 && b !== 11) return forms[0];
      if (a >= 2 && a <= 4 && (b < 10 || b >= 20)) return forms[1];
      return forms[2];
    }

    function draw(q) {
      var query = q.trim();
      var stems = words(q).map(stem);
      list.innerHTML = '';
      results = [];
      active = -1;

      if (!query) {
        if (status) status.textContent = idle;
        return;
      }
      results = rank(q);
      if (!results.length) {
        if (status) status.textContent = 'Ничего не нашлось. Попробуйте другое слово.';
        return;
      }
      if (status) {
        // Счётчик — прописными, запрос — как набран: капс набранного
        // человеком текста выглядит как издевательство над вводом.
        status.innerHTML = '<b>' + results.length + ' ' +
          plural(results.length, ['страница', 'страницы', 'страниц']) + '</b>' +
          ' по запросу «' + esc(query) + '»';
      }

      each(results, function (r, n) {
        var li = document.createElement('li');
        var a = document.createElement('a');
        a.className = 'search__link';
        a.href = r.page.u;
        if (r.page.c) a.setAttribute('data-c', r.page.c);
        a.innerHTML =
          '<span class="search__kicker">' + esc(r.page.k) + '</span>' +
          '<span class="search__title">' + mark(r.page.t, stems) + '</span>' +
          '<span class="search__snippet">' + snippet(r.page, stems) + '</span>';
        li.appendChild(a);
        list.appendChild(li);
      });
    }

    function open() {
      lastFocus = document.activeElement;
      box.hidden = false;
      root.setAttribute('data-search', 'open');
      root.style.overflow = 'hidden';
      requestAnimationFrame(function () { box.classList.add('is-open'); });
      load(function () { if (input.value.trim()) draw(input.value); });
      input.focus();
    }

    function close() {
      box.classList.remove('is-open');
      root.removeAttribute('data-search');
      root.style.overflow = '';
      window.setTimeout(function () { box.hidden = true; }, 260);
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }

    opener.addEventListener('click', function (e) {
      e.preventDefault();
      open();
    });

    each($$('[data-search-close]', box), function (el) {
      el.addEventListener('click', close);
    });

    var timer = null;
    input.addEventListener('input', function () {
      window.clearTimeout(timer);
      timer = window.setTimeout(function () {
        load(function () { draw(input.value); });
      }, 90);
    });

    box.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { e.preventDefault(); close(); return; }

      var links = $$('.search__link', list);
      if (!links.length) return;

      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        e.preventDefault();
        var step = e.key === 'ArrowDown' ? 1 : -1;
        active = (active + step + links.length) % links.length;
        each(links, function (a, i) { a.classList.toggle('is-active', i === active); });
        links[active].scrollIntoView({ block: 'nearest' });
        return;
      }
      if (e.key === 'Enter') {
        e.preventDefault();
        links[active >= 0 ? active : 0].click();
        return;
      }
      // Фокус не должен уходить за пределы панели
      if (e.key !== 'Tab') return;
      var items = $$('a, button, input', box);
      if (!items.length) return;
      var first = items[0], last = items[items.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });

    /* Открытие с клавиатуры: «/» и Ctrl/Cmd+K. Не перехватываем, когда
       человек печатает в поле, — иначе в самом поиске нельзя было бы
       набрать «/» и «k». */
    document.addEventListener('keydown', function (e) {
      if (root.getAttribute('data-search') === 'open') return;
      var tag = (document.activeElement && document.activeElement.tagName) || '';
      if (/^(INPUT|TEXTAREA|SELECT)$/.test(tag)) return;
      var slash = e.key === '/' && !e.metaKey && !e.ctrlKey;
      var k = (e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k';
      if (!slash && !k) return;
      e.preventDefault();
      open();
    });
  }());

  /* ------------------------------------ клики по партнёрским ссылкам */
  /* Единственное событие на сайте, которое прямо связано с доходом.
     Ловим по rel~="sponsored": этот признак уже стоит на всех партнёрских
     ссылках, поэтому новая ссылка попадёт под наблюдение сама, без правки
     разметки. Слушаем на фазе перехвата — если когда-нибудь появится
     обработчик, гасящий всплытие, цель всё равно уйдёт. */
  (function referrals() {
    document.addEventListener('click', function (e) {
      var a = e.target && e.target.closest && e.target.closest('a[rel~="sponsored"]');
      if (!a) return;
      var id = root.getAttribute('data-counter');
      if (!id || typeof window.ym !== 'function') return;   // счётчика нет — молчим
      window.ym(id, 'reachGoal', 'referral_click', {
        article: (location.pathname.split('/').pop() || 'index.html'),
        // куда именно повели: разные продукты в одной статье считаются отдельно
        target: a.getAttribute('href') || ''
      });
    }, true);
  }());

  /* ------------------------------------------------- форма обратной связи */
  /* Форма не уходит на сервер: у блога его нет. Скрипт собирает письмо
     и отдаёт его почтовой программе — поэтому форма работает и на хостинге,
     и при открытии сайта двойным кликом, без единой строчки бэкенда.
     Если появится сервис-приёмник (Formspree, Getform, свой обработчик),
     достаточно вписать его адрес в data-endpoint на самой форме: скрипт
     начнёт отправлять через него, а почта останется запасным путём. */
  (function contact() {
    var form = document.getElementById('contact-form');
    if (!form) return;

    var status = document.getElementById('form-status');
    var button = document.getElementById('contact-send');
    var area   = document.getElementById('f-message');
    var left   = document.getElementById('f-left');
    var trap   = document.getElementById('f-website');
    /* Адрес и почта читаются в момент отправки, а не при загрузке:
       иначе правка data-endpoint в уже открытой странице ни на что
       не влияла бы — а именно это и делают, когда подключают приёмник
       и проверяют, что он заработал. */
    function mail() { return form.getAttribute('data-mail') || ''; }

    /* Пока в data-endpoint стоит заглушка REPLACE_..., считаем приёмник
       незаполненным. Иначе форма честно пыталась бы отправить письмо
       на несуществующий адрес и говорила бы «не получилось». */
    function endpoint() {
      var e = form.getAttribute('data-endpoint') || '';
      return /^https?:\/\//i.test(e) ? e : '';
    }

    function say(text, kind) {
      if (!status) return;
      status.textContent = text;
      status.className = 'form__status' + (kind ? ' is-' + kind : '');
    }

    function reject(el, why) {
      el.setAttribute('aria-invalid', 'true');
      el.focus();
      say(why, 'err');
      return null;
    }

    /* Счётчик знаков. Считает остаток, а не набранное: предел важнее
       для того, кто пишет длинно, и он же подсказывает, когда пора
       заканчивать. */
    function tick() {
      if (!area || !left) return;
      var max = parseInt(area.getAttribute('maxlength'), 10) || 0;
      left.textContent = String(Math.max(0, max - area.value.length));
    }
    if (area) {
      area.addEventListener('input', tick);
      tick();
    }

    /* Поле, из-за которого не отправили, остаётся помеченным, пока в нём
       что-то не изменили — иначе красная рамка висит и после исправления. */
    form.addEventListener('input', function (e) {
      var el = e.target;
      if (el && el.getAttribute && el.getAttribute('aria-invalid')) {
        el.removeAttribute('aria-invalid');
      }
    });

    function collect() {
      var contact = document.getElementById('f-contact');
      var consent = document.getElementById('f-consent');

      if (!contact.value.trim()) {
        return reject(contact, 'Без контакта ответить некуда — впишите почту или ник в телеграме.');
      }
      if (area.value.trim().length < 10) {
        return reject(area, 'Слишком коротко. Напишите хотя бы пару фраз — иначе непонятно, о чём речь.');
      }
      if (!consent.checked) {
        consent.focus();
        say('Нужно согласие на обработку данных: без него у меня нет права читать письмо.', 'err');
        return null;
      }

      var whom = document.getElementById('f-name');
      return {
        topic:   document.getElementById('f-topic').value,
        name:    whom.value.trim(),
        contact: contact.value.trim(),
        message: area.value.trim()
      };
    }

    function letter(d) {
      var lines = ['Повод: ' + d.topic];
      if (d.name) lines.push('Имя: ' + d.name);
      lines.push('Контакт: ' + d.contact, '', d.message, '', '—',
                 'Отправлено с сайта «Понемногу»');
      var subject = 'Понемногу — ' + d.topic + (d.name ? ' — ' + d.name : '');
      return 'mailto:' + mail()
           + '?subject=' + encodeURIComponent(subject)
           + '&body='    + encodeURIComponent(lines.join('\n'));
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();

      /* Ловушка: её заполняет только робот. Такому гостю отвечаем тем же,
         что и человеку, — «письмо ушло», — но никуда ничего не отправляем.
         Говорить «вы робот» нельзя: это подсказка, как обойти проверку. */
      if (trap && trap.value) {
        say('Письмо ушло. Отвечу в течение дня.', 'ok');
        return;
      }

      var d = collect();
      if (!d) return;

      var to = endpoint();
      if (!to) {
        window.location.href = letter(d);
        say('Письмо собрано — отправьте его из почтовой программы. '
           + 'Если она не открылась, напишите на ' + mail() + '.', 'ok');
        return;
      }

      if (button) button.disabled = true;
      say('Отправляю…');
      fetch(to, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(d)
      }).then(function (r) {
        if (!r.ok) throw new Error(String(r.status));
        form.reset();
        tick();
        say('Письмо ушло. Отвечу в течение дня.', 'ok');
      }).catch(function () {
        /* Связь пропала или приёмник отказал — не оставляем человека
           с пустым экраном: даём адрес, который работает всегда. */
        say('Отправить не получилось — похоже, нет связи. Напишите на ' + mail() + '.', 'err');
      }).then(function () {
        if (button) button.disabled = false;
      });
    });
  }());

  /* ------------------------------------------------------- прогресс чтения */
  (function progress() {
    var bar = $('.progress');
    if (!bar) return;

    function frame() {
      var h = root.scrollHeight - window.innerHeight;
      var done = h > 0 ? window.scrollY / h : 0;
      bar.style.transform = 'scaleX(' + Math.max(0, Math.min(1, done)) + ')';
    }

    window.addEventListener('scroll', throttle(frame), { passive: true });
    window.addEventListener('resize', throttle(frame));
    frame();
  }());
}());
