import { API } from "./api";

const API_URL = API;

export const fetchOpponentsList = async ():Promise<Array<string>> => {
    const response = await API_URL.get('/opponents');
    return response.data;
  };