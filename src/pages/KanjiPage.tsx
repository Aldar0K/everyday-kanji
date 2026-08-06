import { motion } from 'motion/react'
import { useLocation, useNavigate, useParams } from 'react-router-dom'
import { BackButton } from '@/components/common/BackButton'
import { MotionButton } from '@/components/common/MotionButton'
import { ScreenError, ScreenLoading } from '@/components/common/ScreenState'
import { LessonStepRow } from '@/components/kanji/LessonStepRow'
import { ReadingTag } from '@/components/kanji/ReadingTag'
import { useAsync } from '@/hooks/useAsync'
import { api } from '@/lib/api'
import { springSoft, staggerContainer, staggerItem } from '@/lib/motion'
import { pluralizeCherta } from '@/lib/russian'

export function KanjiPage() {
  const { kanjiId } = useParams()
  const navigate = useNavigate()
  const location = useLocation()
  const id = Number(kanjiId)

  // Порядковый номер приходит с тропы. При заходе по прямой ссылке его нет —
  // тогда подпись просто короче, вместо лишнего запроса ради одной цифры.
  const position = (location.state as { position?: number } | null)?.position

  const { data: kanji, error, loading, reload } = useAsync(() => api.getKanji(id), [id])

  if (loading) return <ScreenLoading />
  if (error || !kanji) {
    return <ScreenError message={error ?? 'Знак не найден'} onRetry={reload} />
  }

  const strokeCount = kanji.stroke_count ?? kanji.strokes.length
  const steps = [
    { title: 'Что значит знак', duration: '1 мин' },
    { title: 'Чтения и слова', duration: '2 мин' },
    {
      title: `${strokeCount} ${pluralizeCherta(strokeCount)}, по порядку`,
      duration: '1 мин',
    },
  ]

  return (
    <div className="flex min-h-dvh flex-col gap-5 px-6 pt-16.5 pb-10">
      <div className="flex items-center gap-3">
        <BackButton onClick={() => navigate('/')} />
        <span className="text-[13.5px] text-neutral-600">
          {position ? `Тропа · день ${position}` : 'Тропа'}
        </span>
      </div>

      <motion.div
        initial={{ opacity: 0, scale: 0.96, y: 8 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        transition={springSoft}
        className="flex flex-col items-center gap-4 rounded-(--radius-card) bg-neutral-100 px-6.5 pt-8 pb-6.5 shadow-md"
      >
        <div className="font-kanji text-[142px] leading-none text-text">
          {kanji.character}
        </div>
        <div className="font-heading text-[26px] font-semibold text-text">
          {kanji.meaning}
        </div>
        <div className="flex flex-wrap justify-center gap-2">
          {kanji.kun_reading_kana && (
            <ReadingTag
              reading={{
                kana: kanji.kun_reading_kana,
                romaji: kanji.kun_reading_romaji ?? '',
              }}
              variant="accent"
            />
          )}
          {kanji.on_reading_kana && (
            <ReadingTag
              reading={{
                kana: kanji.on_reading_kana,
                romaji: kanji.on_reading_romaji ?? '',
              }}
              variant="accent2"
            />
          )}
        </div>
      </motion.div>

      <motion.div
        variants={staggerContainer}
        initial="hidden"
        animate="visible"
        className="flex flex-col"
      >
        {steps.map((step, i) => (
          <motion.div key={step.title} variants={staggerItem}>
            <LessonStepRow
              index={i + 1}
              title={step.title}
              duration={step.duration}
              isLast={i === steps.length - 1}
            />
          </motion.div>
        ))}
      </motion.div>

      <div className="mt-auto flex flex-col gap-3">
        <MotionButton
          variant="pill"
          size="block"
          onClick={() => navigate(`/day/${id}/breakdown`, { state: { position } })}
        >
          Пройти урок · 4 минуты
        </MotionButton>
      </div>
    </div>
  )
}
