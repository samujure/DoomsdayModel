import { useCallback, useEffect, useMemo, useState } from 'react';
import DashboardUI from './components/DashboardUI.jsx';
import WorldScene from './components/WorldScene.jsx';
import PixelParticles from './components/PixelParticles.jsx';

const RISK_STATES = ['alive', 'warming', 'burning', 'inferno', 'burnt', 'recovering'];
const DOMAIN_LABELS = ['NUCLEAR', 'CLIMATE', 'BIOSECURITY', 'AI / TECH', 'GEOPOLITICAL'];
const DOMAIN_TONES = {
  NUCLEAR: 'red',
  CLIMATE: 'green',
  BIOSECURITY: 'violet',
  'AI / TECH': 'blue',
  GEOPOLITICAL: 'orange',
};
const STATE_BASE_VALUES = {
  alive: {
    NUCLEAR: 12.7,
    CLIMATE: 23.4,
    BIOSECURITY: 16.8,
    'AI / TECH': 18.9,
    GEOPOLITICAL: 20.2,
  },
  warming: {
    NUCLEAR: 20.8,
    CLIMATE: 38.6,
    BIOSECURITY: 22.4,
    'AI / TECH': 29.1,
    GEOPOLITICAL: 33.8,
  },
  burning: {
    NUCLEAR: 45.2,
    CLIMATE: 58.7,
    BIOSECURITY: 39.8,
    'AI / TECH': 48.4,
    GEOPOLITICAL: 55.1,
  },
  inferno: {
    NUCLEAR: 72.8,
    CLIMATE: 81.5,
    BIOSECURITY: 64.2,
    'AI / TECH': 69.6,
    GEOPOLITICAL: 77.3,
  },
  burnt: {
    NUCLEAR: 94.6,
    CLIMATE: 96.2,
    BIOSECURITY: 88.4,
    'AI / TECH': 91.7,
    GEOPOLITICAL: 95.1,
  },
  recovering: {
    NUCLEAR: 23.5,
    CLIMATE: 31.2,
    BIOSECURITY: 20.1,
    'AI / TECH': 26.8,
    GEOPOLITICAL: 28.9,
  },
};

function clamp(value, min, max) {
  return Math.min(max, Math.max(min, value));
}

function stateLabel(state) {
  return state.toUpperCase();
}

function getLocalTimeOfDay(date = new Date()) {
  const hour = date.getHours();
  if (hour >= 7 && hour < 17) return 'day';
  if (hour >= 17 && hour < 21) return 'evening';
  return 'night';
}

export default function App() {
  const [manifest, setManifest] = useState(null);
  const [manifestError, setManifestError] = useState('');
  const [riskState, setRiskState] = useState('alive');
  const [eventSignals, setEventSignals] = useState(() => Object.fromEntries(DOMAIN_LABELS.map((label) => [label, 0])));
  const [nextUpdate, setNextUpdate] = useState(30);
  const [confidenceDrift, setConfidenceDrift] = useState(0);
  const [localTimeOfDay, setLocalTimeOfDay] = useState(() => getLocalTimeOfDay());

  useEffect(() => {
    let cancelled = false;
    fetch('/assets/manifest.json')
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Manifest request failed: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        if (!cancelled) {
          setManifest(data);
        }
      })
      .catch((error) => {
        if (!cancelled) {
          setManifestError(error.message);
        }
      });
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    const onKeyDown = (event) => {
      const index = Number(event.key) - 1;
      if (index >= 0 && index < RISK_STATES.length) {
        setRiskState(RISK_STATES[index]);
      }
    };
    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, []);

  useEffect(() => {
    setEventSignals(Object.fromEntries(DOMAIN_LABELS.map((label) => [label, 0])));
  }, [riskState]);

  useEffect(() => {
    const timer = window.setInterval(() => {
      setNextUpdate((current) => (current <= 1 ? 30 : current - 1));
      setEventSignals((current) =>
        Object.fromEntries(DOMAIN_LABELS.map((label) => [label, current[label] * 0.86])),
      );
      setConfidenceDrift((current) => (current + 1) % 24);
    }, 1000);

    return () => window.clearInterval(timer);
  }, []);

  useEffect(() => {
    const timer = window.setInterval(() => setLocalTimeOfDay(getLocalTimeOfDay()), 60_000);
    return () => window.clearInterval(timer);
  }, []);

  const onMockEvent = useCallback((event) => {
    const impact = event.impact ?? 1;
    setNextUpdate(30);
    setEventSignals((current) => ({
      ...current,
      [event.tag]: clamp((current[event.tag] ?? 0) + impact * 2.4, -8, 10),
    }));
  }, []);

  const domains = useMemo(() => {
    const base = STATE_BASE_VALUES[riskState] ?? STATE_BASE_VALUES.alive;
    return DOMAIN_LABELS.map((label) => {
      const signal = eventSignals[label] ?? 0;
      const value = clamp(base[label] + signal, 1, 99);
      const trend = signal > 1.2 ? 'RISING' : signal < -1.2 ? 'FALLING' : riskState === 'recovering' ? 'FALLING' : 'STABLE';
      return {
        label,
        value: `${value.toFixed(1)}%`,
        trend,
        tone: DOMAIN_TONES[label],
        numericValue: value,
      };
    });
  }, [eventSignals, riskState]);

  const compositeRisk = useMemo(() => {
    const values = domains.map((domain) => domain.numericValue / 100);
    const averageRisk = values.reduce((sum, value) => sum + value, 0) / values.length;
    const maxRisk = Math.max(...values);
    return clamp((averageRisk * 0.78 + maxRisk * 0.22) * 100, 1, 99);
  }, [domains]);

  const modelConfidence = useMemo(() => {
    const pulse = Math.sin(confidenceDrift / 3) * 2.5;
    const statePenalty = riskState === 'inferno' || riskState === 'burnt' ? -8 : riskState === 'recovering' ? 4 : 0;
    return Math.round(clamp(78 + pulse + statePenalty, 58, 92));
  }, [confidenceDrift, riskState]);

  return (
    <main className={`viewport state-${riskState}`}>
      <div className="stage">
        <WorldScene
          manifest={manifest}
          region="global"
          timeOfDay={riskState === 'alive' ? localTimeOfDay : 'evening'}
          riskState={riskState}
        />
        <PixelParticles manifest={manifest} riskState={riskState} />
        <DashboardUI
          manifest={manifest}
          manifestError={manifestError}
          riskState={riskState}
          riskStates={RISK_STATES}
          stateLabel={stateLabel}
          onRiskStateChange={setRiskState}
          domains={domains}
          compositeRisk={compositeRisk}
          modelConfidence={modelConfidence}
          nextUpdate={nextUpdate}
          onMockEvent={onMockEvent}
        />
      </div>
    </main>
  );
}
