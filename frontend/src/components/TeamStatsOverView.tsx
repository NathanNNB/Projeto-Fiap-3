import './TeamStatsOverview.css';
import { PieChart, Pie, Cell, Tooltip, Legend } from 'recharts';

interface TeamStats {
  name: string;
  avg_goals: number;
  opportunites: number;
  goal_suffered: number;
  draws: number;
  victories: number;
  ball_possession: number;
  win_rate: number;
}

interface VictoryDataItem {
  name: string;
  value: number;
}

interface TeamStatsOverviewProps {
  teamA: TeamStats;
  teamB: TeamStats;
  victoryData: VictoryDataItem[];
}

const COLORS = ['#DA291C', '#FDB913', '#1B1B1B']; // Vitória MU, Empate, Derrota

const TeamStatsOverview = ({ teamA, teamB, victoryData }: TeamStatsOverviewProps) => {
  const stats = [
    { label: 'Gols Médios', key: 'avg_goals' },
    { label: 'Oportunidades Criadas', key: 'opportunites' },
    { label: 'Gols Sofridos', key: 'goal_suffered' },
    { label: 'Empates', key: 'draws' },
    { label: 'Vitórias', key: 'victories' },
    { label: 'Posse de Bola (%)', key: 'ball_possession' },
    { label: 'Taxa de Vitórias (%)', key: 'win_rate' },
  ];

  return (
    <div className="stats-overview-container">
      <div className="stats-table-container">
        <h2>Comparativo de Estatísticas</h2>
        <table className="stats-table">
          <thead>
            <tr>
              <th>Estatística</th>
              <th>{teamA.name}</th>
              <th>{teamB.name}</th>
            </tr>
          </thead>
          <tbody>
            {stats.map((stat) => (
              <tr key={stat.key}>
                <td>{stat.label}</td>
                <td>{teamA[stat.key as keyof TeamStats]}</td>
                <td>{teamB[stat.key as keyof TeamStats]}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="victory-chart-container">
        <h2>Probabilidades de Resultado</h2>
        <div className="victory-chart-wrapper">
        <PieChart width={300} height={300}>
          <Pie
            data={victoryData}
            cx="50%"
            cy="50%"
            label
            outerRadius={100}
            dataKey="value"
          >
            {victoryData.map((_, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
        </div>
      </div>
    </div>
  );
};

export default TeamStatsOverview;
