import { APP_START_DATE, UNLOCK_HOUR } from './constants'

const MS_PER_DAY = 24 * 60 * 60 * 1000

function startOfDay(date: Date): Date {
  const d = new Date(date)
  d.setHours(0, 0, 0, 0)
  return d
}

function atHour(date: Date, hour: number): Date {
  const d = new Date(date)
  d.setHours(hour, 0, 0, 0)
  return d
}

/**
 * Which "app day" `now` falls on, where a new day starts at UNLOCK_HOUR
 * local time (not midnight) and day 1 is APP_START_DATE. Returns 0 if
 * `now` is before APP_START_DATE has unlocked.
 */
export function getCurrentDayNumber(now: Date = new Date()): number {
  const todayUnlock = atHour(now, UNLOCK_HOUR)
  const effectiveDay =
    now.getTime() >= todayUnlock.getTime()
      ? startOfDay(now)
      : startOfDay(new Date(now.getTime() - MS_PER_DAY))

  const startDay = startOfDay(APP_START_DATE)
  // Math.round (not floor) so a 23- or 25-hour DST-transition day still
  // counts as exactly one day.
  const diffDays = Math.round((effectiveDay.getTime() - startDay.getTime()) / MS_PER_DAY)
  return Math.max(0, diffDays + 1)
}

/** The instant `dayNumber` unlocks (local time). */
export function getDayUnlockTime(dayNumber: number): Date {
  const startDay = startOfDay(APP_START_DATE)
  const target = new Date(startDay.getTime() + (dayNumber - 1) * MS_PER_DAY)
  return atHour(target, UNLOCK_HOUR)
}
