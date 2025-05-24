import { API } from "./api";

const API_URL = API;

interface opponent {
  team_name: string,
  team_id: number
}
interface opponentsListList {
  opponents: opponent[];
}

export const fetchOpponentsList = async ():Promise<opponentsListList> => {
    const response = await API_URL.get('/opponents');
    return response.data;
  };