import type { ReactNode } from 'react'
import { Badge } from '@/components/ui/badge'
import { cn } from '@/lib/utils'

interface TagProps {
  variant: 'accent' | 'accent2' | 'neutral'
  className?: string
  children: ReactNode
}

export function Tag({ variant, className, children }: TagProps) {
  return (
    <Badge
      variant={variant}
      className={cn('h-auto rounded-full px-3.5 py-1.5 text-[13.5px] font-normal', className)}
    >
      {children}
    </Badge>
  )
}
