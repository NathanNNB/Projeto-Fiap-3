import axios from 'axios';

const baseURL = import.meta.env.VITE_FLASK_API_URL

export const API = axios.create({
  baseURL,
});

