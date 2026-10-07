import React from 'react';
import SvgWaveform from '../components/SvgWaveform';

export default function HomePage({ onNavigate }) {
  return (
    <div className="page home-page">
      {/* Hero Header */}
      <section className="hero-section hairline-b">
        <div className="container">
          <div className="hero-header-meta">
            <span className="meta-tag">FINANCIAL RISK LABORATORY / MONOGRAPH NO. 01</span>
            <span className="meta-tag">PHASE 4 // THRESHOLD CALIBRATION</span>
          </div>

          <h1 className="hero-heading">
            Real-Time Anomaly Detection in <em className="editorial-italic">High-Frequency</em> Financial Transactions.
          </h1>

          <p className="hero-subtext">
            A scholarly instrument engineered to isolate fraudulent behavior within extreme 
            class imbalance regimes (<strong>0.173% positive prevalence</strong>). Unsupervised 
            isolation tree partitioning and local density analysis calibrated over 
            verified cardholder telemetry.
          </p>

          <SvgWaveform height={84} className="hero-waveform" />

          {/* Action CTAs */}
          <div className="hero-cta-group">
            <button 
              type="button" 
              onClick={() => onNavigate('detection')}
              className="primary-btn"
            >
              Enter Detection Console &rarr;
            </button>
            <button 
              type="button" 
              onClick={() => onNavigate('analytics')}
              className="secondary-btn"
            >
              Inspect Dataset Analytics &rarr;
            </button>
            <button 
              type="button" 
              onClick={() => onNavigate('methodology')}
              className="secondary-btn"
            >
              Read Technical Monograph &rarr;
            </button>
          </div>
        </div>
      </section>

      {/* Three Pillars / Station Overview */}
      <section className="pillars-section hairline-b">
        <div className="container grid-3">
          <div className="pillar-card hairline-r">
            <span className="accent-tag">PILLAR 01 // DATA HYGIENE</span>
            <h3>Empirical Baseline & RobustScaler</h3>
            <p>
              Creditcard transaction amounts span from $0.00 to $25,691.16 with severe right-skewness.
              RobustScaler utilizes median and interquartile range (IQR), immune to distortion from extreme outliers.
            </p>
            <div className="card-footer">
              <span className="meta-tag">INPUT: 284,807 SAMPLES &middot; 31 ATTRIBUTES</span>
            </div>
          </div>

          <div className="pillar-card hairline-r">
            <span className="accent-tag">PILLAR 02 // UNSUPERVISED NOVELTY</span>
            <h3>Normal Behavior Baseline (Class == 0)</h3>
            <p>
              Rather than training on noisy, sparse fraudulent instances, the core engine models
              the mathematical manifold of legitimate transactions to detect foreign deviations.
            </p>
            <div className="card-footer">
              <span className="meta-tag">MODELS: ISOLATION FOREST & LOF</span>
            </div>
          </div>

          <div className="pillar-card">
            <span className="accent-tag">PILLAR 03 // RIGOROUS BENCHMARKING</span>
            <h3>Precision-Recall Calibration</h3>
            <p>
              Standard classification accuracy is mathematically invalid under 578:1 imbalance.
              Optimization targets minority Precision, Recall, and continuous score thresholds.
            </p>
            <div className="card-footer">
              <span className="meta-tag">OBJECTIVE: MAXIMUM F1 & PR-AUC</span>
            </div>
          </div>
        </div>
      </section>

      {/* Conceptual System Pipeline Flow */}
      <section className="pipeline-flow-section">
        <div className="container">
          <div className="section-header flex-between">
            <div>
              <span className="meta-tag">ARCHITECTURAL DATA PIPELINE</span>
              <h2>End-to-End System Topology</h2>
            </div>
            <span className="meta-tag">[PHASE 4 PRODUCTION TOPOLOGY]</span>
          </div>

          <div className="flow-diagram-grid hairline-all">
            <div className="flow-step hairline-r">
              <span className="step-num">01</span>
              <h4>Source Telemetry</h4>
              <p>data/creditcard.csv raw ingestion. Zero synthetic samples. Class strictly reserved.</p>
              <span className="status-badge verified">VERIFIED (284K OBS)</span>
            </div>
            <div className="flow-step hairline-r">
              <span className="step-num">02</span>
              <h4>Robust Scaling</h4>
              <p>Median / IQR normalization for Time & Amount. Preserves orthogonal PCA features.</p>
              <span className="status-badge verified">PHASE 1 COMPLETE</span>
            </div>
            <div className="flow-step hairline-r">
              <span className="step-num">03</span>
              <h4>Novelty Modeling</h4>
              <p>Train Isolation Forest & LOF on Class == 0 legitimate baseline manifold.</p>
              <span className="status-badge verified">PHASE 2 & 3 TRAINED</span>
            </div>
            <div className="flow-step">
              <span className="step-num">04</span>
              <h4>REST API Serving</h4>
              <p>FastAPI endpoint exposing real-time transaction scoring and threshold tuning.</p>
              <span className="status-badge verified">PHASE 4 CALIBRATED</span>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
