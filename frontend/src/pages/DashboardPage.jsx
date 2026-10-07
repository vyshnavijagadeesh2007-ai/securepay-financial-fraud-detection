import React from 'react';

export default function DashboardPage({ onNavigate }) {
  return (
    <div className="page dashboard-page">
      <div className="container">
        {/* Page Header */}
        <div className="page-header hairline-b flex-between">
          <div>
            <span className="meta-tag">OPERATIONAL TELEMETRY &middot; STATION 01</span>
            <h1>System Dashboard Overview</h1>
          </div>
          <div className="header-meta-group">
            <span className="accent-tag">PHASE 4 // THRESHOLD CALIBRATION</span>
            <span className="meta-tag">MODEL PIPELINE: IF + LOF READY</span>
          </div>
        </div>

        {/* Phase 4 Integrity Warning Banner */}
        <div className="integrity-banner hairline-all">
          <div className="banner-icon">&sect;</div>
          <div className="banner-text">
            <strong>PHASE 4 CALIBRATION & INTEGRITY STATUS:</strong> Ground-truth transaction counts 
            below reflect the physically verified dataset (<code>data/creditcard.csv</code>). 
            Machine Learning metrics reflect empirical holdout test evaluation (60/20/20 stratified split, 
            <em>N</em> = 56,962 untouched test transactions) under calibrated decision thresholds.
          </div>
        </div>

        {/* Primary Metrics Grid */}
        <div className="metrics-grid hairline-all">
          {/* Row 1: Dataset Ground Truth Metrics (Authentic) */}
          <div className="metric-box hairline-r hairline-b">
            <span className="meta-tag">TOTAL TRANSACTIONS (N)</span>
            <div className="metric-value">284,807</div>
            <span className="metric-subtext">Verified physical CSV observations</span>
          </div>

          <div className="metric-box hairline-r hairline-b">
            <span className="meta-tag">LEGITIMATE TRANSACTIONS (CLASS 0)</span>
            <div className="metric-value">284,315</div>
            <span className="metric-subtext">99.82725% baseline population</span>
          </div>

          <div className="metric-box hairline-b">
            <span className="meta-tag">FRAUD TRANSACTIONS (CLASS 1)</span>
            <div className="metric-value">492</div>
            <span className="metric-subtext">0.17275% minority class (1 : 578 ratio)</span>
          </div>

          {/* Row 2: ML Model Metrics (Phase 4 Calibrated Test Benchmarks) */}
          <div className="metric-box hairline-r hairline-b">
            <span className="meta-tag">CURRENT ACTIVE MODEL</span>
            <div className="metric-value model-name">Isolation Forest</div>
            <span className="metric-subtext">STATUS: <strong style={{ color: 'var(--accent-blue)' }}>MODELS READY</strong></span>
          </div>

          <div className="metric-box hairline-r hairline-b">
            <span className="meta-tag">DETECTED ANOMALIES (TEST SET)</span>
            <div className="metric-value">192</div>
            <span className="metric-subtext">Calibrated holdout test anomalies (TP=29, FP=163)</span>
          </div>

          <div className="metric-box hairline-b">
            <span className="meta-tag">DECISION THRESHOLD</span>
            <div className="metric-value">0.6224</div>
            <span className="metric-subtext">Calibrated validation cutoff (Peak F1)</span>
          </div>

          {/* Row 3: Quantitative Performance Metrics */}
          <div className="metric-box hairline-r">
            <span className="meta-tag">MODEL PRECISION (P)</span>
            <div className="metric-value">15.10%</div>
            <span className="metric-subtext">True Positives / (TP + FP)</span>
          </div>

          <div className="metric-box hairline-r">
            <span className="meta-tag">MODEL RECALL (R)</span>
            <div className="metric-value">29.29%</div>
            <span className="metric-subtext">True Positives / (TP + FN)</span>
          </div>

          <div className="metric-box">
            <span className="meta-tag">F1-SCORE (HARMONIC MEAN)</span>
            <div className="metric-value">0.1993</div>
            <span className="metric-subtext">2 &middot; (P &middot; R) / (P + R)</span>
          </div>
        </div>

        {/* Secondary Details & Directives */}
        <div className="dashboard-subgrid grid-2">
          <div className="info-panel hairline-all">
            <div className="panel-header hairline-b flex-between">
              <h3>Training Strategy Directive</h3>
              <span className="meta-tag">SEMI-SUPERVISED NOVELTY</span>
            </div>
            <div className="panel-body">
              <p>
                The primary model architecture will fit strictly over legitimate transactions (<code>Class == 0</code>),
                learning a non-parametric envelope of normal banking activity. The mixed validation partition
                will subsequently benchmark true fraud isolation rates without biasing tree splits.
              </p>
              <div className="spec-table-container">
                <table className="spec-table">
                  <tbody>
                    <tr>
                      <td className="spec-label">Target Dataset</td>
                      <td className="spec-data">data/creditcard.csv</td>
                    </tr>
                    <tr>
                      <td className="spec-label">Input Features</td>
                      <td className="spec-data">Time, Amount, V1–V28 (30 features)</td>
                    </tr>
                    <tr>
                      <td className="spec-label">Excluded Feature</td>
                      <td className="spec-data">Class (Reserved strictly for evaluation)</td>
                    </tr>
                    <tr>
                      <td className="spec-label">Scaler Normalization</td>
                      <td className="spec-data">RobustScaler (Median / IQR)</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <div className="info-panel hairline-all">
            <div className="panel-header hairline-b flex-between">
              <h3>FastAPI Backend Linkage</h3>
              <span className="meta-tag">PORT 8000 &middot; REST</span>
            </div>
            <div className="panel-body">
              <p>
                The backend service exposes standard Pydantic v2 schemas for real-time inference,
                batch processing, threshold tuning, and exploratory transaction streaming.
              </p>
              <div className="spec-table-container">
                <table className="spec-table">
                  <tbody>
                    <tr>
                      <td className="spec-label">Health Check</td>
                      <td className="spec-data"><code>GET /api/health</code></td>
                    </tr>
                    <tr>
                      <td className="spec-label">Telemetry Summary</td>
                      <td className="spec-data"><code>GET /api/dashboard</code></td>
                    </tr>
                    <tr>
                      <td className="spec-label">Model Benchmarking</td>
                      <td className="spec-data"><code>GET /api/models/comparison</code></td>
                    </tr>
                    <tr>
                      <td className="spec-label">Live Inference</td>
                      <td className="spec-data"><code>POST /api/predict</code></td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div className="panel-action">
                <button 
                  type="button" 
                  onClick={() => onNavigate('detection')} 
                  className="primary-btn"
                >
                  Test Inference Schema &rarr;
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
