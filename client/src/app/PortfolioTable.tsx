import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { usePortfolio } from "./portfolioContext"

export default function PortfolioTable() {
  const { portfolio } = usePortfolio()

  if (!portfolio)
    return <></>

  return (
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
  )
}
