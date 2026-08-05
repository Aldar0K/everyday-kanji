import { useContext, type ReactNode } from 'react'
import { motion, type Variants } from 'motion/react'
import { NavDirectionContext } from '@/context/NavDirectionContext'
import { easeGentle, springSoft } from '@/lib/motion'

const pageVariants: Variants = {
  enter: (direction: number) => ({
    opacity: 0,
    x: direction >= 0 ? 20 : -20,
  }),
  center: {
    opacity: 1,
    x: 0,
    transition: { ...springSoft, opacity: easeGentle },
  },
  exit: (direction: number) => ({
    opacity: 0,
    x: direction >= 0 ? -20 : 20,
    // Leaving is faster than arriving — with AnimatePresence mode="wait" the
    // exit is pure latency before the next screen starts.
    transition: { duration: 0.16, ease: 'easeIn' },
  }),
}

export function PageTransition({ children }: { children: ReactNode }) {
  const direction = useContext(NavDirectionContext)

  return (
    <motion.div
      custom={direction}
      variants={pageVariants}
      initial="enter"
      animate="center"
      exit="exit"
    >
      {children}
    </motion.div>
  )
}
