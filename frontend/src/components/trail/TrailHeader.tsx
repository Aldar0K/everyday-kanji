import { motion } from 'motion/react'
import { easeGentle, springSoft } from '@/lib/motion'

interface TrailHeaderProps {
  dateLabel: string
  greeting: string
  subtitle: string
}

export function TrailHeader({ dateLabel, greeting, subtitle }: TrailHeaderProps) {
  return (
    <motion.div
      initial={{ y: -16, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={springSoft}
      className="relative overflow-hidden rounded-b-[34px] bg-accent-2-200 px-6 pt-[70px] pb-[22px]"
    >
      <motion.div
        initial={{ scale: 0.6, opacity: 0 }}
        animate={{ scale: 1, opacity: 0.55 }}
        transition={{ ...easeGentle, delay: 0.12, duration: 0.5 }}
        className="absolute -top-14 -right-10 size-[170px] rounded-full bg-accent-2-300"
      />
      <div className="relative">
        <span className="text-[12.5px] tracking-[0.09em] text-accent-2-700 uppercase">
          {dateLabel}
        </span>
        <h1 className="mt-1 mb-1 font-heading text-[28px] font-semibold text-accent-2-900">
          {greeting}
        </h1>
        <p className="m-0 text-sm text-accent-2-700">{subtitle}</p>
      </div>
    </motion.div>
  )
}
