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
</div>
