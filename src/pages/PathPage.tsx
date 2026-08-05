import { useNavigate } from 'react-router-dom'
import { TrailConnector } from '@/components/trail/TrailConnector'
import { TrailFooter } from '@/components/trail/TrailFooter'
import { TrailHeader } from '@/components/trail/TrailHeader'
import { FutureNodes, TrailNode } from '@/components/trail/TrailNode'
import { useCurrentDay } from '@/hooks/useCurrentDay'
import { getKanjiByDay } from '@/lib/kanjiData'
import { dateLabel, greeting, trailSubtitle } from '@/lib/russian'

const PAST_OPACITIES = [0.7, 0.8, 1]
const MAX_PAST_VISIBLE = 3
const FUTURE_VISIBLE = 3

export function PathPage() {
  const navigate = useNavigate()
  const currentDay = useCurrentDay()

  if (currentDay < 1) {
    return (
      <div className="flex min-h-dvh items-center justify-center px-6 text-center text-neutral-600">
        Первый знак откроется скоро.
      </div>
    )
  }

  const pastCount = Math.min(MAX_PAST_VISIBLE, currentDay - 1)
  const pastDays = Array.from({ length: pastCount }, (_, i) => currentDay - pastCount + i)
  const opacities = PAST_OPACITIES.slice(PAST_OPACITIES.length - pastCount)
  const today = getKanjiByDay(currentDay)

  return (
    <div className="flex min-h-dvh flex-col">
      <TrailHeader dateLabel={dateLabel()} greeting={greeting()} subtitle={trailSubtitle(currentDay)} />

      <div className="flex flex-1 flex-col items-center px-[34px] pt-[26px]">
        {pastDays.map((day, i) => {
          const kanji = getKanjiByDay(day)
          if (!kanji) return null
          const align = i % 2 === 0 ? 'start' : 'center'
          const isLastPast = i === pastDays.length - 1
          return (
            <div key={day} className="flex w-full flex-col items-center">
              <TrailNode
                variant="completed"
                align={align}
                character={kanji.character}
                label={`день ${day} · ${kanji.meaning}`}
                opacity={opacities[i]}
                onClick={() => navigate(`/day/${day}`)}
              />
              <TrailConnector
                align={align}
                color={isLastPast ? 'neutral' : 'accent2'}
                height={isLastPast ? 24 : 20}
              />
            </div>
          )
        })}

        {today && (
          <>
            <TrailNode
              variant="today"
              align="center"
              character={today.character}
              label={today.meaning}
              sublabel="нажми, чтобы открыть · 4 минуты"
              onClick={() => navigate(`/day/${currentDay}`)}
            />
            <TrailConnector align="center" color="neutral" height={24} />
          </>
        )}

        <FutureNodes count={FUTURE_VISIBLE} />
      </div>

      <TrailFooter />
    </div>
  )
}
