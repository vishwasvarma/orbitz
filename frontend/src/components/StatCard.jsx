export default function StatCard({ label, value, unit, className = '' }) {
  return (
    <article className={`stat-card ${className}`}>
      <p className="stat-label">{label}</p>
      <p className="stat-value">
        {value ?? '—'}
        {unit ? <span className="stat-unit">{unit}</span> : null}
      </p>
    </article>
  )
}
