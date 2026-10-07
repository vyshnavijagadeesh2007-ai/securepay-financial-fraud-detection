# SecurePay AI — Real-Time Anomaly Detection in Financial Transactions
## Comprehensive Performance Analysis & Operational Architecture Report

**Document ID:** `SPAI-REP-002`  
**System Version:** `1.0.0-final`  
**Dataset:** `data/creditcard.csv` (European Cardholders Fraud Detection)  
**Authors:** SecurePay FinTech Engineering & Data Science Group  
**Status:** COMPLETE (Methodologically Validated & Audited)

---

# 1. Executive Summary

SecurePay AI is an unsupervised anomaly and novelty detection system designed for financial payment transaction streams characterized by extreme class imbalance. Traditional supervised models struggle when ground-truth fraud labels are heavily delayed and fraudulent behavioral patterns mutate adversarial tactics. 

This project establishes a scientifically audited unsupervised anomaly detection framework utilizing:
1. **Isolation Forest:** Tree-based recursive space partitioning characterized by a substantially smaller model footprint and lower batch scoring cost than LOF.
2. **Local Outlier Factor (LOF):** Local reachability density estimation ($k$-NN) providing superior anomaly ranking and high-sensitivity fraud capture at the cost of greater computational requirements.
3. **Rigorous Methodological Protocol:** A leakage-free 60/20/20 stratified holdout split (`random_state = 42`), where all thresholds were calibrated exclusively on the validation partition (N=56,961) and evaluated once on the untouched test partition (N=56,962, 99 fraud cases).
4. **Proposed Two-Tier Architecture:** Combining the lightweight screening of Isolation Forest with the high recall and ranking power of Local Outlier Factor as an asynchronous investigation queue.

---

# 2. Project Architecture & Pipeline Design

The system implements an end-to-end architecture encompassing data validation, robust feature scaling, unsupervised anomaly scoring, dynamic threshold calibration, a high-performance REST backend, and an editorial React dashboard:

