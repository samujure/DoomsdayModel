function formatMinutesToMidnight(compositeRisk) {
  const minutes = Math.max(0.12, 15 - (compositeRisk / 100) * 14.5);
  const wholeMinutes = Math.floor(minutes);
  const seconds = Math.floor((minutes - wholeMinutes) * 60);
  return `${String(wholeMinutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}

function needleRotation(compositeRisk) {
  return -50 + (Math.max(0, Math.min(100, compositeRisk)) / 100) * 104;
}

export default function MainClock({ compositeRisk, riskState }) {
  const clockValue = formatMinutesToMidnight(compositeRisk);

  return (
    <section className="main-clock panel">
      <div className="gauge">
        <div className="gauge-arc" />
        <div className={`needle needle-${riskState}`} style={{ transform: `rotate(${needleRotation(compositeRisk)}deg)` }} />
        <div className="tick tick-a" />
        <div className="tick tick-b" />
        <div className="tick tick-c" />
        <div className="tick tick-d" />
        <div className="tick tick-e" />
      </div>
      <div className="clock-label">MINUTES TO MIDNIGHT</div>
      <div className="clock-value">{clockValue}</div>
    </section>
  );
}
