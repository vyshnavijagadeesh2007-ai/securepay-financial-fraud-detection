import React, { useState } from 'react';

export default function ThresholdPage() {
  const [selectedCostScenario, setSelectedCostScenario] = useState(0);

  const contaminationExperiments = [
    { contamination: '0.0010', anomalies: 358, precision: '20.67%', recall: '15.04%', f1: '0.1741', fp: 284, latency: '9.68s' },
    { contamination: '0.0020', anomalies: 701, precision: '18.40%', recall: '26.22%', f1: '0.2163', fp: 572, latency: '9.46s', isOptimal: true },
    { contamination: '0.0050', anomalies: 1684, precision: '12.95%', recall: '44.31%', f1: '0.2004', fp: 1466, latency: '9.35s' },
    { contamination: '0.0100', anomalies: 3205, precision: '9.36%', recall: '60.98%', f1: '0.1623', fp: 2905, latency: '9.39s' },
    { contamination: '0.0200', anomalies: 6125, precision: '5.94%', recall: '73.98%', f1: '0.1100', fp: 5761, latency: '9.30s' },
    { contamination: '0.0300', anomalies: 9012, precision: '4.47%', recall: '81.91%', f1: '0.0848', fp: 8609, latency: '12.32s' },
    { contamination: '0.0500', anomalies: 14773, precision: '2.83%', recall: '84.96%', f1: '0.0548', fp: 14355, latency: '21.86s' }
  ];

  const operatingPoints = [
    {
      model: 'Isolation Forest',
      mode: 'Low False Alarm',
      threshold: '0.6722',
      precision: '25.42%',
      recall: '15.15%',
      f1: '0.1899',
      fpr: '0.077%',
      fp: 44,
      desc: 'Minimizes cardholder insult. Ideal for automated transaction decline.'
    },
    {
      model: 'Isolation Forest',
      mode: 'Balanced (Peak F1)',
      threshold: '0.6224',
      precision: '15.10%',
      recall: '29.29%',
      f1: '0.1993',
      fpr: '0.287%',
      fp: 163,
      desc: 'Harmonizes precision and recall on holdout test partition.'
    },
    {
      model: 'Isolation Forest',
      mode: 'Controlled Low FPR',
      threshold: '0.634134',
      precision: '16.55%',
      recall: '24.24%',
      f1: '0.1967',
      fpr: '0.213%',
      fp: 121,
      desc: 'Enforces strict upper bound (FPR <= 0.25%) for high-volume gateways.'
    },
    {
      model: 'Isolation Forest',
      mode: 'High Recall',
      threshold: '0.5240',
      precision: '4.96%',
      recall: '77.78%',
      f1: '0.0933',
      fpr: '2.592%',
      fp: 1474,
      desc: 'High fraud capture (77/99); generates 1,474 reviews for step-up verification.'
    },
    {
      model: 'Local Outlier Factor',
      mode: 'Low False Alarm',
      threshold: '3.0334',
      precision: '30.77%',
      recall: '32.32%',
      f1: '0.3153',
      fpr: '0.127%',
      fp: 72,
      desc: 'Restricts LOF false alarms to 72 alerts while catching 32.3% of fraud cases.'
    },
    {
      model: 'Local Outlier Factor',
      mode: 'Balanced (Peak F1)',
      threshold: '2.4901',
      precision: '24.68%',
      recall: '57.58%',
      f1: '0.3455',
      fpr: '0.306%',
      fp: 174,
      desc: 'Highest balanced performance (F1=0.3455, Recall=57.6%) across all models.'
    },
    {
      model: 'Local Outlier Factor',
      mode: 'Controlled Low FPR',
      threshold: '2.707283',
      precision: '30.72%',
      recall: '51.52%',
      f1: '0.3849',
      fpr: '0.202%',
      fp: 115,
      desc: 'Enforces strict upper bound (FPR <= 0.25%). Catches 51/99 frauds with 115 FPs.'
    },
    {
      model: 'Local Outlier Factor',
      mode: 'High Recall',
      threshold: '1.9639',
      precision: '13.11%',
      recall: '81.82%',
      f1: '0.2259',
      fpr: '0.944%',
      fp: 537,
      desc: 'Captures 81 of 99 test fraud attacks (81.8% recall) with 537 manual reviews.'
    }
  ];

  const costScenarios = [
    {
      name: 'Balanced Operational Cost (1:10)',
      costFp: 1.0,
      costFn: 10.0,
      iforestThresh: '0.6224',
      iforestCost: '863.0',
      iforestFp: 163,
      iforestFn: 70,
      lofThresh: '2.3705',
      lofCost: '543.0',
      lofFp: 223,
      lofFn: 32,
      desc: 'False negative penalty is 10x false positive review cost. LOF achieves lower total cost (543 vs 863).'
    },
    {
      name: 'High Loss Asymmetry (1:20)',
      costFp: 1.0,
      costFn: 20.0,
      iforestThresh: '0.6111',
      iforestCost: '1,588.0',
      iforestFp: 228,
      iforestFn: 68,
      lofThresh: '2.2162',
      lofCost: '856.0',
      lofFp: 296,
      lofFn: 28,
      desc: 'False negative penalty is 20x. LOF strongly favored due to superior fraud capture (71.7% recall).'
    },
    {
      name: 'Severe Fraud Penalty (1:50)',
      costFp: 1.0,
      costFn: 50.0,
      iforestThresh: '0.5607',
      iforestCost: '2,380.0',
      iforestFp: 780,
      iforestFn: 32,
      lofThresh: '1.9191',
      lofCost: '1,466.0',
      lofFp: 616,
      lofFn: 17,
      desc: 'Extreme fraud penalty forces low thresholds. LOF catches 82.8% of frauds while capping reviews.'
    }
  ];

  const activeScenario = costScenarios[selectedCostScenario];

  return (
    <div className="page threshold-page">
      <div className="container">
        {/* Page Header */}
        <div className="page-header hairline-b flex-between">
          <div>
            <span className="meta-tag">CALIBRATION & TRADEOFF ANALYSIS &middot; STATION 04</span>
            <h1>Threshold Calibration & Operating Points</h1>
          </div>
          <div className="header-meta-group">
            <span className="meta-tag">OBJECTIVE: PRECISION-RECALL OPTIMIZATION</span>
          </div>
        </div>

        {/* Fundamental Distinction Card */}
        <div className="content-card hairline-all" style={{ marginTop: '24px' }}>
          <div className="panel-header hairline-b flex-between">
            <h3>Conceptual Boundary Distinction</h3>
            <span className="meta-tag">MATHEMATICAL FORMULATION</span>
          </div>
          <div className="panel-body grid-2">
            <div className="concept-box hairline-r" style={{ paddingRight: '20px' }}>
              <span className="accent-tag">CONCEPT A // CONTAMINATION PARAMETER (c)</span>
              <h4>Prior Manifold Assumption</h4>
              <p>
                <strong>Contamination</strong> is a training hyperparameter that defines the expected proportion 
                of anomalous samples in the training/fitting population. In scikit-learn, it sets the default offset 
                for separating normal and anomalous observations during fitting:
              </p>
              <div className="formula-box hairline-all">
                <code>c = N_fraud / N_total &asymp; 492 / 284,807 &asymp; 0.001728</code>
              </div>
            </div>

            <div className="concept-box" style={{ paddingLeft: '20px' }}>
              <span className="accent-tag">CONCEPT B // ANOMALY SCORE THRESHOLD (&tau;)</span>
              <h4>Operational Decision Cutoff</h4>
              <p>
                <strong>Decision Threshold (&tau;)</strong> is a post-training operational cutoff applied to the 
                continuous score function s(x). In banking production, compliance officers tune &tau; dynamically 
                to prioritize either:
              </p>
              <ul className="spec-list">
                <li><strong>High Recall Mode:</strong> Flagging suspicious events even at the cost of higher False Positives.</li>
                <li><strong>High Precision Mode:</strong> Minimizing false alarms to avoid cardholder friction.</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Phase 4 Calibrated Operating Points */}
        <div className="content-card hairline-all" style={{ marginTop: '24px' }}>
          <div className="panel-header hairline-b flex-between">
            <div>
              <h3>Calibrated Operating Points (Holdout Test N=56,962 &middot; 99 Frauds)</h3>
              <p style={{ margin: '4px 0 0', fontSize: '13px', color: 'var(--ink-secondary)' }}>
                Selected strictly on 20% validation split (N=56,961); evaluated once on untouched test partition.
              </p>
            </div>
            <span className="meta-tag">PHASE 4 OPERATIONAL CUTOFFS</span>
          </div>
          <div className="table-responsive">
            <table className="comparison-table">
              <thead>
                <tr>
                  <th>Model</th>
                  <th>Operating Mode</th>
                  <th>Threshold (&tau;)</th>
                  <th>Precision</th>
                  <th>Recall</th>
                  <th>F1-Score</th>
                  <th>FPR</th>
                  <th>False Alarms (FP)</th>
                  <th>Strategic Profile</th>
                </tr>
              </thead>
              <tbody>
                {operatingPoints.map((pt, idx) => (
                  <tr key={`${pt.model}-${pt.mode}-${idx}`}>
                    <td><strong>{pt.model}</strong></td>
                    <td>{pt.mode}</td>
                    <td><code>&tau; = {pt.threshold}</code></td>
                    <td>{pt.precision}</td>
                    <td><strong>{pt.recall}</strong></td>
                    <td>{pt.f1}</td>
                    <td>{pt.fpr}</td>
                    <td><span className="badge-alert">{pt.fp}</span></td>
                    <td style={{ fontSize: '12px', color: 'var(--ink-secondary)' }}>{pt.desc}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Business Cost Analysis */}
        <div className="content-card hairline-all" style={{ marginTop: '24px' }}>
          <div className="panel-header hairline-b flex-between">
            <div>
              <h3>Business Cost Optimization & Sensitivity</h3>
              <p style={{ margin: '4px 0 0', fontSize: '13px', color: 'var(--ink-secondary)' }}>
                Configurable loss function: Total Cost = FP &times; Cost_FP + FN &times; Cost_FN
              </p>
            </div>
            <div className="model-toggle-group">
              {costScenarios.map((sc, idx) => (
                <button
                  key={sc.name}
                  type="button"
                  className={`model-btn ${selectedCostScenario === idx ? 'active' : ''}`}
                  onClick={() => setSelectedCostScenario(idx)}
                >
                  {idx === 0 ? 'Ratio 1:10' : idx === 1 ? 'Ratio 1:20' : 'Ratio 1:50'}
                </button>
              ))}
            </div>
          </div>
          
          <div className="panel-body">
            <div className="advisory-box" style={{ marginBottom: '16px' }}>
              <span className="accent-tag">MODELING ASSUMPTION DISCLAIMER</span>
              <p style={{ margin: '4px 0 0', fontSize: '12px' }}>
                Cost parameters (FP=$1, FN=$10, $20, $50) are illustrative modeling assumptions for operational sensitivity analysis, 
                not proprietary SecurePay financial figures.
              </p>
            </div>

            <div className="grid-2" style={{ gap: '20px' }}>
              <div className="metric-box hairline-all" style={{ padding: '16px' }}>
                <span className="meta-tag">ISOLATION FOREST COST PROFILE</span>
                <h4 style={{ margin: '8px 0 4px' }}>Optimal Threshold: &tau; = {activeScenario.iforestThresh}</h4>
                <div style={{ fontSize: '24px', fontWeight: 'bold', color: 'var(--ink-primary)' }}>
                  Total Cost: {activeScenario.iforestCost}
                </div>
                <div style={{ fontSize: '12px', color: 'var(--ink-secondary)', marginTop: '6px' }}>
                  Resulting Test Load: {activeScenario.iforestFp} False Alarms, {activeScenario.iforestFn} Missed Frauds
                </div>
              </div>

              <div className="metric-box hairline-all" style={{ padding: '16px' }}>
                <span className="meta-tag">LOCAL OUTLIER FACTOR COST PROFILE</span>
                <h4 style={{ margin: '8px 0 4px' }}>Optimal Threshold: &tau; = {activeScenario.lofThresh}</h4>
                <div style={{ fontSize: '24px', fontWeight: 'bold', color: 'var(--accent-blue)' }}>
                  Total Cost: {activeScenario.lofCost}
                </div>
                <div style={{ fontSize: '12px', color: 'var(--ink-secondary)', marginTop: '6px' }}>
                  Resulting Test Load: {activeScenario.lofFp} False Alarms, {activeScenario.lofFn} Missed Frauds
                </div>
              </div>
            </div>
            
            <p style={{ marginTop: '16px', fontSize: '13px', color: 'var(--ink-secondary)' }}>
              {activeScenario.desc}
            </p>
          </div>
        </div>

        {/* Empirical Contamination Grid Experiments */}
        <div className="content-card hairline-all" style={{ marginTop: '24px' }}>
          <div className="panel-header hairline-b flex-between">
            <h3>Contamination Parameter Sensitivity Grid (Isolation Forest Baseline)</h3>
            <span className="meta-tag">MEASURED EMPIRICAL EXPERIMENTS</span>
          </div>
          <div className="table-responsive">
            <table className="comparison-table">
              <thead>
                <tr>
                  <th>Contamination (c)</th>
                  <th>Detected Anomalies</th>
                  <th>Precision (P)</th>
                  <th>Recall (R)</th>
                  <th>F1-Score</th>
                  <th>False Positives</th>
                  <th>Full-Dataset Experiment Runtime</th>
                  <th>Calibration Status</th>
                </tr>
              </thead>
              <tbody>
                {contaminationExperiments.map((exp) => (
                  <tr key={exp.contamination}>
                    <td><code>c = {exp.contamination}</code></td>
                    <td>{exp.anomalies.toLocaleString()}</td>
                    <td>{exp.precision}</td>
                    <td><strong>{exp.recall}</strong></td>
                    <td>{exp.f1}</td>
                    <td><span className="badge-alert">{exp.fp.toLocaleString()}</span></td>
                    <td>{exp.latency}</td>
                    <td>
                      <span className="status-badge" style={{ borderColor: 'var(--accent-blue)', color: 'var(--accent-blue)' }}>
                        {exp.isOptimal ? 'OPTIMAL F1' : 'MEASURED'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
