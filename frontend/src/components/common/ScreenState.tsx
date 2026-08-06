import { Button } from '@/components/ui/button'

/** Общие состояния экрана: загрузка и ошибка. Тон — спокойный, без драмы. */

export function ScreenLoading() {
  return (
    <div className="flex min-h-dvh items-center justify-center px-6">
      <span className="text-sm text-neutral-600">Загружаем…</span>
    </div>
  )
}

interface ScreenErrorProps {
  message: string
  onRetry?: () => void
}

export function ScreenError({ message, onRetry }: ScreenErrorProps) {
  return (
    <div className="flex min-h-dvh flex-col items-center justify-center gap-4 px-6 text-center">
      <p className="text-sm text-neutral-700">{message}</p>
      {onRetry && (
        <Button variant="pill-secondary" className="h-auto px-6 py-3" onClick={onRetry}>
          Попробовать снова
        </Button>
      )}
    </div>
  )
}
