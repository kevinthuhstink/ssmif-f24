import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { usePortfolio } from "./context/portfolioContext"

export default function PortfolioTable() {
  const { portfolio } = usePortfolio()

  if (!portfolio)
    return <></>

  return (
    <div>
      {portfolio.status === "ERROR" && <h1 className="text-red-500">{portfolio.error}</h1>}
      {portfolio.weights &&
        <>
          <h1 className="">
            Expected Annualized Return: {portfolio.return}<br/>
            Annualized Volatility: {portfolio.volatility}<br/>
            Sharpe Ratio: {portfolio.sharpe}<br/>
          </h1>
          <Table>
            <TableCaption>Optimized for Max Sharpe ratio</TableCaption>
            <TableHeader>
              <TableRow>
                <TableHead className="w-[100px]">Ticker</TableHead>
                <TableHead className="text-right">Weight</TableHead>
                <TableHead className="text-right"># of Stocks</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              { Object.keys(portfolio.weights).map((k, i) => (
                <TableRow key={i}>
                  <TableCell className="font-medium">{k}</TableCell>
                  <TableCell className="text-right">{portfolio.weights[k]}</TableCell>
                  <TableCell className="text-right">{portfolio.shares[k]}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </>
      }
    </div>
  )
}
