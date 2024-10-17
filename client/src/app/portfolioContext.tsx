import { createContext, useContext, useReducer, Dispatch } from "react"
import { z } from "zod"

export const portfolioSchema = z.object({
  status: z.string(),
  weights: z.record(z.string(), z.number())
}).strict()
export type Portfolio = z.infer<typeof portfolioSchema>
export type PortfolioAction = { type: "SET", payload: Portfolio }

export const PortfolioContext = createContext<{
  portfolio: Portfolio | null,
  portfolioDispatch: Dispatch<PortfolioAction>
}>(null!)
export const usePortfolio = () => useContext(PortfolioContext)

export function PortfolioProvider({ children }: React.PropsWithChildren) {
  function portfolioReducer(state: Portfolio, action: PortfolioAction) {
    switch (action.type) {
      case "SET":
        return action.payload
      default:
        return state
    }
  }

  const [portfolio, portfolioDispatch] = useReducer<typeof portfolioReducer>(portfolioReducer, null!)

  return (
    <PortfolioContext.Provider value={{ portfolio, portfolioDispatch }}>
      {children}
    </PortfolioContext.Provider>
  )
}
