import { useStrokeAnimation } from '@/hooks/useStrokeAnimation'
import type { Stroke } from '@/lib/types'

interface StrokeOrderCanvasProps {
  strokes: Stroke[]
}

export function StrokeOrderCanvas({ strokes }: StrokeOrderCanvasProps) {
  const { activeIndex, pathRefs } = useStrokeAnimation(strokes.length)
  const active = strokes[activeIndex]

  return (
    <svg viewBox="0 0 100 100" className="absolute inset-0 size-full">
      <line
        x1="50"
        y1="6"
        x2="50"
        y2="94"
        stroke="var(--color-neutral-200)"
        strokeWidth="1"
        strokeDasharray="4 4"
      />
      <line
        x1="6"
        y1="50"
        x2="94"
        y2="50"
        stroke="var(--color-neutral-200)"
        strokeWidth="1"
        strokeDasharray="4 4"
      />
      <g fill="none" strokeLinecap="round" strokeLinejoin="round" strokeWidth="7">
        {strokes.map((stroke, i) => (
          <path
            key={i}
            ref={(el) => {
              pathRefs.current[i] = el
            }}
            d={stroke.d}
            stroke={
              i < activeIndex
                ? 'var(--color-neutral-800)'
                : i === activeIndex
                  ? 'var(--color-accent)'
                  : 'var(--color-neutral-300)'
            }
          />
        ))}
      </g>
      {active && activeIndex < strokes.length && (
        <g>
          <circle cx={active.start.x} cy={active.start.y} r="7" fill="var(--color-accent-700)" />
          <text
            x={active.start.x}
            y={active.start.y + 3.4}
            textAnchor="middle"
            fontSize="8.5"
            fontFamily="var(--font-heading)"
            fontWeight="600"
            fill="var(--color-neutral-100)"
          >
            {activeIndex + 1}
          </text>
        </g>
      )}
    </svg>
  )
}
