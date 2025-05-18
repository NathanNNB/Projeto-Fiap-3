import { API } from "./api";


const API_URL = API;

export const fetchSquadsList = async ():Promise<Array<string>> => {
    const squads = await API_URL.get('/squads');
    return squads.data;
  };