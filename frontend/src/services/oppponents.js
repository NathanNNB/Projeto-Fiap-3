import { API } from "./api";

const API_URL = API;

export const fetchOpponentsList = async () => {
    const response = await API_URL.get('/opponents');
    return response.data;
  };