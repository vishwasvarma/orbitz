import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from 'recharts'

export default function ProgressChart({ data, dataKey, color = '#1f6f5b', label }) {
  if (!data?.length) {
    return <p className="muted">No progress data yet. Complete a few check-ins.</p>
  }

  return (
    <div className="chart-wrap">
      <h4>{label}</h4>
      <ResponsiveContainer width="100%" height={220}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.08)" />
          <XAxis dataKey="date" tick={{ fill: '#c9d5cf', fontSize: 11 }} />
          <YAxis tick={{ fill: '#c9d5cf', fontSize: 11 }} />
          <Tooltip />
          <Line type="monotone" dataKey={dataKey} stroke={color} strokeWidth={2.5} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
