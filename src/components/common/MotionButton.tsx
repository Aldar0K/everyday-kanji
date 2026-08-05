import { motion } from 'motion/react'
import { Button } from '@/components/ui/button'
import { pressable } from '@/lib/motion'

const Motion = motion.create(Button)

type MotionButtonProps = React.ComponentProps<typeof Motion>

/**
 * The shadcn Button with the app's shared press feedback already applied.
 * Use this for anything the user taps, so the response is identical
 * everywhere; pass `whileTap` explicitly to override.
 */
export function MotionButton(props: MotionButtonProps) {
  return <Motion whileTap={pressable.whileTap} transition={pressable.transition} {...props} />
}
