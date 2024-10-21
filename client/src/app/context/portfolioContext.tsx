import { createContext, useContext, useReducer, Dispatch } from "react"
import { errorSchema, RequestError } from "../baseRequest"
import { z } from "zod"

export const portfolioSchema = z.object({
  status: z.string(),
  tickers: z.string().array(),
  value: z.number(),
  error: errorSchema.shape.error.optional(),
  return: z.number(),
  volatility: z.number(),
  sharpe: z.number(),
  weights: z.record(z.string(), z.number()),
  shares: z.record(z.string(), z.number()),
  performance: z.record(z.string().datetime(), z.number())
})

export type Portfolio = z.infer<typeof portfolioSchema>
export type PortfolioAction =
  { type: "SET", payload: Portfolio } |
  { type: "ERROR", payload: RequestError }

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
      case "ERROR":
        return {
          ...state,
          status: "ERROR",
          error: action.payload.error
        }
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
