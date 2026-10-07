import React, { useState } from 'react';

export default function ModelLabPage({ onNavigate }) {
  const [selectedModel, setSelectedModel] = useState('Isolation Forest');

  const iforestOperatingPoints = [
    {
      mode: 'Low False Alarm',
      threshold: '0.6722',
      precision: '25.42%',
      recall: '15.15%',
      f1: '0.1899',
      fpr: '0.077%',
      tp: 15,
      fp: 44,
      desc: 'High Precision / Low Insult. Strict cutoff to minimize cardholder friction. Automated block candidate.'
    },
    {
      mode: 'Balanced (Peak F1)',
      threshold: '0.6224',
      precision: '15.10%',
      recall: '29.29%',
      f1: '0.1993',
      fpr: '0.287%',
      tp: 29,
      fp: 163,
      desc: 'Optimal F1 balance calibrated on validation partition. Standard automated triage cutoff.'
    },
    {
      mode: 'Controlled Low FPR',
      threshold: '0.634134',
      precision: '16.55%',
      recall: '24.24%',
      f1: '0.1967',
      fpr: '0.213%',
      tp: 24,
      fp: 121,
      desc: 'Enforces strict upper bound (FPR <= 0.25%) to preserve customer experience SLAs.'
    },
    {
      mode: 'High Recall',
      threshold: '0.5240',
      precision: '4.96%',
      recall: '77.78%',
      f1: '0.0933',
      fpr: '2.592%',
      tp: 77,
      fp: 1474,
      desc: 'Aggressive fraud interception (captures 78/99 frauds). Heavy review load; ideal for soft friction (SMS OTP).'
    }
  ];

  const lofOperatingPoints = [
    {
      mode: 'Low False Alarm',
      threshold: '3.0334',
      precision: '30.77%',
      recall: '32.32%',
      f1: '0.3153',
      fpr: '0.127%',
      tp: 32,
      fp: 72,
      desc: 'High Precision cutoff. Constrains false alerts to 72 while capturing 32% of fraud attacks.'
    },
    {
      mode: 'Balanced (Peak F1)',
      threshold: '2.4901',
      precision: '24.68%',
      recall: '57.58%',
      f1: '0.3455',
      fpr: '0.306%',
      tp: 57,
      fp: 174,
      desc: 'Highest balanced F1 across all models (F1=0.3455) with 57.6% recall and 174 false alarms.'
    },
    {
      mode: 'Controlled Low FPR',
      threshold: '2.707283',
      precision: '30.72%',
      recall: '51.52%',
      f1: '0.3849',
      fpr: '0.202%',
      tp: 51,
      fp: 115,
      desc: 'Enforces strict upper bound (FPR <= 0.25%). Outstanding efficiency: 51.5% recall at only 115 false alarms.'
    },
    {
      mode: 'High Recall',
      threshold: '1.9639',
      precision: '13.11%',
      recall: '81.82%',
      f1: '0.2259',
      fpr: '0.944%',
      tp: 81,
      fp: 537,
      desc: 'Maximum fraud capture: intercepts 81 of 99 holdout fraud cases (81.8% recall) with 537 manual reviews.'
    }
  ];

  const activePoints = selectedModel === 'Isolation Forest' ? iforestOperatingPoints : lofOperatingPoints;

  return (
    <div className="page model-lab-page">
      <div className="container">
        {/* Page Header */}
        <div className="page-header hairline-b flex-between">
          <div>
            <span className="meta-tag">BENCHMARK EXPERIMENTS &middot; STATION 03</span>
            <h1>Model Lab & Algorithmic Comparison</h1>
          </div>
          <div className="header-meta-group">
            <span className="meta-tag">PARADIGMS: ISOLATION FOREST vs LOCAL OUTLIER FACTOR</span>
          </div>
        </div>

        {/* Empirical Benchmark Matrix Notice */}
        <div className="integrity-banner hairline-all">
          <div className="banner-icon">&sect;</div>
          <div className="banner-text">
            <strong>EMPIRICAL BENCHMARK & AUDIT STATUS:</strong> Phase 2 (Isolation Forest), Phase 3 (Local Outlier Factor), and the 
            Methodological Holdout Audit (60/20/20 Stratified Split) are complete. Metrics reflect authentic performance across 30 canonical features 
            with zero label leakage. Both Historical Baselines and Holdout Test metrics are validated and ready for Phase 4 threshold calibration.
          </div>
        </div>

        {/* Comparison Table */}
        <div className="content-card hairline-all" style={{ marginTop: '24px' }}>
          <div className="panel-header hairline-b flex-between">
            <h3>Empirical Comparison Matrix</h3>
            <span className="meta-tag">BENCHMARK MATRIX</span>
          </div>
          <div className="table-responsive">
            <table className="comparison-table">
              <thead>
                <tr>
                  <th>Algorithm</th>
                  <th>Mathematical Mechanism</th>
                  <th>Precision (P)</th>
                  <th>Recall (R)</th>
                  <th>F1-Score</th>
                  <th>False Positives</th>
                  <th>False Negatives</th>
                  <th>PR-AUC</th>
                  <th>Holdout Test Scoring Time</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>
                    <strong>Isolation Forest</strong>
                  </td>
                  <td>Recursive Space Partitioning (Tree Depth)</td>
                  <td>16.55%</td>
                  <td>24.24%</td>
                  <td><strong>0.1967</strong></td>
                  <td>121</td>
                  <td>75</td>
                  <td>0.108084</td>
                  <td>~1.01 s (56,962 transactions)</td>
                  <td>
                    <span className="status-badge" style={{ borderColor: 'var(--accent-blue)', color: 'var(--accent-blue)' }}>
                      READY
                    </span>
                  </td>
                </tr>
                <tr>
                  <td>
                    <strong>Local Outlier Factor (LOF)</strong>
                  </td>
                  <td>Local Reachability Density (k-NN, k=50)</td>
                  <td>30.72%</td>
                  <td>51.52%</td>
                  <td>0.3849</td>
                  <td>115</td>
                  <td>48</td>
                  <td>0.218608</td>
                  <td>~11.36 s (56,962 transactions)</td>
                  <td>
                    <span className="status-badge" style={{ borderColor: 'var(--accent-blue)', color: 'var(--accent-blue)' }}>
                      READY
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        {/* Phase 4 Calibrated Operating Points Section */}
        <div className="content-card hairline-all" style={{ marginTop: '24px' }}>
          <div className="panel-header hairline-b flex-between">
            <div>
              <h3>Phase 4 Calibrated Operating Points (Holdout Test N=56,962 &middot; 99 Frauds)</h3>
              <p style={{ margin: '4px 0 0', fontSize: '13px', color: 'var(--ink-secondary)' }}>
                Thresholds selected strictly on 20% validation partition; evaluated once on untouched test partition.
              </p>
            </div>
            <div className="model-toggle-group">
              <button
                type="button"
                className={`model-btn ${selectedModel === 'Isolation Forest' ? 'active' : ''}`}
                onClick={() => setSelectedModel('Isolation Forest')}
              >
                Isolation Forest
              </button>
              <button
                type="button"
                className={`model-btn ${selectedModel === 'Local Outlier Factor' ? 'active' : ''}`}
                onClick={() => setSelectedModel('Local Outlier Factor')}
              >
                Local Outlier Factor
              </button>
            </div>
          </div>
          
          <div className="table-responsive">
            <table className="comparison-table">
              <thead>
                <tr>
                  <th>Operating Mode</th>
                  <th>Threshold (&tau;)</th>
                  <th>Precision</th>
                  <th>Recall</th>
                  <th>F1-Score</th>
                  <th>FPR</th>
                  <th>True Positives (TP)</th>
                  <th>False Alarms (FP)</th>
                  <th>Operational Description</th>
                </tr>
              </thead>
              <tbody>
                {activePoints.map((pt) => (
                  <tr key={pt.mode}>
                    <td><strong>{pt.mode}</strong></td>
                    <td><code>&tau; = {pt.threshold}</code></td>
                    <td>{pt.precision}</td>
                    <td><strong>{pt.recall}</strong></td>
                    <td>{pt.f1}</td>
                    <td>{pt.fpr}</td>
                    <td>{pt.tp} / 99</td>
                    <td><span className="badge-alert">{pt.fp}</span></td>
                    <td style={{ fontSize: '12px', color: 'var(--ink-secondary)' }}>{pt.desc}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="panel-body hairline-t" style={{ backgroundColor: 'var(--surface-subtle)', padding: '16px 20px' }}>
            <div className="flex-between" style={{ alignItems: 'flex-start', gap: '20px' }}>
              <div>
                <span className="accent-tag">OPERATIONAL TRADE-OFF DYNAMICS</span>
                <p style={{ margin: '6px 0 0', fontSize: '13px', lineHeight: '1.6', color: 'var(--ink-primary)' }}>
                  Changing the operating point shifts the balance between <strong>Fraud Detection Sensitivity (Recall)</strong> and 
                  <strong> False-Alert Investigation Burden (FPR / FPs)</strong>. High Recall captures up to 81.8% of attacks but increases manual reviews; 
                  Low False Alarm constrains false alarms to under 75 alerts for automated blocking.
                </p>
              </div>
              <div style={{ minWidth: '220px', textAlign: 'right' }}>
                <span className="meta-tag">TEST PR-AUC</span>
                <div style={{ fontSize: '20px', fontWeight: 'bold', color: 'var(--ink-primary)', marginTop: '4px' }}>
                  {selectedModel === 'Isolation Forest' ? '0.1081 (62x baseline)' : '0.2186 (126x baseline)'}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Deep Dive Cards: Algorithm Mechanics */}
        <div className="analytics-grid grid-2" style={{ marginTop: '24px' }}>
          {/* Isolation Forest */}
          <div className="content-card hairline-all">
            <div className="panel-header hairline-b flex-between">
              <h3>Isolation Forest (iForest)</h3>
              <span className="meta-tag">O(n log n) &middot; TREE ENSEMBLE</span>
            </div>
            <div className="panel-body">
              <p>
                <strong>Principle:</strong> Anomalies are &ldquo;few and different,&rdquo; rendering them susceptible 
                to premature isolation in random recursive space partitioning.
              </p>
              <ul className="spec-list">
                <li>
                  <strong>Splitting Rule:</strong> Chooses a random feature and a random split value between minimum and maximum.
                </li>
                <li>
                  <strong>Path Length $h(x)$:</strong> Shorter average tree depth implies higher likelihood of anomaly status.
                </li>
                <li>
                  <strong>Holdout Batch Scoring:</strong> Approximately 1.01 seconds for 56,962 test transactions; this is not a single-request API latency measure.
                </li>
              </ul>
            </div>
          </div>

          {/* Local Outlier Factor */}
          <div className="content-card hairline-all">
            <div className="panel-header hairline-b flex-between">
              <h3>Local Outlier Factor (LOF)</h3>
              <span className="meta-tag">O(n&sup2;) &middot; DENSITY-BASED</span>
            </div>
            <div className="panel-body">
              <p>
                <strong>Principle:</strong> Computes the local density of an observation relative to its $k$-nearest neighbors.
              </p>
              <ul className="spec-list">
                <li>
                  <strong>Local Reachability:</strong> Detects outliers in non-uniform density clusters where global distance metrics fail.
                </li>
                <li>
                  <strong>Novelty Mode:</strong> Configured with <code>novelty=True</code> to permit out-of-sample inference on streaming transactions.
                </li>
                <li>
                  <strong>Latency Trade-off:</strong> Substantially higher memory footprint and computational overhead due to nearest neighbor searches.
                </li>
              </ul>
            </div>
          </div>
        </div>

        {/* Navigation CTAs */}
        <div className="hero-cta-group" style={{ marginTop: '24px' }}>
          <button 
            type="button" 
            onClick={() => onNavigate && onNavigate('threshold')} 
            className="primary-btn"
          >
            Proceed to Threshold Calibration &rarr;
          </button>
          <button 
            type="button" 
            onClick={() => onNavigate && onNavigate('detection')} 
            className="secondary-btn"
          >
            Open Detection Console &rarr;
          </button>
        </div>
      </div>
    </div>
  );
}
