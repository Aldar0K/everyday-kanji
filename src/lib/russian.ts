const CARDINALS = [
  '',
  'один',
  'два',
  'три',
  'четыре',
  'пять',
  'шесть',
  'семь',
  'восемь',
  'девять',
  'десять',
  'одиннадцать',
  'двенадцать',
  'тринадцать',
  'четырнадцать',
  'пятнадцать',
  'шестнадцать',
  'семнадцать',
  'восемнадцать',
  'девятнадцать',
  'двадцать',
]

const ORDINALS = [
  '',
  'первый',
  'второй',
  'третий',
  'четвёртый',
  'пятый',
  'шестой',
  'седьмой',
  'восьмой',
  'девятый',
  'десятый',
  'одиннадцатый',
  'двенадцатый',
  'тринадцатый',
  'четырнадцатый',
  'пятнадцатый',
  'шестнадцатый',
  'семнадцатый',
  'восемнадцатый',
  'девятнадцатый',
  'двадцатый',
]

function cardinal(n: number): string {
  return CARDINALS[n] ?? String(n)
}

function ordinal(n: number): string {
  return ORDINALS[n] ?? `${n}-й`
}

function capitalize(s: string): string {
  return s.charAt(0).toUpperCase() + s.slice(1)
}

/** знак / знака / знаков, by standard Russian count-noun agreement. */
function pluralizeZnak(n: number): string {
  const mod10 = n % 10
  const mod100 = n % 100
  if (mod100 >= 11 && mod100 <= 14) return 'знаков'
  if (mod10 === 1) return 'знак'
  if (mod10 >= 2 && mod10 <= 4) return 'знака'
  return 'знаков'
}

export function trailSubtitle(currentDay: number): string {
  const behind = currentDay - 1
  if (behind <= 0) return 'Это твой первый знак.'
  return `${capitalize(cardinal(behind))} ${pluralizeZnak(behind)} позади. Сегодня ${ordinal(currentDay)}.`
}

export function greeting(date: Date = new Date()): string {
  const hour = date.getHours()
  if (hour < 12) return 'Доброе утро'
  if (hour < 18) return 'Добрый день'
  return 'Добрый вечер'
}

/** черта / черты / черт */
export function pluralizeCherta(n: number): string {
  const mod10 = n % 10
  const mod100 = n % 100
  if (mod100 >= 11 && mod100 <= 14) return 'черт'
  if (mod10 === 1) return 'черта'
  if (mod10 >= 2 && mod10 <= 4) return 'черты'
  return 'черт'
}

export function dateLabel(date: Date = new Date()): string {
  return new Intl.DateTimeFormat('ru-RU', { day: 'numeric', month: 'long' }).format(date).toUpperCase()
}
