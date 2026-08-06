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


class KanjiListOut(BaseModel):
    items: list[KanjiOut]
    total: int
    limit: int
    offset: int
