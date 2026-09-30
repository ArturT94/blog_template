<header class="masthead">
  <div class="wrap">
    <div class="masthead__meta">
      <span>Блог обо всём понемногу</span>
      <span>Выпуск № 12 — сентябрь 2026</span>
    </div>

    <div class="masthead__bar">
      <a class="wordmark" href="/">
        <svg class="mark" aria-hidden="true"><use href="#i-mark"></use></svg>
        <span>Понемногу</span>
      </a>

      <div class="masthead__tools">
        <nav class="nav" id="nav" aria-label="Основная навигация">
          <a href="/blog/" @if(Route::is('blog')) aria-current="page" @endif><span class="nav__n">01</span>Истории</a>
          <a href="/about/" @if(Route::is('about')) aria-current="page" @endif><span class="nav__n">02</span>Об авторе</a>
          <a href="/voprosy/" @if(Route::is('voprosy')) aria-current="page" @endif><span class="nav__n">03</span>Вопросы</a>
          <a href="/chestno/" @if(Route::is('chestno')) aria-current="page" @endif><span class="nav__n">04</span>Честно о ссылках</a>
          <a href="/sotrudnichestvo/" @if(Route::is('sotrudnichestvo')) aria-current="page" @endif><span class="nav__n">05</span>Сотрудничество</a>
        </nav>

        <!-- Без JS это обычная ссылка на blog.html, где перечислены все
             истории с фильтром по разделам. С JS main.js перехватывает
             клик и открывает панель поиска. -->
        <a class="search-open" href="/blog/" aria-label="Поиск по сайту" title="Поиск — клавиша /">
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
