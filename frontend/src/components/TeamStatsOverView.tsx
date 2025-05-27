import './TeamStatsOverview.css';
import { PieChart, Pie, Cell, Tooltip, Legend } from 'recharts';

interface TeamStats {
  team_id: number;
  team_name: string;
  avg_total_goals_team: number;
  avg_shots_on_goal_team: number;
  avg_possession_team: number;
  avg_expected_goals_team: number;
  avg_passes_accurate_team: number;
  avg_total_passes_team: number;
}


interface TeamStatsOverviewProps {
  teamA: TeamStats;
  teamB: TeamStats;
  victoryData: [number, number, number][];
}

const COLORS = ['#DA291C', '#5F5F5F', '#FFFFFF']; // Vitória MU, Empate, Derrota

const TeamStatsOverview = ({ teamA, teamB, victoryData }: TeamStatsOverviewProps) => {

  if (!teamA && !teamB && victoryData) {
    return;
  }

  const win = parseFloat((victoryData[0][2]*100).toFixed(1))
  const lose = parseFloat((victoryData[0][0]*100).toFixed(1))
  const draw = parseFloat((victoryData[0][1]*100).toFixed(1))
  const chartData = [
    { name: 'Vitória Manchester United', value: win },
    { name: 'Empate', value: draw },
    { name: 'Vitória Adversário', value: lose },
  ];
  

  const stats = [
    { label: 'Média de Gols', key: 'avg_total_goals_team' },
    { label: 'Média Oportunidades Criadas', key: 'avg_shots_on_goal_team' },
    { label: 'Gols Esperados', key: 'avg_expected_goals_team' },
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
              <th>{teamA.team_name}</th>
              <th>{teamB.team_name}</th>
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
            data={chartData}
            cx="50%"
            cy="50%"
            label
            outerRadius={100}
            dataKey="value"
          >
            {chartData.map((_, index) => (
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
