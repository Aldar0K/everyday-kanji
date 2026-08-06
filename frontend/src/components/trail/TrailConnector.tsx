import { motion, type Variants } from 'motion/react'
import { cn } from '@/lib/utils'

/** Grows downward, so the trail reads as being drawn from the top. */
const connectorVariants: Variants = {
  hidden: { scaleY: 0, opacity: 0 },
  visible: {
    scaleY: 1,
    opacity: 1,
    transition: { duration: 0.24, ease: 'easeOut' },
  },
}

interface TrailConnectorProps {
  align: 'start' | 'center'
  color: 'accent2' | 'neutral'
  height?: number
}

export function TrailConnector({ align, color, height = 20 }: TrailConnectorProps) {
  return (
    <motion.div
      variants={connectorVariants}
      className={cn(
        'w-0.5 origin-top',
        color === 'accent2' ? 'bg-accent-2-300' : 'bg-neutral-300',
        align === 'center' ? 'self-center' : 'ml-[21px] self-start',
      )}
      style={{ height }}
    />
  )
}
