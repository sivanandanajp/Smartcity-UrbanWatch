import {
  CircularProgressbar
} from "react-circular-progressbar";

import "react-circular-progressbar/dist/styles.css";

function RiskMeter({score}) {


  return (

    <div className="risk-meter-card">

      <CircularProgressbar
        value={score}
        text={`${score}%`}
      />

      <h3>Risk Score</h3>

      <p>
        High Risk Zone
      </p>

    </div>

  );
}

export default RiskMeter;