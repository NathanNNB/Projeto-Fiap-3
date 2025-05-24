/* eslint-disable @typescript-eslint/no-unused-vars */
// src/components/Formulario.tsx

import React, { useState, useEffect } from 'react';
import './form.css';
import { fetchOpponentsList } from '../services/oppponents';
import { fetchSquadsList } from '../services/squads';
import TeamStatsOverview from './TeamStatsOverView';
import fetchMatchPrediction from '../services/matchPrediction';

const Formulario = () => {
  const [selectedSquad, setSelectedSquad] = useState('');
  const [selectedOpponent, setSelectedOpponent] = useState<number | null>(null);
  const [selectedSide, setSelectedSide] = useState('');
  const [squadOptions, setSquadOptions] = useState<JSX.Element[]>([]);
  const [opponentOptions, setOpponentOptions] = useState<JSX.Element[]>([]);

  const teamA = {
    name: 'Manchester United',
    avg_goals: 1.8,
    opportunites: 12,
    goal_suffered: 1.1,
    draws: 5,
    victories: 18,
    ball_possession: 55,
    win_rate: 62,
  };

  const teamB = {
    name: 'Liverpool',
    avg_goals: 2.1,
    opportunites: 14,
    goal_suffered: 0.9,
    draws: 6,
    victories: 20,
    ball_possession: 60,
    win_rate: 67,
  };

  const victoryData = [
    { name: 'Vitória Manchester United', value: 55 },
    { name: 'Empate', value: 25 },
    { name: 'Vitória Adversário', value: 20 },
  ];

  useEffect(() => {
    const fetchOptions = async () => {
      try {
        const { squads } = await fetchSquadsList();
        if (squads?.length) {
          setSquadOptions(
            squads.map((squad: string) => (
              <option key={squad} value={squad}>
                {squad}
              </option>
            ))
          );
        }
      } catch {
        console.log('Erro ao consultar squads');
      }

      try {
        const { opponents } = await fetchOpponentsList();
        if (opponents?.length) {
          setOpponentOptions(
            opponents.map((opponent: any) => (
              <option key={opponent.team_id} value={opponent.team_id}>
                {opponent.team_name}
              </option>
            ))
          );
        }
      } catch {
        console.log('Erro ao consultar opponents');
      }
    };

    fetchOptions();
  }, []);

  const getReport = async (e: React.FormEvent) => {
    e.preventDefault();

    const predictionParams = {
      field: selectedSide,
      squad: selectedSquad,
      opponent_id: selectedOpponent,
    };

    try {
      const { scout_data } = await fetchMatchPrediction(predictionParams);

      // Aqui você pode setar o resultado em um state e exibir os dados no TeamStatsOverview
      console.log('Resultado:', scout_data);
    } catch {
      console.log('Erro ao consultar API');
    }
  };

  return (
    <>
      <form className="form" onSubmit={getReport}>
        <select
          defaultValue=""
          onChange={(e) => setSelectedSide(e.target.value)}
          required
        >
          <option value="" disabled>
            Selecione o Mando de Campo
          </option>
          <option value="visitor">Visitante</option>
          <option value="home">Mandante</option>
        </select>

        <select
          defaultValue=""
          onChange={(e) => setSelectedSquad(e.target.value)}
          required
        >
          <option value="" disabled>
            Selecione a Formação do seu time
          </option>
          {squadOptions}
        </select>

        <select
          defaultValue=""
          onChange={(e) => setSelectedOpponent(Number(e.target.value))}
          required
        >
          <option value={""} disabled>
            Selecione o oponente
          </option>
          {opponentOptions}
        </select>

        <button type="submit">Enviar</button>
      </form>

      <TeamStatsOverview teamA={teamA} teamB={teamB} victoryData={victoryData} />
    </>
  );
};

export default Formulario;
