<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Section extends Model
{
    protected $fillable = [
        'key',
        'title',
        'sort',

    ];
    public function articles(): hasMany {
        return $this->hasMany(Article::class);
    }
}
