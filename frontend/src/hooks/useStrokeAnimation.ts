import { useLayoutEffect, useRef, useState } from 'react'

/**
 * Draws strokes in order via stroke-dasharray/stroke-dashoffset transitions:
 * ~500ms ease-out per stroke, then a ~200ms pause before the next one starts.
 *
 * To replay from the start, remount this hook's owner with a fresh `key`
 * (see StrokeOrderPage) rather than trying to reverse an in-flight
 * transition — that avoids a visible "undraw" flash and any state-timing
 * races between a manual reset and the in-progress animation.
 */
export function useStrokeAnimation(strokeCount: number) {
  const [activeIndex, setActiveIndex] = useState(0)
  const pathRefs = useRef<(SVGPathElement | null)[]>([])
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | undefined>(undefined)

  // Runs once per mount: hide every stroke with no transition before the
  // sequencing effect below starts drawing stroke 0.
  useLayoutEffect(() => {
    pathRefs.current.forEach((path) => {
      if (!path) return
      const length = path.getTotalLength()
      path.style.transition = 'none'
      path.style.strokeDasharray = `${length}`
      path.style.strokeDashoffset = `${length}`
    })
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  useLayoutEffect(() => {
    if (activeIndex >= strokeCount) return
    const path = pathRefs.current[activeIndex]
    if (!path) return

    const raf = requestAnimationFrame(() => {
      path.style.transition = 'stroke-dashoffset 500ms ease-out'
      path.style.strokeDashoffset = '0'
    })

    const handleTransitionEnd = (e: TransitionEvent) => {
      if (e.propertyName !== 'stroke-dashoffset') return
      timeoutRef.current = setTimeout(() => setActiveIndex((i) => i + 1), 200)
    }
    path.addEventListener('transitionend', handleTransitionEnd)

    return () => {
      cancelAnimationFrame(raf)
      path.removeEventListener('transitionend', handleTransitionEnd)
      clearTimeout(timeoutRef.current)
    }
  }, [activeIndex, strokeCount])

  return { activeIndex, pathRefs, isDone: activeIndex >= strokeCount }
}
