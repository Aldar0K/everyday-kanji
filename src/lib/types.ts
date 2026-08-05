export interface ReadingInfo {
  kana: string
  romaji: string
}

export interface ExampleWord {
  word: string
  kana: string
  romaji: string
  translation: string
}

export interface Stroke {
  /** SVG path data in a shared 0-100 viewBox. */
  d: string
  /** Starting point of the stroke, in the same 0-100 viewBox. */
  start: { x: number; y: number }
  /** Short instruction shown under the stroke's mini thumbnail. */
  instruction: string
}

export interface Kanji {
  day: number
  character: string
  meaning: string
  kunReading: ReadingInfo
  onReading: ReadingInfo
  jlptLevel: string
  strokeCount: number
  exampleWords: ExampleWord[]
  strokes: Stroke[]
  /** Short prose description of the writing order, shown under the stroke canvas. */
  writingNote: string
}
