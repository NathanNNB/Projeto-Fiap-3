import { API } from "./api";


const API_URL = API;
interface squadsList {
  squads: string[]
}
export const fetchSquadsList = async ():Promise<squadsList> => {
    const squads = await API_URL.get('/squads');
    return squads.data;
  };