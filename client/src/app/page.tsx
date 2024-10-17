"use client"

import { useState, useEffect } from "react"
import { serverRequest } from "./baseRequest"
import { PortfolioProvider } from "./portfolioContext"
import PortfolioForm from "./PortfolioForm"
import PortfolioTable from "./PortfolioTable"

export default function Page() {
  const [error, setError] = useState<Error>(null!)

  useEffect(() => {
    serverRequest.get("/healthcheck").then(async res => {
      if (res.status !== 200)
        throw new Error("healthcheck failed. is the server running?")
    }).catch(err => {
      console.error(err)
      setError(err)
    })
  }, [])

  if (error)
    return <>{error.message}</>

  return (
    <main>
      <PortfolioProvider>
        <PortfolioForm />
        <PortfolioTable />
      </PortfolioProvider>
    </main>
  );
}
