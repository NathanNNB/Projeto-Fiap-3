import { API } from "./api";

const API_URL = API;

interface opponentsListList {
  opponents: string[];
}

export const fetchOpponentsList = async ():Promise<opponentsListList> => {
    const response = await API_URL.get('/opponents');
    return response.data;
  };