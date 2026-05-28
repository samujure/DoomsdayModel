export default function WorldScene({ manifest, region, timeOfDay, riskState }) {
  const plate =
    manifest?.worlds?.[region]?.[timeOfDay]?.[riskState]?.plate ??
    manifest?.worlds?.[region]?.evening?.[riskState]?.plate ??
    manifest?.worlds?.[region]?.evening?.alive?.plate;

  return (
    <div className="world-scene" aria-hidden="true">
      {plate ? (
        <div
          key={plate}
          className="world-bg"
          style={{ '--world-plate': `url("${plate}")` }}
        />
      ) : (
        <div className="world-missing" />
      )}
      <div className="world-bottom-fill" />
      <div className="world-vignette" />
      <div className="scanlines" />
    </div>
  );
}