```
[ data/creditcard.csv ] (284,807 rows × 31 cols)
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│                 60 / 20 / 20 Stratified Split               │
│  - Train Legitimate: 170,589 txs (Unsupervised Fitting)     │
│  - Validation: 56,961 txs (Dense 216-Quantile Thresholds)   │
│  - Untouched Test: 56,962 txs (Single-Pass Final Evaluation)│
└─────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│                 Robust Feature Preprocessing                │
│  - RobustScaler fitted strictly on Train Legitimate         │
│  - Robust scaling of Time & Amount; PCA features preserved  │
│  - Target Class strictly excluded from all model inputs     │
└─────────────────────────────────────────────────────────────┘
          │
          ├──────────────────────────────┬──────────────────────────────┐
          ▼                                                             ▼
┌────────────────────────────────────────┐    ┌────────────────────────────────────────┐
│      Isolation Forest Detector         │    │      Local Outlier Factor Detector     │
│  - n_estimators = 200, samples = 256   │    │  - k = 50 neighbors, novelty = True    │
│  - Compact 1.84 MB footprint           │    │  - Density-based reachability          │
│  - Test PR-AUC: 0.1081 (62.2x baseline)│    │  - Test PR-AUC: 0.2186 (125.8x base)   │
└────────────────────────────────────────┘    └────────────────────────────────────────┘
          │                                                             │
          └──────────────────────────────┬──────────────────────────────┘
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                    FastAPI Backend (REST Service Engine)                     │
│  - GET  /api/health (Readiness & dataset checks)                             │
│  - POST /api/predict (Dynamic operating modes: balanced, low_fa, high_recall)│
│  - GET  /api/threshold/operating-points (Validation & cost analysis metrics) │
│  - GET  /api/models/comparison (Multi-metric benchmarks)                     │
└──────────────────────────────────────────────────────────────────────────────┘
                                         │
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                    React + Vite Modern Editorial Frontend                    │
│  - Station 01: Operational Dashboard & Telemetry Readouts                    │
│  - Station 02: Transaction Stream & Latent PCA Feature Explorer              │
│  - Station 03: Model Lab & Algorithmic Comparison Benchmarks                 │
│  - Station 04: Dynamic Threshold Calibration & Business Cost Analysis        │
│  - Station 05: Real-Time Detection Console with Mode Calibration             │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

# 3. Technology Stack & Implementation

* **Data Science & ML Core:** Python 3.14, NumPy, Pandas, Scikit-Learn 1.6, SciPy, Joblib
* **Data Visualization:** Matplotlib, Seaborn
* **Backend REST API:** FastAPI 0.115, Pydantic v2, Uvicorn, Starlette
* **Frontend Web Application:** React 19, Vite 8, Vanilla CSS Design System (Custom Editorial Stationery Aesthetic)
* **Testing & Quality Assurance:** Pytest 9.1, AnyIO, Starlette TestClient, Oxlint

---

# 4. Data Integrity Verification & Physical Profile

Prior to modeling, rigorous data validation established absolute dataset preservation:
* **File Location:** `data/creditcard.csv` (Size: 150,828,752 bytes, ~143.84 MiB)
* **Dimensions:** 284,807 transactions, 31 columns (30 input features + 1 target `Class`)
* **Data Completeness:** 0 missing, null, or NaN values across all 8.82 million data cells (100.00% completeness)
* **Integrity Constraint:** `data/creditcard.csv` remains strictly read-only and unmodified throughout all phases.

---

# 5. Dataset Description

The project uses the **Credit Card Fraud Detection** dataset from Kaggle. The dataset contains anonymized credit-card transaction records and is designed for studying highly imbalanced fraud-detection problems.

The dataset contains:

* **Total transactions:** 284,807
* **Legitimate transactions:** 284,315
* **Fraudulent transactions:** 492
* **Total features:** 31
* **Fraud percentage:** approximately 0.173%
* **Observation period:** approximately 48 hours
* **Missing values:** 0

The dataset contains the following feature groups:

| Feature  | Description                                     |
| -------- | ----------------------------------------------- |
| `Time`   | Time elapsed since the first transaction        |
| `V1–V28` | PCA-transformed anonymized transaction features |
| `Amount` | Transaction amount                              |
| `Class`  | Target label: 0 = legitimate, 1 = fraud         |

The `Class` column is used only as the evaluation target and is **not provided to the anomaly-detection models during training**.

The dataset contains **1,081 duplicate rows**, representing approximately 0.38% of the dataset. The original CSV file is preserved unchanged. Duplicate legitimate observations are removed only from the legitimate training pool to avoid artificially increasing local density during anomaly-model training.

---

# 6. Exploratory Data Analysis

## 6.1 Class Distribution

The dataset is extremely imbalanced.

Out of 284,807 transactions:

* 284,315 are legitimate.
* 492 are fraudulent.

This means that there are approximately **578 legitimate transactions for every fraudulent transaction**.

This imbalance demonstrates why accuracy is not an appropriate primary metric for this problem.

For example, a model that classified almost every transaction as legitimate could obtain very high accuracy while detecting very few fraudulent transactions.

Therefore, the project focuses on **Precision, Recall, F1-score, PR-AUC, and False Positive Rate**.

## 6.2 Transaction Amount

The transaction amount is strongly right-skewed.

Important observations include:

* Mean transaction amount: **$88.35**
* Median transaction amount: **$22.00**
* Maximum transaction amount: **$25,691.16**
* Amount skewness: approximately **16.98**

The large difference between the mean and median indicates the presence of high-value transactions.

For fraudulent transactions:

* Median amount: **$9.25**
* Mean amount: **$122.21**

Because the `Amount` feature contains strong outliers, ordinary standardization can be sensitive to extreme values.

## 6.3 Time

The transactions cover approximately **48 hours**.

The `Time` feature is therefore retained as a potentially useful temporal behavioral feature.

## 6.4 PCA Features

The `V1–V28` features are anonymized PCA-derived variables. They are already transformed and show relatively low correlation with each other.

The strongest observed correlations with the fraud class include:

* `V17`: approximately -0.327
* `V14`: approximately -0.303
* `V12`: approximately -0.261
* `V10`: approximately -0.217
* `V16`: approximately -0.197

These relationships provide useful exploratory information but do not directly determine the anomaly-detection model.

---

# 7. Data Preprocessing

The preprocessing pipeline uses 30 model input features:

`Time, V1, V2, ..., V28, Amount`

The `Class` column is excluded from model inputs.

## 7.1 Robust Scaling

A **RobustScaler** is applied to:

* `Time`
* `Amount`

RobustScaler is appropriate because financial transaction amounts contain extreme values and are highly skewed.

The PCA-derived `V1–V28` features are not additionally scaled.

## 7.2 Prevention of Data Leakage

The final evaluation uses a strict train/validation/test methodology.

The dataset is divided into:

* **60% training**
* **20% validation**
* **20% test**

The split is stratified so that the rare fraudulent observations are represented consistently.

The final split contains:

| Dataset    |   Total | Legitimate | Fraud |
| ---------- | ------: | ---------: | ----: |
| Training   | 170,884 |    170,589 |   295 |
| Validation |  56,961 |     56,863 |    98 |
| Test       |  56,962 |     56,863 |    99 |

The anomaly-detection models are trained using only legitimate transactions from the training set.

The preprocessing scaler is also fitted only on the legitimate training data.

The test set remains untouched until the final evaluation.

This prevents information from the test set from influencing model training or threshold selection.

---

# 8. Isolation Forest

## 8.1 Method

Isolation Forest is an unsupervised anomaly-detection algorithm based on the idea that anomalous observations are easier to isolate than normal observations.

An Isolation Forest repeatedly partitions the feature space using random decision trees.

Anomalous observations generally require fewer partitions to become isolated.

Therefore:

> Shorter isolation paths indicate potentially anomalous transactions.

The project uses the anomaly-score convention:

**Higher score = more anomalous.**

## 8.2 Training

The Isolation Forest model is trained primarily on legitimate transactions.

The main configuration includes:

* `n_estimators = 200`
* `random_state = 42`
* parallel processing enabled
* contamination settings evaluated during experimentation

The historical experiment evaluated contamination values from:

**0.001 to 0.05**

The historical experiments were subsequently classified as baseline experiments because their evaluation included training observations.

The final holdout evaluation uses the proper train/validation/test protocol.

## 8.3 Holdout Performance

At the original baseline threshold corresponding to contamination 0.002, the untouched test set produced:

* TP = 24
* FP = 114
* FN = 75
* TN = 56,749
* Precision = **17.39%**
* Recall = **24.24%**
* F1-score = **20.25%**
* PR-AUC = **0.1081**
* FPR = **0.201%**

The PR-AUC is substantially higher than the no-skill baseline of approximately **0.001738**.

---

# 9. Local Outlier Factor

## 9.1 Method

Local Outlier Factor (LOF) identifies observations that have substantially lower local density than their surrounding observations.

The method compares the local density of a transaction with the density of neighboring transactions.

A transaction that lies in a sparse region compared with its neighbors can therefore be considered anomalous.

The project uses LOF with:

`novelty=True`

This allows the trained model to score new transactions.

The anomaly-score convention is:

**Higher score = more anomalous.**

## 9.2 Hyperparameter Experiments

The project evaluated:

* `n_neighbors`: 10, 20, 35, 50
* contamination: 0.001, 0.002, 0.005, 0.010

This produced **16 configurations**.

The historical experiments showed that the configuration:

**n_neighbors = 50, contamination = 0.010**

performed best among the tested historical configurations.

However, the final evaluation uses the leakage-controlled holdout methodology.

## 9.3 Holdout Performance

Using the final test evaluation, LOF achieved:

* TP = 81
* FP = 548
* FN = 18
* TN = 56,315
* Precision = **12.88%**
* Recall = **81.82%**
* F1-score = **22.25%**
* PR-AUC = **0.2186**
* FPR = **0.964%**

LOF therefore detects substantially more fraudulent transactions than the original Isolation Forest operating point, although it produces more false positives and requires considerably more computational resources.

---

# 10. Evaluation Audit and Scientific Validation

An important methodological improvement was introduced before final threshold tuning.

The initial Phase 2 and Phase 3 experiments evaluated the complete dataset after training on the legitimate baseline. This was useful for historical model comparison, but it was not strictly out-of-sample because some legitimate training observations were also present during evaluation.

Therefore, these results were reclassified as:

**Historical Baseline Experiments**

A new 60/20/20 evaluation protocol was then introduced.

### Training

Only legitimate transactions from the training split are used to fit the anomaly detectors.

### Validation

The validation set is used to:

* compare operating points
* select thresholds
* analyze precision/recall trade-offs
* estimate business costs

### Test

The test set remains untouched until all threshold decisions are finalized.

This provides a more reliable estimate of how the anomaly-detection system may behave on unseen transactions.

---

# 11. Threshold Calibration

A single anomaly threshold does not suit every financial-fraud operation.

A lower threshold generally increases recall but also increases false positives.

A higher threshold generally reduces false positives but can miss more fraudulent transactions.

Therefore, thresholds were calibrated using the **validation set only**.

At least 100 threshold points were evaluated across the continuous anomaly-score distributions. The final implementation evaluated **216 validation quantiles** for each model.

The final test set was evaluated only after the thresholds were finalized.

---

# 12. Final Model Results

## 12.1 Isolation Forest Operating Points

### Low False Alarm

Test results:

* Threshold = **0.672168**
* Precision = **25.42%**
* Recall = **15.15%**
* F1 = **18.99%**
* FPR = **0.077%**
* TP = 15
* FP = 44

This operating point is suitable when minimizing false alerts is particularly important.

### Balanced

Test results:

* Threshold = **0.622447**
* Precision = **15.10%**
* Recall = **29.29%**
* F1 = **19.93%**
* FPR = **0.287%**
* TP = 29
* FP = 163

### Controlled Low FPR

Test results:

* Threshold = **0.634134**
* Precision = **16.55%**
* Recall = **24.24%**
* F1 = **19.67%**
* FPR = **0.213%**
* TP = 24
* FP = 121

### High Recall

Test results:

* Threshold = **0.523974**
* Precision = **4.96%**
* Recall = **77.78%**
* F1 = **9.33%**
* FPR = **2.592%**
* TP = 77
* FP = 1,474

This demonstrates the fundamental trade-off between fraud detection and false-alert volume.

---

# 13. LOF Operating Points

### Low False Alarm

Test results:

* Threshold = **3.033381**
* Precision = **30.77%**
* Recall = **32.32%**
* F1 = **31.53%**
* FPR = **0.127%**
* TP = 32
* FP = 72

### Balanced

Test results:

* Threshold = **2.490138**
* Precision = **24.68%**
* Recall = **57.58%**
* F1 = **34.55%**
* FPR = **0.306%**
* TP = 57
* FP = 174

### Controlled Low FPR

Test results:

* Threshold = **2.707283**
* Precision = **30.72%**
* Recall = **51.52%**
* F1 = **38.49%**
* FPR = **0.202%**
* TP = 51
* FP = 115

### High Recall

Test results:

* Threshold = **1.963896**
* Precision = **13.11%**
* Recall = **81.82%**
* F1 = **22.59%**
* FPR = **0.944%**
* TP = 81
* FP = 537

The controlled-low-FPR LOF operating point provides a particularly useful balance between detection and false-alert volume.

---

# 14. Model Comparison

The final test-set PR-AUC results are:

| Metric                              | Isolation Forest |             LOF |
| ----------------------------------- | ---------------: | --------------: |
| PR-AUC                              |       **0.1081** |      **0.2186** |
| No-skill baseline                   |         0.001738 |        0.001738 |
| PR-AUC improvement                  |   62.2× baseline | 125.8× baseline |
| Recall at selected holdout baseline |           24.24% |          81.82% |
| F1 at selected holdout baseline     |           20.25% |          22.25% |
| FPR                                 |           0.201% |          0.964% |

LOF achieves approximately **2.02× the PR-AUC of Isolation Forest**.

LOF therefore demonstrates stronger anomaly-ranking performance on the final test set.

However, Isolation Forest has important practical advantages:

* Substantially smaller model footprint (1.84 MB vs 185.8 MB)
* Lower computational cost and batch scoring overhead
* Better suitability for lightweight inline screening

Earlier batch benchmarking showed approximately 11.3× lower batch scoring time for Isolation Forest than LOF (approximately 1.01 s vs 11.36 s on the evaluated test partition). This is a batch benchmark and should not be interpreted as per-request production API latency.

The verified live API measurements were:
- Isolation Forest API request: 83.47 ms
- LOF API request: 190.43 ms

These are API request timings and should not be described as pure model inference latency.

LOF has higher computational and memory requirements because it relies on local-neighborhood information and stores the reference training manifold.

---

# 15. Business Cost Analysis

To demonstrate the operational trade-off, an illustrative cost function was used:

**Total Cost = FP × C_FP + FN × C_FN**

Three hypothetical cost scenarios were examined:

* FP:FN = 1:10
* FP:FN = 1:20
* FP:FN = 1:50

These values are **illustrative assumptions only** and do not represent actual SecurePay financial costs.

Across all three scenarios, LOF produced a lower operational cost than Isolation Forest because of its stronger ability to identify fraudulent transactions.

For example, under the 1:20 cost scenario:

* Isolation Forest test cost = **1,588**
* LOF test cost = **856**

Under the 1:50 scenario:

* Isolation Forest test cost = **2,380**
* LOF test cost = **1,466**

This indicates that when missed fraud is considered significantly more expensive than reviewing a false alert, the stronger recall of LOF becomes particularly valuable.

---

# 16. Proposed Two-Tier Architecture

Based on the experimental results, the project proposes a two-tier anomaly-detection architecture.

## Tier 1 — Isolation Forest

Isolation Forest is proposed as the lightweight first-stage screening model because it has a substantially smaller model footprint and lower batch scoring cost than LOF. A conservative operating point such as Controlled Low FPR (τ = 0.634134) can be used when false-alert reduction is important.

A stricter threshold of approximately:

**0.6722**

can be used when reducing false alerts is the primary objective.

## Tier 2 — Local Outlier Factor

LOF is proposed as a secondary investigation or audit model because it achieved stronger test PR-AUC and higher recall at sensitive operating points, at the cost of greater computational and memory requirements.

The controlled-low-FPR LOF threshold is approximately:

**2.7073**

while the balanced threshold is approximately:

**2.4901**

This second layer can be implemented as a deeper review or asynchronous investigation stage rather than assuming that every transaction must pass through LOF synchronously.

---

# 17. System Workflow

The proposed workflow is:

**Transaction**

↓

**Data Validation**

↓

**Robust Preprocessing**

↓

**Isolation Forest Screening**

↓

**Normal Transaction → Allow**

**Suspicious Transaction → Secondary Analysis**

↓

**Local Outlier Factor**

↓

**Risk Classification**

↓

**Investigation / Review / Action**

This architecture combines the efficiency of Isolation Forest with the stronger detection capability of LOF.

---

# 18. Limitations

The project has several limitations.

### 18.1 Dataset Limitation

The dataset contains anonymized PCA-transformed features. Therefore, individual variables cannot be directly interpreted as real-world financial attributes.

### 18.2 Class Imbalance

Fraud remains extremely rare, which means that even a model with strong recall can generate a significant number of false positives.

### 18.3 LOF Computational Cost

LOF requires substantially more memory and computational resources than Isolation Forest.

### 18.4 Concept Drift

Real financial behavior changes over time. A model trained on historical transactions may become less effective when customer behavior or fraud patterns change.

### 18.5 Threshold Dependence

The optimal threshold depends on the operational cost of false positives and false negatives.

Therefore, the selected thresholds should not be considered universally optimal.

### 18.6 Production Validation

The proposed architecture has been evaluated experimentally and should not be interpreted as a deployed production fraud-detection system.

A real deployment would require additional monitoring, retraining, latency testing, security controls, and business validation.

---

# 19. Conclusion

This project developed and evaluated an anomaly-detection framework for identifying potentially fraudulent financial transactions.

The dataset contained **284,807 transactions**, of which only **492 were fraudulent**, demonstrating the extreme class imbalance associated with financial fraud detection.

The project implemented two unsupervised anomaly-detection algorithms:

1. **Isolation Forest**
2. **Local Outlier Factor**

Robust preprocessing was applied to the `Time` and `Amount` features, while the PCA-derived transaction features were retained.

A major methodological improvement was the introduction of a strict train/validation/test evaluation procedure. Models were trained only on legitimate training observations, thresholds were selected using validation data, and the final test set was kept untouched until evaluation.

On the final test set:

* Isolation Forest achieved a **PR-AUC of 0.1081**.
* Local Outlier Factor achieved a **PR-AUC of 0.2186**.

LOF therefore achieved approximately **2.02 times the PR-AUC** of Isolation Forest and demonstrated substantially stronger recall at sensitive operating points.

However, Isolation Forest provides important operational benefits through lower computational and memory requirements.

Based on the combined performance and operational analysis, a **two-tier architecture** is proposed. Isolation Forest can provide fast initial screening, while LOF can perform deeper analysis of suspicious transactions.

Overall, the project demonstrates that anomaly detection can provide a useful approach to highly imbalanced financial fraud detection, particularly when model evaluation focuses on **precision-recall behavior, threshold selection, false-positive control, and business cost rather than accuracy alone**.

---

# 20. Future Scope

Future improvements could include:

* Incorporating transaction history and customer-level behavioral features.
* Adding temporal sequence analysis.
* Evaluating additional anomaly-detection algorithms.
* Investigating ensemble anomaly scores.
* Implementing automated concept-drift detection.
* Developing adaptive thresholds based on transaction context.
* Adding real-time streaming transaction ingestion.
* Integrating human-in-the-loop fraud investigation.
* Monitoring model performance continuously after deployment.
* Periodically retraining models as fraud patterns evolve.

The system could also be extended into a real-time risk-scoring platform where anomaly scores are combined with additional business rules and investigation signals.
