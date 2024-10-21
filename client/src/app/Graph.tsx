import { usePortfolio } from "./context/portfolioContext"

export default function Graph() {
  const { portfolio } = usePortfolio()

  if (!portfolio)
    return <></>

  return (
    <div>
      { Object.entries(portfolio.performance).map(([timestamp, value], i) => {
        return <p key={i}>{`${timestamp}: ${value}`}</p>
      })}
    </div>
  )
}
