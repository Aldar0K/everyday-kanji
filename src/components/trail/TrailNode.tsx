import { cn } from '@/lib/utils'

type Align = 'start' | 'center'

interface CompletedNodeProps {
  variant: 'completed'
  align: Align
  character: string
  label: string
  opacity: number
  onClick: () => void
}

interface TodayNodeProps {
  variant: 'today'
  align: Align
  character: string
  label: string
  sublabel: string
  onClick: () => void
}

type TrailNodeProps = CompletedNodeProps | TodayNodeProps

export function TrailNode(props: TrailNodeProps) {
  if (props.variant === 'today') {
    const { align, character, label, sublabel, onClick } = props
    return (
      <button
        type="button"
        onClick={onClick}
        className={cn(
          'group my-1 flex flex-col items-center gap-3',
          align === 'center' ? 'self-center' : 'self-start',
        )}
      >
        <div className="relative flex items-center justify-center">
          <div className="absolute size-[150px] rounded-full bg-accent-200 opacity-65" />
          <div className="relative flex size-[118px] items-center justify-center rounded-full bg-accent font-kanji text-[62px] text-neutral-100 shadow-lg transition-colors group-hover:bg-accent-600 group-active:bg-accent-700">
            {character}
          </div>
        </div>
        <div className="flex flex-col items-center gap-0.5">
          <span className="font-heading text-lg font-semibold text-text">{label}</span>
          <span className="text-[12.5px] text-accent-700">{sublabel}</span>
        </div>
      </button>
    )
  }

  const { align, character, label, opacity, onClick } = props
  return (
    <button
      type="button"
      onClick={onClick}
      style={{ opacity }}
      className={cn('flex items-center gap-4', align === 'center' ? 'self-center' : 'self-start')}
    >
      <span className="flex size-11 items-center justify-center rounded-full bg-accent-2-300 font-kanji text-[21px] text-accent-2-800">
        {character}
      </span>
      <span className="text-[13px] text-neutral-700">{label}</span>
    </button>
  )
}

interface FutureNodesProps {
  count: number
}

const FUTURE_OPACITIES = [0.65, 0.45, 0.25]

export function FutureNodes({ count }: FutureNodesProps) {
  return (
    <div className="flex gap-3.5 self-center">
      {Array.from({ length: count }, (_, i) => (
        <div
          key={i}
          className="size-9 rounded-full border-2 border-dashed border-neutral-400"
          style={{ opacity: FUTURE_OPACITIES[i] ?? 0.25 }}
        />
      ))}
    </div>
  )
}
