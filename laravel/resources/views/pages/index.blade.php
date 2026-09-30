@extends('layouts.blog')

@section('content')

  <!-- ================= Ведущий материал ================= -->
  <!-- Картинка стоит СЗАДИ текста: полотно растянуто на всю ширину окна,
       а метка, заголовок, лид и фигура «0 ₽» лежат поверх него. Плотное
       в картинке собрано в правой четверти — там, где текста нет, —
       поэтому заголовок и ограничен по ширине (см. раздел 28 styles.css).
       alt пустой: это фон, а не содержание, смысл тот же, что в тексте
       рядом. Живёт в img/lead-perevody.svg, рисуется tools/make-art.py. -->
  <section class="lead lead--front" data-c="dengi">
    <figure class="lead__art" aria-hidden="true">
      <img src="img/lead-perevody.svg" width="1600" height="1000" decoding="async" alt="">
    </figure>

    <div class="wrap lead__inner">
      <p class="kicker kicker--accent reveal">§ 01 — Про деньги</p>

      <h1 class="reveal">Я перестал платить за&nbsp;переводы себе в&nbsp;другой&nbsp;банк</h1>

      <div class="split split--7-5 lead__foot">

        <div class="reveal">
          <p class="lead__standfirst">
            В марте я разложил деньги по двум банкам и приготовился терять
            на комиссиях. Через семь месяцев открыл выписку и посчитал,
            сколько это стоило на самом деле.
          </p>
          <p class="lead__byline meta">
            <span>Артур Тарасов</span>
            <span>8 минут чтения</span>
            <span>14 сентября 2026</span>
          </p>
          <p class="lead__more">
            <a class="link" href="perevody.html">Читать историю</a>
          </p>
        </div>

        <figure class="figure reveal">
          <p class="figure__numeral">0<span class="figure__unit">₽</span></p>
          <figcaption>
            столько комиссий за переводы себе в другой банк
            я заплатил за семь месяцев — по данным моей выписки
          </figcaption>
        </figure>

      </div>

    </div>
  </section>

  <!-- ================= Пять разделов ================= -->
  <section class="wrap section" aria-labelledby="rail-h">
    <div class="index__head">
      <h2 class="kicker" id="rail-h">Пять разделов</h2>
      <span class="kicker">Обо всём понемногу</span>
    </div>

    <div class="rail">
      <a class="rail__panel" href="/blog/#dengi" data-c="dengi">
        <span class="rail__n">§ 01–07</span>
        <span class="rail__name">Деньги</span>
        <span class="rail__text">Переводы, кэшбэк, накопления, карты. Семь историй о том, как устроены мои собственные деньги — с цифрами из выписок.</span>
        <span class="rail__count">Семь историй</span>
      </a>
      <a class="rail__panel" href="/blog/#biznes" data-c="biznes">
        <span class="rail__n">§ 08</span>
        <span class="rail__name">Бизнес</span>
        <span class="rail__text">Как я потратил чужие сорок тысяч на рекламу и узнал, что выручка и деньги — разные числа.</span>
        <span class="rail__count">Одна история</span>
      </a>
      <a class="rail__panel" href="/blog/#it" data-c="it">
        <span class="rail__n">§ 09</span>
        <span class="rail__name">Техника</span>
        <span class="rail__text">Домашний сервер, подписки и один диск, который умер ровно тогда, когда не должен был.</span>
        <span class="rail__count">Одна история</span>
      </a>
      <a class="rail__panel" href="/blog/#sport" data-c="sport">
        <span class="rail__n">§ 10</span>
        <span class="rail__name">Спорт</span>
        <span class="rail__text">Год без зала: ходьба, турник в коридоре и двенадцать недель, о которых обычно не пишут.</span>
        <span class="rail__count">Одна история</span>
      </a>
      <a class="rail__panel" href="/blog/#zhizn" data-c="zhizn">
        <span class="rail__n">§ 11</span>
        <span class="rail__name">Жизнь</span>
        <span class="rail__text">Переезд, смета и факт. И всё остальное, что не про деньги напрямую, но всё равно про них.</span>
        <span class="rail__count">Одна история</span>
      </a>
    </div>

  </section>

  <!-- ================= Что я пробовал ================= -->
  <section class="wrap section" aria-labelledby="tried-h">
    <div class="index__head">
      <h2 class="kicker" id="tried-h">Что я пробовал и чем кончилось</h2>
      <span class="kicker">Одиннадцать историй в одной таблице</span>
    </div>

    <table class="tried">
      <caption>
        Не советы, а результат. Столбец «Бросил» — не провал: просто
        не прижилось, и об этом тоже написано.
      </caption>
      <thead>
        <tr>
          <th scope="col">Что</th>
          <th scope="col">Пробовал</th>
          <th scope="col">Бросил</th>
          <th scope="col">Осталось</th>
        </tr>
      </thead>
      <tbody>
          <tr data-c="dengi" style="--i: 0">
            <th scope="row">Вести бюджет в таблице<span class="tried__topic">Деньги</span></th>
            <td><span class="tried__yes" aria-hidden="true">✓</span><span class="visually-hidden">да</span></td>
            <td><span class="tried__yes" aria-hidden="true">✓</span><span class="visually-hidden">да</span></td>
            <td><span class="tried__no" aria-hidden="true">—</span><span class="visually-hidden">нет</span></td>
          </tr>
          <tr data-c="dengi" style="--i: 1">
            <th scope="row">Считать каждую покупку<span class="tried__topic">Деньги</span></th>
            <td><span class="tried__yes" aria-hidden="true">✓</span><span class="visually-hidden">да</span></td>
            <td><span class="tried__yes" aria-hidden="true">✓</span><span class="visually-hidden">да</span></td>
            <td><span class="tried__no" aria-hidden="true">—</span><span class="visually-hidden">нет</span></td>
          </tr>
          <tr data-c="dengi" style="--i: 2">
            <th scope="row">Держать четыре карты сразу<span class="tried__topic">Деньги</span></th>
            <td><span class="tried__yes" aria-hidden="true">✓</span><span class="visually-hidden">да</span></td>
            <td><span class="tried__yes" aria-hidden="true">✓</span><span class="visually-hidden">да</span></td>
            <td><span class="tried__no" aria-hidden="true">—</span><span class="visually-hidden">нет</span></td>
          </tr>
          <tr data-c="sport" style="--i: 3">
            <th scope="row">Абонемент в зал<span class="tried__topic">Спорт</span></th>
            <td><span class="tried__yes" aria-hidden="true">✓</span><span class="visually-hidden">да</span></td>
            <td><span class="tried__yes" aria-hidden="true">✓</span><span class="visually-hidden">да</span></td>
            <td><span class="tried__no" aria-hidden="true">—</span><span class="visually-hidden">нет</span></td>
          </tr>
          <tr data-c="dengi" style="--i: 4">
            <th scope="row">Приложение банка на главном экране<span class="tried__topic">Деньги</span></th>
            <td><span class="tried__yes" aria-hidden="true">✓</span><span class="visually-hidden">да</span></td>
            <td><span class="tried__yes" aria-hidden="true">✓</span><span class="visually-hidden">да</span></td>
            <td><span class="tried__no" aria-hidden="true">—</span><span class="visually-hidden">нет</span></td>
          </tr>
          <tr data-c="it" style="--i: 5">
            <th scope="row">Домашний сервер<span class="tried__topic">Техника</span></th>
            <td><span class="tried__yes" aria-hidden="true">✓</span><span class="visually-hidden">да</span></td>
            <td><span class="tried__no" aria-hidden="true">—</span><span class="visually-hidden">нет</span></td>
            <td><span class="tried__yes" aria-hidden="true">✓</span><span class="visually-hidden">да</span></td>
          </tr>
          <tr data-c="it" style="--i: 6">
            <th scope="row">Отдельная карта для подписок<span class="tried__topic">Техника</span></th>
            <td><span class="tried__yes" aria-hidden="true">✓</span><span class="visually-hidden">да</span></td>
            <td><span class="tried__no" aria-hidden="true">—</span><span class="visually-hidden">нет</span></td>
            <td><span class="tried__yes" aria-hidden="true">✓</span><span class="visually-hidden">да</span></td>
          </tr>
          <tr data-c="sport" style="--i: 7">
            <th scope="row">Ходить пешком каждый день<span class="tried__topic">Спорт</span></th>
            <td><span class="tried__yes" aria-hidden="true">✓</span><span class="visually-hidden">да</span></td>
            <td><span class="tried__no" aria-hidden="true">—</span><span class="visually-hidden">нет</span></td>
            <td><span class="tried__yes" aria-hidden="true">✓</span><span class="visually-hidden">да</span></td>
          </tr>
          <tr data-c="zhizn" style="--i: 8">
            <th scope="row">Подушка на накопительном счёте<span class="tried__topic">Жизнь</span></th>
            <td><span class="tried__yes" aria-hidden="true">✓</span><span class="visually-hidden">да</span></td>
            <td><span class="tried__no" aria-hidden="true">—</span><span class="visually-hidden">нет</span></td>
            <td><span class="tried__yes" aria-hidden="true">✓</span><span class="visually-hidden">да</span></td>
          </tr>
      </tbody>
    </table>
  </section>

  <!-- ================= Свежее ================= -->
  <section class="wrap section" aria-labelledby="fresh-h">
    <div class="index__head">
      <h2 class="kicker" id="fresh-h">Свежее</h2>
      <span class="kicker">Четыре истории</span>
    </div>

    <div data-slider>
      <div class="slider__track" tabindex="0" role="group" aria-label="Свежие истории">

        <article class="card" data-c="dengi">
          <a class="card__link" href="byudzhet.html">
            <span class="card__cover">
              <img src="img/cover-byudzhet.svg" alt="" width="1200" height="800" loading="lazy" decoding="async">
            </span>
            <span class="card__no">§ 07 — Про бюджет</span>
            <h3 class="card__title">Я вёл бюджет год и&nbsp;бросил. Вот что осталось</h3>
            <span class="card__meta"><span>7 минут</span><span>27 сентября</span></span>
          </a>
        </article>

        <article class="card" data-c="zhizn">
          <a class="card__link" href="zhizn.html">
            <span class="card__cover">
              <img src="img/cover-zhizn.svg" alt="" width="1200" height="800" loading="lazy" decoding="async">
            </span>
            <span class="card__no">§ 11 — Про жизнь</span>
            <h3 class="card__title">Переезд: смета против факта</h3>
            <span class="card__meta"><span>7 минут</span><span>25 сентября</span></span>
          </a>
        </article>

        <article class="card" data-c="dengi">
          <a class="card__link" href="bezopasnost.html">
            <span class="card__cover">
              <img src="img/cover-bezopasnost.svg" alt="" width="1200" height="800" loading="lazy" decoding="async">
            </span>
            <span class="card__no">§ 06 — Про безопасность</span>
            <h3 class="card__title">Мне позвонили из банка. Это был не&nbsp;банк</h3>
            <span class="card__meta"><span>5 минут</span><span>24 сентября</span></span>
          </a>
        </article>

        <article class="card" data-c="dengi">
          <a class="card__link" href="prilozheniya.html">
            <span class="card__cover">
              <img src="img/cover-prilozheniya.svg" alt="" width="1200" height="800" loading="lazy" decoding="async">
            </span>
            <span class="card__no">§ 05 — Про приложения</span>
            <h3 class="card__title">Я убрал приложение банка с&nbsp;главного экрана</h3>
            <span class="card__meta"><span>5 минут</span><span>22 сентября</span></span>
          </a>
        </article>

      </div>

      <div class="slider__bar">
        <span class="slider__count" data-count aria-live="polite">01 / 04</span>
        <div class="slider__nav">
          <button class="slider__btn" type="button" data-prev aria-label="Предыдущая история">
            <svg aria-hidden="true"><use href="#i-arrow-left"></use></svg>
          </button>
          <button class="slider__btn" type="button" data-next aria-label="Следующая история">
            <svg aria-hidden="true"><use href="#i-arrow-right"></use></svg>
          </button>
        </div>
      </div>
    </div>
  </section>

  <!-- ================= Указатель материалов ================= -->
  <section class="index" id="index">
    <div class="wrap">

      <div class="index__head">
        <p class="kicker">Указатель</p>
        <p class="meta">Одиннадцать материалов · 70 минут чтения</p>
      </div>

      <article class="entry reveal" data-c="dengi">
        <a class="entry__link" href="perevody.html">
          <span class="entry__no">01</span>
          <span class="entry__body">
            <span class="entry__title">Я перестал платить за переводы себе в другой банк</span>
            <span class="entry__dek">Как я развёл зарплату и карту по разным банкам, чего боялся и что показала выписка за семь месяцев.</span>
          </span>
          <span class="entry__topic">Деньги</span>
          <span class="entry__time">8 мин</span>
        </a>
      </article>

      <article class="entry reveal" data-c="dengi">
        <a class="entry__link" href="keshbek.html">
          <span class="entry__no">02</span>
          <span class="entry__body">
            <span class="entry__title">Кэшбэк, который я полгода считал в таблице</span>
            <span class="entry__dek">Я записывал каждую покупку, чтобы понять, какие категории мне нужны на самом деле. Таблица сказала не то, что я ожидал.</span>
          </span>
          <span class="entry__topic">Деньги</span>
          <span class="entry__time">6 мин</span>
        </a>
      </article>

      <article class="entry reveal" data-c="dengi">
        <a class="entry__link" href="kopilka.html">
          <span class="entry__no">03</span>
          <span class="entry__body">
            <span class="entry__title">Копилка, которую я не заметил</span>
            <span class="entry__dek">Я не умею копить. Поэтому перестал копить и просто перестал мешать деньгам оставаться на счёте.</span>
          </span>
          <span class="entry__topic">Деньги</span>
          <span class="entry__time">5 мин</span>
        </a>
      </article>

      <article class="entry reveal" data-c="dengi">
        <a class="entry__link" href="karty.html">
          <span class="entry__no">04</span>
          <span class="entry__body">
            <span class="entry__title">У меня было четыре карты, и три оказались лишними</span>
            <span class="entry__dek">Я посчитал, во что обходится держать карты, которые лежат в ящике. Первый расчёт оказался неверным — и поэтому я его переделал.</span>
          </span>
          <span class="entry__topic">Деньги</span>
          <span class="entry__time">6 мин</span>
        </a>
      </article>

      <article class="entry reveal" data-c="dengi">
        <a class="entry__link" href="prilozheniya.html">
          <span class="entry__no">05</span>
          <span class="entry__body">
            <span class="entry__title">Я убрал приложение банка с главного экрана</span>
            <span class="entry__dek">Не удалил, а убрал в папку на третью страницу. Открывать стал в шесть раз реже — и что из этого вышло на самом деле.</span>
          </span>
          <span class="entry__topic">Деньги</span>
          <span class="entry__time">5 мин</span>
        </a>
      </article>

      <article class="entry reveal" data-c="dengi">
        <a class="entry__link" href="bezopasnost.html">
          <span class="entry__no">06</span>
          <span class="entry__body">
            <span class="entry__title">Мне позвонили из банка. Это был не банк</span>
            <span class="entry__dek">Он знал моё имя, отчество и последние четыре цифры карты. Я не потерял денег — но только потому, что мне было лень.</span>
          </span>
          <span class="entry__topic">Деньги</span>
          <span class="entry__time">5 мин</span>
        </a>
      </article>

      <article class="entry reveal" data-c="dengi">
        <a class="entry__link" href="byudzhet.html">
          <span class="entry__no">07</span>
          <span class="entry__body">
            <span class="entry__title">Я вёл бюджет год и бросил. Вот что осталось</span>
            <span class="entry__dek">Двадцать две категории, четыре таблицы и двенадцать месяцев учёта. В итоге пригодилось одно число и десять минут в воскресенье.</span>
          </span>
          <span class="entry__topic">Деньги</span>
          <span class="entry__time">7 мин</span>
        </a>
      </article>

      <article class="entry reveal" data-c="biznes">
        <a class="entry__link" href="biznes.html">
          <span class="entry__no">08</span>
          <span class="entry__body">
            <span class="entry__title">Первый счёт за рекламу</span>
            <span class="entry__dek">Сорок тысяч, тридцать один заказ и восемьдесят четыре тысячи выручки, которая оказалась меньше затрат.</span>
          </span>
          <span class="entry__topic">Бизнес</span>
          <span class="entry__time">8 мин</span>
        </a>
      </article>

      <article class="entry reveal" data-c="it">
        <a class="entry__link" href="it.html">
          <span class="entry__no">09</span>
          <span class="entry__body">
            <span class="entry__title">Я собрал домашний сервер и полгода его чинил</span>
            <span class="entry__dek">Мини-компьютер, четыре службы и диск, который умер не вовремя. Осталось две службы и одно правило.</span>
          </span>
          <span class="entry__topic">Техника</span>
          <span class="entry__time">7 мин</span>
        </a>
      </article>

      <article class="entry reveal" data-c="sport">
        <a class="entry__link" href="sport.html">
          <span class="entry__no">10</span>
          <span class="entry__body">
            <span class="entry__title">Год без зала</span>
            <span class="entry__dek">Тридцать две тысячи за абонемент, сорок один поход и двенадцать недель, о которых обычно не пишут.</span>
          </span>
          <span class="entry__topic">Спорт</span>
          <span class="entry__time">6 мин</span>
        </a>
      </article>

      <article class="entry reveal" data-c="zhizn">
        <a class="entry__link" href="zhizn.html">
          <span class="entry__no">11</span>
          <span class="entry__body">
            <span class="entry__title">Переезд: смета против факта</span>
            <span class="entry__dek">Я посчитал, что переезд обойдётся в сто двадцать тысяч. Он обошёлся в сто девяносто семь. Разница выросла из семи мелочей.</span>
          </span>
          <span class="entry__topic">Жизнь</span>
          <span class="entry__time">7 мин</span>
        </a>
      </article>

    </div>
  </section>

  <!-- ================= Честно о том, как это устроено ================= -->
  <section class="manifesto">
    <div class="wrap">
      <p class="reveal">
        Это блог обо всём понемногу: деньги, работа, техника, спорт, жизнь.
        Я не продаю курсы и не учу, как разбогатеть, — я разбираю собственный
        опыт и считаю цифры. В части текстов есть <em>партнёрская ссылка</em>,
        и я всегда говорю об этом прямо, в начале материала.
      </p>
      <p class="manifesto__foot reveal">
        Если вы оформите карту по моей ссылке, банк заплатит мне. Вам это
        не будет стоить ничего: цена и условия те же, что и при обычном
        оформлении. Я пишу только о том, чем пользуюсь сам, и не беру
        денег за отзывы.
      </p>
    </div>
  </section>

@endsection
