import { usePortfolio } from "./context/portfolioContext"
import {
  Chart,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Legend
} from "chart.js"
import { Line } from "react-chartjs-2"

Chart.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Legend
)

export default function Graph() {
  const { portfolio } = usePortfolio()

  if (!portfolio)
    return <></>

  const times = Object.keys(portfolio.performance)
  const values = Object.values(portfolio.performance)

  const chartData = {
    labels: times.map(time => new Date(time).toDateString()),
    datasets: [{
      label: "Portfolio Value",
      data: values.map(v => v * portfolio.value)
    }]
  }

  const chartOptions = {
    plugins: {
      title: {
        display: true,
        text: "1yr Historical Portfolio Growth"
      }
    },
    scales: {
      y: {
        min: 0
      }
    }
  }

  return (
    <Line data={chartData} options={chartOptions} />
  )
}
