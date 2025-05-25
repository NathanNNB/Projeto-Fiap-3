import './TeamStatsOverview.css';
import { PieChart, Pie, Cell, Tooltip, Legend } from 'recharts';

interface TeamStats {
  team_id: number;
  avg_total_goals_team: number;
  avg_shots_on_goal_team: number;
  avg_possession_team: number;
  avg_expected_goals_team: number;
  avg_passes_accurate_team: number;
  avg_total_passes_team: number;
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

const COLORS = ['#DA291C', '#5F5F5F', '#FFFFFF']; // Vitória MU, Empate, Derrota

const TeamStatsOverview = ({ teamA, teamB, victoryData }: TeamStatsOverviewProps) => {

  if (!teamA && !teamB && victoryData) {
    return;
  }
  const stats = [
    { label: 'Média de Gols', key: 'avg_total_goals_team' },
    { label: 'Média Oportunidades Criadas', key: 'avg_shots_on_goal_team' },
    { label: 'Gols Esperados (%)', key: 'avg_expected_goals_team' },
    { label: 'Posse de Bola (%)', key: 'avg_possession_team' },
    { label: 'Média de Passes', key: 'avg_total_passes_team' },
  ];

  return (
    <div className="stats-overview-container">
      <div className="stats-table-container">
        <h2>Comparativo de Estatísticas</h2>
        <table className="stats-table">
          <thead>
            <tr>
              <th>Estatística</th>
              <th>{teamA.team_id}</th>
              <th>{teamB.team_id}</th>
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
