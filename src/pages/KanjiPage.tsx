import { motion } from 'motion/react'
import { Navigate, useNavigate, useParams } from 'react-router-dom'
import { BackButton } from '@/components/common/BackButton'
import { MotionButton } from '@/components/common/MotionButton'
import { LessonStepRow } from '@/components/kanji/LessonStepRow'
import { ReadingTag } from '@/components/kanji/ReadingTag'
import { useCurrentDay } from '@/hooks/useCurrentDay'
import { getKanjiByDay } from '@/lib/kanjiData'
import { springSoft, staggerContainer, staggerItem } from '@/lib/motion'

const LESSON_STEPS = [
  { title: 'Что значит знак', duration: '1 мин' },
  { title: 'Чтения и слова', duration: '2 мин' },
  { title: 'Три черты, по порядку', duration: '1 мин' },
]

export function KanjiPage() {
  const { dayNumber } = useParams()
  const navigate = useNavigate()
  const currentDay = useCurrentDay()
  const day = Number(dayNumber)
  const kanji = getKanjiByDay(day)
  const yesterday = getKanjiByDay(day - 1)

  if (!kanji || !Number.isInteger(day) || day > currentDay) {
    return <Navigate to="/" replace />
  }

  return (
    <div className="flex min-h-dvh flex-col gap-5 px-6 pt-[66px] pb-10">
      <div className="flex items-center gap-3">
        <BackButton onClick={() => navigate('/')} />
        <span className="text-[13.5px] text-neutral-600">Тропа · день {day}</span>
      </div>

      <motion.div
        initial={{ opacity: 0, scale: 0.96, y: 8 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        transition={springSoft}
        className="flex flex-col items-center gap-4 rounded-(--radius-card) bg-neutral-100 px-[26px] pt-8 pb-[26px] shadow-md"
      >
        <div className="font-kanji text-[142px] leading-none text-text">{kanji.character}</div>
        <div className="font-heading text-[26px] font-semibold text-text">{kanji.meaning}</div>
        <div className="flex flex-wrap justify-center gap-2">
          <ReadingTag reading={kanji.kunReading} variant="accent" />
          <ReadingTag reading={kanji.onReading} variant="accent2" />
        </div>
      </motion.div>

      <motion.div
        variants={staggerContainer}
        initial="hidden"
        animate="visible"
        className="flex flex-col"
      >
        {LESSON_STEPS.map((step, i) => (
          <motion.div key={step.title} variants={staggerItem}>
            <LessonStepRow
              index={i + 1}
              title={step.title}
              duration={step.duration}
              isLast={i === LESSON_STEPS.length - 1}
            />
          </motion.div>
        ))}
      </motion.div>

      <div className="mt-auto flex flex-col gap-3">
        <MotionButton
          variant="pill"
          size="block"
          onClick={() => navigate(`/day/${day}/breakdown`)}
        >
          Пройти урок · 4 минуты
        </MotionButton>
        {yesterday && (
          <div className="flex items-center justify-center gap-2 text-[13.5px] text-neutral-600">
            Вчера
            <span className="font-kanji text-[17px] text-text">{yesterday.character}</span>
            {yesterday.meaning}
          </div>
        )}
      </div>
    </div>
  )
}
