import { useEffect, useMemo, useRef, useState } from 'react';

const EVENT_POOL = {
  alive: [
    ['AI / TECH', 'Safety consortium publishes alignment benchmark update', -0.9],
    ['CLIMATE', 'Grid storage deployment lowers regional outage risk', -0.7],
    ['GEOPOLITICAL', 'Back-channel talks resume between rival blocs', -0.6],
    ['BIOSECURITY', 'Wastewater surveillance shows no unusual pathogen signal', -0.5],
    ['NUCLEAR', 'Arms-control inspection window completed without incident', -0.8],
  ],
  warming: [
    ['CLIMATE', 'Heat dome forecast expands across multiple population centers', 1.2],
    ['GEOPOLITICAL', 'Fuel and food price protests disrupt capital districts', 0.9],
    ['AI / TECH', 'Autonomous cyber incident reported by infrastructure operator', 0.8],
    ['NUCLEAR', 'Missile exercise notice raises regional alert posture', 0.7],
    ['BIOSECURITY', 'Hospital syndromic reports show early anomaly cluster', 0.6],
  ],
  burning: [
    ['NUCLEAR', 'Missile test near contested border sparks diplomatic protest', 1.4],
    ['CLIMATE', 'Heatwave intensity breaks regional records across three continents', 1.5],
    ['GEOPOLITICAL', 'Emergency summit convenes after cross-border strike', 1.3],
    ['AI / TECH', 'Cyberattack disrupts government services in multiple regions', 1.2],
    ['BIOSECURITY', 'New pathogen strain identified with increased transmission potential', 1.1],
  ],
  inferno: [
    ['NUCLEAR', 'Strategic forces placed on elevated readiness by two states', 1.9],
    ['GEOPOLITICAL', 'Maritime exclusion zone declared near contested corridor', 1.6],
    ['CLIMATE', 'Compound firestorm overwhelms emergency response capacity', 1.8],
    ['AI / TECH', 'Critical infrastructure AI rollback fails across grid nodes', 1.5],
    ['BIOSECURITY', 'Containment perimeter breached at emergency quarantine site', 1.4],
  ],
  burnt: [
    ['GEOPOLITICAL', 'Multiple command centers report communications blackout', 2.1],
    ['CLIMATE', 'Satellite heat signatures show expanding urban fire fronts', 2.2],
    ['NUCLEAR', 'Unconfirmed detonation alert triggers automated shelter orders', 2],
    ['AI / TECH', 'Autonomous defense network enters degraded-control mode', 1.8],
    ['BIOSECURITY', 'Field clinics report collapse of regional testing capacity', 1.7],
  ],
  recovering: [
    ['CLIMATE', 'Rainfall suppresses active fire zones across western corridor', -1.4],
    ['GEOPOLITICAL', 'Ceasefire observers confirm first stable quiet window', -1.2],
    ['BIOSECURITY', 'Transmission estimates decline for third consecutive update', -1.1],
    ['AI / TECH', 'Manual control restored to affected infrastructure nodes', -1],
    ['NUCLEAR', 'Hotline exchange confirms de-escalation protocol remains active', -1.3],
  ],
};

const TAG_CLASS = {
  'AI / TECH': 'tag-ai',
  BIOSECURITY: 'tag-bio',
  CLIMATE: 'tag-climate',
  GEOPOLITICAL: 'tag-geo',
  NUCLEAR: 'tag-nuclear',
};
const TAG_LABEL = {
  'AI / TECH': 'AI / TECH',
  BIOSECURITY: 'BIOSECURITY',
  CLIMATE: 'CLIMATE',
  GEOPOLITICAL: 'GEOPOLITICAL',
  NUCLEAR: 'NUCLEAR',
};

function formatUtcTime(date) {
  return date.toLocaleTimeString('en-GB', {
    hour: '2-digit',
    minute: '2-digit',
    timeZone: 'UTC',
  });
}

function buildEvent(state, cursor, date = new Date()) {
  const pool = EVENT_POOL[state] ?? EVENT_POOL.alive;
  const [tag, text, impact] = pool[cursor % pool.length];
  return {
    id: `${date.getTime()}-${cursor}`,
    tag,
    impact,
    text,
    time: `${formatUtcTime(date)} UTC`,
  };
}

export default function EventFeed({ onMockEvent, riskState }) {
  const feedScrollRef = useRef(null);
  const initialEvents = useMemo(
    () =>
      Array.from({ length: 7 }, (_, index) =>
        buildEvent(riskState, index, new Date(Date.now() - (6 - index) * 6 * 60 * 1000)),
      ),
    [riskState],
  );
  const [cursor, setCursor] = useState(7);
  const [events, setEvents] = useState(initialEvents);

  useEffect(() => {
    setCursor(7);
    setEvents(initialEvents);
  }, [initialEvents]);

  useEffect(() => {
    const timer = window.setInterval(() => {
      setCursor((current) => {
        const event = buildEvent(riskState, current);
        onMockEvent?.(event);
        setEvents((eventsNow) => [...eventsNow, event].slice(-12));
        return current + 1;
      });
    }, 3200);

    return () => window.clearInterval(timer);
  }, [onMockEvent, riskState]);

  useEffect(() => {
    const node = feedScrollRef.current;
    if (!node) return;
    node.scrollTo({
      top: node.scrollHeight,
      behavior: 'smooth',
    });
  }, [events]);

  return (
    <aside className="event-feed panel">
      <div className="feed-title">
        <span>LIVE EVENT FEED</span>
        <i />
      </div>
      <div className="feed-scroll" ref={feedScrollRef}>
        <div className="feed-list">
          {events.map((event, index) => (
            <article className={`feed-item ${index === events.length - 1 ? 'is-new' : ''}`} key={event.id}>
              <time>{event.time}</time>
              <div>
                <p>{event.text}</p>
                <strong className={TAG_CLASS[event.tag] ?? ''}><i />{TAG_LABEL[event.tag] ?? event.tag}</strong>
              </div>
            </article>
          ))}
        </div>
      </div>
      <button type="button" className="view-events">VIEW ALL EVENTS →</button>
    </aside>
  );
}
