import { createContext, useCallback, useContext, useMemo, useState, type ReactNode } from 'react'
import { loadCompletedDays, saveCompletedDays } from '@/lib/progress'

interface ProgressContextValue {
  completedDays: Set<number>
  isDayComplete: (day: number) => boolean
  markDayComplete: (day: number) => void
}

const ProgressContext = createContext<ProgressContextValue | null>(null)

export function ProgressProvider({ children }: { children: ReactNode }) {
  const [completedDays, setCompletedDays] = useState<Set<number>>(() => loadCompletedDays())

  const markDayComplete = useCallback((day: number) => {
    setCompletedDays((prev) => {
      if (prev.has(day)) return prev
      const next = new Set(prev)
      next.add(day)
      saveCompletedDays(next)
      return next
    })
  }, [])

  const isDayComplete = useCallback((day: number) => completedDays.has(day), [completedDays])

  const value = useMemo(
    () => ({ completedDays, isDayComplete, markDayComplete }),
    [completedDays, isDayComplete, markDayComplete],
  )

  return <ProgressContext.Provider value={value}>{children}</ProgressContext.Provider>
}

export function useProgress(): ProgressContextValue {
  const ctx = useContext(ProgressContext)
  if (!ctx) throw new Error('useProgress must be used within a ProgressProvider')
  return ctx
}
