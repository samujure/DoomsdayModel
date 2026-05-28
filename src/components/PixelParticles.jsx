const FIRE_POSITIONS = [
  { left: '48%', top: '39%', scale: 0.8 },
  { left: '63%', top: '34%', scale: 1.1 },
  { left: '73%', top: '44%', scale: 0.9 },
  { left: '81%', top: '53%', scale: 0.7 },
];

const BURNT_FIRE_POSITIONS = [
  { left: '15%', top: '58%', scale: 0.95 },
  { left: '22%', top: '50%', scale: 0.72 },
  { left: '29%', top: '62%', scale: 1.1 },
  { left: '36%', top: '46%', scale: 0.82 },
  { left: '44%', top: '57%', scale: 1.18 },
  { left: '52%', top: '42%', scale: 0.86 },
  { left: '61%', top: '36%', scale: 1.25 },
  { left: '70%', top: '48%', scale: 1.05 },
  { left: '78%', top: '40%', scale: 0.92 },
  { left: '86%', top: '55%', scale: 1.15 },
];

const SMOKE_SOURCES = [
  { left: 34, top: 43, width: 84 },
  { left: 42, top: 38, width: 96 },
  { left: 50, top: 32, width: 112 },
  { left: 59, top: 29, width: 128 },
  { left: 66, top: 24, width: 142 },
  { left: 73, top: 36, width: 118 },
  { left: 80, top: 45, width: 96 },
];

const SMOKE_DENSITY = {
  alive: 0,
  warming: 10,
  burning: 18,
  inferno: 30,
  burnt: 22,
  recovering: 4,
};

function smokeStyle(index, riskState) {
  const isBurnt = riskState === 'burnt';
  const isInferno = riskState === 'inferno';
  const isWarming = riskState === 'warming';
  const source = SMOKE_SOURCES[index % SMOKE_SOURCES.length];
  const spread = isBurnt ? 34 : isInferno ? 18 : isWarming ? 7 : 12;
  const left = source.left + (((index * 11) % (spread * 2 + 1)) - spread);
  const top = source.top + (((index * 7) % 11) - 5);
  const width = isBurnt
    ? 110 + ((index * 29) % 86)
    : isInferno
      ? source.width + 22 + ((index * 19) % 84)
      : isWarming
        ? source.width * 0.72 + ((index * 11) % 28)
        : source.width + ((index * 17) % 52);
  const duration = isBurnt ? 18 + (index % 8) * 1.4 : isInferno ? 9 + (index % 6) * 0.8 : 10 + (index % 5) * 0.75;
  const opacity = isBurnt ? 0.48 : isInferno ? 0.8 : isWarming ? 0.64 : 0.72;

  return {
    left: `${left}%`,
    top: `${top}%`,
    width: `${width}px`,
    animationDelay: `${index * -0.68}s`,
    animationDuration: `${duration}s`,
    '--smoke-opacity': opacity,
    '--smoke-drift': `${index % 2 === 0 ? '-' : ''}${10 + (index % 6) * 8}px`,
  };
}

function sprite(src, className, style, index) {
  if (!src) return null;
  return <img key={`${className}-${index}`} src={src} className={`fx-sprite ${className}`} style={style} alt="" aria-hidden="true" />;
}

export default function PixelParticles({ manifest, riskState }) {
  const clouds = manifest?.fx?.clouds ?? [];
  const smoke = manifest?.fx?.smoke ?? [];
  const fire = manifest?.fx?.fire ?? [];
  const birds = manifest?.fx?.birds ?? [];
  const particles = manifest?.fx?.particles ?? {};

  const showClouds = ['alive', 'recovering'].includes(riskState);
  const showBirds = riskState === 'alive';
  const smokeCount = SMOKE_DENSITY[riskState] ?? 0;
  const showSmoke = smokeCount > 0;
  const showFire = ['burning', 'inferno', 'burnt'].includes(riskState);
  const showEmbers = ['burning', 'inferno', 'burnt'].includes(riskState);
  const showAsh = ['inferno', 'burnt'].includes(riskState);
  const showRain = riskState === 'recovering';

  return (
    <div className="pixel-particles" aria-hidden="true">
      {showClouds &&
        clouds.slice(0, 3).map((src, index) =>
          sprite(src, `fx-cloud cloud-${index + 1}`, { top: `${8 + index * 9}%`, animationDelay: `${index * -18}s` }, index),
        )}

      {showBirds &&
        birds.slice(0, 1).map((src, index) => sprite(src, 'fx-bird', { top: '21%', animationDelay: '-7s' }, index))}

      {showSmoke &&
        Array.from({ length: smokeCount }, (_, index) =>
          sprite(smoke[Math.min(1, smoke.length - 1)] ?? smoke[0], `fx-smoke smoke-${riskState}`, smokeStyle(index, riskState), index),
        )}

      {showFire &&
        (riskState === 'burnt' ? BURNT_FIRE_POSITIONS : FIRE_POSITIONS).map((pos, index) =>
          sprite(fire[index % Math.max(1, fire.length)], 'fx-fire', {
            left: pos.left,
            top: pos.top,
            transform: `scale(${riskState === 'inferno' ? pos.scale * 1.35 : riskState === 'burnt' ? pos.scale * 1.25 : pos.scale})`,
            animationDelay: `${index * -0.19}s`,
          }, index),
        )}

      {showEmbers &&
        Array.from({ length: riskState === 'burnt' ? 30 : riskState === 'inferno' ? 22 : 12 }, (_, index) =>
          sprite(particles.ember, 'fx-ember', {
            left: `${22 + ((index * 13) % 70)}%`,
            top: `${68 + (index % 8)}%`,
            animationDelay: `${index * -0.37}s`,
          }, index),
        )}

      {showAsh &&
        Array.from({ length: 18 }, (_, index) =>
          sprite(particles.ash, 'fx-ash', {
            left: `${4 + ((index * 17) % 92)}%`,
            animationDelay: `${index * -0.41}s`,
          }, index),
        )}

      {showRain &&
        Array.from({ length: 38 }, (_, index) =>
          sprite(particles.rain, 'fx-rain', {
            left: `${(index * 7) % 100}%`,
            animationDelay: `${index * -0.08}s`,
          }, index),
        )}
    </div>
  );
}
