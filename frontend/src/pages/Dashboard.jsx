import { useState, useEffect } from "react";
import TopJunctionRanking from "../components/TopJunctionRanking";
import jsPDF from "jspdf";
import Header from "../components/Header";
import MapCard from "../components/MapCard";
import StatsCards from "../components/StatsCards";
import ViolationStats from "../components/ViolationStats";
import TrendChart from "../components/TrendChart";


import "../styles/dashboard.css";
function Dashboard() {
    const [riskData, setRiskData] =
useState(null);

const [junctions, setJunctions] =
useState([]);


const [selectedJunction,
setSelectedJunction] =
useState("STATUE NORTH");

const [selectedDay,
setSelectedDay] =
useState("Monday");

const [searchTerm,
setSearchTerm] =
useState("");

const [violationStats,
setViolationStats] =
useState(null);

const [hourRanking, setHourRanking] =
useState([]);

const [selectedTimeRange, setSelectedTimeRange] =
useState("0-2");

const [
  violationPeakHours,
  setViolationPeakHours
] = useState({});

const [
  expectedViolations,
  setExpectedViolations
] = useState({});

const [autoRotate,
setAutoRotate] =
useState(true);

  const exportReport = () => {

    if(!riskData)
      return;

    const csvContent = [
  [
    "Junction",
    "Day",
    "Risk Score",
    "Expected Violations",
    "Peak Hours",
    "Top Violation",
    "Highest Risk Camera"
  ].join(","),

  [
    selectedJunction,
    selectedDay,
    riskData.risk_score,
    riskData.expected_violations,
    riskData.peak_hours,
    riskData.most_common_violation,
    riskData.highest_risk_camera
  ].join(",")

].join("\n");

    const blob = new Blob(
      [csvContent],
      {
        type:"text/csv"
      }
    );
    
    const url =
      window.URL.createObjectURL(
        blob
      );

    const link =
      document.createElement("a");

    link.href = url;

    link.download =
      `UrbanWatch_${selectedJunction}_${selectedDay}.csv`;

    link.click();

  };
const sendNotification = () => {

  if (
    !window.confirm(
      `Send traffic alert for ${selectedDay}?`
    )
  ) {
    return;
  }

  fetch(
    "http://127.0.0.1:5000/send-alert",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        day: selectedDay
      })
    }
  )
  .then(res => res.json())
  .then(data => {
    alert(data.message);
  })
  .catch(() => {
    alert("Failed to send email.");
  });

};

useEffect(() => {

  fetch(
    "http://127.0.0.1:5000/risk-assessment",
    {
      method: "POST",

      headers: {
        "Content-Type":
          "application/json"
      },

      body: JSON.stringify({

        junction:
          selectedJunction,

        day:
          selectedDay

      })

    }
  )

  .then(
    response =>
      response.json()
  )

  .then(
    data => {

      setRiskData(data);

    }
  );

  fetch(
    "http://127.0.0.1:5000/violation-stats",
    {
      method: "POST",

      headers: {
        "Content-Type":
          "application/json"
      },

      body: JSON.stringify({

        junction:
          selectedJunction,

        day:
          selectedDay

      })

    }
  )

  .then(
    response =>
      response.json()
  )

  .then(
    data => {

      setViolationStats(data);

    }
  );

}, [

  selectedJunction,

  selectedDay

]);
useEffect(() => {

  fetch(
    "http://127.0.0.1:5000/violation-peak-hours",
    {
      method: "POST",

      headers: {
        "Content-Type":
          "application/json"
      },

      body: JSON.stringify({

        junction:
          selectedJunction

      })

    }
  )

  .then(
    res => res.json()
  )

  .then(
    data => {

      setViolationPeakHours(
        data
      );

    }
  );

}, [selectedJunction]);

  useEffect(() => {

  fetch(
    "http://127.0.0.1:5000/junctions"
  )

  .then(res => res.json())

  .then(data => {

    setJunctions(data);

    if(data.length > 0){

      setSelectedJunction(
        data[0]
      );

    }

  });

}, []);
useEffect(() => {

  if(
    !searchTerm ||
    searchTerm.length < 2
  )
    return;

  const foundJunction =

    junctions.find(

      (junction) =>

        junction
        .toLowerCase()

        .includes(

          searchTerm
          .toLowerCase()

        )

    );

  if(foundJunction){

    setSelectedJunction(
      foundJunction
    );

  }

}, [

  searchTerm,

  junctions

]);

useEffect(() => {

  fetch(
    "http://127.0.0.1:5000/hour-ranking",
    {
      method:"POST",

      headers:{
        "Content-Type":
        "application/json"
      },

      body:JSON.stringify({
        range:selectedTimeRange
      })
    }
  )

  .then(res=>res.json())

  .then(data=>{
    setHourRanking(data);
  });

}, [selectedTimeRange]);

useEffect(() => {

  if(
    !autoRotate ||
    junctions.length === 0
  )
    return;

  const interval =

    setInterval(() => {

      setSelectedJunction(
        current => {

          const currentIndex =

            junctions.indexOf(
              current
            );

          const nextIndex =

            (
              currentIndex + 1
            )

            %

            junctions.length;

          return junctions[
            nextIndex
          ];

        }
      );

    }, 5000);

  return () =>
    clearInterval(
      interval
    );

}, [

  autoRotate,

  junctions

]);

