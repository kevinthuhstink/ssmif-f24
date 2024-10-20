import { createContext, useContext, useState } from "react"
import { errorSchema } from "../baseRequest"
import { z } from "zod"

export const jwtSchema = z.object({
  jwt: z.string().optional(),
  error: errorSchema.shape.error.optional(),
})
export type JWT = z.infer<typeof jwtSchema>
export const AuthContext = createContext<{
  auth: JWT,
  setAuth: React.Dispatch<React.SetStateAction<JWT>>
}>(null!)

export const useAuth = () => useContext(AuthContext)


export function AuthProvider({ children }: React.PropsWithChildren) {
  const [auth, setAuth] = useState<JWT>({})

  return (
    <AuthContext.Provider value={{ auth, setAuth }}>
      {children}
    </AuthContext.Provider>
  )
}
