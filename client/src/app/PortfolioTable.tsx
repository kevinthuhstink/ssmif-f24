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
      <Table>
        <TableCaption>Ticker to weight</TableCaption>
        <TableHeader>
          <TableRow>
            <TableHead className="w-[100px]">Ticker</TableHead>
            <TableHead className="text-right">Weight</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          { Object.entries(portfolio.weights).map(([k, v], i) => (
            <TableRow key={i}>
              <TableCell className="font-medium">{k}</TableCell>
              <TableCell className="text-right">{v}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      }
    </div>
  )
}
