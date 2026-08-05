import { BrowserRouter, Route, Routes } from 'react-router-dom'
import { ProgressProvider } from '@/context/ProgressContext'
import { BreakdownPage } from '@/pages/BreakdownPage'
import { KanjiPage } from '@/pages/KanjiPage'
import { PathPage } from '@/pages/PathPage'
import { StrokeOrderPage } from '@/pages/StrokeOrderPage'

function App() {
  return (
    <ProgressProvider>
      <BrowserRouter>
        <div className="mx-auto min-h-dvh max-w-md bg-bg">
          <Routes>
            <Route path="/" element={<PathPage />} />
            <Route path="/day/:dayNumber" element={<KanjiPage />} />
            <Route path="/day/:dayNumber/breakdown" element={<BreakdownPage />} />
            <Route path="/day/:dayNumber/strokes" element={<StrokeOrderPage />} />
          </Routes>
        </div>
      </BrowserRouter>
    </ProgressProvider>
  )
}

export default App
