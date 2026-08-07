from pydantic import BaseModel, ConfigDict


class ExampleWordOut(BaseModel):
    word: str
    kana: str | None = None
    romaji: str | None = None
    translation: str | None = None


class StrokePointOut(BaseModel):
    x: float
    y: float


class StrokeOut(BaseModel):
    d: str
    start: StrokePointOut | None = None
    instruction: str | None = None


class KanjiOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    character: str
    order_index: int
    meaning: str | None
    kun_reading_kana: str | None
    kun_reading_romaji: str | None
    on_reading_kana: str | None
    on_reading_romaji: str | None
    jlpt_level: str | None
    stroke_count: int | None
    writing_note: str | None
    example_words: list[ExampleWordOut]
    strokes: list[StrokeOut]


class KanjiListItemOut(BaseModel):
    """Урезанная карточка для списка справочника.

    Отличается от KanjiOut отсутствием strokes, writing_note и example_words —
    это материал экрана урока, а не списка. Пути черт занимали половину веса
    ответа (139 КБ против 69 КБ на страницу из 81 записи) и точно так же
    ложились в кэш Redis, где место ограничено 256 МБ с вытеснением по LRU:
    один запрос справочника вытеснял бы полезные ключи вдвое быстрее, чем нужно.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    character: str
    order_index: int
    meaning: str | None
    kun_reading_kana: str | None
    kun_reading_romaji: str | None
    on_reading_kana: str | None
    on_reading_romaji: str | None
    jlpt_level: str | None
    stroke_count: int | None


class KanjiListOut(BaseModel):
    items: list[KanjiListItemOut]
    total: int
    limit: int
    offset: int
