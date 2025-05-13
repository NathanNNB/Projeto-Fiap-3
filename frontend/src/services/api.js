import axios from 'axios';

// const baseURL = import.meta.env.VITE_API_BASE_URL
const baseURL = ""
export const API = axios.create({
  baseURL,
});

