import { cn } from '@/lib/utils'

interface TrailConnectorProps {
  align: 'start' | 'center'
  color: 'accent2' | 'neutral'
  height?: number
}

export function TrailConnector({ align, color, height = 20 }: TrailConnectorProps) {
  return (
    <div
      className={cn(
        'w-0.5',
        color === 'accent2' ? 'bg-accent-2-300' : 'bg-neutral-300',
        align === 'center' ? 'self-center' : 'ml-[21px] self-start',
      )}
      style={{ height }}
    />
  )
}
