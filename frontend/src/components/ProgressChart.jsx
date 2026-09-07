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
  const ink = isDark ? '#aaaaaa' : '#606060'
  const grid = isDark ? '#303030' : '#e5e5e5'
  const tooltipBg = isDark ? '#212121' : '#ffffff'
  const tooltipText = isDark ? '#f1f1f1' : '#0f0f0f'
  const stroke = color || (isDark ? '#3ea6ff' : '#065fd4')

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
              background: tooltipBg,
              border: `1px solid ${grid}`,
              color: tooltipText,
              borderRadius: 12,
            }}
          />
          <Line type="monotone" dataKey={dataKey} stroke={stroke} strokeWidth={2.5} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
