import { Fragment } from 'react'
import { motion } from 'motion/react'
import { useNavigate } from 'react-router-dom'
import { ScreenError, ScreenLoading } from '@/components/common/ScreenState'
import { TrailConnector } from '@/components/trail/TrailConnector'
import { TrailFooter } from '@/components/trail/TrailFooter'
import { TrailHeader } from '@/components/trail/TrailHeader'
import { FutureNodes, TrailNode } from '@/components/trail/TrailNode'
import { useAsync } from '@/hooks/useAsync'
import { api } from '@/lib/api'
import { easeGentle, staggerContainer } from '@/lib/motion'
import { dateLabel, greeting, trailSubtitle } from '@/lib/russian'

const PAST_OPACITIES = [0.7, 0.8, 1]
const FUTURE_VISIBLE = 3

export function PathPage() {
  const navigate = useNavigate()
  const { data, error, loading, reload } = useAsync(() => api.getTrail())

  if (loading) return <ScreenLoading />
  if (error || !data) {
    return <ScreenError message={error ?? 'Не удалось загрузить тропу'} onRetry={reload} />
  }

  const { recent, today, studied_count: studiedCount } = data
  // Прозрачность нарастает по мере приближения к сегодняшнему дню.
  const opacities = PAST_OPACITIES.slice(PAST_OPACITIES.length - recent.length)

  return (
    <div className="flex min-h-dvh flex-col">
      <TrailHeader
        dateLabel={dateLabel()}
        greeting={greeting()}
        subtitle={trailSubtitle(
          today ? today.position : studiedCount + 1,
          data.today_completed,
        )}
      />

      <motion.div
        variants={staggerContainer}
        initial="hidden"
        animate="visible"
        className="flex flex-1 flex-col items-center px-8.5 pt-6.5"
      >
        {recent.map((node, i) => {
          const align = i % 2 === 0 ? 'start' : 'center'
          const isLast = i === recent.length - 1
          return (
            <Fragment key={node.kanji.id}>
              <TrailNode
                variant="completed"
                align={align}
                character={node.kanji.character}
                label={`день ${node.position} · ${node.kanji.meaning ?? ''}`}
                opacity={opacities[i] ?? 1}
                onClick={() =>
                  navigate(`/day/${node.kanji.id}`, {
                    state: { position: node.position },
                  })
                }
              />
              <TrailConnector
                align={align}
                color={isLast ? 'neutral' : 'accent2'}
                height={isLast ? 24 : 20}
              />
            </Fragment>
          )
        })}

        {today && (
          <>
            <TrailNode
              variant="today"
              align="center"
              character={today.kanji.character}
              label={today.kanji.meaning ?? ''}
              sublabel={
                data.today_completed
                  ? 'урок пройден · можно повторить'
                  : 'нажми, чтобы открыть · 4 минуты'
              }
              onClick={() =>
                navigate(`/day/${today.kanji.id}`, {
                  state: { position: today.position },
                })
              }
            />
            <TrailConnector align="center" color="neutral" height={24} />
          </>
        )}

        <FutureNodes count={FUTURE_VISIBLE} />
      </motion.div>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ ...easeGentle, delay: 0.5 }}
      >
        <TrailFooter />
      </motion.div>
    </div>
  )
}
