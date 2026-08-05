/** New day unlocks at this local hour. */
export const UNLOCK_HOUR = 0

/**
 * Day 1 unlocks at this instant. Chosen so day 12 (山, the kanji the design
 * mockups' copy is written around — "Тропа · день 12", "Одиннадцать знаков
 * позади") lands on today when this file was authored.
 */
export const APP_START_DATE = new Date(2026, 6, 25, UNLOCK_HOUR, 0, 0)

export const PROGRESS_STORAGE_KEY = 'kanji-app:completed-days'

/** Used only as the first-run fallback, before any localStorage state exists. */
export const DEFAULT_COMPLETED_DAYS = Array.from({ length: 11 }, (_, i) => i + 1)
