function About() {

  return (

    <div
      style={{
        padding: "40px",
        width: "100%"
      }}
    >

      <h1
        style={{
          fontSize: "4rem",
          marginBottom: "20px"
        }}
      >
        About UrbanWatch
      </h1>

      <div
        style={{
          marginTop: "25px",
          
          padding: "30px",
          borderRadius: "20px",
          boxShadow:
            "0 4px 12px rgba(0,0,0,0.3)",
          lineHeight: "1.8",
          fontSize: "1.5rem"
        }}
      >

        <p>

          <strong>UrbanWatch</strong> is an AI-powered
          Urban Traffic Intelligence System designed
          to analyze traffic violations and identify
          high-risk junctions across the city.

        </p>

        <br />

        <p>

          The system uses historical traffic
          violation data and machine learning
          models to predict expected violations,
          assess risk levels, identify peak traffic
          hours, and determine the most critical
          locations requiring attention.

        </p>

        <br />

        <p>

          Through interactive dashboards,
          heatmaps, analytics, and risk assessment
          modules, UrbanWatch helps authorities
          make data-driven decisions to improve
          road safety and traffic management.

        </p>

        <br />

        <p>

          The platform provides real-time insights
          into traffic patterns, violation trends,
          and camera-level risk analysis, enabling
          smarter monitoring and efficient resource
          allocation.

        </p>

      </div>

    </div>

  );

}

export default About;