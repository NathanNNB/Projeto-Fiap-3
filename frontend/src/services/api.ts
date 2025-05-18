import axios from 'axios';

// TODO validar quando é prod ou nao
// const baseURL = import.meta.env.VITE_API_BASE_URL
const baseURL = "http://127.0.0.1:5000/"
export const API = axios.create({
  baseURL,
});

