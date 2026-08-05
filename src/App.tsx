import { useEffect, useRef } from 'react'
import { BrowserRouter, Route, Routes, useLocation } from 'react-router-dom'
import { AnimatePresence, MotionConfig } from 'motion/react'
import { PageTransition } from '@/components/common/PageTransition'
import { NavDirectionContext } from '@/context/NavDirectionContext'
import { ProgressProvider } from '@/context/ProgressContext'
import { routeDepth } from '@/lib/routeDepth'
import { BreakdownPage } from '@/pages/BreakdownPage'
import { KanjiPage } from '@/pages/KanjiPage'
import { PathPage } from '@/pages/PathPage'
import { StrokeOrderPage } from '@/pages/StrokeOrderPage'

function AnimatedRoutes() {
  const location = useLocation()
  const depth = routeDepth(location.pathname)
  const previousDepth = useRef(depth)
  const direction = depth >= previousDepth.current ? 1 : -1

  useEffect(() => {
    previousDepth.current = depth
  }, [depth])

  return (
    <NavDirectionContext.Provider value={direction}>
      {/* `mode="wait"` keeps the two screens from overlapping, so neither
          needs to be pulled out of normal flow to animate.
          No `initial={false}`: it would suppress the first render's entrance
          for the whole subtree, including the trail's stagger. */}
      <AnimatePresence mode="wait" custom={direction}>
        <Routes location={location} key={location.pathname}>
          <Route
            path="/"
            element={
              <PageTransition>
                <PathPage />
              </PageTransition>
            }
          />
          <Route
            path="/day/:dayNumber"
            element={
              <PageTransition>
                <KanjiPage />
              </PageTransition>
            }
          />
          <Route
            path="/day/:dayNumber/breakdown"
            element={
              <PageTransition>
                <BreakdownPage />
              </PageTransition>
            }
          />
          <Route
            path="/day/:dayNumber/strokes"
            element={
              <PageTransition>
                <StrokeOrderPage />
              </PageTransition>
            }
          />
        </Routes>
      </AnimatePresence>
    </NavDirectionContext.Provider>
  )
}

function App() {
  return (
    // `reducedMotion="user"` drops transform/layout animation for anyone with
    // the OS setting on, keeping only opacity — nothing here conveys meaning
    // through movement alone.
    <MotionConfig reducedMotion="user">
      <ProgressProvider>
        <BrowserRouter>
          <div className="mx-auto min-h-dvh max-w-md overflow-x-hidden bg-bg">
            <AnimatedRoutes />
          </div>
        </BrowserRouter>
      </ProgressProvider>
    </MotionConfig>
  )
}

export default App
