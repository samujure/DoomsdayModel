import { Activity, BarChart3, Clock3, Database, FileText, Globe2, Home, Pause, Settings, SlidersHorizontal } from 'lucide-react';
import { useEffect, useMemo, useState } from 'react';
import DomainCard from './DomainCard.jsx';
import EventFeed from './EventFeed.jsx';
import Logo from './Logo.jsx';
import MainClock from './MainClock.jsx';

const nav = [
  ['Overview', Home],
  ['Domains', Globe2],
  ['Scenarios', SlidersHorizontal],
  ['Simulations', Activity],
  ['Insights', BarChart3],
  ['Reports', FileText],
  ['Settings', Settings],
];

function formatLiveStamp(date) {
  const day = date
    .toLocaleDateString('en-US', {
      month: 'short',
      day: '2-digit',
      year: 'numeric',
    })
    .toUpperCase();
  const time = date.toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  });
  return `${day}  ${time}`;
}

export default function DashboardUI({
  manifest,
  manifestError,
  riskState,
  riskStates,
  stateLabel,
  onRiskStateChange,
  domains,
  compositeRisk,
  modelConfidence,
  nextUpdate,
  onMockEvent,
}) {
  const [now, setNow] = useState(() => new Date());
  const liveStamp = useMemo(() => formatLiveStamp(now), [now]);

  useEffect(() => {
    const timer = window.setInterval(() => setNow(new Date()), 1000);
    return () => window.clearInterval(timer);
  }, []);

  return (
    <section className="dashboard">
      <aside className="sidebar panel">
        <Logo manifest={manifest} />
        <nav className="nav-list">
          {nav.map(([label, Icon], index) => (
            <button key={label} className={`nav-item ${index === 0 ? 'active' : ''}`} type="button">
              <Icon size={18} />
              <span>{label}</span>
            </button>
          ))}
        </nav>
        <div className="system-status">
          <div className="status-title"><span className="status-dot" /> SYSTEM STATUS</div>
          <p>All systems nominal<br />Mock pipeline online</p>
          <div className="mini-graph" />
        </div>
      </aside>

      <div className="main-column">
        <header className="top-row">
          <div className="speed-controls panel">
            <button type="button"><Pause size={15} /> PAUSE</button>
            <button type="button" className="active">1x</button>
            <button type="button">2x</button>
            <button type="button">5x</button>
          </div>
          <div className="live-stamp panel">
            <span>{liveStamp}</span>
            <strong><i /> LIVE</strong>
          </div>
        </header>

        <div className="title-stack">
          <h1>DOOMSDAY MODEL</h1>
          <p>:: MULTI-DOMAIN PROBABILISTIC THREAT ENGINE ::</p>
        </div>

        <div className="warning-chip">WARNING — {stateLabel(riskState)}</div>

        {manifestError && <div className="manifest-warning panel">Manifest unavailable: {manifestError}</div>}

        <MainClock compositeRisk={compositeRisk} riskState={riskState} />

        <div className="domain-grid">
          {domains.map((domain) => (
            <DomainCard key={domain.label} domain={domain} />
          ))}
        </div>

        <div className="state-switcher panel" aria-label="Risk state controls">
          <span>DEV STATE</span>
          {riskStates.map((state) => (
            <button
              type="button"
              key={state}
              className={state === riskState ? 'active' : ''}
              onClick={() => onRiskStateChange(state)}
            >
              {stateLabel(state)}
            </button>
          ))}
        </div>

        <footer className="bottom-strip panel">
          <div>
            <span>COMPOSITE RISK</span>
            <strong>{compositeRisk.toFixed(1)}%</strong>
          </div>
          <div>
            <Database size={22} />
            <span>MODEL CONFIDENCE</span>
            <strong>{modelConfidence}%</strong>
          </div>
          <div>
            <Clock3 size={22} />
            <span>NEXT UPDATE</span>
            <strong>00:{String(nextUpdate).padStart(2, '0')}</strong>
          </div>
        </footer>
      </div>

      <EventFeed onMockEvent={onMockEvent} riskState={riskState} />
    </section>
  );
}
