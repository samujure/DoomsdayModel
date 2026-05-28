import { Biohazard, Cpu, Globe2, Leaf, RadioTower } from 'lucide-react';

const ICONS = {
  NUCLEAR: RadioTower,
  CLIMATE: Leaf,
  BIOSECURITY: Biohazard,
  'AI / TECH': Cpu,
  GEOPOLITICAL: Globe2,
};

export default function DomainCard({ domain }) {
  const Icon = ICONS[domain.label];

  return (
    <article className={`domain-card panel tone-${domain.tone}`}>
      <div className="domain-head">
        <span className="domain-icon">{Icon && <Icon size={30} strokeWidth={1.8} />}</span>
        <h2>{domain.label}</h2>
      </div>
      <span className="domain-kicker">PROBABILITY</span>
      <strong className="domain-value">{domain.value}</strong>
      <div className="sparkline" />
      <div className="domain-foot">
        <span>TREND</span>
        <strong>{domain.trend}</strong>
      </div>
    </article>
  );
}
