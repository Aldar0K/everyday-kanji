import { motion, type Variants } from 'motion/react'
import { cn } from '@/lib/utils'
import { pressable, springSoft, staggerContainer } from '@/lib/motion'

type Align = 'start' | 'center'

/**
 * Resting opacity is passed through `custom` rather than baked into the
 * variant: past days fade with distance (0.7 / 0.8 / 1), and animating
 * straight to 1 would flatten that gradient on entrance.
 */
const nodeVariants: Variants = {
  hidden: { opacity: 0, y: 14 },
  visible: (restOpacity: number) => ({
    opacity: restOpacity,
    y: 0,
    transition: springSoft,
  }),
}

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
      <motion.button
        type="button"
        onClick={onClick}
        variants={nodeVariants}
        custom={1}
        whileTap={pressable.whileTap}
        transition={pressable.transition}
        className={cn(
          'group my-1 flex flex-col items-center gap-3',
          align === 'center' ? 'self-center' : 'self-start',
        )}
      >
        <div className="relative flex items-center justify-center">
          {/* Slow breath on the halo — the only ambient movement in the app,
              here to mark which circle is today's without a badge or count. */}
          <motion.div
            className="absolute size-[150px] rounded-full bg-accent-200"
            animate={{ scale: [1, 1.07, 1], opacity: [0.65, 0.5, 0.65] }}
            transition={{ duration: 3.6, ease: 'easeInOut', repeat: Infinity }}
          />
          <div className="relative flex size-[118px] items-center justify-center rounded-full bg-accent font-kanji text-[62px] text-neutral-100 shadow-lg transition-colors group-hover:bg-accent-600">
            {character}
          </div>
        </div>
        <div className="flex flex-col items-center gap-0.5">
          <span className="font-heading text-lg font-semibold text-text">{label}</span>
          <span className="text-[12.5px] text-accent-700">{sublabel}</span>
        </div>
      </motion.button>
    )
  }

  const { align, character, label, opacity, onClick } = props
  return (
    <motion.button
      type="button"
      onClick={onClick}
      variants={nodeVariants}
      custom={opacity}
      whileTap={pressable.whileTap}
      transition={pressable.transition}
      className={cn('flex items-center gap-4', align === 'center' ? 'self-center' : 'self-start')}
    >
      <span className="flex size-11 items-center justify-center rounded-full bg-accent-2-300 font-kanji text-[21px] text-accent-2-800">
        {character}
      </span>
      <span className="text-[13px] text-neutral-700">{label}</span>
    </motion.button>
  )
}

interface FutureNodesProps {
  count: number
}

const FUTURE_OPACITIES = [0.65, 0.45, 0.25]

export function FutureNodes({ count }: FutureNodesProps) {
  // A motion element, not a plain div: variants only propagate to children
  // through motion components, and these dots inherit the trail's stagger.
  return (
    <motion.div variants={staggerContainer} className="flex gap-3.5 self-center">
      {Array.from({ length: count }, (_, i) => (
        <motion.div
          key={i}
          variants={nodeVariants}
          custom={FUTURE_OPACITIES[i] ?? 0.25}
          className="size-9 rounded-full border-2 border-dashed border-neutral-400"
        />
      ))}
    </motion.div>
  )
}
