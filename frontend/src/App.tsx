
import Form from './components/Form'

import './App.css';
import TeamStatsOverview from './components/TeamStatsOverview';

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
  { name: 'Vitória MU', value: 35 },
  { name: 'Empate', value: 30 },
  { name: 'Vitória Adversário', value: 35 },
];

function App() {

  const victoryData = [
  { name: 'Vitória MU', value: 55 },
  { name: 'Empate', value: 25 },
  { name: 'Vitória Adversário', value: 20 },
  ];

  return (
    <>
    <div className="app-container">
      <h1>Manchester United Match Prediction</h1>
      <Form />
      <TeamStatsOverview teamA={teamA} teamB={teamB} victoryData={victoryData} />
    </div>
    </>
  )
}

export default App
