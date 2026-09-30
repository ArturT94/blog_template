<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Support\Str;

/**
 * @property mixed $lead
 */
class Article extends Model
{
    protected $fillable = [
        'section_id', 'number', 'slug', 'title', 'lead',
        'art', 'art_alt', 'body', 'published_at',
    ];

    protected function casts(): array
    {
        return ['published_at' => 'datetime'];
    }

    public function section(): BelongsTo
    {
        return $this->belongsTo(Section::class);
    }

    public function scopePublished($query) {
        return $query->whereNotNull('published_at')->where('published_at', '<=', now());
    }

    protected function leadText(): Attribute {
        return Attribute::get(fn () => Str::of($this->lead)->stripTags()->squish());
    }

}
