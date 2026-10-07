import React from 'react';

export default function MethodologyPage() {
  return (
    <div className="page methodology-page">
      <div className="container">
        {/* Page Header */}
        <div className="page-header hairline-b flex-between">
          <div>
            <span className="meta-tag">TECHNICAL SPECIFICATION &middot; STATION 07</span>
            <h1>Methodology & Theoretical Foundations</h1>
          </div>
          <div className="header-meta-group">
            <span className="meta-tag">DOCUMENT REF: SPAI-TECH-SPEC-2026</span>
          </div>
        </div>

        {/* Paper / Monograph Body */}
        <div className="monograph-container">
          {/* 1. Problem Formulation */}
          <section className="monograph-section hairline-b">
            <span className="accent-tag">SECTION 01</span>
            <h2>Problem Formulation & Extreme Class Asymmetry</h2>
            <p>
              Credit card payment clearing involves extreme volumetric asymmetry. In modern retail payment rails,
              fraudulent transactions comprise less than two-tenths of one percent of all settlement events ($0.173\%$).
              Supervised machine learning algorithms trained directly on raw unbalanced datasets suffer from severe
              inductive bias toward the majority class: optimizing for raw accuracy produces a degenerate model that
              classifies all transactions as legitimate, achieving $99.83\%$ accuracy while failing to intercept a single
              fraudulent charge.
            </p>
          </section>

          {/* 2. Dataset Architecture */}
          <section className="monograph-section hairline-b">
            <span className="accent-tag">SECTION 02</span>
            <h2>Dataset Topology & Confidentiality PCA</h2>
            <p>
              The primary dataset (<code>data/creditcard.csv</code>) contains $284,807$ electronic card transactions
              recorded across a 48-hour window in September 2013 by European cardholders. Due to stringent privacy and
              PCI-DSS confidentiality regulations, attributes $V_1$ through $V_{28}$ represent numerical principal components
              extracted via Principal Component Analysis (PCA). The only untransformed features are <code>Time</code> (elapsed
              seconds from origin) and <code>Amount</code> (transaction monetary sum).
            </p>
            <div className="callout-box hairline-all">
              <strong>Ground-Truth Label Reservation:</strong> The binary <code>Class</code> feature ($0$ = Legitimate,
              $1$ = Fraud) is strictly excluded from the training input feature matrix $X$. The unsupervised and
              novelty models learn purely from feature structures without label leakage.
            </div>
          </section>

          {/* 3. RobustScaler Preprocessing */}
          <section className="monograph-section hairline-b">
            <span className="accent-tag">SECTION 03</span>
            <h2>RobustScaler Preprocessing Formulation</h2>
            <p>
              Transaction amounts exhibit heavy positive skewness with high-value outliers (max $25,691.16, mean $88.35,
              median $22.00). Classical standard score scaling (z = (x - &mu;) / &sigma;) is heavily compromised by
              extreme values, shifting the empirical mean and inflating standard deviation. SecurePay AI employs 
              <strong>RobustScaler</strong>:
            </p>
            <div className="formula-box hairline-all">
              <code>x&prime; = (x - Q2(x)) / (Q3(x) - Q1(x)) = (x - median(x)) / IQR(x)</code>
            </div>
            <p>
              Because the median and interquartile range ($IQR$) are robust statistics (breakdown point $= 50\%$),
              outliers do not influence scaling boundaries, preserving the geometric distances required by tree partitioners
              and nearest-neighbor density estimators.
            </p>
          </section>

          {/* 4. Normal Baseline Novelty Training Strategy */}
          <section className="monograph-section hairline-b">
            <span className="accent-tag">SECTION 04</span>
            <h2>Novelty Detection Baseline Strategy</h2>
            <p>
              Rather than attempting to capture fraud patterns directly through supervised classifiers (which struggle with
              rapidly shifting fraudulent modus operandi), SecurePay AI trains on <strong>Class == 0</strong> (legitimate transactions)
              exclusively. The model constructs a tight boundary enclosing normal customer spending behavior. Any transaction
              projected outside this envelope is classified as an empirical anomaly.
            </p>
          </section>

          {/* 5. Isolation Forest vs LOF */}
          <section className="monograph-section hairline-b">
            <span className="accent-tag">SECTION 05</span>
            <h2>Algorithmic Engines: Isolation Forest vs LOF</h2>
            <div className="grid-2" style={{ marginTop: '16px' }}>
              <div className="concept-box hairline-r" style={{ paddingRight: '16px' }}>
                <h4>Isolation Forest (iForest)</h4>
                <p>
                  Recursively bisects feature space using random hyperplanes. Because anomalies reside in sparse regions,
                  they are isolated at shallow tree depths. The anomaly score is inversely proportional to average path
                  length h(x) across an ensemble of iTrees. High computational efficiency (O(n &middot; log n)) makes it ideal
                  for online transaction pipelines.
                </p>
              </div>
              <div className="concept-box" style={{ paddingLeft: '16px' }}>
                <h4>Local Outlier Factor (LOF)</h4>
                <p>
                  Measures the local density of an observation with respect to its $k$-nearest neighbors. An observation
                  is flagged if its local density is substantially lower than that of its neighbors. LOF excels at identifying
                  anomalies within clusters of varying densities where global distance metrics fail.
                </p>
              </div>
            </div>
          </section>

          {/* 6. Evaluation Protocol: Precision, Recall, F1 */}
          <section className="monograph-section hairline-b">
            <span className="accent-tag">SECTION 06</span>
            <h2>Evaluation Protocol & Cost-Matrix Tradeoffs</h2>
            <p>
              Performance validation is conducted strictly on an independent mixed test partition containing both normal and
              fraudulent transactions using asymmetric metrics:
            </p>
              <ul className="spec-list">
                <li>
                  <strong>Recall [ TP / (TP + FN) ]:</strong> The proportion of actual fraudulent events captured by the system.
                  In financial systems, minimizing False Negatives protects against direct capital loss.
                </li>
                <li>
                  <strong>Precision [ TP / (TP + FP) ]:</strong> The proportion of flagged transactions that are genuinely fraudulent.
                  Minimizing False Positives prevents unnecessary card declines and customer dissatisfaction.
                </li>
                <li>
                  <strong>F1-Score [ 2 &middot; (P &middot; R) / (P + R) ]:</strong> Harmonic mean balancing detection sensitivity against
                  investigative overhead.
                </li>
                <li>
                  <strong>PR-AUC:</strong> Area under the Precision-Recall curve across all continuous threshold values &tau; &in; [0, 1].
                </li>
              </ul>
          </section>

          {/* 7. Limitations & Future Roadmap */}
          <section className="monograph-section">
            <span className="accent-tag">SECTION 07</span>
            <h2>System Limitations & Engineering Roadmap</h2>
            <ul className="spec-list">
              <li>
                <strong>Concept Drift:</strong> Legitimate customer habits evolve during holiday seasons; model retraining must be scheduled periodically.
              </li>
              <li>
                <strong>PCA Interpretability:</strong> Anonymized PCA features hinder human explanation of specific feature causes (e.g. merchant category).
              </li>
              <li>
                <strong>Planned Roadmap:</strong> Phase 1 (EDA & Preprocessing) &rarr; Phase 2 (Unsupervised Training & Calibration) &rarr; Phase 3 (Full API Integration & Real-Time Scoring).
              </li>
            </ul>
          </section>
        </div>
      </div>
    </div>
  );
}
