"use client"

import { useState, useEffect } from "react"
import { serverRequest } from "./baseRequest"
import { PortfolioProvider } from "./context/portfolioContext"
import PortfolioForm from "./PortfolioForm"
import PortfolioTable from "./PortfolioTable"

export default function Page() {
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    serverRequest.get("/healthcheck").then(async res => {
      if (res.status !== 200)
        throw new Error("healthcheck failed.")
    }).catch(err => {
      console.error(err)
      setError(`${err.message}. Is the server running?`)
    })
  }, [])

  return (
    <main>
      {error && <h1 className="text-red-500">{error}</h1>}
      <PortfolioProvider>
        <PortfolioForm />
        <PortfolioTable />
      </PortfolioProvider>
    </main>
  );
}
