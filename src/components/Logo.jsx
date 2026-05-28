export default function Logo({ manifest }) {
  const logo = manifest?.logo?.earthOrbit64;

  return (
    <div className="brand">
      <div className="brand-badge">
        {logo ? (
          <img src={logo} className="brand-logo" alt="Doomsday Model Earth orbit logo" />
        ) : (
          <div className="brand-logo-placeholder" />
        )}
      </div>
      <div className="brand-text">
        <strong>DOOMSDAY</strong>
        <span>MODEL</span>
      </div>
    </div>
  );
}

