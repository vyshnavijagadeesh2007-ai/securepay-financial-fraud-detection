import React from 'react';

export default function FooterWordmark() {
  return (
    <footer className="editorial-footer hairline-t">
      <div className="container footer-content">
        <div className="footer-meta-row flex-between">
          <div className="meta-tag">
            SECUREPAY AI RESEARCH INITIATIVE / DEPT OF COMPUTATIONAL RISK
          </div>
          <div className="meta-tag">
            SPECIFICATION: IEEE / ACM STANDARDS COMPLIANT
          </div>
          <div className="meta-tag">
            STATUS: PHASE 4 THRESHOLD CALIBRATION COMPLETE
          </div>
        </div>

        {/* Large spread wordmark */}
        <div className="large-wordmark-container" aria-label="SecurePay AI Wordmark">
          <span className="spread-wordmark">SECUREPAY&nbsp;AI.</span>
        </div>

        <div className="footer-sub-row flex-between hairline-t">
          <span className="meta-tag">
            DATASET: ULB MACHINE LEARNING GROUP (CREDITCARD.CSV)
          </span>
          <span className="meta-tag">
            SCALER: ROBUSTSCALER | UNSUPERVISED NOVELTY: ISOLATION FOREST & LOF
          </span>
        </div>
      </div>
    </footer>
  );
}
