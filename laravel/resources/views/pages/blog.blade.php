@extends('layouts.blog')

@section('content')

    <header class="page__head">
        <div class="wrap">
            <p class="kicker kicker--accent">Указатель</p>
            <h1>Все истории</h1>
            <p class="article__standfirst">
                Одиннадцать историй в пяти разделах — деньги, бизнес, техника,
                спорт, жизнь. Разделы можно отфильтровать, но читать лучше с любого
                места и в любом порядке: связи между текстами нет, это не курс.
            </p>
        </div>
    </header>

    <section class="wrap" style="padding-block: var(--sp-7) var(--sp-8)">
        <div class="chips" role="group" aria-label="Отфильтровать по разделу">
            <button class="chip" type="button" data-filter="all" aria-pressed="true">Все</button>
            <button class="chip" type="button" data-filter="dengi" data-c="dengi" aria-pressed="false">Деньги</button>
            <button class="chip" type="button" data-filter="biznes" data-c="biznes" aria-pressed="false">Бизнес</button>
            <button class="chip" type="button" data-filter="it" data-c="it" aria-pressed="false">Техника</button>
            <button class="chip" type="button" data-filter="sport" data-c="sport" aria-pressed="false">Спорт</button>
            <button class="chip" type="button" data-filter="zhizn" data-c="zhizn" aria-pressed="false">Жизнь</button>
        </div>
    </section>

    <!-- ================= Деньги ================= -->
    <section class="wrap topic" id="dengi" data-topic="dengi" data-c="dengi" aria-labelledby="dengi-h">
        <div class="topic__head">
            <h2 class="topic__name" id="dengi-h">Деньги</h2>
            <p class="topic__count">Семь историй</p>
        </div>

        <ul class="cards cascade">

            <li class="card">
                <a class="card__link" href="perevody.html">
          <span class="card__cover">
            <img src="img/cover-perevody.svg" alt="" width="1200" height="800" loading="lazy" decoding="async">
          </span>
                    <span class="card__no">§ 01 — Про деньги</span>
                    <h3 class="card__title">Я перестал платить за переводы себе в&nbsp;другой банк</h3>
                    <p class="card__dek">Как я развёл зарплату и карту по разным банкам, чего боялся и что показала выписка за семь месяцев.</p>
                    <span class="card__meta"><span>8 минут</span><span>14 сентября 2026</span></span>
                </a>
            </li>

            <li class="card">
                <a class="card__link" href="keshbek.html">
          <span class="card__cover">
            <img src="img/cover-keshbek.svg" alt="" width="1200" height="800" loading="lazy" decoding="async">
          </span>
                    <span class="card__no">§ 02 — Про деньги</span>
                    <h3 class="card__title">Кэшбэк, который я полгода считал в&nbsp;таблице</h3>
                    <p class="card__dek">Я записывал каждую покупку, чтобы понять, какие категории мне нужны на самом деле. Таблица сказала не то, что я ожидал.</p>
                    <span class="card__meta"><span>6 минут</span><span>21 сентября 2026</span></span>
                </a>
            </li>

            <li class="card">
                <a class="card__link" href="kopilka.html">
          <span class="card__cover">
            <img src="img/cover-kopilka.svg" alt="" width="1200" height="800" loading="lazy" decoding="async">
          </span>
                    <span class="card__no">§ 03 — Про деньги</span>
                    <h3 class="card__title">Копилка, которую я не&nbsp;заметил</h3>
                    <p class="card__dek">Я не умею копить. Поэтому перестал копить и просто перестал мешать деньгам оставаться на счёте.</p>
                    <span class="card__meta"><span>5 минут</span><span>26 сентября 2026</span></span>
                </a>
            </li>

            <li class="card">
                <a class="card__link" href="karty.html">
          <span class="card__cover">
            <img src="img/cover-karty.svg" alt="" width="1200" height="800" loading="lazy" decoding="async">
          </span>
                    <span class="card__no">§ 04 — Про деньги</span>
                    <h3 class="card__title">У меня было четыре карты, и три оказались лишними</h3>
                    <p class="card__dek">Я посчитал, во что обходится держать карты, которые лежат в ящике. Первый расчёт оказался неверным — и поэтому я его переделал.</p>
                    <span class="card__meta"><span>6 минут</span><span>20 сентября 2026</span></span>
                </a>
            </li>

            <li class="card">
                <a class="card__link" href="prilozheniya.html">
          <span class="card__cover">
            <img src="img/cover-prilozheniya.svg" alt="" width="1200" height="800" loading="lazy" decoding="async">
          </span>
                    <span class="card__no">§ 05 — Про деньги</span>
                    <h3 class="card__title">Я убрал приложение банка с&nbsp;главного экрана</h3>
                    <p class="card__dek">Не удалил, а убрал в папку на третью страницу. Открывать стал в шесть раз реже — и что из этого вышло на самом деле.</p>
                    <span class="card__meta"><span>5 минут</span><span>22 сентября 2026</span></span>
                </a>
            </li>

            <li class="card">
                <a class="card__link" href="bezopasnost.html">
          <span class="card__cover">
            <img src="img/cover-bezopasnost.svg" alt="" width="1200" height="800" loading="lazy" decoding="async">
          </span>
                    <span class="card__no">§ 06 — Про деньги</span>
                    <h3 class="card__title">Мне позвонили из банка. Это был не&nbsp;банк</h3>
                    <p class="card__dek">Он знал моё имя, отчество и последние четыре цифры карты. Я не потерял денег — но только потому, что мне было лень.</p>
                    <span class="card__meta"><span>5 минут</span><span>24 сентября 2026</span></span>
                </a>
            </li>

            <li class="card">
                <a class="card__link" href="byudzhet.html">
          <span class="card__cover">
            <img src="img/cover-byudzhet.svg" alt="" width="1200" height="800" loading="lazy" decoding="async">
          </span>
                    <span class="card__no">§ 07 — Про деньги</span>
                    <h3 class="card__title">Я вёл бюджет год и&nbsp;бросил. Вот что осталось</h3>
                    <p class="card__dek">Двадцать две категории, четыре таблицы и двенадцать месяцев учёта. В итоге пригодилось одно число и десять минут в воскресенье.</p>
                    <span class="card__meta"><span>7 минут</span><span>27 сентября 2026</span></span>
                </a>
            </li>

        </ul>
    </section>

    <!-- ================= Бизнес ================= -->
    <section class="wrap topic" id="biznes" data-topic="biznes" data-c="biznes" aria-labelledby="biznes-h">
        <div class="topic__head">
            <h2 class="topic__name" id="biznes-h">Бизнес</h2>
            <p class="topic__count">Одна история</p>
        </div>

        <ul class="cards cascade">

            <li class="card">
                <a class="card__link" href="biznes.html">
          <span class="card__cover">
            <img src="img/cover-biznes.svg" alt="" width="1200" height="800" loading="lazy" decoding="async">
          </span>
                    <span class="card__no">§ 08 — Про бизнес</span>
                    <h3 class="card__title">Первый счёт за рекламу</h3>
                    <p class="card__dek">Сорок тысяч рублей, тридцать один заказ и восемьдесят четыре тысячи выручки, которая оказалась меньше затрат.</p>
                    <span class="card__meta"><span>8 минут</span><span>15 сентября 2026</span></span>
                </a>
            </li>

        </ul>
    </section>

    <!-- ================= Техника ================= -->
    <section class="wrap topic" id="it" data-topic="it" data-c="it" aria-labelledby="it-h">
        <div class="topic__head">
            <h2 class="topic__name" id="it-h">Техника</h2>
            <p class="topic__count">Одна история</p>
        </div>

        <ul class="cards cascade">

            <li class="card">
                <a class="card__link" href="it.html">
          <span class="card__cover">
            <img src="img/cover-it.svg" alt="" width="1200" height="800" loading="lazy" decoding="async">
          </span>
                    <span class="card__no">§ 09 — Про технику</span>
                    <h3 class="card__title">Я собрал домашний сервер и&nbsp;полгода его чинил</h3>
                    <p class="card__dek">Мини-компьютер за двенадцать тысяч, четыре службы и диск, который умер ровно тогда, когда не должен был.</p>
                    <span class="card__meta"><span>7 минут</span><span>17 сентября 2026</span></span>
                </a>
            </li>

        </ul>
    </section>

    <!-- ================= Спорт ================= -->
    <section class="wrap topic" id="sport" data-topic="sport" data-c="sport" aria-labelledby="sport-h">
        <div class="topic__head">
            <h2 class="topic__name" id="sport-h">Спорт</h2>
            <p class="topic__count">Одна история</p>
        </div>

        <ul class="cards cascade">

            <li class="card">
                <a class="card__link" href="sport.html">
          <span class="card__cover">
            <img src="img/cover-sport.svg" alt="" width="1200" height="800" loading="lazy" decoding="async">
          </span>
                    <span class="card__no">§ 10 — Про спорт</span>
                    <h3 class="card__title">Год без зала</h3>
                    <p class="card__dek">Тридцать две тысячи за абонемент, сорок один поход за год и двенадцать недель, о которых обычно не пишут.</p>
                    <span class="card__meta"><span>6 минут</span><span>19 сентября 2026</span></span>
                </a>
            </li>

        </ul>
    </section>

    <!-- ================= Жизнь ================= -->
    <section class="wrap topic" id="zhizn" data-topic="zhizn" data-c="zhizn" aria-labelledby="zhizn-h">
        <div class="topic__head">
            <h2 class="topic__name" id="zhizn-h">Жизнь</h2>
            <p class="topic__count">Одна история</p>
        </div>

        <ul class="cards cascade">

            <li class="card">
                <a class="card__link" href="zhizn.html">
          <span class="card__cover">
            <img src="img/cover-zhizn.svg" alt="" width="1200" height="800" loading="lazy" decoding="async">
          </span>
                    <span class="card__no">§ 11 — Про жизнь</span>
                    <h3 class="card__title">Переезд: смета против факта</h3>
                    <p class="card__dek">Я посчитал, что переезд обойдётся в сто двадцать тысяч. Он обошёлся в сто девяносто семь. Разница выросла из семи мелочей.</p>
                    <span class="card__meta"><span>7 минут</span><span>25 сентября 2026</span></span>
                </a>
            </li>

        </ul>
    </section>

    <!-- ================= Цитаты ================= -->
    <section class="band" aria-labelledby="quotes-h">
        <div class="wrap">
            <div class="index__head" style="border:0;padding-top:0">
                <h2 class="kicker" id="quotes-h">Из текстов</h2>
                <span class="kicker">Пролистайте →</span>
            </div>
        </div>

        <div class="wrap" data-slider>
            <div class="slider__track" tabindex="0" role="group" aria-label="Цитаты из историй">

                <blockquote class="slide" data-c="dengi">
                    <p>Ноль. Не «почти ноль», не «копейки», не «в пределах погрешности». Ноль рублей за семь месяцев.</p>
                    <footer><a class="link" href="perevody.html">01 — Про деньги</a></footer>
                </blockquote>

                <blockquote class="slide" data-c="dengi">
                    <p>Таблица показала, что две трети кэшбэка мне приносят категории, которые я выбрал наугад в первый месяц.</p>
                    <footer><a class="link" href="keshbek.html">02 — Про деньги</a></footer>
                </blockquote>

                <blockquote class="slide" data-c="dengi">
                    <p>Я девять раз за полгода залезал в копилку. Каждый раз — за день до зарплаты.</p>
                    <footer><a class="link" href="kopilka.html">03 — Про деньги</a></footer>
                </blockquote>

                <blockquote class="slide" data-c="dengi">
                    <p>Бесплатная карта, которой я не пользуюсь, — не бесплатная. Она бесплатная при условии, которое я обязан выполнять.</p>
                    <footer><a class="link" href="karty.html">04 — Про деньги</a></footer>
                </blockquote>

                <blockquote class="slide" data-c="dengi">
                    <p>Тридцать одно уведомление от одного приложения за сутки. Полезных из них — два.</p>
                    <footer><a class="link" href="prilozheniya.html">05 — Про деньги</a></footer>
                </blockquote>

                <blockquote class="slide" data-c="dengi">
                    <p>Я не разоблачил мошенника — в первые сорок секунд я верил ему полностью. Спасло меня то, что я не выспался и мне было лень.</p>
                    <footer><a class="link" href="bezopasnost.html">06 — Про деньги</a></footer>
                </blockquote>

                <blockquote class="slide" data-c="dengi">
                    <p>Я бы сказал: «процентов тридцать пять от дохода». По факту вышло шестьдесят один.</p>
                    <footer><a class="link" href="byudzhet.html">07 — Про деньги</a></footer>
                </blockquote>

                <blockquote class="slide" data-c="biznes">
                    <p>Выручка не значит ничего, она просто красивая. Решение принимается по нижней строке.</p>
                    <footer><a class="link" href="biznes.html">08 — Про бизнес</a></footer>
                </blockquote>

                <blockquote class="slide" data-c="it">
                    <p>Домашний сервер — это не хобби, а дежурство. Если ты единственный, кто может его починить, ты дежуришь всегда.</p>
                    <footer><a class="link" href="it.html">09 — Про технику</a></footer>
                </blockquote>

                <blockquote class="slide" data-c="sport">
                    <p>У меня не «год ходьбы», а сорок недель ходьбы и двенадцать недель лежания на диване.</p>
                    <footer><a class="link" href="sport.html">10 — Про спорт</a></footer>
                </blockquote>

                <blockquote class="slide" data-c="zhizn">
                    <p>Смета была не про деньги. Она была про спокойствие: я хотел знать, что справлюсь.</p>
                    <footer><a class="link" href="zhizn.html">11 — Про жизнь</a></footer>
                </blockquote>

                <blockquote class="slide" >
                    <p>Мне платят за то, что я привёл человека, а не за то, что этот человек много потратил.</p>
                    <footer><a class="link" href="/chestno/">Честно о ссылках</a></footer>
                </blockquote>

            </div>

            <div class="slider__bar">
                <span class="slider__count" data-count aria-live="polite">01 / 12</span>
                <div class="slider__nav">
                    <button class="slider__btn" type="button" data-prev aria-label="Предыдущая цитата">
                        <svg aria-hidden="true"><use href="#i-arrow-left"></use></svg>
                    </button>
                    <button class="slider__btn" type="button" data-next aria-label="Следующая цитата">
                        <svg aria-hidden="true"><use href="#i-arrow-right"></use></svg>
                    </button>
                </div>
            </div>
        </div>
    </section>

    <!-- ================= С чего начать ================= -->
    <section class="wrap" style="padding-block: var(--section-gap)">
        <div class="index__head" style="margin-bottom:0">
            <h2 class="kicker">Если впервые здесь</h2>
            <span class="kicker">Три шага</span>
        </div>

        <div class="steps cascade">
            <article class="step">
                <p class="step__no">01</p>
                <div>
                    <h3 class="step__title">Прочитайте «Честно о ссылках»</h3>
                    <p class="step__text">
                        Четыре минуты. Там написано, как я зарабатываю и почему
                        в текстах нет ни одной ставки. После этого остальные истории
                        читаются спокойнее.
                    </p>
                </div>
            </article>
            <article class="step">
                <p class="step__no">02</p>
                <div>
                    <h3 class="step__title">Начните с того раздела, который ближе</h3>
                    <p class="step__text">
                        Истории не связаны между собой. Про деньги — семь текстов,
                        про бизнес, технику, спорт и жизнь — по одному, и они
                        ничуть не хуже.
                    </p>
                </div>
            </article>
            <article class="step">
                <p class="step__no">03</p>
                <div>
                    <h3 class="step__title">Проверьте условия сами</h3>
                    <p class="step__text">
                        Я не пересказываю тарифы, потому что они меняются. Перед тем
                        как что-то оформлять, посмотрите условия в приложении банка —
                        там всегда актуальная версия.
                    </p>
                </div>
            </article>
        </div>
    </section>

@endsection
