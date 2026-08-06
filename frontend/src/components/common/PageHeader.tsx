import { cn } from '@/lib/utils'
import { BackButton } from './BackButton'

interface PageHeaderProps {
  label: string
  onBack: () => void
  className?: string
}

export function PageHeader({ label, onBack, className }: PageHeaderProps) {
  return (
    <div className={cn('flex items-center gap-3', className)}>
      <BackButton onClick={onBack} />
      <span className="text-[13.5px] text-neutral-600">{label}</span>
    </div>
  )
}
