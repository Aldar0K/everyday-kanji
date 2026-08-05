import { MotionButton } from '@/components/common/MotionButton'
import { PageHeader } from '@/components/common/PageHeader'
import { Tag } from '@/components/common/Tag'
import { ExampleWordRow } from '@/components/kanji/ExampleWordRow'
import { ReadingRow } from '@/components/kanji/ReadingRow'
import { useCurrentDay } from '@/hooks/useCurrentDay'
import { getKanjiByDay } from '@/lib/kanjiData'
import { springSoft, staggerContainer, staggerItem } from '@/lib/motion'
import { pluralizeCherta } from '@/lib/russian'
import { motion } from 'motion/react'
import { Navigate, useNavigate, useParams } from 'react-router-dom'

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
    <div className="flex min-h-dvh flex-col gap-5 px-5.5 pt-16.5 pb-10">
      <PageHeader label={`Урок ${day} · шаг 1 из 3`} onBack={() => navigate(`/day/${day}`)} />

      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={springSoft}
        className="flex items-center gap-5 rounded-2xl bg-neutral-100 px-5.5 py-5 shadow-sm"
      >
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
      </motion.div>

      <motion.div variants={staggerContainer} initial="hidden" animate="visible">
        <motion.h2
          variants={staggerItem}
          className="mb-2.5 font-heading text-[19px] font-semibold text-text"
        >
          Чтения
        </motion.h2>
        <div className="flex flex-col gap-2.5">
          <motion.div variants={staggerItem}>
            <ReadingRow label="кун" reading={kanji.kunReading} gloss="японское" variant="accent" />
          </motion.div>
          <motion.div variants={staggerItem}>
            <ReadingRow label="он" reading={kanji.onReading} gloss="китайское" variant="accent2" />
          </motion.div>
        </div>
      </motion.div>

      <motion.div variants={staggerContainer} initial="hidden" animate="visible">
        <motion.h2
          variants={staggerItem}
          className="mb-2.5 font-heading text-[19px] font-semibold text-text"
        >
          Слова со знаком
        </motion.h2>
        <div className="flex flex-col">
          {kanji.exampleWords.map((word, i) => (
            <motion.div key={word.word} variants={staggerItem}>
              <ExampleWordRow word={word} isLast={i === kanji.exampleWords.length - 1} />
            </motion.div>
          ))}
        </div>
      </motion.div>

      <div className="mt-auto">
        <MotionButton
          variant="pill"
          size="block"
          onClick={() => navigate(`/day/${day}/strokes`)}
        >
          Дальше · как писать
        </MotionButton>
      </div>
    </div>
  )
}
