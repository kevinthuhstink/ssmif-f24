"use client"

import { useState, useEffect } from "react"

export default function Page() {
  const [text, setText] = useState<string>(null!)

  useEffect(() => {
    const serverUrl = process.env.NEXT_PUBLIC_SERVER_URL
    fetch(`${serverUrl}/healthcheck`).then(async res => {
      setText(await res.text())
    }).catch(err => {
      console.error(err)
      setText(err.message)
    })
  }, [])

  if (!text)
    return <>Loading...</>

  return (
    <div>{text}</div>
  );
}
