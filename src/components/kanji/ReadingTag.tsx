import { Tag } from '@/components/common/Tag'
import type { ReadingInfo } from '@/lib/types'

interface ReadingTagProps {
  reading: ReadingInfo
  variant: 'accent' | 'accent2'
}

export function ReadingTag({ reading, variant }: ReadingTagProps) {
  return (
    <Tag variant={variant} className="gap-1.5">
      <b className="font-kana font-medium">{reading.kana}</b> {reading.romaji}
    </Tag>
  )
}
