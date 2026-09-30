<?php

namespace Database\Seeders;

use App\Models\Section;
use Illuminate\Database\Seeder;

class SectionSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        $sections = [
            ['key' => 'dengi',  'title' => 'Деньги', 'sort' => 1],
            ['key' => 'biznes', 'title' => 'Бизнес', 'sort' => 2],
            ['key' => 'it',     'title' => 'ИТ',     'sort' => 3],
            ['key' => 'sport',  'title' => 'Спорт',  'sort' => 4],
            ['key' => 'zhizn',  'title' => 'Жизнь',  'sort' => 5],
        ];

        foreach ($sections as $section) {
            Section::updateOrCreate([
                'key' => $section['key'],
            ], $section);
        }
    }
}
