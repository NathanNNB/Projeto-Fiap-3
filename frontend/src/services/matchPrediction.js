import { API } from "./api";

const API_URL = API;

export const fetchMatchPrediction = async (params) => {
    const response = await API_URL.get('/formations', {
      params: params ,
    });
    return response.data;
  };