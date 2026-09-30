@extends('layouts.blog')

@section('content')

    <header class="page__head">
        <div class="wrap">
            <p class="kicker kicker--accent">Кто это пишет</p>
            <h1>Об авторе</h1>
            <p class="article__standfirst">
                Меня зовут Артур. Я не финансист, не аналитик и не сотрудник банка.
                Я просто человек, который однажды сел и посчитал свои собственные
                деньги — и удивился тому, что нашёл.
            </p>
        </div>
    </header>

    <section class="wrap" style="padding-block: var(--sp-8) var(--section-gap)">
        <div class="author cascade">

            <div>
                <div class="brandplate">
                    <svg class="brandplate__mark" aria-hidden="true"><use href="#i-mark"></use></svg>
                </div>
                <p class="brandplate__name">Понемногу <span>с 2026 года</span></p>
                <p class="disclosure" style="margin-top: var(--sp-4)">
                    Здесь могло быть фото. Стоит знак блога: подобранный портрет
                    из фотобанка — это чужое лицо, а своё я показывать не хочу.
                </p>
            </div>

            <div class="prose">
                <p>
                    Первую версию этого блога я написал для себя. Хотел разложить
                    по полкам то, что понял за год: почему у меня уходили деньги
                    на переводах, почему кэшбэк оказывался меньше, чем я думал,
                    и почему копилка не работала.
                </p>
                <p>
                    Когда текстов про деньги стало семь, оказалось, что показывать
                    их по одному неудобно: у каждого свой сюжет — карты, приложения,
                    безопасность, бюджет. Так появился сайт с указателем. А потом
                    выяснилось, что про деньги я пишу не потому, что они мне
                    интереснее всего, а просто так вышло. Теперь здесь пять
                    разделов: деньги, бизнес, техника, спорт и жизнь.
                </p>

                <h2>Почему здесь нет советов</h2>
                <p>
                    Потому что я не имею права их давать. Я не знаю вашу ситуацию,
                    ваш доход, ваши обязательства и вашу готовность к риску. Всё,
                    что я могу, — рассказать, что сделал сам, и показать цифры
                    из своих выписок.
                </p>
                <p>
                    Отсюда же и правило: <strong>в текстах нет ни одной ставки
                        и ни одного процента, поданного как факт.</strong> Тарифы
                    меняются, и я не хочу, чтобы через полгода этот сайт врал.
                    Вместо цифр — указание, где их смотреть.
                </p>

                <h2>Как я решаю, о чём писать</h2>
                <p>
                    Только о том, через что прошёл сам. Если я чем-то не пользовался —
                    я об этом не пишу, даже если тема выгодная. Это не благородство,
                    а расчёт: выдуманную историю невозможно проверить, а
                    непроверяемому тексту никто не поверит.
                </p>

                <h2>Про деньги</h2>
                <p>
                    Блог окупается партнёрскими ссылками на карту, которой я
                    пользуюсь. Мне платят фиксированную сумму за человека, который
                    оформил карту и выполнил условия банка, — не процент с чужих
                    трат. Подробно это разобрано на странице
                    <a class="link" href="/chestno/">«Честно о ссылках»</a>.
                </p>
            </div>

        </div>
    </section>

    <section class="wrap" style="padding-bottom: var(--section-gap)">
        <figure class="plate plate--parallax plate--reveal" style="--plate-ratio: 8 / 3">
            <img src="img/wide-vypiska.svg" alt="Полосы, похожие на строки банковской выписки" width="1600" height="600" loading="lazy" decoding="async">
        </figure>
        <p class="plate__cap">
            Так выглядит моя выписка, если убрать из неё всё лишнее: строки,
            из которых две — комиссии. Именно из-за них я начал этот блог.
        </p>
    </section>

    <section class="wrap" style="padding-bottom: var(--section-gap)">
        <div class="index__head" style="margin-bottom:0">
            <h2 class="kicker">Написать мне</h2>
            <span class="kicker">Отвечаю сам</span>
        </div>
        <div class="steps cascade">
            <article class="step">
                <p class="step__no">Почта</p>
                <div>
                    <h3 class="step__title"><a class="link" href="mailto:hi@example.com">hi@example.com</a></h3>
                    <p class="step__text">
                        По любым вопросам, включая партнёрскую программу. Обычно
                        отвечаю в течение дня.
                    </p>
                </div>
            </article>
            <article class="step">
                <p class="step__no">Телеграм</p>
                <div>
                    <h3 class="step__title"><a class="link" href="REPLACE_TELEGRAM_LINK" rel="noopener" target="_blank">Канал блога</a></h3>
                    <p class="step__text">
                        Короткие заметки между большими текстами. Ссылка ведёт
                        на канал — замените её на свой.
                    </p>
                </div>
            </article>
        </div>
    </section>

@endsection
