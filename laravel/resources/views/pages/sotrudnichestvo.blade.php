@extends('layouts.blog')

@section('content')

    <header class="page__head">
        <div class="wrap">
            <p class="kicker kicker--accent">Как со мной работать</p>
            <h1>Сотрудничество</h1>
            <p class="article__standfirst">
                Блог ведёт один человек: без редакции, без отдела продаж
                и без прайса на всё подряд. Ниже — что я действительно беру
                в работу, чего не возьму ни за какие деньги и как написать,
                чтобы получить ответ.
            </p>
        </div>
    </header>

    <section class="wrap" style="padding-block: var(--sp-8) var(--section-gap)">
        <div class="index__head" style="margin-bottom:0">
            <h2 class="kicker">Что можно предложить</h2>
            <span class="kicker">Четыре повода написать</span>
        </div>

        <div class="steps cascade">

            <article class="step">
                <p class="step__no">01 — бесплатно</p>
                <div>
                    <h3 class="step__title">Предложить тему</h3>
                    <p class="step__text">
                        Если вы знаете сюжет, который стоит разобрать, — расскажите.
                        Свой опыт или чужой, неважно: мне интересны случаи, где есть
                        цифры, ошибка и развязка. Если тема мне незнакома, я скажу
                        об этом прямо и писать по чужим словам не стану.
                    </p>
                </div>
            </article>

            <article class="step">
                <p class="step__no">02 — бесплатно, но без гарантий</p>
                <div>
                    <h3 class="step__title">Прислать продукт на тест</h3>
                    <p class="step__text">
                        Присылайте, если готовы к тому, что я напишу как есть — вместе
                        с минусами и с тем, что мне не пригодилось. Вещь верну, отдам
                        или оставлю, как скажете. Текст покажу до публикации, но правки
                        принимаю только по фактам: «уберите этот абзац» без причины —
                        не приму.
                    </p>
                </div>
            </article>

            <article class="step">
                <p class="step__no">03 — платно</p>
                <div>
                    <h3 class="step__title">Размещение с пометкой</h3>
                    <p class="step__text">
                        Реклама здесь есть, но она выглядит как реклама: отдельная
                        плашка, слово «Реклама» в начале и маркировка по закону. Стоимость
                        зависит от объёма и от того, сколько времени займёт проверка
                        фактов, — обсуждаем в переписке, без медиакита с круглыми цифрами.
                    </p>
                </div>
            </article>

            <article class="step">
                <p class="step__no">04 — бесплатно, и это ценнее всего</p>
                <div>
                    <h3 class="step__title">Сообщить об ошибке</h3>
                    <p class="step__text">
                        Нашли неточность — напишите. Исправлю и допишу в конце текста,
                        что именно поменялось и когда. Молча правлю только опечатки:
                        тихая правка по смыслу — это то же враньё, просто аккуратнее
                        оформленное.
                    </p>
                </div>
            </article>

        </div>
    </section>

    <section class="wrap" style="padding-bottom: var(--section-gap)">
        <div class="index__head">
            <h2 class="kicker">Чего здесь не будет</h2>
            <span class="kicker">Пять пунктов, ради которых предыдущие что-то значат</span>
        </div>

        <div class="split split--7-5">
            <div class="prose">
                <p>
                    Список короткий, но именно из-за него первые три пункта выше
                    что-то значат.
                </p>

                <ul class="list">
                    <li>Ссылок за деньги без пометки — ни в тексте, ни в подвале,
                        ни «в благодарность за помощь».</li>
                    <li>Обзоров по брифу: когда заранее известно, что написать
                        и каким должен быть вывод.</li>
                    <li>Чужих текстов под моим именем — включая «полезные статьи»
                        с ссылкой внутри.</li>
                    <li>Обмена ссылками и ссылочных бирж. Это не про честность,
                        это про то, что от них сайт перестаёт быть нужным людям.</li>
                    <li>Ставок, процентов и лимитов как факта. Тарифы меняются,
                        а текст на сайте — нет; вместо цифр я показываю, где
                        их смотреть.</li>
                </ul>

                <p>
                    Если ваше предложение попадает в этот список — я отвечу отказом,
                    но отвечу, а не пропаду. Правила, по которым я веду блог целиком,
                    разобраны на странице
                    <a class="link" href="/chestno/">«Честно о ссылках»</a>.
                </p>
            </div>

            <aside>
                <p class="kicker" style="margin-bottom: var(--sp-5)">Ответ за день</p>
                <p class="step__text">
                    Пишу сам и читаю всё сам, поэтому отвечаю обычно в течение дня,
                    иногда — на следующий. Если ответа нет неделю, значит письмо
                    потерялось: напишите ещё раз, я не игнорирую намеренно.
                </p>
                <p class="disclosure" style="margin-top: var(--sp-5)">
                    Форма ниже отправляет письмо с вашего адреса. Ничего не сохраняется
                    на сайте — см. <a class="link" href="#dannye">«Что будет с вашими
                        данными»</a>.
                </p>
            </aside>
        </div>
    </section>

    <!-- ================= Форма обратной связи ================= -->
    <section class="wrap" id="napishite" style="padding-bottom: var(--section-gap)">
        <div class="index__head">
            <h2 class="kicker">Написать</h2>
            <span class="kicker">Ответ придёт на указанный контакт</span>
        </div>

        <div class="split split--5-7">
            <div>
                <p class="step__text">
                    Пяти полей хватит, чтобы я понял, о чём речь. Если удобнее
                    написать сразу письмом — адрес
                    <a class="link" href="mailto:hi@example.com">hi@example.com</a>,
                    разницы нет.
                </p>

                <div class="index__head" style="margin: var(--sp-7) 0 var(--sp-4)">
                    <h3 class="kicker">Чтобы ответить по делу</h3>
                </div>
                <ul class="list">
                    <li>Чем вы занимаетесь — одной строкой, без презентации
                        компании на три абзаца.</li>
                    <li>Что предлагаете и что нужно от меня: тема, тест, размещение.</li>
                    <li>Срок, если он есть. Без срока я отвечу, но не быстро.</li>
                </ul>

                <p class="disclosure" style="margin-top: var(--sp-5)">
                    Капчи здесь нет намеренно: она мешает людям и почти не мешает
                    роботам. Вместо неё — поле-ловушка, которого вы не увидите.
                </p>
            </div>

            <form class="form" id="contact-form" novalidate
                  data-endpoint="REPLACE_FORM_ENDPOINT"
                  data-mail="hi@example.com">

                <div class="form__grid">

                    <div class="field">
                        <label class="field__label" for="f-topic">Повод</label>
                        <div class="field__wrap">
                            <select class="field__input field__input--select" id="f-topic" name="topic">
                                <option>Предложить тему</option>
                                <option>Прислать продукт на тест</option>
                                <option>Размещение с пометкой</option>
                                <option>Нашёл ошибку в тексте</option>
                                <option>Другое</option>
                            </select>
                            <svg class="field__chevron" aria-hidden="true"><use href="#i-chevron-down"></use></svg>
                        </div>
                    </div>

                    <div class="field">
                        <label class="field__label" for="f-name">
                            Как вас зовут <span class="field__opt">не обязательно</span>
                        </label>
                        <input class="field__input" id="f-name" name="name" type="text"
                               maxlength="80" autocomplete="name" placeholder="Артур">
                    </div>

                    <div class="field field--wide">
                        <label class="field__label" for="f-contact">Куда ответить</label>
                        <input class="field__input" id="f-contact" name="contact" type="text"
                               required maxlength="120" autocomplete="email"
                               aria-describedby="f-contact-hint" placeholder="Почта или ник в телеграме">
                        <p class="field__hint" id="f-contact-hint">
                            Почта или ник в телеграме — как вам удобнее.
                        </p>
                    </div>

                    <div class="field field--wide">
                        <label class="field__label" for="f-message">Письмо</label>
                        <textarea class="field__input field__input--area" id="f-message" name="message"
                                  rows="7" required maxlength="1000"
                                  aria-describedby="f-message-hint"
                                  placeholder="Пара абзацев — этого достаточно."></textarea>
                        <p class="field__hint" id="f-message-hint">
                            До 1000 знаков. Осталось: <span class="num" id="f-left">1000</span>
                        </p>
                    </div>

                </div>

                <!-- Ловушка для роботов. Люди этого поля не видят: оно уведено
                     за край экрана, а не спрятано через display:none — те
                     не заполняют поля, которых нет в разметке. -->
                <div class="field field--trap">
                    <label class="field__label" for="f-website">Не заполняйте, если вы человек</label>
                    <input id="f-website" name="website" type="text" tabindex="-1" autocomplete="off">
                </div>

                <label class="consent" for="f-consent">
                    <input class="consent__box" id="f-consent" name="consent" type="checkbox" required>
                    <span>
            Согласен на обработку персональных данных —
            <a class="link" href="#dannye">что это значит на практике</a>.
          </span>
                </label>

                <div class="form__foot">
                    <button class="btn" type="submit" id="contact-send">
                        <svg class="icon" aria-hidden="true"><use href="#i-send"></use></svg>
                        Отправить
                    </button>
                    <p class="form__status" id="form-status" role="status" aria-live="polite"></p>
                </div>

            </form>

            <!-- Без скрипта письмо собрать не из чего: форма не уходит на сервер,
                 а зовёт почтовую программу. Поэтому честно говорим, куда писать,
                 вместо того чтобы делать вид, что кнопка работает. Стоит снаружи
                 <form>, чтобы правило .no-js .form её не гасило. -->
            <p class="form__noscript">
                Форма отправляется скриптом: он собирает письмо и открывает вашу
                почтовую программу. Скрипт выключен, поэтому кнопка не работает —
                напишите напрямую на
                <a class="link" href="mailto:hi@example.com">hi@example.com</a>.
            </p>
        </div>
    </section>

    <!-- ================= Данные ================= -->
    <section class="wrap" id="dannye" style="padding-bottom: var(--section-gap)">
        <div class="index__head">
            <h2 class="kicker">Что будет с вашими данными</h2>
            <span class="kicker">Коротко и без юридического тумана</span>
        </div>

        <div class="prose">
            <p>
                Форма собирает ровно то, что вы в неё вписали: повод, имя,
                контакт и текст письма. Больше ничего — ни cookies, ни счётчика
                на этой странице нет.
            </p>

            <h3>Куда это попадает</h3>
            <p>
                Письмо уходит с вашего адреса мне на почту. На сайте оно
                не сохраняется: у блога нет базы данных и нет админки, куда
                что-то складывать. Копия остаётся только в вашей папке
                «Отправленные» — и её можно удалить в любой момент, я не обижусь.
            </p>

            <h3>Зачем</h3>
            <p>
                Только чтобы ответить. Я не подписываю на рассылку, не передаю
                адрес третьим лицам и не использую его, чтобы напомнить о себе
                через полгода.
            </p>

            <h3>Сколько хранится</h3>
            <p>
                Пока идёт переписка. Когда разговор закончился и тема закрыта,
                письма удаляю — обычно вместе с разбором почты раз в пару месяцев.
                Если хотите, чтобы удалил прямо сейчас, — напишите, и удалю.
            </p>

            <p class="disclosure" style="margin-top: var(--sp-6)">
                Это не юридический документ, а честное описание того, что
                происходит технически. Если вам нужна политика обработки
                персональных данных в том виде, в каком её требует закон, —
                её у этого блога пока нет, и до её появления лучше писать мне
                на почту, минуя форму.
            </p>
        </div>
    </section>

@endsection
