<!doctype html>
<html lang="ru" class="no-js" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>@yield('title', 'Понемногу — блог обо всём понемногу')</title>
<meta name="description" content="@yield('description', 'Деньги, бизнес, техника, спорт, жизнь — одиннадцать историй с цифрами из собственных выписок. Без давления и без обещаний доходности. Партнёрские ссылки всегда помечены.')">
<!-- Светлая тема — оформление по умолчанию; тёмная включается только
     переключателем, поэтому theme-color здесь один и меняется из JS. -->
<meta name="theme-color" content="#FFFCF7">
<!-- @seo — правится в tools/make-seo.py -->
<link rel="canonical" href="https://REPLACE-DOMAIN/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Понемногу">
<meta property="og:locale" content="ru_RU">
<meta property="og:url" content="https://REPLACE-DOMAIN/">
<meta property="og:title" content="Понемногу — блог обо всём понемногу">
<meta property="og:description" content="Деньги, бизнес, техника, спорт, жизнь — одиннадцать историй с цифрами из собственных выписок. Без давления и без обещаний доходности. Партнёрские ссылки всегда помечены.">
<meta property="og:image" content="https://REPLACE-DOMAIN/img/og/og-default.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Понемногу — блог обо всём понемногу">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Понемногу — блог обо всём понемногу">
<meta name="twitter:description" content="Деньги, бизнес, техника, спорт, жизнь — одиннадцать историй с цифрами из собственных выписок. Без давления и без обещаний доходности. Партнёрские ссылки всегда помечены.">
<meta name="twitter:image" content="https://REPLACE-DOMAIN/img/og/og-default.png">
<script type="application/ld+json">{"@@context":"https://schema.org","@graph":[{"@type":"WebSite","@id":"https://REPLACE-DOMAIN/#site","url":"https://REPLACE-DOMAIN/","name":"Понемногу","inLanguage":"ru-RU","description":"Блог обо всём понемногу: деньги, бизнес, техника, спорт, жизнь."},{"@type":"Person","@id":"https://REPLACE-DOMAIN/#author","name":"Артур Тарасов","url":"https://REPLACE-DOMAIN/o-sebe.html"},{"@type":"Organization","@id":"https://REPLACE-DOMAIN/#publisher","name":"Понемногу","url":"https://REPLACE-DOMAIN/"}]}</script>
<!-- /@seo -->


<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%23FFFCF7'/%3E%3Cg transform='translate(5.12 5.12) scale(0.68)'%3E%3Cg fill='%231B1613'%3E%3Crect x='3.4' y='23.8' width='12.0' height='7.2' rx='3.6'/%3E%3Crect x='7.0' y='12.4' width='15.6' height='7.2' rx='3.6'/%3E%3C/g%3E%3Crect x='10.6' y='1.0' width='19.2' height='7.2' rx='3.6' fill='%23E8501E'/%3E%3C/g%3E%3C/svg%3E">

<link rel="preload" href="{{ asset('fonts/literata-normal-cyrillic.woff2') }}" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{{ asset('fonts/literata-normal-latin.woff2') }}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{{ asset('styles.css') }}">
<script src="{{ asset('main.js') }}" defer></script>
<script>
/* Тема выставляется до первой отрисовки, иначе будет вспышка светлого фона. */
(function () {
  var root = document.documentElement;
  root.className = root.className.replace('no-js', 'js');
  try {
    // На <html> уже стоит data-theme="light": система на оформление
    // не влияет, тёмная включается только переключателем.
    var saved = localStorage.getItem('theme');
    if (saved) {
      root.setAttribute('data-theme', saved);
      if (saved === 'dark') {
        var meta = document.querySelector('meta[name="theme-color"]');
        if (meta) meta.setAttribute('content', '#14110E');
      }
    }
  } catch (e) { /* приватный режим — остаётся светлая */ }
}());
</script>
</head>

<body id="top">

@include('partials.sprite')

<div class="progress" aria-hidden="true"></div>
<a class="skip" href="#main">К содержанию</a>

@include('partials.masthead')

@include('partials.overlays')

<main id="main">
@yield('content')
</main>

@include('partials.colophon')
</body>
</html>
