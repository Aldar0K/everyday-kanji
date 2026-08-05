import { cn } from '@/lib/utils'
import type { Stroke } from '@/lib/types'

interface StrokeMiniThumbProps {
  strokes: Stroke[]
  thisIndex: number
  instruction: string
  /** Only the first thumbnail in a list gets the accent treatment, per the
   *  design mockup — a static "start here" emphasis, not animation state. */
  variant: 'accent' | 'neutral'
}

export function StrokeMiniThumb({ strokes, thisIndex, instruction, variant }: StrokeMiniThumbProps) {
  const bg = variant === 'accent' ? 'bg-accent-200' : 'bg-surface'
  const labelColor = variant === 'accent' ? 'text-accent-700' : 'text-neutral-700'
  const highlightColor = variant === 'accent' ? 'var(--color-accent-700)' : 'var(--color-text)'
  const dimColor = variant === 'accent' ? 'var(--color-accent-300)' : 'var(--color-neutral-300)'
  const writtenColor = variant === 'accent' ? 'var(--color-accent-300)' : 'var(--color-neutral-700)'

  return (
    <div className={cn('flex min-w-0 flex-1 flex-col items-center gap-1.5 rounded-[20px] p-2.5', bg)}>
      <svg viewBox="0 0 100 100" className="w-full min-w-0">
        <g fill="none" strokeLinecap="round" strokeLinejoin="round" strokeWidth="8">
          {strokes.map((stroke, i) => (
            <path
              key={i}
              d={stroke.d}
              stroke={
                i === thisIndex ? highlightColor : i < thisIndex ? writtenColor : dimColor
              }
            />
          ))}
        </g>
      </svg>
      <span className={cn('w-full text-center text-[11.5px] break-words', labelColor)}>{instruction}</span>
    </div>
  )
}
