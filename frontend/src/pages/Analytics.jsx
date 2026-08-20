import { useEffect, useState } from "react";

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  LineChart,
  Line
} from "recharts";

function Analytics() {

  const [analytics,
    setAnalytics] =
    useState(null);

  const [weekdayData,
    setWeekdayData] =
    useState([]);

  useEffect(() => {

    fetch(
      "http://127.0.0.1:5000/analytics"
    )

    .then(
      response =>
        response.json()
    )

    .then(
      data =>
        setAnalytics(data)
    );

    fetch(
      "http://127.0.0.1:5000/weekday-analytics"
    )

    .then(
      response =>
        response.json()
    )

    .then(
      data =>
        setWeekdayData(data)
    );

  }, []);

  if (!analytics) {

    return (

      <div
        style={{
          padding: "20px"
        }}
      >
        Loading Analytics...
      </div>

    );

  }

  const COLORS = [

    "#2563eb",
    "#22c55e",
    "#f59e0b",
    "#ef4444",
    "#8b5cf6"

  ];

  return (

    <div
      style={{
        padding: "20px",
        width: "100%"
      }}
    >

      <h1>
        Analytics Dashboard
      </h1>

      <div

        style={{

          display: "grid",

          gridTemplateColumns:
            "repeat(4, 1fr)",

          gap: "20px",

          marginTop: "20px"

        }}

      >

        <div className="small-stat-card">

          <h2>
            {analytics.total_violations}
          </h2>

          <p>
            Total Violations
          </p>

        </div>

        <div className="small-stat-card">

          <h2>
            {analytics.top_junction}
          </h2>

          <p>
            Top Junction
          </p>

        </div>

        <div className="small-stat-card">

          <h2>
            {analytics.most_common_violation}
          </h2>

          <p>
            Top Violation
          </p>

        </div>

        <div className="small-stat-card">

          <h2
            style={{
              fontSize: "1.5rem",
              lineHeight: "1.2"
            }}
          >
            {analytics.highest_risk_camera}
          </h2>

          <p>
            Highest Risk Camera
          </p>

        </div>

      </div>

      <div

        style={{

          display: "grid",

          gridTemplateColumns:
            "1fr 1fr",

          gap: "30px",

          marginTop: "40px"

        }}

      >

        <div

          style={{

            background: "white",

            padding: "20px",

            borderRadius: "20px",

            height: "450px"

          }}

        >

          <h3>
            Violation Distribution
          </h3>

          <ResponsiveContainer
            width="100%"
            height="100%"
          >

            <PieChart>

              <Pie

                data={
                  analytics.violation_distribution
                }

                dataKey="value"

                nameKey="name"

                outerRadius={130}

                label={({name}) => name}

              >

                {

                  analytics
                    .violation_distribution

                    .map(

                      (_, index) => (

                        <Cell

                          key={index}

                          fill={
                            COLORS[
                              index %
                              COLORS.length
                            ]
                          }

                        />

                      )

                    )

                }

              </Pie>

              <Tooltip />

            </PieChart>

          </ResponsiveContainer>

        </div>

        <div

          style={{

            background: "white",

            padding: "20px",

            borderRadius: "20px",

            height: "450px"

          }}

        >

          <h3>
            Top 5 Risk Junctions
          </h3>

          <ResponsiveContainer
            width="100%"
            height="100%"
          >

            <BarChart
              data={
                analytics.top5
              }
            >

              <CartesianGrid
                strokeDasharray="3 3"
              />

              <XAxis

                dataKey="junction"

                angle={-25}

                textAnchor="end"

                interval={0}

              />

              <YAxis />

              <Tooltip />

              <Bar

                dataKey="violations"

                fill="#2563eb"

              />

            </BarChart>

          </ResponsiveContainer>

        </div>

      </div>

      <div

        style={{

          background: "white",

          padding: "20px",

          borderRadius: "20px",

          marginTop: "30px",

          height: "450px"

        }}

      >

        <h3>
          Violations by Weekday
        </h3>

        <ResponsiveContainer
          width="100%"
          height="100%"
        >

          <LineChart
            data={weekdayData}
          >

            <CartesianGrid
              strokeDasharray="3 3"
            />

            <XAxis
              dataKey="weekday"
            />

            <YAxis />

            <Tooltip />

            <Line

              type="monotone"

              dataKey="violations"

              stroke="#2563eb"

              strokeWidth={3}

            />

          </LineChart>

        </ResponsiveContainer>

      </div>

    </div>

  );

}

export default Analytics;