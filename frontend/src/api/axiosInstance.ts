import axios from "axios";


export const axiosInstance = axios.create({
  baseURL: 'https://moretech.flint3s.ru/api'
})