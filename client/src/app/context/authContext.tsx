import { createContext, useContext, useState } from "react"
import { z } from "zod"

export const jwtSchema = z.string()
export const AuthContext = createContext<{
  auth: string,
  setAuth: React.Dispatch<React.SetStateAction<string>>
}>(null!)
export const useAuth = () => useContext(AuthContext)

export function AuthProvider({ children }: React.PropsWithChildren) {
  const [auth, setAuth] = useState<string>("")

  return (
    <AuthContext.Provider value={{ auth, setAuth }}>
      {children}
    </AuthContext.Provider>
  )
}