const exportPDF = () => {

  if (!riskData) return;

  const pdf = new jsPDF();

  pdf.setFontSize(20);
  pdf.text("UrbanWatch Traffic Report", 20, 20);

  pdf.setFontSize(12);

  pdf.text(`Junction: ${selectedJunction}`, 20, 40);
  pdf.text(`Day: ${selectedDay}`, 20, 50);
  pdf.text(`Risk Score: ${riskData.risk_score}`, 20, 60);
  pdf.text(`Expected Violations: ${riskData.expected_violations}`, 20, 70);
  pdf.text(`Peak Hours: ${riskData.peak_hours}`, 20, 80);
  pdf.text(`Top Violation: ${riskData.most_common_violation}`, 20, 90);
  pdf.text(`Highest Risk Camera: ${riskData.highest_risk_camera}`, 20, 100);

  pdf.save(
    `UrbanWatch_${selectedJunction}_${selectedDay}.pdf`
  );
};

  return (

    <div
  className="dashboard-content"
  id="report-content"
>

      <Header

  searchTerm={
    searchTerm
  }

  setSearchTerm={
    setSearchTerm
  }

/>
 <div className="top-controls">

  <button
    onClick={exportReport}
    className="export-btn"
  >
    Export Report
  </button>

  <button
    onClick={exportPDF}
    className="export-btn"
  >
    Export PDF
  </button>

  <select

    value={selectedJunction}

    onChange={(e)=>{

      setSelectedJunction(
        e.target.value
      );

      setAutoRotate(false);

    }}

  >

    {

      junctions.map(

        (junction)=>(

          <option
            key={junction}
            value={junction}
          >

            {junction}

          </option>

        )

      )

    }

  </select>

  <select

    value={selectedDay}
        onChange={(e)=>{

      setSelectedDay(
        e.target.value
      );

      setAutoRotate(false);

    }}

  >

    <option>Monday</option>
    <option>Tuesday</option>
    <option>Wednesday</option>
    <option>Thursday</option>
    <option>Friday</option>
    <option>Saturday</option>
    <option>Sunday</option>

  </select>

  <button
    className="export-btn"
    onClick={()=>
      setAutoRotate(
        !autoRotate
      )
    }
  >

    {

      autoRotate

      ?

      "Stop Rotation"

      :

      "Start Rotation"

    }

  </button>

   <button
  className="export-btn"
  onClick={sendNotification}
>
  Notify Authority
</button>
</div>



      <div className="top-section">

        <div className="left-panel">

          <MapCard
  selectedJunction={
    selectedJunction
   }
    />
    

        
        </div>
        

        <StatsCards
          riskData={riskData}
        />

      </div>

  <div className="junction-summary-card">

  <div className="top-summary">

    <div className="summary-box">
      <h4>Current Junction</h4>
      <h2>{selectedJunction}</h2>
    </div>

    <div className="summary-box">
      <h4>Day</h4>
      <h2>{selectedDay}</h2>
    </div>

  </div>

  <div className="violation-box">
  <h3>Violation of Red Light</h3>
  <p>
    {
      violationPeakHours[
        "Violation of Red Light"
      ] || "-"
    }
  </p>
</div>

<div className="violation-box">
  <h3>Triple Riding</h3>
  <p>
    {
      violationPeakHours[
        "Triple Riding"
      ] || "-"
    }
  </p>
</div>

<div className="violation-box">
  <h3>No Helmet</h3>
  <p>
    {
      violationPeakHours[
        "No Helmet"
      ] || "-"
    }
  </p>
</div>

<div className="violation-box">
  <h3>Speed Violation</h3>
  <p>
    {
      violationPeakHours[
        "Speed Violation"
      ] || "-"
    }
  </p>
</div>

</div>



      <div className="bottom-section">

        <ViolationStats
  violationStats={violationStats}
/>

        <TrendChart

  selectedJunction={
    selectedJunction
  }

  selectedDay={
    selectedDay
  }

/>


      </div>

     <TopJunctionRanking
  ranking={hourRanking}
  selectedTimeRange={selectedTimeRange}
  setSelectedTimeRange={setSelectedTimeRange}
/>
<select
  value={selectedTimeRange}
  onChange={(e)=>
    setSelectedTimeRange(
      e.target.value
    )
  }
>

  <option value="0-2">12 AM - 2 AM</option>
  <option value="2-4">2 AM - 4 AM</option>
  <option value="4-6">4 AM - 6 AM</option>
  <option value="6-8">6 AM - 8 AM</option>
  <option value="8-10">8 AM - 10 AM</option>
  <option value="10-12">10 AM - 12 PM</option>
  <option value="12-14">12 PM - 2 PM</option>
  <option value="14-16">2 PM - 4 PM</option>
  <option value="16-18">4 PM - 6 PM</option>
  <option value="18-20">6 PM - 8 PM</option>
  <option value="20-22">8 PM - 10 PM</option>
  <option value="22-24">10 PM - 12 AM</option>

</select>

    </div>
    

  );
}

export default Dashboard;