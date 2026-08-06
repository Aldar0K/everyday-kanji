import { useCallback, useEffect, useState } from 'react'

interface AsyncState<T> {
  data: T | null
  error: string | null
  loading: boolean
}

/**
 * Загрузка данных с перезапросом по требованию.
 *
 * Библиотеку вроде React Query не берём: экранов четыре, запросов три, и
 * отдельная зависимость ради этого не окупается.
 */
export function useAsync<T>(fn: () => Promise<T>, deps: unknown[] = []) {
  const [state, setState] = useState<AsyncState<T>>({
    data: null,
    error: null,
    loading: true,
  })

  const run = useCallback(() => {
    let cancelled = false
    setState((prev) => ({ ...prev, loading: true, error: null }))
    fn()
      .then((data) => {
        // Ответ пришёл после размонтирования — обновлять нечего.
        if (!cancelled) setState({ data, error: null, loading: false })
      })
      .catch((err: unknown) => {
        if (cancelled) return
        const message = err instanceof Error ? err.message : 'Что-то пошло не так'
        setState({ data: null, error: message, loading: false })
      })
    return () => {
      cancelled = true
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps)

  useEffect(run, [run])

  return { ...state, reload: run }
}
