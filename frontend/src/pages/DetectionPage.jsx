import React, { useState } from 'react';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL?.replace(/\/+$/, '');

const formatMetric = (value) => (
  typeof value === 'number' && Number.isFinite(value) ? value.toFixed(6) : '--'
);

// Authentic raw sample feature sets from creditcard.csv for testing
const SAMPLE_NORMAL = {
  Time: 0.0,
  Amount: 149.62,
  V1: -1.359807, V2: -0.072781, V3: 2.536347, V4: 1.378155,
  V5: -0.338321, V6: 0.462388, V7: 0.239599, V8: 0.098698,
  V9: 0.363787, V10: 0.090794, V11: -0.551600, V12: -0.617801,
  V13: -0.991390, V14: -0.311169, V15: 1.468177, V16: -0.470401,
  V17: 0.207971, V18: 0.025791, V19: 0.403993, V20: 0.251412,
  V21: -0.018307, V22: 0.277838, V23: -0.110474, V24: 0.066928,
  V25: 0.128539, V26: -0.189115, V27: 0.133558, V28: -0.021053
};

const SAMPLE_FRAUD = {
  Time: 406.0,
  Amount: 0.00,
  V1: -2.312227, V2: 1.951992, V3: -1.609851, V4: 3.997906,
  V5: -0.522188, V6: -1.426545, V7: -2.537387, V8: 1.391657,
  V9: -2.770089, V10: -2.772272, V11: 3.202033, V12: -2.899907,
  V13: -0.595222, V14: -4.289254, V15: 0.389724, V16: -1.140747,
  V17: -2.830056, V18: -0.016822, V19: 0.416956, V20: 0.126911,
  V21: 0.517232, V22: -0.035049, V23: -0.465211, V24: 0.320198,
  V25: 0.044519, V26: 0.177840, V27: 0.261145, V28: -0.143276
};

