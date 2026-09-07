import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from 'recharts'
import { useTheme } from '../context/ThemeContext'

export default function ProgressChart({ data, dataKey, color, label }) {
  const { theme } = useTheme()
  const isDark = theme === 'dark'
  const ink = isDark ? '#ffffff' : '#000000'
  const grid = isDark ? 'rgba(255,255,255,0.2)' : 'rgba(0,0,0,0.15)'
  const stroke = color || ink

  if (!data?.length) {
    return <p className="muted">No progress data yet. Complete a few check-ins.</p>
  }

  return (
    <div className="chart-wrap">
      <h4>{label}</h4>
      <ResponsiveContainer width="100%" height={220}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke={grid} />
          <XAxis dataKey="date" tick={{ fill: ink, fontSize: 11 }} />
          <YAxis tick={{ fill: ink, fontSize: 11 }} />
          <Tooltip
            contentStyle={{
              background: isDark ? '#000000' : '#ffffff',
              border: `1px solid ${ink}`,
              color: ink,
            }}
          />
          <Line type="monotone" dataKey={dataKey} stroke={stroke} strokeWidth={2.5} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
