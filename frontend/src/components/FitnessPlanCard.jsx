export default function FitnessPlanCard({ plan, compact = false }) {
  if (!plan) {
    return (
      <article className="plan-card">
        <h3>Tomorrow&apos;s Plan</h3>
        <p className="muted">Complete today&apos;s check-in to generate your plan.</p>
      </article>
    )
  }

  const data = plan.plan || plan
  const sections = data.sections || {}

  return (
    <article className={`plan-card ${compact ? 'compact' : ''}`}>
      <h3>{data.title || "Tomorrow's Plan"}</h3>
      {data.intensity ? <p className="chip">Intensity: {data.intensity.replaceAll('_', ' ')}</p> : null}

      {sections.strength?.length ? (
        <section>
          <h4>Strength</h4>
          <ul>
            {sections.strength.map((item) => (
              <li key={item.name}>
                {item.name} {item.prescription ? `— ${item.prescription}` : ''}
              </li>
            ))}
          </ul>
        </section>
      ) : null}

      {sections.activity?.length ? (
        <section>
          <h4>Activity</h4>
          <ul>
            {sections.activity.map((item) => (
              <li key={item.name}>
                {item.name} {item.prescription ? `— ${item.prescription}` : ''}
              </li>
            ))}
          </ul>
        </section>
      ) : null}

      {sections.recovery?.length ? (
        <section>
          <h4>Recovery</h4>
          <ul>
            {sections.recovery.map((item) => (
              <li key={item.name}>
                {item.name} {item.prescription ? `— ${item.prescription}` : ''}
              </li>
            ))}
          </ul>
        </section>
      ) : null}

      {!compact && (sections.diet || data.diet) ? (
        <section>
          <h4>Diet {(sections.diet || data.diet)?.preference === 'non_veg' ? '(non-veg)' : '(veg)'}</h4>
          <ul>
            {(sections.diet || data.diet)?.meals?.map((meal) => (
              <li key={meal.meal}>
                <strong>{meal.meal}:</strong>{' '}
                {(meal.items || [])
                  .map((item) => `${item.name}${item.amount ? ` ${item.amount}` : ''}`)
                  .join(', ')}
              </li>
            ))}
          </ul>
          {(sections.diet || data.diet)?.notes ? (
            <p className="muted">{(sections.diet || data.diet).notes}</p>
          ) : null}
        </section>
      ) : null}

      {!compact && data.avoided_exercises?.length ? (
        <p className="muted">Left out for medical reasons: {data.avoided_exercises.join(', ')}</p>
      ) : null}

      {compact && (sections.diet || data.diet) ? (
        <p className="muted">
          Diet: {(sections.diet || data.diet)?.preference === 'non_veg' ? 'non-veg' : 'veg'}
        </p>
      ) : null}

      <div className="plan-meta">
        {sections.hydration?.aim ? <p>Hydration: {sections.hydration.aim}</p> : null}
        {sections.sleep?.aim ? <p>Sleep: {sections.sleep.aim}</p> : null}
      </div>

      {data.notes ? <p className="muted">{data.notes}</p> : null}
    </article>
  )
}
