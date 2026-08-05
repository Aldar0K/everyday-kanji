/**
 * How deep a route sits in the lesson flow:
 * `/` → 0, `/day/12` → 1, `/day/12/breakdown` → 2, `/day/12/strokes` → 3.
 *
 * Comparing depths across a navigation tells us whether the user moved
 * forward or back, which is what decides the page-transition direction.
 */
export function routeDepth(pathname: string): number {
  const segments = pathname.split('/').filter(Boolean)
  // `/day/:n` is two segments but one level down, so the day number doesn't
  // count toward depth.
  return Math.max(0, segments.length - 1)
}
