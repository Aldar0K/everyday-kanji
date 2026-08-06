import { useState } from 'react'
import { motion } from 'motion/react'
import { useLocation, useNavigate, useParams } from 'react-router-dom'
import { MotionButton } from '@/components/common/MotionButton'
import { PageHeader } from '@/components/common/PageHeader'
import { ScreenError, ScreenLoading } from '@/components/common/ScreenState'
import { StrokeMiniThumb } from '@/components/kanji/StrokeMiniThumb'
import { StrokeOrderCanvas } from '@/components/kanji/StrokeOrderCanvas'
import { useAsync } from '@/hooks/useAsync'
import { api, type Grade } from '@/lib/api'
import { easeGentle, springSoft, staggerContainer, staggerItem } from '@/lib/motion'

/**
 * Три оценки вместо одной кнопки «Урок пройден»: без них SRS выродился бы в
 * фиксированную лестницу интервалов, одинаковую для лёгких и трудных знаков.
 */
const GRADES: { grade: Grade; label: string; variant: string; flex: string }[] = [
  { grade: 'again', label: 'Не помню', variant: 'pill-secondary', flex: 'flex-1' },
  { grade: 'good', label: 'Помню', variant: 'pill', flex: 'flex-1' },
  { grade: 'easy', label: 'Легко', variant: 'pill-accent2', flex: 'flex-1' },
]

export function StrokeOrderPage() {
  const { kanjiId } = useParams()
  const navigate = useNavigate()
  const location = useLocation()
  const id = Number(kanjiId)
  const position = (location.state as { position?: number } | null)?.position

  const [replayKey, setReplayKey] = useState(0)
  const [submitting, setSubmitting] = useState(false)
  const [submitError, setSubmitError] = useState<string | null>(null)

  const { data: kanji, error, loading, reload } = useAsync(() => api.getKanji(id), [id])

  if (loading) return <ScreenLoading />
  if (error || !kanji) {
    return <ScreenError message={error ?? 'Знак не найден'} onRetry={reload} />
  }

  const strokes = kanji.strokes

  async function handleGrade(grade: Grade) {
    setSubmitting(true)
    setSubmitError(null)
    try {
      await api.submitReview(id, grade)
      navigate('/')
    } catch (err) {
      setSubmitError(err instanceof Error ? err.message : 'Не удалось сохранить ответ')
      setSubmitting(false)
    }
  }

  return (
    <div className="flex min-h-dvh flex-col items-center gap-5 px-6 pt-16.5 pb-10">
      <PageHeader
        label={position ? `Урок ${position} · шаг 3 из 3` : 'Шаг 3 из 3'}
        onBack={() => navigate(`/day/${id}/breakdown`, { state: { position } })}
        className="flex w-full items-center gap-3"
      />

      <h1 className="w-full font-heading text-[28px] font-semibold text-text">
        Как писать <span className="font-kanji font-normal">{kanji.character}</span>
      </h1>

      <motion.div
        initial={{ opacity: 0, scale: 0.97 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={springSoft}
        className="relative aspect-square w-full overflow-hidden rounded-(--radius-card) bg-neutral-100 shadow-md"
      >
        <StrokeOrderCanvas key={replayKey} strokes={strokes} />
      </motion.div>

      {strokes.length > 0 && strokes.length <= 6 && (
        <motion.div
          variants={staggerContainer}
          initial="hidden"
          animate="visible"
          className="flex w-full gap-3"
        >
          {strokes.map((stroke, i) => (
            <motion.div key={i} variants={staggerItem} className="flex min-w-0 flex-1">
              <StrokeMiniThumb
                strokes={strokes}
                thisIndex={i}
                // Подписи к отдельным чертам есть не у всех знаков — тогда
                // показываем только номер, а не «1 — null».
                instruction={
                  stroke.instruction ? `${i + 1} — ${stroke.instruction}` : `${i + 1}`
                }
                variant={i === 0 ? 'accent' : 'neutral'}
              />
            </motion.div>
          ))}
        </motion.div>
      )}

      {kanji.writing_note && (
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ ...easeGentle, delay: 0.35 }}
          className="w-full max-w-[320px] text-sm leading-relaxed text-neutral-700"
        >
          {kanji.writing_note}
        </motion.p>
      )}

      <div className="mt-auto flex w-full flex-col gap-3">
        {submitError && (
          <p className="text-center text-[13px] text-neutral-700">{submitError}</p>
        )}

        <MotionButton
          variant="pill-secondary"
          className="h-auto w-full py-3 text-sm"
          onClick={() => setReplayKey((k) => k + 1)}
        >
          Показать ещё раз
        </MotionButton>

        <div className="flex w-full gap-2">
          {GRADES.map(({ grade, label, variant, flex }) => (
            <MotionButton
              key={grade}
              variant={variant as never}
              disabled={submitting}
              className={`h-auto ${flex} px-1 py-3.5 text-[15px]`}
              onClick={() => handleGrade(grade)}
            >
              {label}
            </MotionButton>
          ))}
        </div>
      </div>
    </div>
  )
}
