import { useState } from 'react'
import { Navigate, useNavigate, useParams } from 'react-router-dom'
import { PageHeader } from '@/components/common/PageHeader'
import { StrokeMiniThumb } from '@/components/kanji/StrokeMiniThumb'
import { StrokeOrderCanvas } from '@/components/kanji/StrokeOrderCanvas'
import { Button } from '@/components/ui/button'
import { useProgress } from '@/context/ProgressContext'
import { useCurrentDay } from '@/hooks/useCurrentDay'
import { getKanjiByDay } from '@/lib/kanjiData'

export function StrokeOrderPage() {
  const { dayNumber } = useParams()
  const navigate = useNavigate()
  const currentDay = useCurrentDay()
  const { markDayComplete } = useProgress()
  const [replayKey, setReplayKey] = useState(0)
  const day = Number(dayNumber)
  const kanji = getKanjiByDay(day)

  if (!kanji || !Number.isInteger(day) || day > currentDay) {
    return <Navigate to="/" replace />
  }

  function handleComplete() {
    markDayComplete(day)
    navigate('/')
  }

  const strokes = kanji.strokes

  return (
    <div className="flex min-h-dvh flex-col items-center gap-5 px-6 pt-[66px] pb-10">
      <PageHeader label={`Урок ${day} · шаг 3 из 3`} onBack={() => navigate(`/day/${day}/breakdown`)} className="flex w-full items-center gap-3" />

      <h1 className="w-full font-heading text-[28px] font-semibold text-text">
        Как писать <span className="font-kanji font-normal">{kanji.character}</span>
      </h1>

      <div className="relative aspect-square w-full overflow-hidden rounded-(--radius-card) bg-neutral-100 shadow-md">
        <StrokeOrderCanvas key={replayKey} strokes={strokes} />
      </div>

      <div className="flex w-full gap-3">
        {strokes.map((stroke, i) => (
          <StrokeMiniThumb
            key={i}
            strokes={strokes}
            thisIndex={i}
            instruction={`${i + 1} — ${stroke.instruction}`}
            variant={i === 0 ? 'accent' : 'neutral'}
          />
        ))}
      </div>

      <p className="w-full max-w-[320px] text-sm leading-relaxed text-neutral-700">
        {kanji.writingNote}
      </p>

      <div className="mt-auto flex w-full gap-2.5">
        <Button
          variant="pill-secondary"
          className="h-auto flex-1 py-[17px] text-base"
          onClick={() => setReplayKey((k) => k + 1)}
        >
          Ещё раз
        </Button>
        <Button
          variant="pill-accent2"
          className="h-auto flex-[2] py-[17px] text-base"
          onClick={handleComplete}
        >
          Урок пройден
        </Button>
      </div>
    </div>
  )
}
