import { cn } from '@/lib/utils'
import type { ReadingInfo } from '@/lib/types'

interface ReadingRowProps {
  label: string
  reading: ReadingInfo
  gloss: string
  variant: 'accent' | 'accent2'
}

export function ReadingRow({ label, reading, gloss, variant }: ReadingRowProps) {
  const textColor = variant === 'accent' ? 'text-accent-700' : 'text-accent-2-700'
  const bg = variant === 'accent' ? 'bg-accent-200' : 'bg-accent-2-200'

  return (
    <div className={cn('flex items-center gap-3 rounded-[20px] px-[18px] py-3.5', bg)}>
      <span className={cn('w-[52px] shrink-0 text-[11.5px] tracking-[0.08em] uppercase', textColor)}>
        {label}
      </span>
      <span className="shrink-0 font-kana text-[22px] whitespace-nowrap text-text">{reading.kana}</span>
      <span className={cn('ml-auto text-right text-sm', textColor)}>
        {reading.romaji} · «{gloss}»
      </span>
    </div>
  )
}
