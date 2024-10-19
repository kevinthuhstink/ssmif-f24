import { Button } from "@/components/ui/button"

export default function Authenticator() {
  return (
    <div className="mb-24">
      <h1 className="text-4xl">YOU NEED TO BE AUTHENTICATED TO USE THIS APP</h1>
      <p>
        Authenticate here <span className="text-4xl mx-2">{"\u27A1"}</span>
        <Button className="bg-white border-4 border-black hover:bg-neutral-400 text-black">
          Free jwts (they persist between browser sessions)
        </Button>
      </p>
    </div>
  )
}
