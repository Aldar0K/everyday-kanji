"""Админка только на чтение.

Смотреть, что происходит на проде: какие знаки опубликованы, сколько устройств,
в каком состоянии SRS у карточек. Ничего не редактирует и не удаляет.

ПОЧЕМУ ТОЛЬКО ЧТЕНИЕ. Источник правды для контента — файлы в git
(data/kanji_ru.json), из них build_dataset собирает kanji.json, а seed заливает
его в базу. В seed.py есть кортеж UPDATABLE, и в нём перечислены ровно все
содержательные поля: meaning, writing_note, example_words, is_published. Любая
правка через браузер прожила бы до ближайшего деплоя, который тронет kanji.json,
и исчезла бы молча — заливка идёт автоматически.

Чтобы админка могла писать, нужно сначала решить обратное: признать базу
источником правды, убрать поля из UPDATABLE и согласиться, что правки контента
перестанут проходить ревью в PR. Это отдельное решение, а не настройка.

ДОСТУП. Наружу /admin закрыт HTTP Basic в nginx (nginx/default.conf). Своей
авторизации у админки нет намеренно: в приложении нет ни пользователей, ни
сессий, и заводить их ради одного служебного экрана незачем.
"""

from __future__ import annotations

from starlette.requests import Request
from starlette_admin.contrib.sqla import Admin, ModelView

from app.database import engine
from app.models import Device, Kanji, Review


class ReadOnlyView(ModelView):
    """Базовый вид без создания, правки и удаления.

    can_* у starlette-admin — это МЕТОДЫ, а не булевы поля, и они СИНХРОННЫЕ.
    Оба уточнения существенны. Присвоить `can_create = False` мало: библиотека
    вызывает их как функции. А объявить их `async def` — хуже, чем не трогать
    вовсе: библиотека проверяет результат без await, корутина всегда истинна,
    и режим «только чтение» молча превращается в разрешение писать. Ровно так
    здесь и вышло на первой версии — POST на /admin/kanji/create создавал
    строку в базе при внешне работающих ограничениях.
    """

    def can_create(self, request: Request) -> bool:  # noqa: ARG002
        return False

    def can_edit(self, request: Request) -> bool:  # noqa: ARG002
        return False

    def can_delete(self, request: Request) -> bool:  # noqa: ARG002
        return False


class KanjiView(ReadOnlyView):
    fields = [
        Kanji.order_index,
        Kanji.character,
        Kanji.meaning,
        Kanji.meaning_suggested_ru,
        Kanji.meaning_en,
        Kanji.kun_reading_kana,
        Kanji.kun_reading_romaji,
        Kanji.on_reading_kana,
        Kanji.on_reading_romaji,
        Kanji.jlpt_level,
        Kanji.stroke_count,
        Kanji.frequency,
        Kanji.is_published,
        Kanji.needs_review,
        Kanji.writing_note,
        Kanji.example_words,
    ]
    # strokes намеренно не в списке: это килобайты путей SVG на строку, в
    # таблице они нечитаемы и только замедляют выдачу.
    sortable_fields = [
        Kanji.order_index,
        Kanji.character,
        Kanji.jlpt_level,
        Kanji.stroke_count,
        Kanji.frequency,
        Kanji.is_published,
    ]
    searchable_fields = [Kanji.character, Kanji.meaning, Kanji.meaning_en]
    page_size = 50
    name = "Кандзи"
    label = "Кандзи"
    icon = "fa fa-language"


class DeviceView(ReadOnlyView):
    name = "Устройство"
    label = "Устройства"
    icon = "fa fa-mobile"


class ReviewView(ReadOnlyView):
    name = "Повторение"
    label = "Повторения"
    icon = "fa fa-repeat"


def mount_admin(app) -> None:  # noqa: ANN001
    admin = Admin(
        engine,
        title="Кандзи дня",
        base_url="/admin",
    )
    admin.add_view(KanjiView(Kanji))
    admin.add_view(DeviceView(Device))
    admin.add_view(ReviewView(Review))
    admin.mount_to(app)