export default function DetectionPage() {
  const [selectedModel, setSelectedModel] = useState('Isolation Forest');
  const [formData, setFormData] = useState(SAMPLE_NORMAL);
  const [inferenceResult, setInferenceResult] = useState(null);
  const [isEvaluating, setIsEvaluating] = useState(false);
  const [apiError, setApiError] = useState(null);

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: parseFloat(value) || 0.0
    }));
  };

  const handleLoadSample = (sampleType) => {
    if (sampleType === 'normal') {
      setFormData(SAMPLE_NORMAL);
    } else {
      setFormData(SAMPLE_FRAUD);
    }
    setInferenceResult(null);
    setApiError(null);
  };

  const handleClear = () => {
    const blank = { Time: 0.0, Amount: 0.0 };
    for (let i = 1; i <= 28; i++) {
      blank[`V${i}`] = 0.0;
    }
    setFormData(blank);
    setInferenceResult(null);
    setApiError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setInferenceResult(null);
    setApiError(null);
    setIsEvaluating(true);

    try {
      if (!API_BASE_URL) {
        throw new Error('API URL is not configured. Set VITE_API_BASE_URL and restart the frontend.');
      }

      const response = await fetch(`${API_BASE_URL}/api/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          transaction: formData,
          model: selectedModel,
          operating_mode: 'low_fpr'
        })
      });

      let result;
      try {
        result = await response.json();
      } catch {
        throw new Error(`The prediction API returned an invalid response (HTTP ${response.status}).`);
      }

      if (!response.ok) {
        const detail = typeof result.detail === 'string'
          ? result.detail
          : JSON.stringify(result.detail ?? result);
        throw new Error(`Prediction failed (HTTP ${response.status}): ${detail}`);
      }

      setInferenceResult(result);
    } catch (error) {
      setApiError(error instanceof Error ? error.message : 'Unable to complete the prediction request.');
    } finally {
      setIsEvaluating(false);
    }
  };

  return (
    <div className="page detection-page">
      <div className="container">
        {/* Page Header */}
        <div className="page-header hairline-b flex-between">
          <div>
            <span className="meta-tag">INFERENCE CONSOLE &middot; STATION 05</span>
            <h1>Real-Time Transaction Detection</h1>
          </div>
          <div className="header-meta-group">
            <span className="meta-tag">TARGET ARCHITECTURE: REST API &middot; /api/predict</span>
          </div>
        </div>

        {/* Console Layout */}
        <div className="detection-grid grid-2">
          {/* Left Column: Input Form */}
          <div className="form-panel hairline-all">
            <div className="panel-header hairline-b flex-between">
              <h3>Input Telemetry Vector</h3>
              <div className="sample-btn-group">
                <button 
                  type="button" 
                  onClick={() => handleLoadSample('normal')}
                  className="preset-btn"
                >
                  Load Sample Legit
                </button>
                <button 
                  type="button" 
                  onClick={() => handleLoadSample('fraud')}
                  className="preset-btn"
                >
                  Load Sample Fraud
                </button>
                <button 
                  type="button" 
                  onClick={handleClear}
                  className="preset-btn"
                >
                  Clear
                </button>
              </div>
            </div>

            <form onSubmit={handleSubmit} className="detection-form">
              {/* Algorithm Selection */}
              <div className="form-section hairline-b">
                <label className="meta-tag field-label">SELECT NOVELTY DETECTOR:</label>
                <div className="model-toggle-group">
                  <button
                    type="button"
                    className={`model-btn ${selectedModel === 'Isolation Forest' ? 'active' : ''}`}
                    aria-pressed={selectedModel === 'Isolation Forest'}
                    onClick={() => {
                      setSelectedModel('Isolation Forest');
                      setInferenceResult(null);
                      setApiError(null);
                    }}
                  >
                    Isolation Forest
                  </button>
                  <button
                    type="button"
                    className={`model-btn ${selectedModel === 'Local Outlier Factor' ? 'active' : ''}`}
                    aria-pressed={selectedModel === 'Local Outlier Factor'}
                    onClick={() => {
                      setSelectedModel('Local Outlier Factor');
                      setInferenceResult(null);
                      setApiError(null);
                    }}
                  >
                    Local Outlier Factor (LOF)
                  </button>
                </div>
              </div>

              {/* Primary Attributes: Time & Amount */}
              <div className="form-section hairline-b">
                <span className="meta-tag field-label">UNPROCESSED MONETARY & TEMPORAL FEATURES:</span>
                <div className="input-pair-grid">
                  <div className="input-field">
                    <label htmlFor="input-time">Time (Elapsed Sec)</label>
                    <input
                      id="input-time"
                      type="number"
                      step="any"
                      value={formData.Time}
                      onChange={(e) => handleInputChange('Time', e.target.value)}
                    />
                  </div>
                  <div className="input-field">
                    <label htmlFor="input-amount">Amount (Currency)</label>
                    <input
                      id="input-amount"
                      type="number"
                      step="any"
                      value={formData.Amount}
                      onChange={(e) => handleInputChange('Amount', e.target.value)}
                    />
                  </div>
                </div>
              </div>

              {/* PCA Features V1 - V28 */}
              <div className="form-section">
                <div className="flex-between" style={{ marginBottom: '8px' }}>
                  <span className="meta-tag field-label">PCA DECOMPOSED COMPONENTS (V1 &ndash; V28):</span>
                  <span className="meta-tag">LATENT SPACE</span>
                </div>

                <div className="pca-inputs-grid">
                  {Array.from({ length: 28 }, (_, i) => i + 1).map((idx) => {
                    const key = `V${idx}`;
                    return (
                      <div key={key} className="pca-input-item">
                        <label htmlFor={`input-${key}`}>{key}</label>
                        <input
                          id={`input-${key}`}
                          type="number"
                          step="any"
                          value={formData[key] ?? 0.0}
                          onChange={(e) => handleInputChange(key, e.target.value)}
                        />
                      </div>
                    );
                  })}
                </div>
              </div>

              <div className="form-actions hairline-t">
                <button 
                  type="submit" 
                  disabled={isEvaluating} 
                  className="primary-btn submit-btn"
                >
                  {isEvaluating ? 'Evaluating Vector...' : 'Transmit Transaction for Inference \u2192'}
                </button>
              </div>
            </form>
          </div>

          {/* Right Column: Output Readout & Integrity Display */}
          <div className="readout-panel">
            <div className="readout-box hairline-all">
              <div className="panel-header hairline-b flex-between">
                <h3>Inference Diagnostic Stream</h3>
                <span className="meta-tag">DIAGNOSTIC CHANNEL</span>
              </div>

              <div className="readout-body">
                <div className="diagnostic-row flex-between hairline-b">
                  <span className="meta-tag">TARGET MODEL:</span>
                  <strong style={{ color: 'var(--ink-primary)' }}>{selectedModel}</strong>
                </div>

                <div className="diagnostic-row flex-between hairline-b">
                  <span className="meta-tag">ENGINE STATUS:</span>
                  <span className="status-badge" style={{ color: 'var(--accent-blue)', borderColor: 'var(--accent-blue)' }}>
                    IF + LOF MODELS READY
                  </span>
                </div>

                <div className="diagnostic-row flex-between hairline-b">
                  <span className="meta-tag">ANOMALY SCORE:</span>
                  <span className="metric-figure placeholder-val">
                    {formatMetric(inferenceResult?.anomaly_score)}
                  </span>
                </div>

                <div className="diagnostic-row flex-between hairline-b">
                  <span className="meta-tag">CALIBRATED THRESHOLD:</span>
                  <span className="metric-figure placeholder-val">
                    {formatMetric(inferenceResult?.threshold)}
                  </span>
                </div>

                <div className="diagnostic-row flex-between hairline-b">
                  <span className="meta-tag">OPERATING MODE:</span>
                  <span className="metric-figure placeholder-val">
                    {inferenceResult?.operating_mode || inferenceResult?.operating_point || '--'}
                  </span>
                </div>

                <div className="diagnostic-row flex-between hairline-b">
                  <span className="meta-tag">CLASSIFICATION:</span>
                  <span className="metric-figure placeholder-val">
                    {inferenceResult
                      ? inferenceResult.is_anomaly === true || inferenceResult.prediction === 1
                        ? 'ANOMALY'
                        : inferenceResult.status === 'NORMAL' || inferenceResult.prediction === 0
                          ? 'NORMAL'
                          : inferenceResult.status
                      : '--'}
                  </span>
                </div>

                {/* Status Notice */}
                <div className="advisory-box">
                  <span className="accent-tag">[INFERENCE ENGINE STATUS]</span>
                  <p>
                    {apiError ? (
                      <span role="alert" style={{ color: 'var(--status-pending)' }}>{apiError}</span>
                    ) : inferenceResult ? (
                      inferenceResult.message
                    ) : (
                      'Awaiting feature submission. Requests use the Phase 4 controlled low-FPR operating point.'
                    )}
                  </p>
                </div>
              </div>
            </div>

            {/* Architecture schema reference */}
            <div className="schema-reference-box hairline-all">
              <div className="panel-header hairline-b flex-between">
                <span className="meta-tag">REST API INFERENCE CONTRACT</span>
                <span className="meta-tag">JSON / POST</span>
              </div>
              <pre className="code-block">
                {inferenceResult
                  ? JSON.stringify(inferenceResult, null, 2)
                  : `POST ${API_BASE_URL || 'VITE_API_BASE_URL'}/api/predict\nModel: ${selectedModel}\nOperating mode: low_fpr`}
              </pre>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
