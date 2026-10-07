import React from 'react';

/**
 * Travelling Visual Element:
 * Subtle Transaction Signal / Anomaly Trace representing transaction state
 * advancing across the architectural pipeline stages:
 * HOME → PROBLEM → ANALYTICS → MODEL LAB → THRESHOLD → DETECTION
 */
export default function SignalTrace({ activePage, onNavigate }) {
  const stages = [
    { id: 'home', label: '01. ORIGIN' },
    { id: 'analytics', label: '02. ANALYTICS' },
    { id: 'model-lab', label: '03. MODEL LAB' },
    { id: 'threshold', label: '04. THRESHOLD' },
    { id: 'detection', label: '05. INFERENCE' },
  ];

  // Find index corresponding to current active page or default
  const activeIndex = Math.max(0, stages.findIndex(s => s.id === activePage));

  return (
    <div className="signal-trace-strip" aria-label="System Pipeline Stage Progress">
      <div className="signal-trace-inner">
        <span className="signal-trace-label meta-tag">TRANSACTION PIPELINE TRACE :</span>
        
        <div className="signal-trace-pipeline">
          {stages.map((stage, idx) => {
            const isCurrent = stage.id === activePage;
            const isPassed = idx < activeIndex;

            return (
              <React.Fragment key={stage.id}>
                <button
                  type="button"
                  onClick={() => onNavigate(stage.id)}
                  className={`signal-node-btn ${isCurrent ? 'current' : ''} ${isPassed ? 'passed' : ''}`}
                  aria-current={isCurrent ? 'step' : undefined}
                >
                  <span className="node-marker"></span>
                  <span className="node-text">{stage.label}</span>
                </button>
                {idx < stages.length - 1 && (
                  <div className={`signal-wire ${idx < activeIndex ? 'active-wire' : ''}`}>
                    <span className="wire-pulse"></span>
                  </div>
                )}
              </React.Fragment>
            );
          })}
        </div>
      </div>
    </div>
  );
}
