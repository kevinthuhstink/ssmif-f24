import axios from "axios"
import { z } from "zod"

export const serverRequest = axios.create({
    baseURL: process.env.NEXT_PUBLIC_SERVER_URL
})

export const errorSchema = z.object({
  error: z.string()
})
export type RequestError = z.infer<typeof errorSchema>

export const unknownError = { error: "Unknown error occurred. Is the server running?" }
