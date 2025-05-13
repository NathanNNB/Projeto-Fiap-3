import { API } from "./api";

const API_URL = API;

export const fetchFormationList = async () => {
    const response = await API_URL.get('/formations');
    return response.data;
  };