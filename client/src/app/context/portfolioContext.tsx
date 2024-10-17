import { createContext, useContext, useReducer, Dispatch } from "react"
import { z } from "zod"

export const portfolioErrorSchema = z.object({
  error: z.string()
})

export const portfolioSchema = z.object({
  status: z.string(),
  error: portfolioErrorSchema.shape.error.optional(),
  return: z.number(),
  volatility: z.number(),
  sharpe: z.number(),
  weights: z.record(z.string(), z.number())
})

export type Portfolio = z.infer<typeof portfolioSchema>
export type PortfolioError = z.infer<typeof portfolioErrorSchema>
export type PortfolioAction =
  { type: "SET", payload: Portfolio } |
  { type: "ERROR", payload: PortfolioError }

export const PortfolioContext = createContext<{
  portfolio: Portfolio | null,
  portfolioDispatch: Dispatch<PortfolioAction>
}>(null!)
export const usePortfolio = () => useContext(PortfolioContext)

export const unknownErrorAction: PortfolioAction = {
  type: "ERROR",
  payload: { error: "Unknown error occurred. Is the server running?" }
}

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
