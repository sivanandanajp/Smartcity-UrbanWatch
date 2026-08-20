import "../styles/violationstats.css";

function ViolationStats({

  violationStats

}) {

  if(!violationStats){

    return null;

  }

  return (

    <div className="violation-card">

      <h2>
        Violation Stats
      </h2>

      <div className="violation-grid">

        <div className="violation-item">

          <h3>
            {violationStats["No Helmet"] || 0}
          </h3>

          <p>
            No Helmet
          </p>

        </div>

        <div className="violation-item">

          <h3>
            {violationStats["Red Light"] || 0}
          </h3>

          <p>
            Red Light
          </p>

        </div>

        <div className="violation-item">

          <h3>
            {violationStats["Speeding"] || 0}
          </h3>

          <p>
            Speeding
          </p>

        </div>

        <div className="violation-item">

          <h3>
            {violationStats["Triple Riding"] || 0}
          </h3>

          <p>
            Triple Riding
          </p>

        </div>

      </div>

    </div>

  );

}

export default ViolationStats;