import { describe, expect, it } from 'vitest'
import { APP_START_DATE } from './constants'
import { getCurrentDayNumber, getDayUnlockTime } from './dayUnlock'

describe('getCurrentDayNumber', () => {
  it('is 0 before the app has started', () => {
    expect(getCurrentDayNumber(new Date(2026, 6, 20, 12, 0, 0))).toBe(0)
  })

  it('is day 1 exactly at the start instant', () => {
    expect(getCurrentDayNumber(new Date(APP_START_DATE))).toBe(1)
  })

  it('stays on the previous day at 5:59, rolls to the next at 6:00', () => {
    // day 2 unlocks 2026-07-26 06:00
    expect(getCurrentDayNumber(new Date(2026, 6, 26, 5, 59, 59))).toBe(1)
    expect(getCurrentDayNumber(new Date(2026, 6, 26, 6, 0, 0))).toBe(2)
  })

  it('holds steady through the middle of the day', () => {
    expect(getCurrentDayNumber(new Date(2026, 6, 27, 14, 30, 0))).toBe(3)
    expect(getCurrentDayNumber(new Date(2026, 6, 27, 23, 59, 0))).toBe(3)
  })

  it('resolves today (2026-08-05) to day 12, matching the design mockups', () => {
    expect(getCurrentDayNumber(new Date(2026, 7, 5, 9, 0, 0))).toBe(12)
  })
})

describe('getDayUnlockTime', () => {
  it('round-trips with getCurrentDayNumber across a run of days', () => {
    for (let day = 1; day <= 20; day++) {
      const unlock = getDayUnlockTime(day)
      expect(getCurrentDayNumber(unlock)).toBe(day)
      expect(getCurrentDayNumber(new Date(unlock.getTime() - 1))).toBe(day - 1)
    }
  })
})
