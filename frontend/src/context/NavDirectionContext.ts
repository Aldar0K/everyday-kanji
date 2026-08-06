import { createContext } from 'react'

/**
 * +1 when navigating deeper into the lesson, -1 when coming back. Lives in
 * context because the page being animated sits several levels below the
 * router that knows which way we moved.
 */
export const NavDirectionContext = createContext(1)
