import { cn } from '@/lib/utils'

interface BackButtonProps {
  onClick?: () => void
  className?: string
}

export function BackButton({ onClick, className }: BackButtonProps) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-label="Назад"
      className={cn(
        'flex size-[38px] shrink-0 items-center justify-center rounded-full bg-surface transition-colors hover:bg-neutral-300',
        className,
      )}
    >
      <svg width="9" height="15" viewBox="0 0 9 15" fill="none" aria-hidden="true">
        <path
          d="M7.5 1.5L2 7.5l5.5 6"
          stroke="var(--color-neutral-700)"
          strokeWidth="2.75"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    </button>
  )
}
