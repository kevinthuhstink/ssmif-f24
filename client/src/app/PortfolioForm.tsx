import { AxiosError } from "axios"
import { z } from "zod"
import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { serverRequest } from "./baseRequest"
import {
  portfolioSchema,
  portfolioErrorSchema,
  usePortfolio,
  PortfolioError,
} from "./context/portfolioContext"

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
  const form = useForm<FormInput>({
    resolver: zodResolver(formSchema)
  })

  async function onSubmit(input: FormInput) {
    const tickerArray = input.tickers.split(", ")
    const res = await serverRequest.put("/weights", {
      value: input.value,
      tickers: tickerArray,
    }).catch((err: AxiosError) => {
      if (err.response) {
        portfolioErrorSchema.parse(err.response.data)
        portfolioDispatch({ type: "ERROR", payload: err.response.data as PortfolioError })
      } else console.log("idfk man")
    })

    if (!res)
      return

    portfolioSchema.parse(res.data)
    portfolioDispatch({ type: "SET", payload: res.data })
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
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
                The tickers to optimize portfolio on.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">Submit</Button>
      </form>
    </Form>
  )
}
