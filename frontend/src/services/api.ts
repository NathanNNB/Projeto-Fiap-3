import axios from 'axios';

// const baseURL = import.meta.env.VITE_API_BASE_URL
const baseURL = "http://127.0.0.1:5000/"
export const API = axios.create({
  baseURL,
});

