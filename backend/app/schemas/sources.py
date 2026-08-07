from pydantic import BaseModel


class SourceOut(BaseModel):
    id: str
    title: str
    url: str
    authors: str
    license: str
    license_url: str
    provides: str
    version: str | None = None
    modifications: list[str]


class SourcesOut(BaseModel):
    sources: list[SourceOut]
    # Источники, чья лицензия требует указания авторства прямо в интерфейсе.
    screen_attribution_required: list[str]
