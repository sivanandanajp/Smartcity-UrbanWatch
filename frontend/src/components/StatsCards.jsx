import RiskMeter from "./RiskMeter";
import "../styles/cards.css";

function StatsCards({ riskData }) {

  const riskLevel =

    riskData?.risk_score >= 70

      ? "HIGH"

      : riskData?.risk_score >= 40

      ? "MEDIUM"

      : "LOW";

  return (

    <div className="stats-wrapper">

      <div className="stats-list">

        <div className="small-stat-card">

          <h2>
            {riskData?.expected_violations || 0}
          </h2>

          <div className="trend positive">

            {

              riskData?.trend_percentage >= 0

                ? `↑ ${riskData?.trend_percentage}%`

                : `↓ ${Math.abs(
                    riskData?.trend_percentage
                  )}%`

            }

          </div>

          <p className="trend-label">

            Compared to

            {" "}

            {riskData?.previous_day}

          </p>

          <p>
            🚨 Expected Violations
          </p>

        </div>

        <div className="small-stat-card">

          <h2>
            {riskData?.peak_hours || "-"}
          </h2>

          <p>
            🕒 Peak Hours
          </p>

        </div>

        <div className="small-stat-card">

          <h2>
            {riskData?.most_common_violation || "-"}
          </h2>

          <p>
            🚦 Top Violation
          </p>

        </div>

        <div className="small-stat-card">

          <h2>
            {riskData?.highest_risk_camera || "-"}
          </h2>

          <p>
            📷 Highest Risk Camera
          </p>

        </div>

        <div className="small-stat-card">

          <h2>
            {riskLevel}
          </h2>

          <p>
            ⚠ Risk Level
          </p>

        </div>

        <div className="small-stat-card">

          <h2>
            {riskData?.risk_score || 0}%
          </h2>

          <p>
            📊 Risk Index
          </p>

        </div>

      </div>

      <RiskMeter
        score={riskData?.risk_score || 0}
      />

    </div>

  );

}

export default StatsCards;