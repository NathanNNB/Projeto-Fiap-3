import { API } from "./api";

const API_URL = API;

interface Prediction {
  field: string;
  squad: string;
  opponent_id: number | null;
}

const fetchMatchPrediction = async (predictionParams: Prediction) => {
  debugger
    const response = await API_URL.get('/report', {
      params: predictionParams ,
    });
    return response.data;
  };

export default fetchMatchPrediction;