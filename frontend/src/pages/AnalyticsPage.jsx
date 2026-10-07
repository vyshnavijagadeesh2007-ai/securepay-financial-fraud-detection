import React from 'react';

export default function AnalyticsPage() {
  return (
    <div className="page analytics-page">
      <div className="container">
        {/* Page Header */}
        <div className="page-header hairline-b flex-between">
          <div>
            <span className="meta-tag">EXPLORATORY TELEMETRY &middot; STATION 02</span>
            <h1>Dataset Analytics & Empirical Profile</h1>
          </div>
          <div className="header-meta-group">
            <span className="meta-tag">SOURCE: DATA/CREDITCARD.CSV (VERIFIED)</span>
          </div>
        </div>

        {/* Overview Stats Row */}
        <div className="stats-strip hairline-all">
          <div className="stat-item hairline-r">
            <span className="meta-tag">OBSERVATIONS (N)</span>
            <div className="stat-number">284,807</div>
          </div>
          <div className="stat-item hairline-r">
            <span className="meta-tag">DIMENSIONALITY</span>
            <div className="stat-number">31 Features</div>
          </div>
          <div className="stat-item hairline-r">
            <span className="meta-tag">MISSING VALUES</span>
            <div className="stat-number">0 (100% Complete)</div>
          </div>
          <div className="stat-item hairline-r">
            <span className="meta-tag">DUPLICATE ROWS</span>
            <div className="stat-number">1,081 Audited</div>
          </div>
          <div className="stat-item">
            <span className="meta-tag">DATA INTEGRITY</span>
            <div className="stat-number" style={{ color: 'var(--accent-blue)' }}>VERIFIED</div>
          </div>
        </div>

        {/* Section 1: Extreme Class Imbalance */}
        <div className="content-card hairline-all" style={{ marginTop: '24px' }}>
          <div className="panel-header hairline-b flex-between">
            <h3>Extreme Class Asymmetry Analysis</h3>
            <span className="meta-tag">TARGET RATIO: 1 : 578</span>
          </div>
          <div className="panel-body">
            <p>
              Credit card fraud represents an extreme needle-in-a-haystack problem.
              The dataset contains <strong>284,315 legitimate</strong> transactions against only 
              <strong> 492 fraudulent</strong> transactions ($0.17275\%$).
            </p>

            {/* Imbalance visual bar */}
            <div className="imbalance-bar-container">
              <div className="imbalance-bar-track">
                <div className="imbalance-bar-legit" style={{ width: '99.827%' }}></div>
                <div className="imbalance-bar-fraud" style={{ width: '0.173%' }}></div>
              </div>
              <div className="imbalance-legend flex-between">
                <span>
                  <strong style={{ color: 'var(--ink-primary)' }}>&block; CLASS 0 (LEGITIMATE):</strong> 284,315 instances (99.827%)
                </span>
                <span>
                  <strong style={{ color: 'var(--accent-blue)' }}>&block; CLASS 1 (FRAUD):</strong> 492 instances (0.173%)
                </span>
              </div>
            </div>

            <div className="method-note">
              <strong>Mathematical Implication:</strong> Standard classification accuracy is clinically deceptive.
              A naive model predicting &ldquo;always legitimate&rdquo; scores $99.827\%$ accuracy while detecting 
              $0$ fraudulent transactions. Performance must be benchmarked strictly via 
              <strong> Precision-Recall Curves, Recall, and F1-Score</strong>.
            </div>
          </div>
        </div>

        {/* Section 2: Distribution Profile of Time & Amount */}
        <div className="analytics-grid grid-2" style={{ marginTop: '24px' }}>
          {/* Amount Distribution */}
          <div className="content-card hairline-all">
            <div className="panel-header hairline-b flex-between">
              <h3>Amount Metric Quantiles</h3>
              <span className="meta-tag">MONETARY SKEW</span>
            </div>
            <div className="panel-body">
              <p>
                Transaction amount exhibits heavy positive right-skewness. Median transaction value is 
                <strong> $22.00</strong>, while the maximum reaches <strong>$25,691.16</strong>.
              </p>
              <table className="spec-table">
                <tbody>
                  <tr>
                    <td className="spec-label">Mean (&mu;)</td>
                    <td className="spec-data">$88.35</td>
                  </tr>
                  <tr>
                    <td className="spec-label">Std Dev (&sigma;)</td>
                    <td className="spec-data">$250.12</td>
                  </tr>
                  <tr>
                    <td className="spec-label">Min</td>
                    <td className="spec-data">$0.00 (Card verification pings)</td>
                  </tr>
                  <tr>
                    <td className="spec-label">25th Percentile (Q1)</td>
                    <td className="spec-data">$5.60</td>
                  </tr>
                  <tr>
                    <td className="spec-label">Median (Q2)</td>
                    <td className="spec-data">$22.00</td>
                  </tr>
                  <tr>
                    <td className="spec-label">75th Percentile (Q3)</td>
                    <td className="spec-data">$77.17</td>
                  </tr>
                  <tr>
                    <td className="spec-label">Max</td>
                    <td className="spec-data">$25,691.16</td>
                  </tr>
                  <tr>
                    <td className="spec-label">IQR</td>
                    <td className="spec-data">$71.57</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          {/* Time Distribution */}
          <div className="content-card hairline-all">
            <div className="panel-header hairline-b flex-between">
              <h3>Time Metric Quantiles</h3>
              <span className="meta-tag">48-HOUR SPAN</span>
            </div>
            <div className="panel-body">
              <p>
                Elapsed seconds relative to the initial transaction, spanning approximately 
                <strong> 48 hours (2 complete diurnal cycles)</strong>.
              </p>
              <table className="spec-table">
                <tbody>
                  <tr>
                    <td className="spec-label">Min Time</td>
                    <td className="spec-data">0.00 s (T0 Origin)</td>
                  </tr>
                  <tr>
                    <td className="spec-label">25th Percentile (Q1)</td>
                    <td className="spec-data">54,201.50 s (~15.06 h)</td>
                  </tr>
                  <tr>
                    <td className="spec-label">Median (Q2)</td>
                    <td className="spec-data">84,692.00 s (~23.53 h)</td>
                  </tr>
                  <tr>
                    <td className="spec-label">75th Percentile (Q3)</td>
                    <td className="spec-data">139,320.50 s (~38.70 h)</td>
                  </tr>
                  <tr>
                    <td className="spec-label">Max Time</td>
                    <td className="spec-data">172,792.00 s (~48.00 h)</td>
                  </tr>
                  <tr>
                    <td className="spec-label">Diurnal Cycles</td>
                    <td className="spec-data">2 distinct daytime transaction waves</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Section 3: Scaler Justification & Dimensionality Projection */}
        <div className="analytics-grid grid-2" style={{ marginTop: '24px' }}>
          <div className="content-card hairline-all">
            <div className="panel-header hairline-b flex-between">
              <h3>Empirical RobustScaler Justification</h3>
              <span className="meta-tag">PREPROCESSING FORMULATION</span>
            </div>
            <div className="panel-body">
              <p>
                Because <code>Amount</code> contains extreme positive outliers (up to $25k), standard 
                z-score standardization (<code>StandardScaler</code>) would compress normal transactions into 
                an indistinguishable micro-interval.
              </p>
              <div className="formula-box hairline-all">
                <code>x&prime; = (x - median(x)) / IQR(x)</code>
              </div>
              <p style={{ marginTop: '12px' }}>
                By standardizing via the interquartile range ($IQR = Q3 - Q1 = \$71.57$), the scaling preserves 
                outlier discriminability without corrupting tree split thresholds or nearest-neighbor distances.
              </p>
            </div>
          </div>

          <div className="content-card hairline-all">
            <div className="panel-header hairline-b flex-between">
              <h3>PCA 2D Manifold Projection</h3>
              <span className="meta-tag">LATENT SPACE CLUSTERING</span>
            </div>
            <div className="panel-body">
              <p>
                Features <code>V1</code> through <code>V28</code> represent PCA components already extracted 
                for customer confidentiality. In Phase 1 & 2, low-dimensional projection plots (PCA 2D/3D) 
                will visually illustrate decision contours separating normal vs anomaly clusters.
              </p>
              <div className="placeholder-chart-box hairline-all">
                <span className="meta-tag">[PHASE 1 / 2 PROJECTION PIPELINE]</span>
                <p>PCA Scatter Plot & Decision Contours will be generated during Phase 1 EDA.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
