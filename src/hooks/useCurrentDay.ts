import { useEffect, useState } from 'react'
import { getCurrentDayNumber } from '@/lib/dayUnlock'

/**
 * Re-derives the current day number periodically and on tab focus, so a
 * 6am rollover reflects promptly in a tab left open overnight.
 */
export function useCurrentDay(): number {
  const [day, setDay] = useState(() => getCurrentDayNumber())

  useEffect(() => {
    const recompute = () => setDay(getCurrentDayNumber())
    const interval = setInterval(recompute, 60_000)
    window.addEventListener('focus', recompute)
    document.addEventListener('visibilitychange', recompute)
    return () => {
      clearInterval(interval)
      window.removeEventListener('focus', recompute)
      document.removeEventListener('visibilitychange', recompute)
    }
  }, [])

  return day
}
