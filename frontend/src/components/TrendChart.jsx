import {
  useEffect,
  useState
} from "react";

import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip
} from "recharts";

import "../styles/trendchart.css";

function TrendChart({

  selectedJunction,

  selectedDay

}) {

  const [data,
    setData] =
    useState([]);

  useEffect(() => {

    if(
      !selectedJunction
    )
      return;

    fetch(

      "http://127.0.0.1:5000/hourly-trend",

      {

        method:"POST",

        headers:{
          "Content-Type":
          "application/json"
        },

        body:JSON.stringify({

          junction:
          selectedJunction,

          day:
          selectedDay

        })

      }

    )

    .then(
      res =>
      res.json()
    )

    .then(
      trendData => {

        const formatted =

          trendData.map(

            item => ({

              time:
              item.hour,

              violations:
              item.count

            })

          );

        setData(
          formatted
        );

      }

    );

  }, [

    selectedJunction,

    selectedDay

  ]);

  return (

    <div className="trend-card">

      <h2>
        Trend Chart
      </h2>

      <ResponsiveContainer
        width="100%"
        height={250}
      >

        <LineChart
          data={data}
        >

          <XAxis
            dataKey="time"
          />

          <YAxis />

          <Tooltip />

          <Line

            type="monotone"

            dataKey="violations"

            stroke="#2563eb"

            strokeWidth={3}

            dot={{ r: 5 }}

          />

        </LineChart>

      </ResponsiveContainer>

    </div>

  );

}

export default TrendChart;