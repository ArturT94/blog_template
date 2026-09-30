<?php

use Illuminate\Support\Facades\Route;

Route::view('/', 'pages.index')->name('home');
Route::view('/voprosy', 'pages.voprosy')->name('voprosy');
Route::view('/about', 'pages.about')->name('about');
Route::view('/chestno', 'pages.chestno')->name('chestno');
Route::view('/sotrudnichestvo', 'pages.sotrudnichestvo')->name('sotrudnichestvo');
Route::view('/blog', 'pages.blog')->name('blog');
