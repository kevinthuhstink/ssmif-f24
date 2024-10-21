import { AxiosError } from "axios"
import { z } from "zod"
import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { serverRequest, errorSchema, unknownError } from "./baseRequest"
import { portfolioSchema, usePortfolio } from "./context/portfolioContext"
import { useAuth } from "./context/authContext"

import { Button } from "@/components/ui/button"
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"


const formSchema = z.object({
  value: z.number({ message: "Portfolio value must be a number" })
    .positive({ message: "Portfolio value must be a positive number" }),
  tickers: z.string()
})

type FormInput = z.infer<typeof formSchema>

export default function PortfolioForm() {
  const { portfolioDispatch } = usePortfolio()
  const { auth, setAuth } = useAuth()
  const form = useForm<FormInput>({
    resolver: zodResolver(formSchema)
  })

  async function onSubmit(input: FormInput) {
    const tickerArray = input.tickers.split(/\s*,\s*/)
    const res = await serverRequest.put("/model", {
      value: input.value,
      tickers: tickerArray,
    }, {
      headers: { Authorization: auth.jwt }
    }).catch((err: AxiosError) => {
      console.error(err)
      try {
        const errorData = errorSchema.parse(err.response?.data)
        if (err.status == 444)
          setAuth(errorData)
        else
          portfolioDispatch({ type: "ERROR", payload: errorData })
      } catch {
        portfolioDispatch({ type: "ERROR", payload: unknownError })
      }
    })

    if (!res) // end function early if catch block is invoked
      return

    try {
      const data = portfolioSchema.parse(res.data)
      portfolioDispatch({ type: "SET", payload: data })
    } catch (err) {
      console.error(err)
      portfolioDispatch({
        type: "ERROR",
        payload: { error: "Portfolio optimization response type is invalid. Did the model fail?" }
      })
    }
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8 mb-24">
        <FormField
          control={form.control}
          name="value"
          render={() => (
            <FormItem>
              <FormLabel>Portfolio Value (USD)</FormLabel>
              <FormControl>
                <Input
                  type="number"
                  {...form.register("value", { valueAsNumber: true })}
                />
              </FormControl>
              <FormDescription>
                The desired portfolio value.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="tickers"
          render={() => (
            <FormItem>
              <FormLabel>Tickers</FormLabel>
              <FormControl>
                <Input {...form.register("tickers")} />
              </FormControl>
              <FormDescription>
                Comma separated list of tickers to optimize portfolio on.<br/>
                Please do not add any trailing commas or extra spaces between tickers.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button
          type="submit"
          disabled={!auth.jwt}
        >Submit</Button>
      </form>
    </Form>
  )
}
