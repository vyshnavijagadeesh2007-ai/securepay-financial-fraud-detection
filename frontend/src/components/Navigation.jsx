import React from 'react';

export default function Navigation({ activePage, setActivePage }) {
  const navItems = [
    { id: 'home', label: 'Overview' },
    { id: 'dashboard', label: 'Dashboard' },
    { id: 'detection', label: 'Detection' },
    { id: 'analytics', label: 'Analytics' },
    { id: 'model-lab', label: 'Model Lab' },
    { id: 'threshold', label: 'Threshold' },
    { id: 'explorer', label: 'Explorer' },
    { id: 'methodology', label: 'Methodology' },
  ];

  return (
    <header className="site-header hairline-b">
      {/* Top Technical Metadata Bar */}
      <div className="top-metadata-bar hairline-b">
        <div className="container flex-between">
          <div className="system-status-indicator">
            <span className="status-dot"></span>
            <span className="meta-tag">PHASE 4 // THRESHOLD CALIBRATION</span>
          </div>
          <div className="system-dataset-indicator">
            <span className="meta-tag">
              DATASET: <strong style={{ color: 'var(--ink-primary)' }}>CREDITCARD.CSV (284,807 OBS)</strong> | STATUS: <strong style={{ color: 'var(--accent-blue)' }}>IF + LOF MODELS READY</strong>
            </span>
          </div>
        </div>
      </div>

      {/* Main Masthead & Navigation */}
      <div className="masthead-bar">
        <div className="container masthead-content">
          <div className="brand-group" onClick={() => setActivePage('home')} style={{ cursor: 'pointer' }}>
            <span className="brand-title">SECUREPAY AI.</span>
            <span className="brand-subtitle">FINANCIAL ANOMALY DETECTION INSTRUMENT</span>
          </div>

          <nav className="main-nav" aria-label="Primary Navigation">
            <ul className="nav-list">
              {navItems.map((item) => (
                <li key={item.id} className="nav-item">
                  <button
                    type="button"
                    onClick={() => setActivePage(item.id)}
                    className={`nav-btn ${activePage === item.id ? 'active' : ''}`}
                    aria-current={activePage === item.id ? 'page' : undefined}
                  >
                    {item.label}
                  </button>
                </li>
              ))}
            </ul>
          </nav>
        </div>
      </div>
    </header>
  );
}
