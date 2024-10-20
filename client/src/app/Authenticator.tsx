import { AxiosError } from "axios"
import { Button } from "@/components/ui/button"
import { serverRequest, errorSchema, unknownError } from "./baseRequest"
import { useAuth, jwtSchema } from "./context/authContext"

export default function Authenticator() {
  const { auth, setAuth } = useAuth()
  const arrowUnicode = "\u27A1"

  async function onClick() {
    const res = await serverRequest.get("/jwt")
    .catch((err: AxiosError) => {
      console.error(err)
      try {
        const errorData = errorSchema.parse(err.response?.data)
        setAuth(errorData)
      } catch {
        setAuth(unknownError)
      }
    })

    if (!res)
      return

    try {
      const data = jwtSchema.parse(res.data)
      setAuth(data)
    } catch (err) {
      console.error(err)
      setAuth({ error: "JWT response type is invalid. Did the model fail?" })
    }
  }

  return (
    <div className="mb-24">
      <h1 className="text-4xl">
        { auth.jwt ? "THANK YOU FOR AUTHENTICATING :)" : "YOU NEED TO BE AUTHENTICATED TO USE THIS APP" }
      </h1>
      { auth.error && <p className="text-red-500">{auth.error}</p> }
      <p>
        Authenticate here <span className="text-4xl mx-2">{arrowUnicode}</span>
        <Button
          className="bg-white border-4 border-black hover:bg-neutral-200 text-black"
          onClick={onClick}
        >
          get jwt
        </Button>
      </p>
    </div>
  )
}
