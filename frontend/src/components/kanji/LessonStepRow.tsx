import { cn } from '@/lib/utils'

interface LessonStepRowProps {
  index: number
  title: string
  duration: string
  isLast?: boolean
}

export function LessonStepRow({ index, title, duration, isLast }: LessonStepRowProps) {
  return (
    <div
      className={cn(
        'flex items-center gap-3.5 px-0.5 py-3',
        !isLast && 'border-b border-divider',
      )}
    >
      <span className="flex size-[26px] shrink-0 items-center justify-center rounded-full bg-surface text-xs text-neutral-700">
        {index}
      </span>
      <span className="text-[15px] text-text">{title}</span>
      <span className="ml-auto text-[13px] text-neutral-600">{duration}</span>
    </div>
  )
}
