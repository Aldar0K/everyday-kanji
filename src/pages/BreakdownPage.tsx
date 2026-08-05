import { Navigate, useNavigate, useParams } from 'react-router-dom'
import { PageHeader } from '@/components/common/PageHeader'
import { Tag } from '@/components/common/Tag'
import { ExampleWordRow } from '@/components/kanji/ExampleWordRow'
import { ReadingRow } from '@/components/kanji/ReadingRow'
import { Button } from '@/components/ui/button'
import { useCurrentDay } from '@/hooks/useCurrentDay'
import { getKanjiByDay } from '@/lib/kanjiData'
import { pluralizeCherta } from '@/lib/russian'

export function BreakdownPage() {
  const { dayNumber } = useParams()
  const navigate = useNavigate()
  const currentDay = useCurrentDay()
  const day = Number(dayNumber)
  const kanji = getKanjiByDay(day)

  if (!kanji || !Number.isInteger(day) || day > currentDay) {
    return <Navigate to="/" replace />
  }

  return (
    <div className="flex min-h-dvh flex-col gap-5 px-[22px] pt-[66px] pb-10">
      <PageHeader label={`Урок ${day} · шаг 1 из 3`} onBack={() => navigate(`/day/${day}`)} />

      <div className="flex items-center gap-5 rounded-2xl bg-neutral-100 px-[22px] py-5 shadow-sm">
        <div className="font-kanji text-[82px] leading-none text-text">{kanji.character}</div>
        <div className="flex flex-col gap-1.5">
          <div className="font-heading text-[27px] font-semibold text-text">{kanji.meaning}</div>
          <div className="flex gap-1.5">
            <Tag variant="neutral" className="px-2.5 py-1 text-[11.5px]">
              {kanji.strokeCount} {pluralizeCherta(kanji.strokeCount)}
            </Tag>
            <Tag variant="accent2" className="px-2.5 py-1 text-[11.5px]">
              {kanji.jlptLevel}
            </Tag>
          </div>
        </div>
      </div>

      <div>
        <h2 className="mb-2.5 font-heading text-[19px] font-semibold text-text">Чтения</h2>
        <div className="flex flex-col gap-2.5">
          <ReadingRow label="кун" reading={kanji.kunReading} gloss="японское" variant="accent" />
          <ReadingRow label="он" reading={kanji.onReading} gloss="китайское" variant="accent2" />
        </div>
      </div>

      <div>
        <h2 className="mb-2.5 font-heading text-[19px] font-semibold text-text">Слова со знаком</h2>
        <div className="flex flex-col">
          {kanji.exampleWords.map((word, i) => (
            <ExampleWordRow key={word.word} word={word} isLast={i === kanji.exampleWords.length - 1} />
          ))}
        </div>
      </div>

      <div className="mt-auto">
        <Button variant="pill" size="block" onClick={() => navigate(`/day/${day}/strokes`)}>
          Дальше · как писать
        </Button>
      </div>
    </div>
  )
}
