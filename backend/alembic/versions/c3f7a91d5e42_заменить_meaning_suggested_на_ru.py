"""заменить meaning_suggested на meaning_suggested_ru

Старое поле хранило догадку косвенного вывода значения из словаря слов. Тот
путь закрыт: он ошибался на самых базовых иероглифах (山 → «спекуляция; риск»
вместо «гора», 本 → «счётный суффикс» вместо «книга»), и держать заведомо
ложный черновик рядом с честным машинным переводом хуже, чем не держать
никакого — на вычитке человек видел бы два конкурирующих варианта.

Новое поле заполняется переводом готовых английских глосс KANJIDIC2
(scripts/etl/translate_meanings.py) и точно так же наружу не отдаётся.

Данные старой колонки не переносятся: они не имеют ценности, а перенос создал
бы видимость преемственности между разными по надёжности источниками.

Revision ID: c3f7a91d5e42
Revises: 6b28124140cd
Create Date: 2026-08-06 14:10:02.114508
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'c3f7a91d5e42'
down_revision: Union[str, None] = '6b28124140cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('kanji', sa.Column('meaning_suggested_ru', sa.Text(), nullable=True))
    op.drop_column('kanji', 'meaning_suggested')


def downgrade() -> None:
    op.add_column('kanji', sa.Column('meaning_suggested', sa.Text(), nullable=True))
    op.drop_column('kanji', 'meaning_suggested_ru')
