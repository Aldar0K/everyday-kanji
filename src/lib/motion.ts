import type { Transition, Variants } from 'motion/react'

/**
 * Shared motion tokens. The app's tone is deliberately calm, so springs are
 * damped enough not to overshoot visibly — the movement should read as
 * "settling", never as "bouncing".
 */

/** Default for layout/position changes: soft, no visible overshoot. */
export const springSoft: Transition = {
  type: 'spring',
  stiffness: 260,
  damping: 30,
}

/** Slightly quicker — for press feedback, where latency is felt. */
export const springSnappy: Transition = {
  type: 'spring',
  stiffness: 400,
  damping: 28,
}

/** Fades and other non-spatial changes. */
export const easeGentle: Transition = {
  duration: 0.28,
  ease: [0.22, 0.61, 0.36, 1],
}

/**
 * Press feedback shared by every tappable surface. Scale is subtle on
 * purpose: large targets (the 118px "today" circle) would look rubbery at
 * the more common 0.9.
 */
export const pressable = {
  whileTap: { scale: 0.96 },
  transition: springSnappy,
}

/** Container that reveals its children one after another. */
export const staggerContainer: Variants = {
  hidden: {},
  visible: {
    transition: { staggerChildren: 0.06, delayChildren: 0.04 },
  },
}

/** The child half of `staggerContainer` — drifts up as it fades in. */
export const staggerItem: Variants = {
  hidden: { opacity: 0, y: 12 },
  visible: { opacity: 1, y: 0, transition: springSoft },
}
