import { cn } from '@/lib/utils'
import type { ExampleWord } from '@/lib/types'

interface ExampleWordRowProps {
  word: ExampleWord
  isLast?: boolean
}

export function ExampleWordRow({ word, isLast }: ExampleWordRowProps) {
  return (
    <div
      className={cn(
        'flex items-baseline gap-3 px-1 py-3',
        !isLast && 'border-b border-divider',
      )}
    >
      <span className="font-kanji text-2xl text-text">{word.word}</span>
      <span className="font-kana text-[13px] text-neutral-600">
        {word.kana} · {word.romaji}
      </span>
      <span className="ml-auto text-[15px] text-text">{word.translation}</span>
    </div>
  )
}
