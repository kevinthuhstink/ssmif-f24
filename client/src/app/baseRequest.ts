import axios from "axios"

const serverRequest = axios.create({
    baseURL: process.env.NEXT_PUBLIC_SERVER_URL
})

export default serverRequest
