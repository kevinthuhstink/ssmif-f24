"use client"

import { useState, useReducer, useEffect } from "react"
import serverRequest from "./baseRequest"
import PortfolioForm from "./PortfolioForm"

type Action = { type: "SET", payload: string }

export default function Page() {
  const [error, setError] = useState<Error>(null!)

  function displayReducer(state: string, action: Action) {
    switch (action.type) {
      case "SET":
        return action.payload
      default:
        return state
    }
  }

  const [display, displayDispatch] = useReducer<typeof displayReducer>(displayReducer, null!)

  useEffect(() => {
    serverRequest.get("/healthcheck").then(async res => {
      if (res.status !== 200)
        throw new Error("healthcheck failed. is the server running?")
      displayDispatch({ type: "SET", payload: JSON.stringify(res.data) })
    }).catch(err => {
      console.error(err)
      setError(err)
    })
  }, [])

  if (error)
    return <>{error.message}</>

  return (
    <main>
      <h1>{display}</h1>
      <PortfolioForm displayDispatch={displayDispatch} />
    </main>
  );
}
