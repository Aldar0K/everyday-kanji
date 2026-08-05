import { DEFAULT_COMPLETED_DAYS, PROGRESS_STORAGE_KEY } from './constants'

export function loadCompletedDays(): Set<number> {
  const raw = window.localStorage.getItem(PROGRESS_STORAGE_KEY)
  if (raw === null) return new Set(DEFAULT_COMPLETED_DAYS)

  try {
    const parsed: unknown = JSON.parse(raw)
    if (Array.isArray(parsed) && parsed.every((n) => typeof n === 'number')) {
      return new Set(parsed)
    }
  } catch {
    // fall through to default
  }
  return new Set(DEFAULT_COMPLETED_DAYS)
}

export function saveCompletedDays(days: Set<number>): void {
  window.localStorage.setItem(PROGRESS_STORAGE_KEY, JSON.stringify([...days]))
}
