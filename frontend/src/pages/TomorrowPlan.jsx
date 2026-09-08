import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import Navbar from "../components/Navbar";
import FitnessPlanCard from "../components/FitnessPlanCard";
import Loading from "../components/Loading";
import { api } from "../services/api";

export default function TomorrowPlan() {
  const [plan, setPlan] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .get("/plans/tomorrow")
      .then(setPlan)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <Loading />;

  return (
    <div className="page">
      <Navbar />
      <main className="form-page">
        <h1>Tomorrow&apos;s Plan</h1>

        {error ? <p className="error">{error}</p> : null}
        <FitnessPlanCard plan={plan} />
        {plan?.reason ? <p className="muted reason">{plan.reason}</p> : null}
        <div className="dash-cta">
          <Link className="btn primary" to="/dashboard">
            Back to Dashboard
          </Link>
        </div>
      </main>
    </div>
  );
}
