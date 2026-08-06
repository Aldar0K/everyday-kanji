/**
 * Клиент API.
 *
 * Запросы идут на относительный /api, а не на адрес бэкенда напрямую: в
 * разработке их проксирует Vite, в продакшене — nginx. Благодаря этому
 * запрос всегда однодоменный, и кука device_id ходит сама собой, без CORS и
 * без credentials-плясок.
 */

export interface ExampleWord {
  word: string
  kana: string | null
  romaji: string | null
  translation: string | null
}

export interface StrokePoint {
  x: number
  y: number
}

export interface Stroke {
  d: string
  start: StrokePoint | null
  instruction: string | null
}

/** Чтение — кана плюс ромадзи. Используется в подписях и тегах. */
export interface ReadingInfo {
  kana: string
  romaji: string
}

export interface Kanji {
  id: number
  character: string
  order_index: number
  meaning: string | null
  kun_reading_kana: string | null
  kun_reading_romaji: string | null
  on_reading_kana: string | null
  on_reading_romaji: string | null
  jlpt_level: string | null
  stroke_count: number | null
  writing_note: string | null
  example_words: ExampleWord[]
  strokes: Stroke[]
}

export interface TrailNode {
  kanji: Kanji
  position: number
}

export interface Trail {
  studied_count: number
  recent: TrailNode[]
  today: TrailNode | null
  today_completed: boolean
  due_count: number
  published_total: number
  timezone: string
}

export type Grade = 'again' | 'good' | 'easy'

export interface ReviewResult {
  kanji_id: number
  repetitions: number
  interval_days: number
  ease_factor: number
  next_review_at: string
  last_reviewed_at: string | null
  lapses: number
  total_reviews: number
}

export class ApiError extends Error {
  // Поле объявлено отдельно, а не параметром конструктора: в проекте включён
  // erasableSyntaxOnly, который запрещает сокращённую форму.
  status: number

  constructor(status: number, message: string) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

/** Таймзона устройства — от неё зависит граница суток для дневных счётчиков. */
function deviceTimezone(): string {
  try {
    return Intl.DateTimeFormat().resolvedOptions().timeZone || 'UTC'
  } catch {
    return 'UTC'
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`/api${path}`, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      'X-Timezone': deviceTimezone(),
      ...init?.headers,
    },
    // Кука device_id — единственный идентификатор пользователя, без неё
    // сервер на каждый запрос заводил бы новое устройство.
    credentials: 'same-origin',
  })

  if (!response.ok) {
    const message =
      response.status === 429
        ? 'Слишком много запросов. Подождите минуту.'
        : `Запрос не удался (${response.status})`
    throw new ApiError(response.status, message)
  }

  return (await response.json()) as T
}

export const api = {
  getTrail: () => request<Trail>('/trail'),
  getKanji: (id: number) => request<Kanji>(`/kanji/${id}`),
  submitReview: (kanjiId: number, grade: Grade) =>
    request<ReviewResult>(`/reviews/${kanjiId}`, {
      method: 'POST',
      body: JSON.stringify({ grade }),
    }),
}
