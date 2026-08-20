function TopJunctionRanking({ ranking }) {
  return (
    <div className="ranking-card">
      <h2>Top 5 Violating Junctions</h2>

      {ranking.map((item, index) => (
        <div
          key={index}
          className="ranking-item"
        >
          <span>
            {index + 1}. {item.junction}
          </span>

          <span>
            {item.violations}
          </span>
        </div>
      ))}
    </div>
  );
}

export default TopJunctionRanking;