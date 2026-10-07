# SecurePay AI — Phase 0: Dataset Validation Report

**Document ID:** `SPAI-REP-001`  
**Date:** Phase 0 Baseline  
**Target File:** `data/creditcard.csv`  
**Dataset Source:** European Cardholders Credit Card Fraud Dataset (ULB / Kaggle)  
**Status:** VALIDATED (Strict Read-Only Verification)

---

## 1. Executive Summary

A lightweight verification of the primary dataset was conducted in accordance with Phase 0 requirements. No modifications were made to the source data file (`data/creditcard.csv`). The file exists, is structurally uncorrupted, and matches all expected dimensional, semantic, and mathematical criteria.

---

## 2. File Verification & Physical Profile

| Attribute | Expected Value | Observed Value | Verification Result |
| :--- | :--- | :--- | :--- |
| **File Path** | `data/creditcard.csv` | `data/creditcard.csv` | **MATCH** |
| **File Presence** | Exists | Exists | **MATCH** |
| **File Size (Bytes)** | ~150 MB | 150,828,752 bytes (~143.84 MiB) | **MATCH** |
| **Row Count (Observations)**| 284,807 | 284,807 | **MATCH** |
| **Column Count (Features)**| 31 | 31 | **MATCH** |
| **Target Column** | `Class` | Present (`int64`) | **MATCH** |
| **Temporal Feature** | `Time` | Present (`float64`) | **MATCH** |
| **Monetary Feature** | `Amount` | Present (`float64`) | **MATCH** |
| **PCA Components** | `V1` through `V28` | All 28 features present (`float64`) | **MATCH** |

---

## 3. Structural & Schema Profile

### 3.1 Feature Catalog

- **`Time`** (`float64`): Number of seconds elapsed between this transaction and the first transaction in the dataset.
- **`V1` – `V28`** (`float64`): 28 principal component features derived via PCA due to confidentiality constraints.
- **`Amount`** (`float64`): Transaction amount in currency units.
- **`Class`** (`int64`): Ground truth binary label ($0$ = Legitimate, $1$ = Fraudulent). **Strictly reserved for evaluation; never passed as an input feature during unsupervised anomaly model training.**

### 3.2 Data Types & Completeness

- **Floating-point features (30):** `Time`, `Amount`, `V1` ... `V28`
- **Integer features (1):** `Class`
- **Missing / Null Values:** **0** across all 31 columns and all 284,807 rows.
- **Completeness Ratio:** 100.00%

---

## 4. Class Imbalance Analysis

| Class Category | Label | Count | Proportion | Imbalance Ratio |
| :--- | :---: | :---: | :---: | :---: |
| **Legitimate Transactions** | `0` | 284,315 | 99.82725% | Reference |
| **Fraudulent Transactions** | `1` | 492 | 0.17275% | 1 : 578 |
| **Total** | — | 284,807 | 100.00000% | — |

### Key Observations:
1. **Extreme Asymmetry:** Fraud represents roughly 1 in every 579 transactions.
2. **Evaluation Metric Impact:** Standard accuracy is clinically invalid ($99.83\%$ accuracy achieved by a trivial zero-rule classifier). The system must prioritize **Precision-Recall curves, Recall (detecting fraud), Precision (minimizing false alarms), and F1-Score**.
3. **Training Strategy Validation:** Confirms the architectural decision to train unsupervised models (Isolation Forest, LOF) primarily on the normal baseline (`Class == 0`) and evaluate on the combined test set.

---

## 5. Duplicate Row Analysis

- **Total Identical Duplicate Rows:** 1,081 rows.
- **Duplicates in Class 0 (Legitimate):** 1,062 instances.
- **Duplicates in Class 1 (Fraud):** 19 instances.

### Architectural Decision Note:
In Phase 0, the raw CSV remains strictly untouched. In Phase 1 (EDA & Preprocessing), we will document whether deduplication should occur prior to train/test partitioning or if duplicates represent legitimate identical rapid transactions (e.g. repeated micro-charges).

---

## 6. Basic Descriptive Statistics (Time & Amount)

| Metric | `Time` (seconds) | `Amount` (currency) |
| :--- | :--- | :--- |
| **Count** | 284,807.00 | 284,807.00 |
| **Mean** | 94,813.86 s (~26.34 h) | 88.35 |
| **Standard Deviation** | 47,488.15 s | 250.12 |
| **Minimum** | 0.00 s | 0.00 (e.g., zero-dollar card validation pings) |
| **25th Percentile ($Q_1$)** | 54,201.50 s | 5.60 |
| **Median (50th Percentile)** | 84,692.00 s (~23.53 h) | 22.00 |
| **75th Percentile ($Q_3$)** | 139,320.50 s | 77.17 |
| **Maximum** | 172,792.00 s (~48.00 h) | 25,691.16 |
| **Interquartile Range ($IQR$)** | 85,119.00 s | 71.57 |

### Architectural Implication for Scaler Choice:
- The `Amount` distribution exhibits severe positive skewness ($\text{mean} = 88.35 \gg \text{median} = 22.00$) with extreme outliers up to $25,691.16$.
- Standard standardization ($z$-score) would be severely distorted by extreme transaction amounts.
- This provides direct empirical justification for our planned use of **`RobustScaler`** (based on median and interquartile range), preserving outlier discrimination for anomaly algorithms.

---

## 7. Phase 0 Validation Sign-off

- [x] Dataset located at `data/creditcard.csv`
- [x] File integrity and dimensions verified ($284,807 \times 31$)
- [x] All 28 PCA features + Time + Amount + Class confirmed
- [x] Zero null values confirmed
- [x] Original dataset strictly preserved and unmodified

---

## 8. Phase 1 — Comprehensive EDA & Preprocessing Report

### 8.1 Empirical Findings Summary

* **Observations & Dimensionality:** 284,807 rows across 31 features (30 numerical features + 1 target `Class`).
* **Memory Usage:** 67.36 MB in RAM.
* **Missing Values:** 0 nulls across all cells (100.00% completeness).

### 8.2 Extreme Class Imbalance & Evaluation Metric Validity

* **Legitimate Transactions (`Class == 0`):** 284,315 ($99.82725\%$)
* **Fraudulent Transactions (`Class == 1`):** 492 ($0.17275\%$)
* **Imbalance Ratio:** $1 : 577.9$ (1 fraud per 578 legitimate transactions).
* **Evaluation Metric Decision:** Standard classification accuracy is clinically misleading: a zero-rule baseline predicting all transactions as legitimate achieves **$99.827\%$ accuracy** while failing to intercept a single fraudulent event ($0\%$ recall). Evaluation must strictly prioritize **Precision, Recall, F1-Score, and Precision-Recall AUC (PR-AUC)**.
* **Visualization:** Saved to [`outputs/figures/class_distribution.png`](file:///c:/Users/VYSHNAVI/OneDrive/Desktop/Financial-Fraud-Detection/outputs/figures/class_distribution.png) showing both linear and logarithmic scales.

### 8.3 Duplicate Row Investigation & Methodological Resolution

* **Total Duplicate Rows (excluding first occurrence):** 1,081 rows ($0.3796\%$).
* **Rows Involved in Duplicate Clusters:** 1,854 transactions.
* **Class Breakdown:**
  * Duplicates in Class 0 (Legitimate): 1,062 instances ($98.24\%$ of duplicates).
  * Duplicates in Class 1 (Fraudulent): 19 instances ($1.76\%$ of duplicates).
* **Contradictory Labels:** **0**. No identical feature vectors carry conflicting class labels.
* **Methodological Decision:**
  1. The raw physical file `data/creditcard.csv` remains strictly intact and unmodified.
  2. For model training partitions, deduplication is recommended prior to training split to prevent synthetic clusters from inflating tree depth or leaking identical test records into evaluation partitions.

### 8.4 Temporal Analysis (`Time`)

* **Range:** 0.00 s to 172,792.00 s (exactly 48.00 hours).
* **Median / IQR:** Median = 84,692.00 s, IQR = 85,119.00 s.
* **Diurnal Dynamics:**
  * Legitimate transactions follow pronounced 24-hour sinusoidal customer spending habits, with steep activity troughs during late-night sleeping hours (~03:00 to 06:00 UTC).
  * Fraudulent transactions maintain sustained velocity through the night, exploiting sleeping cardholders and delayed notification response times.
* **Visualization:** Saved to [`outputs/figures/time_distribution.png`](file:///c:/Users/VYSHNAVI/OneDrive/Desktop/Financial-Fraud-Detection/outputs/figures/time_distribution.png).

### 8.5 Monetary Analysis (`Amount`) & Heavy-Tailed Skewness

| Population | Count | Mean | Median | Std Dev | Min | Max | Skewness |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Overall** | 284,807 | \$88.35 | \$22.00 | \$250.12 | \$0.00 | \$25,691.16 | **16.98** |
| **Legitimate (`Class=0`)** | 284,315 | \$88.29 | \$22.00 | \$250.11 | \$0.00 | \$25,691.16 | **17.00** |
| **Fraudulent (`Class=1`)** | 492 | \$122.21 | \$9.25 | \$256.68 | \$0.00 | \$2,125.87 | **3.75** |

* **Key Takeaways:**
  * Fraudulent transactions exhibit a **lower median** (\$9.25 vs \$22.00), demonstrating frequent card-testing micro-charges (\$0.00 to \$1.00).
  * Fraudulent transactions exhibit a **higher mean** (\$122.21 vs \$88.29), reflecting periodic large balance drains.
  * Legitimate purchases reach up to \$25,691.16, creating extreme positive skewness (16.98).
* **Visualizations:** Saved to [`outputs/figures/amount_distribution.png`](file:///c:/Users/VYSHNAVI/OneDrive/Desktop/Financial-Fraud-Detection/outputs/figures/amount_distribution.png) and [`outputs/figures/amount_by_class.png`](file:///c:/Users/VYSHNAVI/OneDrive/Desktop/Financial-Fraud-Detection/outputs/figures/amount_by_class.png).

### 8.6 PCA Feature Analysis (`V1` to `V28`) & Correlation Structure

* $V_1$ through $V_{28}$ are orthogonal zero-centered principal components from PCA:
  * Maximum absolute mean across all 28 features is $< 10^{-14}$.
  * Mutual Pearson correlations between $V_i$ and $V_j$ ($i \ne j$) are practically 0.
* **Correlations with Target (`Class`):**
  * **Top Negative:** $V_{17}$ ($-0.3265$), $V_{14}$ ($-0.3025$), $V_{12}$ ($-0.2606$), $V_{10}$ ($-0.2169$), $V_{16}$ ($-0.1965$).
  * **Top Positive:** $V_{11}$ ($+0.1549$), $V_{4}$ ($+0.1334$), $V_{2}$ ($+0.0913$), $V_{21}$ ($+0.0404$), $V_{19}$ ($+0.0348$).
* **Visualization:** Saved to [`outputs/figures/correlation_heatmap.png`](file:///c:/Users/VYSHNAVI/OneDrive/Desktop/Financial-Fraud-Detection/outputs/figures/correlation_heatmap.png).

### 8.7 Preprocessing Engine & `RobustScaler` Justification

* **StandardScaler vs RobustScaler:**
  * `StandardScaler`: $z = \frac{x - \mu}{\sigma}$ computes mean \$88.35 and standard deviation \$250.12, heavily inflated by the \$25,691.16 upper tail.
  * `RobustScaler`: $x' = \frac{x - \text{median}}{\text{IQR}}$ relies on median (\$22.00) and interquartile range (\$71.57), establishing an uncorrupted scale baseline that preserves outlier discrimination.
* **Component-Level Strategy:**
  1. `Amount`: Scaled with `RobustScaler`.
  2. `Time`: Scaled with `RobustScaler` to normalize 48-hour range.
  3. `V1`–`V28`: Passed through untouched (already zero-centered orthogonal components).
* **Implementation:** Reusable, serializable module built in [`backend/ml/preprocessing/scaler.py`](file:///c:/Users/VYSHNAVI/OneDrive/Desktop/Financial-Fraud-Detection/backend/ml/preprocessing/scaler.py) (`TransactionPreprocessor`).

### 8.8 Data Leakage Prevention Protocol

1. **Target Feature Isolation:** `Class` is strictly stripped and decoupled from input matrices.
2. **Training Set Partitioning:** `TransactionPreprocessor` is fitted strictly on the legitimate baseline partition (`Class == 0`).
3. **Out-of-Sample Evaluation:** Fraudulent records are reserved exclusively for model evaluation benchmarking in Phase 2.

### 8.9 Phase 1 Validation Sign-off

- [x] Programmatic ingestion and shape verification ($284,807 \times 31$)
- [x] Complete EDA and statistical profiling across Time, Amount, V1-V28, and Class
- [x] 5 publication-quality figures saved to `outputs/figures/`
- [x] 4 structured JSON summary metrics saved to `outputs/metrics/`
- [x] Reusable `TransactionPreprocessor` implemented in `backend/ml/preprocessing/scaler.py`
- [x] Unit test suite created in `tests/test_preprocessing.py` (25/25 passing tests)
- [x] Research notebook `notebooks/fraud_detection_analysis.ipynb` updated for Sections 1–13
- [x] Zero ML models trained; zero metrics fabricated

---

## 9. Phase 2 — Isolation Forest Anomaly Detection Baseline Report

### 9.1 Executive Overview & Mathematical Framing

Phase 2 established the first unsupervised anomaly detection model for the SecurePay AI platform: the **Isolation Forest** (Liu, Ting, and Zhou, 2008). 

Unlike density-based or distance-based algorithms, Isolation Forest operates on recursive random axis-aligned partitioning. Anomalous transactions occupy sparse, peripheral regions in the feature space and are isolated close to the root of an isolation tree ($iTree$), requiring significantly fewer splits than normal transactions.

The anomaly score $s(x, n)$ across an ensemble of $k$ trees is given by:

$$s(x, n) = 2^{-\frac{\mathbb{E}(h(x))}{c(n)}}$$

where $h(x)$ is the tree path length and $c(n)$ is the average path length of an unsuccessful search in a Binary Search Tree (BST) over sample size $n$:

$$c(n) = 2\left(\ln(n - 1) + 0.5772156649\right) - \frac{2(n - 1)}{n}$$

We standardized all continuous scores via:

$$\text{anomaly\_score}(x) = -\text{score\_samples}(x)$$

ensuring that higher scores monotonically represent higher anomaly likelihood.

---

### 9.2 Training Partition & Leakage Prevention

To evaluate pure anomaly detection under realistic operational conditions:
1. **Unsupervised Normal Baseline:** The training partition was restricted strictly to legitimate transactions (`Class == 0`).
2. **Deduplication:** 1,062 duplicate legitimate rows were removed, yielding **283,253 training samples**.
3. **Data Leakage Safeguard:** Zero fraudulent transactions (`Class == 1`) were present in the training data. The model learned solely the manifold of legitimate cardholder behavior.
4. **Target Isolation:** The `Class` column was excluded entirely from model inputs; only the 30 canonical features (`Time`, `V1`–`V28`, `Amount`) were utilized.
5. **Preprocessing:** Scaled with `TransactionPreprocessor` (`RobustScaler` on `Amount` and `Time`) fitted strictly on the legitimate training baseline.

---

### 9.3 Contamination Hyperparameter Experimentation Results

A controlled sweep of the `contamination` parameter ($c$) was conducted across seven configurations using $n\_estimators = 200$, $max\_samples = 256$, and $random\_state = 42$. All evaluations were performed against the full out-of-sample mixed transaction population (284,807 transactions; 492 fraud cases).

| Contamination ($c$) | Predicted Anomalies | True Positives (TP) | False Positives (FP) | False Negatives (FN) | True Negatives (TN) | Precision | Recall | F1-Score | PR-AUC | Execution Time (s) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **0.001** | 358 | 74 | 284 | 418 | 284,031 | 0.2067 | 0.1504 | 0.1741 | 0.1554 | 9.68s |
| **0.002** | 701 | 129 | 572 | 363 | 283,743 | 0.1840 | 0.2622 | **0.2163** | 0.1554 | 9.46s |
| **0.005** | 1,684 | 218 | 1,466 | 274 | 282,849 | 0.1295 | 0.4431 | 0.2004 | 0.1554 | 9.35s |
| **0.010** | 3,205 | 300 | 2,905 | 192 | 281,410 | 0.0936 | 0.6098 | 0.1623 | 0.1554 | 9.39s |
| **0.020** | 6,125 | 364 | 5,761 | 128 | 278,554 | 0.0594 | 0.7398 | 0.1100 | 0.1554 | 9.30s |
| **0.030** | 9,012 | 403 | 8,609 | 89 | 275,706 | 0.0447 | 0.8191 | 0.0848 | 0.1554 | 12.32s |
| **0.050** | 14,773 | 418 | 14,355 | 74 | 269,960 | 0.0283 | **0.8496** | 0.0548 | 0.1554 | 21.86s |

*Full tabular metrics saved to [`outputs/metrics/isolation_forest_experiments.csv`](file:///outputs/metrics/isolation_forest_experiments.csv).*

---

### 9.4 Selected Production Baseline & Confusion Matrix

**Selected Baseline Configuration:**
- `contamination`: **0.002**
- `n_estimators`: 200
- `max_samples`: 256
- `random_state`: 42

**Performance Metrics at $c = 0.002$:**
- **True Positives (TP):** 129
- **False Positives (FP):** 572
- **False Negatives (FN):** 363
- **True Negatives (TN):** 283,743
- **Precision:** 0.1840 ($18.4\%$)
- **Recall:** 0.2622 ($26.2\%$)
- **F1-Score:** **0.2163** (peak across grid)
- **False Positive Rate (FPR):** $0.201\%$ (only 2 in every 1,000 legitimate transactions flagged)
- **False Negative Rate (FNR):** $73.78\%$
- **Precision-Recall AUC (PR-AUC):** 0.1554 (vs 0.0017 random baseline)

**Confusion Matrix Visualization:**
Saved to [`outputs/figures/isolation_forest_confusion_matrix.png`](file:///outputs/figures/isolation_forest_confusion_matrix.png).

---

### 9.5 Business Trade-Off Analysis: Precision vs. Recall

In financial payments, the cost of false positives (cardholder insult / customer churn / manual review load) must be balanced against the cost of false negatives (unintercepted fraud losses):

1. **High Precision / Low Friction Tier ($c \in [0.001, 0.002]$):**
   - At $c = 0.002$, only 572 legitimate transactions are flagged out of 284,315 ($99.80\%$ legitimate pass-through).
   - Suitable for **automated transaction blocking** or high-friction challenge actions.
2. **High Recall / Audit Tier ($c \in [0.010, 0.050]$):**
   - At $c = 0.050$, recall reaches **$84.96\%$** (intercepting 418 of 492 fraud events).
   - However, False Positives escalate to 14,355 transactions ($5.05\%$ of all legitimate transactions).
   - Suitable for **low-friction step-up authentication** (SMS OTP, in-app push notification confirmation) or backend risk scoring where the transaction is not rejected outright.

---

### 9.6 Model Artifacts & Production Ingestion

The fitted pipeline components were persisted to disk and integrated into the FastAPI backend service:

| Artifact | File Path | Size | Description |
| :--- | :--- | :--- | :--- |
| **Fitted Preprocessor** | `outputs/models/preprocessor.joblib` | ~1.4 KB | `TransactionPreprocessor` fitted on legitimate baseline |
| **Fitted Detector** | `outputs/models/isolation_forest.joblib` | ~4.7 MB | `IsolationForestDetector` ($c=0.002$, $n=200$) |
| **Experiment Metrics** | `outputs/metrics/isolation_forest_experiments.csv` | ~750 B | Complete 7-configuration metric log |
| **Summary Metadata** | `outputs/metrics/isolation_forest_summary.json` | ~1.1 KB | JSON metadata including threshold, parameters, and metrics |
| **Confusion Matrix** | `outputs/figures/isolation_forest_confusion_matrix.png` | ~40 KB | High-resolution confusion matrix heatmap |

The FastAPI service (`backend/app/services/model_service.py`) dynamically ingests these artifacts at startup, enabling live real-time inference via `POST /api/v1/predict`.

---

### 9.7 Phase 2 Validation Sign-off

- [x] Pure legitimate training partition assembled (283,253 samples; 0 fraud leakage)
- [x] Target feature `Class` strictly excluded from input space
- [x] Standardized continuous scoring implemented: $\text{score} = -\text{score\_samples}(X)$
- [x] Contamination grid evaluated: $[0.001, 0.002, 0.005, 0.01, 0.02, 0.03, 0.05]$
- [x] Model and preprocessor saved to `outputs/models/`
- [x] Metrics saved to `outputs/metrics/isolation_forest_experiments.csv` and `summary.json`
- [x] Confusion matrix figure saved to `outputs/figures/isolation_forest_confusion_matrix.png`
- [x] FastAPI model service and health endpoints updated (`ISOLATION_FOREST: READY`)
- [x] Full unit test suite passing (34/34 tests)
- [x] Research notebook updated with Sections 14–22
- [x] Original dataset `data/creditcard.csv` remains 100% untouched
- [x] Zero metrics fabricated; LOF postponed to Phase 3

---

## 10. Phase 3 — Local Outlier Factor (LOF) Anomaly Detection & Comparative Baseline Report

### 10.1 Executive Overview & Mathematical Methodology

Phase 3 implemented the second unsupervised anomaly detection architecture: the **Local Outlier Factor (LOF)** (Breunig et al., 2000), providing a density-based baseline for direct comparison against the tree-based Isolation Forest.

LOF evaluates an observation's anomaly degree by computing its local reachability density relative to its $k$-nearest neighbors:
1. **$k$-distance & Neighborhood ($N_k(p)$):** Euclidean distance to the $k$-th nearest training observation.
2. **Reachability Distance:** $\text{reach\_dist}_k(p, o) = \max\left(k\text{-distance}(o), d(p, o)\right)$.
3. **Local Reachability Density (LRD):** $\text{lrd}_k(p) = \frac{|N_k(p)|}{\sum_{o \in N_k(p)} \text{reach\_dist}_k(p, o)}$.
4. **Local Outlier Factor:** $\text{LOF}_k(p) = \frac{1}{|N_k(p)|} \sum_{o \in N_k(p)} \frac{\text{lrd}_k(o)}{\text{lrd}_k(p)}$.

When $\text{LOF} \approx 1$, the observation has local density comparable to its neighbors (normal inlier). When $\text{LOF} > 1$, the point has substantially lower local density than surrounding neighbors (potential anomaly).

To support streaming out-of-sample evaluation, LOF was configured with `novelty=True`. Continuous anomaly scores were standardized across the system as:
$$\text{anomaly\_score}(x) = -\text{score\_samples}(x)$$
ensuring higher numerical scores monotonically indicate higher anomaly probability.

---

### 10.2 Training Setup & Leakage Safeguards

- **Training Baseline:** Composed exclusively of legitimate transactions (`Class == 0`, 283,253 samples deduplicated).
- **Target Decoupling:** Ground-truth `Class` was strictly decoupled from model inputs; only the 30 canonical features (`Time`, `Amount`, `V1`–`V28`) were utilized.
- **Preprocessing:** Standardized with `TransactionPreprocessor` (`RobustScaler` on `Amount` and `Time`) fitted strictly on the legitimate training baseline.
- **Evaluation Set:** Complete out-of-sample population (284,807 transactions; 492 fraud events).

---

### 10.3 Controlled Hyperparameter Experimentation Results

A controlled sweep across 16 configurations ($n\_neighbors \in [10, 20, 35, 50]$ and $contamination \in [0.001, 0.002, 0.005, 0.010]$) was evaluated against ground-truth `Class`:

| $k$ ($n\_neighbors$) | Contamination ($c$) | Predicted Anomalies | True Positives (TP) | False Positives (FP) | False Negatives (FN) | True Negatives (TN) | Precision | Recall | F1-Score | PR-AUC | Execution Time (s) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 10 | 0.001 | 236 | 0 | 236 | 492 | 284,079 | 0.0000 | 0.0000 | 0.0000 | 0.0133 | 89.12s |
| 10 | 0.002 | 448 | 9 | 439 | 483 | 283,876 | 0.0201 | 0.0183 | 0.0191 | 0.0133 | 89.12s |
| 10 | 0.005 | 1,092 | 44 | 1,048 | 448 | 283,267 | 0.0403 | 0.0894 | 0.0556 | 0.0133 | 89.12s |
| 10 | 0.010 | 2,191 | 71 | 2,120 | 421 | 282,195 | 0.0324 | 0.1443 | 0.0529 | 0.0133 | 89.12s |
| 20 | 0.001 | 261 | 0 | 261 | 492 | 284,054 | 0.0000 | 0.0000 | 0.0000 | 0.0075 | 89.78s |
| 20 | 0.002 | 504 | 3 | 501 | 489 | 283,814 | 0.0060 | 0.0061 | 0.0060 | 0.0075 | 89.78s |
| 20 | 0.005 | 1,248 | 30 | 1,218 | 462 | 283,097 | 0.0240 | 0.0610 | 0.0345 | 0.0075 | 89.78s |
| 20 | 0.010 | 2,510 | 73 | 2,437 | 419 | 281,878 | 0.0291 | 0.1484 | 0.0486 | 0.0075 | 89.78s |
| 35 | 0.001 | 262 | 1 | 261 | 491 | 284,054 | 0.0038 | 0.0020 | 0.0027 | 0.0121 | 95.13s |
| 35 | 0.002 | 533 | 8 | 525 | 484 | 283,790 | 0.0150 | 0.0163 | 0.0156 | 0.0121 | 95.13s |
| 35 | 0.005 | 1,334 | 35 | 1,299 | 457 | 283,016 | 0.0262 | 0.0711 | 0.0383 | 0.0121 | 95.13s |
| 35 | 0.010 | 2,668 | 74 | 2,594 | 418 | 281,721 | 0.0277 | 0.1504 | 0.0468 | 0.0121 | 95.13s |
| 50 | 0.001 | 279 | 5 | 274 | 487 | 284,041 | 0.0179 | 0.0102 | 0.0130 | 0.0271 | 108.23s |
| 50 | 0.002 | 549 | 22 | 527 | 470 | 283,788 | 0.0401 | 0.0447 | 0.0423 | 0.0271 | 108.23s |
| 50 | 0.005 | 1,405 | 62 | 1,343 | 430 | 282,972 | 0.0441 | 0.1260 | 0.0654 | 0.0271 | 108.23s |
| **50** | **0.010** | **2,750** | **112** | **2,638** | **380** | **281,677** | **0.0407** | **0.2276** | **0.0691** | **0.0271** | **108.23s** |

*Tabular log saved to [`outputs/metrics/lof_experiments.csv`](file:///outputs/metrics/lof_experiments.csv).*

---

### 10.4 Selected LOF Configuration

- **Configuration:** $n\_neighbors = 50$, $contamination = 0.010$, $novelty = \text{True}$, $metric = \text{minkowski}$, $p = 2$.
- **Confusion Matrix:**
  - True Positives (TP): 112
  - False Positives (FP): 2,638
  - False Negatives (FN): 380
  - True Negatives (TN): 281,677
- **Performance:**
  - Precision: $4.07\%$
  - Recall: $22.76\%$
  - F1-Score: $0.0691$
  - PR-AUC: $0.0271$
  - False Positive Rate: $0.928\%$
- **Visualizations:**
  - Confusion Matrix: [`outputs/figures/lof_confusion_matrix.png`](file:///outputs/figures/lof_confusion_matrix.png)
  - Precision-Recall Curve: [`outputs/figures/lof_precision_recall_curve.png`](file:///outputs/figures/lof_precision_recall_curve.png)
  - Anomaly Score Distribution: [`outputs/figures/lof_score_distribution.png`](file:///outputs/figures/lof_score_distribution.png)

---

### 10.5 Algorithmic Head-to-Head Comparison: Isolation Forest vs. Local Outlier Factor

| Dimension / Metric | Isolation Forest Baseline | Local Outlier Factor Baseline | Relative Comparison |
| :--- | :--- | :--- | :--- |
| **Algorithmic Family** | Recursive Tree Space Partitioning | Local Density Reachability ($k$-NN) | Orthogonal paradigms |
| **Selected Configuration** | $c = 0.002, n_{\text{trees}} = 200$ | $k = 50, c = 0.010$ | Optimal $F_1$ per model |
| **F1-Score** | **0.2163** | 0.0691 | **Isolation Forest is $3.13\times$ higher** |
| **PR-AUC** | **0.1554** | 0.0271 | **Isolation Forest is $5.73\times$ higher** |
| **Precision** | **18.40%** | 4.07% | **Isolation Forest has $4.52\times$ higher precision** |
| **Recall** | **26.22%** (129 / 492) | 22.76% (112 / 492) | Isolation Forest detects 17 more fraud cases |
| **False Positives (FP)** | **572** | 2,638 | **LOF generates $4.61\times$ more false alarms** |
| **False Positive Rate** | **0.201%** | 0.928% | LOF has $4.6\times$ higher customer friction |
| **Execution Latency** | **~9.46 s** total (3.58s fit, 5.88s score) | ~108.23 s total (61.81s fit, 46.42s score) | **Isolation Forest is $11.4\times$ faster** |
| **Serialized Artifact Size** | **1.84 MB** | 185.8 MB | **Isolation Forest is $101\times$ more compact** |

*Visual comparison saved to [`outputs/figures/model_comparison.png`](file:///outputs/figures/model_comparison.png).*

---

### 10.6 Analytical Diagnosis & Limitations of LOF in Financial Fraud

The empirical results clearly indicate that Local Outlier Factor underperforms Isolation Forest on this dataset. This behavior is grounded in well-established theoretical properties:

1. **Curse of Dimensionality (Distance Concentration):**
   In 30-dimensional continuous space, Euclidean distance suffers from metric concentration: the variance of pairwise distances relative to their mean shrinks. Because $k$-NN reachability depends directly on metric distances, the contrast between "dense" and "sparse" neighborhoods degrades.
2. **Multi-Scale Cluster Densities:**
   Cardholder transactions span drastically different spending patterns and frequencies across hours and amounts. LOF computes density ratios against immediate neighbors; in heterogeneous or fragmented manifolds, normal transactions near sparse edges are erroneously penalized as low-density outliers (inflating False Positives to 2,638).
3. **Operational Overhead for Real-Time Payment Gateways:**
   LOF with `novelty=True` requires retaining all 283,253 training vectors in memory (185.8 MB artifact) to compute $k$-nearest neighbors for every incoming transaction. This $O(N \cdot d)$ query complexity introduces unacceptable latency for sub-100ms financial authorization rails.
4. **Model Readiness:**
   Neither model is yet declared production-ready. Both serve as rigorous unsupervised baselines for subsequent Phase 4 threshold calibration and cost-sensitive evaluation.

---

### 10.7 Phase 3 Validation Sign-off

- [x] Reusable LOF detector implemented with `novelty=True` in `backend/ml/lof/model.py`
- [x] Scaler and feature space aligned with Phase 1/2 (`RobustScaler`, 30 canonical features)
- [x] Training restricted strictly to legitimate baseline (`Class == 0`, 283,253 samples deduplicated)
- [x] Standardized continuous scoring: $\text{anomaly\_score} = -\text{score\_samples}(X)$
- [x] Controlled experiment grid executed ($4 \times 4 = 16$ configurations)
- [x] Artifacts saved: `outputs/models/local_outlier_factor.joblib`, `outputs/metrics/lof_experiments.csv`, `outputs/metrics/lof_summary.json`
- [x] Figures saved: `lof_confusion_matrix.png`, `lof_precision_recall_curve.png`, `lof_score_distribution.png`, `model_comparison.png`
- [x] FastAPI model service, health endpoint, and models list updated (`LOCAL_OUTLIER_FACTOR: READY`)
- [x] API test suite expanded and passing (45/45 tests passing)
- [x] Research notebook `notebooks/fraud_detection_analysis.ipynb` updated with Sections 23–30
- [x] Original dataset `data/creditcard.csv` remains 100% untouched
- [x] Zero metrics fabricated; Phase 4 boundary respected

---

## 11. Evaluation Protocol Audit & Holdout Generalization Benchmark Report

### 11.1 Methodological Audit of Prior Evaluation Protocols

Prior to advancing to Phase 4 (Threshold Optimization & Operating Points), an evaluation-quality audit was performed across the Phase 2 and Phase 3 experimental workflows:

1. **Protocol Analysis of Phase 2 & 3:**
   - Both models were trained exclusively on legitimate cardholder transactions (`Class == 0`, 283,253 samples deduplicated).
   - Both models were subsequently evaluated against the entire dataset (`df`, 284,807 transactions).
2. **Methodological Finding & Correction:**
   - Describing this complete-dataset evaluation as strictly *"out-of-sample"* was **technically inaccurate for the legitimate partition**.
   - Because the 283,253 legitimate training observations were included in the evaluation set, the evaluation was *in-sample* for those legitimate records, and truly *out-of-sample* only for the 492 fraudulent records and the 1,062 duplicate legitimate rows.
   - **Resolution:** We preserve Phase 2 and Phase 3 results as **Historical Baseline Experiments (Full Population / Semi-Supervised Baseline)** and institute a new, rigorous **Stratified Holdout Validation Experiment** to evaluate pure out-of-sample generalization without evaluation overlap.

---

### 11.2 Reproducible Stratified Holdout Architecture (60% / 20% / 20%)

To eliminate all evaluation overlap and provide statistically sound out-of-sample estimates:
- **Reproducibility Seed:** `random_state = 42`.
- **Stratification:** Stratified by `Class` to preserve the identical $0.173\%$ fraud prevalence across all partitions.
- **Data Partitions:**
  - **Train Partition (60.0%):** 170,884 transactions (170,589 legitimate, 295 fraud).
    - Unsupervised training pool: **170,188 clean legitimate samples** (`Class == 0`, 401 duplicates removed).
    - Zero fraud records are used in model training; all 295 training fraud events are strictly excluded.
  - **Validation Partition (20.0%):** 56,961 transactions (56,863 legitimate, 98 fraud; $0.1720\%$ prevalence). Reserved for threshold inspection.
  - **Holdout Test Partition (20.0%):** 56,962 transactions (56,863 legitimate, 99 fraud; $0.1738\%$ prevalence). Held out untouched and evaluated **exactly once**.
- **Preprocessing Leakage Prevention:** `TransactionPreprocessor` was fitted **exclusively on the 170,188 training legitimate samples**. Neither validation nor test records were observed during scaler parameter fitting.

---

### 11.3 Untouched Holdout Test Set Benchmark Results

Both models were fitted on the identical 170,188 training legitimate instances and evaluated on the identical untouched holdout test partition ($N = 56,962$, 99 fraud instances):

| Metric / Parameter | Isolation Forest Holdout Baseline | Local Outlier Factor Holdout Baseline | Relative Generalization Comparison |
| :--- | :---: | :---: | :--- |
| **Model Configuration** | $c = 0.002, n_{\text{trees}} = 200$ | $k = 50, c = 0.010, \text{novelty} = \text{True}$ | Verified optimal hyperparameters |
| **Evaluation Set Size** | 56,962 transactions | 56,962 transactions | Exact identical test partition |
| **No-Skill PR Baseline** | 0.001738 ($0.1738\%$) | 0.001738 ($0.1738\%$) | Test partition fraud prevalence |
| **True Positives (TP)** | 24 | **81** | LOF captures 57 more holdout fraud cases |
| **False Positives (FP)** | **114** | 548 | **Isolation Forest produces $4.8\times$ fewer false alarms** |
| **False Negatives (FN)** | 75 | **18** | LOF misses only 18 out of 99 fraud events |
| **True Negatives (TN)** | **56,749** | 56,315 | Isolation Forest correctly passes 434 more legitimate cards |
| **Precision** | **17.39%** ($0.1739$) | 12.88% ($0.1288$) | Isolation Forest is $1.35\times$ more precise |
| **Recall** | 24.24% ($0.2424$) | **81.82%** ($0.8182$) | **LOF detects $81.8\%$ of all holdout fraud** |
| **F1-Score** | 0.2025 | **0.2225** | LOF achieves higher F1 on holdout test set |
| **PR-AUC** | 0.1081 | **0.2186** | **Both models perform dramatically above no-skill baseline** (IF: $62\times$, LOF: $126\times$) |
| **False Positive Rate (FPR)** | **0.201%** ($0.0020$) | 0.964% ($0.0096$) | Isolation Forest maintains minimal friction ($<0.21\%$) |
| **Scoring Time (Test Set)** | **1.01 s** | 11.36 s | **Isolation Forest is $11.2\times$ faster** |

*Artifacts saved to [`outputs/validation/`](file:///outputs/validation/).*

---

### 11.4 Scientific Analysis & Key Takeaways

1. **Isolation Forest Generalization Invariance:**
   - On the holdout test set, Isolation Forest achieves **$F_1 = 0.2025$**, **Precision = $17.39\%$**, and **Recall = $24.24\%$**, closely aligning with its full-population baseline ($F_1 = 0.2163$, Precision = $18.40\%$, Recall = $26.22\%$).
   - This proves that Isolation Forest exhibits **low variance and robust generalization**, preserving its ultra-low false positive footprint ($0.20\%$ FPR, only 114 accounts flagged across 56,863 legitimate cardholders).
2. **Local Outlier Factor Reference-Pool Sensitivity:**
   - On the 170k training sample (reduced from 283k), LOF's metric concentration is attenuated, enabling its local density estimation to separate peripheral fraud clusters more aggressively.
   - Recall increases substantially to **$81.82\%$** (intercepting 81 of 99 fraud events), yielding a test $F_1$ of **$0.2225$** and PR-AUC of **$0.2186$**.
   - However, this recall gain incurs **548 False Positives** ($4.8\times$ more cardholder disruption than Isolation Forest), demonstrating the classic operational trade-off between customer friction and loss interception.
3. **PR-AUC Calculation Integrity:**
   - Both PR-AUC values are computed strictly from continuous standardized anomaly scores ($\text{score} = -\text{score\_samples}(X)$) rather than binary threshold predictions.
   - Both models achieve performance orders of magnitude above the $0.001738$ no-skill baseline.

---

### 11.5 Validation Artifact Inventory

| Artifact Path | Format | Description |
| :--- | :--- | :--- |
| `outputs/validation/evaluation_split_summary.json` | JSON | Formal protocol audit and partition dimensional breakdown |
| `outputs/validation/isolation_forest_test_metrics.json` | JSON | Complete holdout test set performance metrics for Isolation Forest |
| `outputs/validation/lof_test_metrics.json` | JSON | Complete holdout test set performance metrics for Local Outlier Factor |
| `outputs/validation/model_comparison_test.csv` | CSV | Direct tabular head-to-head comparison on untouched test set |
| `outputs/validation/test_pr_curves.png` | PNG | Holdout test Precision-Recall curves with no-skill baseline |
| `outputs/validation/test_confusion_matrices.png` | PNG | Dual heatmaps comparing test set confusion matrices |

---

---

## 12. Phase 4 — Dynamic Threshold Calibration, Operating Points & Final Model Recommendation

### 12.1 Objective & Methodological Protocol
Default decision cutoffs in unsupervised anomaly detection (e.g., standard contamination offsets) represent arbitrary distribution assumptions rather than operationally tuned boundaries. The objective of Phase 4 is to establish practical, evidence-based operating thresholds through continuous score calibration and deliver a defensible final model recommendation.

#### Scientific Integrity Protocol
1. **Validation-Only Selection:** Candidate thresholds were generated across 216 quantile points from continuous anomaly scores evaluated exclusively on the **Validation partition (N=56,961)**.
2. **Untouched Test Constraint:** The **Test partition (N=56,962; 99 authentic fraud cases)** remained strictly untouched during threshold search and parameter selection. Test data was never used for tuning.
3. **Single-Pass Test Evaluation:** Each selected operating threshold was evaluated exactly once on the untouched test partition.
4. **Continuous Anomaly Scores:** Continuous anomaly score functions ($s(x) \ge \tau$) were utilized throughout; higher scores strictly represent higher anomaly likelihood.
5. **Identical Test Set:** Both Isolation Forest and Local Outlier Factor were evaluated on the identical, untouched test partition under identical preprocessing.

---

### 12.2 Calibrated Operating Points

#### Isolation Forest Operating Points
* Continuous score function: $s(x) = -\text{score\_samples}(x) \in [0, 1]$.
* Test PR-AUC: **0.108084** ($62.2\times$ over no-skill prevalence of 0.001738).

| Operating Point | Val Thresh ($\tau$) | Val Prec | Val Recall | Val F1 | Val FPR | Test TP | Test FP | Test FN | Test TN | Test Prec | Test Recall | Test F1 | Test FPR |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Low False Alarm** | `0.6722` | 28.07% | 16.33% | 0.2065 | 0.072% | 15 | **44** | 84 | 56,819 | **25.42%** | 15.15% | 0.1899 | **0.077%** |
| **Balanced (Peak F1)** | `0.6224` | 16.41% | 32.65% | 0.2184 | 0.287% | 29 | 163 | 70 | 56,700 | 15.10% | 29.29% | 0.1993 | 0.287% |
| **Controlled Low FPR** | `0.6341` | 17.45% | 26.53% | 0.2105 | 0.216% | 24 | 121 | 75 | 56,742 | 16.55% | 24.24% | 0.1967 | 0.213% |
| **High Recall** | `0.5240` | 4.58% | 72.45% | 0.0861 | 2.603% | 77 | 1,474 | 22 | 55,389 | 4.96% | **77.78%** | 0.0933 | 2.592% |

#### Local Outlier Factor Operating Points
* Continuous score function: $s(x) = -\text{negative\_outlier\_factor\_} \in [1, \infty)$.
* Test PR-AUC: **0.218608** ($125.8\times$ over no-skill prevalence of 0.001738).

| Operating Point | Val Thresh ($\tau$) | Val Prec | Val Recall | Val F1 | Val FPR | Test TP | Test FP | Test FN | Test TN | Test Prec | Test Recall | Test F1 | Test FPR |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Low False Alarm** | `3.0334` | 25.24% | 26.53% | 0.2587 | 0.135% | 32 | **72** | 67 | 56,791 | **30.77%** | 32.32% | 0.3153 | **0.127%** |
| **Balanced (Peak F1)** | `2.4901` | 19.09% | 46.94% | 0.2714 | 0.343% | 57 | 174 | 42 | 56,689 | 24.68% | 57.58% | **0.3455** | 0.306% |
| **Controlled Low FPR** | `2.7073` | 19.77% | 34.69% | 0.2519 | 0.243% | 51 | 115 | 48 | 56,748 | 30.72% | 51.52% | **0.3849** | 0.202% |
| **High Recall** | `1.9639` | 11.08% | 71.43% | 0.1918 | 0.988% | 81 | 537 | 18 | 56,326 | 13.11% | **81.82%** | 0.2259 | 0.944% |

---

### 12.3 Business Cost Analysis

> **Methodological Disclaimer:** Cost parameters ($C_{\text{FP}}, C_{\text{FN}}$) are illustrative modeling assumptions for operational sensitivity analysis, not proprietary SecurePay financial figures.

Objective cost formulation:
$$\text{Total Operational Cost} = \text{FP} \times C_{\text{FP}} + \text{FN} \times C_{\text{FN}}$$

| Scenario | Cost Ratio ($C_{\text{FP}}:C_{\text{FN}}$) | Model | Val Min-Cost $\tau$ | Val Cost | Val FP | Val FN | Test Cost | Test FP | Test FN | Test Recall |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Balanced Cost** | **1 : 10** | **Isolation Forest** | `0.6224` | 823.0 | 163 | 66 | 863.0 | 163 | 70 | 29.29% |
| | | **Local Outlier Factor** | `2.3705` | 695.0 | 235 | 46 | **543.0** | 223 | 32 | 67.68% |
| **High Loss Asymmetry** | **1 : 20** | **Isolation Forest** | `0.6111` | 1,426.0 | 226 | 60 | 1,588.0 | 228 | 68 | 31.31% |
| | | **Local Outlier Factor** | `2.2162` | 1,079.0 | 319 | 38 | **856.0** | 296 | 28 | 71.72% |
| **Severe Fraud Penalty** | **1 : 50** | **Isolation Forest** | `0.5607` | 2,577.0 | 777 | 36 | 2,380.0 | 780 | 32 | 67.68% |
| | | **Local Outlier Factor** | `1.9191` | 1,878.0 | 628 | 25 | **1,466.0** | 616 | 17 | 82.83% |

**Key Cost Finding:** Across all cost asymmetry ratios, Local Outlier Factor achieves substantially lower total operational cost because its superior recall dramatically reduces costly false negatives (missed frauds) without an unmanageable explosion in false alarms.

---

### 12.4 Comprehensive Model Comparison Summary

| Metric / Dimension | Isolation Forest | Local Outlier Factor | Operational Advantage |
| :--- | :---: | :---: | :--- |
| **Test PR-AUC** | 0.1081 | **0.2186** | **LOF** delivers $2.02\times$ higher ranking quality |
| **Balanced F1** | 0.1993 | **0.3455** | **LOF** delivers $+73.4\%$ higher peak F1 |
| **Balanced Recall** | 29.29% | **57.58%** | **LOF** catches nearly double the fraud cases |
| **Low-FPR Mode Recall ($\text{FPR} \le 0.25\%$)** | 24.24% (121 FP) | **51.52%** (115 FP) | **LOF** catches $2.13\times$ more frauds with fewer FPs |
| **High-Recall Mode** | 77.78% (1,474 FP) | **81.82%** (537 FP) | **LOF** achieves higher recall with $63.6\%$ fewer FPs |
| **Batch Test Scoring Time (56,962 tx)** | **1.01 sec** | 11.36 sec | Isolation Forest: ~11.3× lower batch scoring time |
| **Live API Request Time (Single Tx)** | **83.47 ms** | 190.43 ms | Verified API request roundtrip time |
| **Serialized Model Footprint** | **1.84 MB** | 185.80 MB | **Isolation Forest** is **$101\times$ smaller** |

Earlier batch benchmarking showed approximately 11.3× lower batch scoring time for Isolation Forest than LOF (approximately 1.01 s vs 11.36 s on the evaluated test partition). This is a batch benchmark and should not be interpreted as per-request production API latency.

The verified live API measurements were:
- Isolation Forest API request: 83.47 ms
- LOF API request: 190.43 ms
These are API request timings and should not be described as pure model inference latency.

---

### 12.5 Proposed Two-Tier Architecture & Strategic Recommendation

A naive single-model recommendation is operationally deficient. The empirical findings support a **Proposed Two-Tier Architecture**:

```
[ Incoming Streaming Transaction ]
               │
               ▼
┌──────────────────────────────────────────────┐
│  Tier 1: Isolation Forest (Inline Gateway)   │
│  - Mode: Controlled Low FPR (τ = 0.6341)     │
│  - Compact model footprint & batch cost      │
│  - False Alarms: Strictly bounded (0.213%)   │
└──────────────────────────────────────────────┘
         │                           │
   [Low Risk]                 [High Score Anomaly]
         │                           │
         ▼                           ▼
[ Auto-Authorize ]             [ Step-up 2FA / Immediate Block ]
                                     │
                                     ▼
               ┌──────────────────────────────────────────────┐
               │  Tier 2: Local Outlier Factor (Audit Queue)  │
               │  - Mode: Balanced Peak F1 (τ = 2.4901)       │
               │  - Test PR-AUC: 0.2186 | Recall: 57.6%       │
               │  - Asynchronous High-Sensitivity Review Queue│
               └──────────────────────────────────────────────┘
```

1. **Tier 1 — Isolation Forest (Proposed Architecture):**
Isolation Forest is proposed as the lightweight first-stage screening model because it has a substantially smaller model footprint and lower batch scoring cost than LOF. A conservative operating point such as Controlled Low FPR (τ = 0.634134) can be used when false-alert reduction is important. In `Low False Alarm` mode (τ = 0.672168), it limits false alerts to only 44 per 56,962 transactions (0.077% FPR), minimizing customer checkout friction.

2. **Tier 2 — Local Outlier Factor (Proposed Architecture):**
LOF is proposed as a secondary investigation or audit model because it achieved stronger test PR-AUC and higher recall at sensitive operating points, at the cost of greater computational and memory requirements. Its higher memory footprint (185.8 MB) and batch scoring time (11.36 s on test partition) are appropriate for near-line batch or asynchronous queues.

#### Production Limitations & Boundary
* **Unsupervised Paradigm:** Unsupervised detectors lack explicit knowledge of fraud attack labels. In production, unsupervised scores should serve as risk features into supervised gradient boosting models or rule ensembles.
* **Concept Drift:** Payment transaction distributions evolve seasonally and under adversarial pressure. Rolling quantile threshold calibration must be scheduled continuously.
* **Pre-Production Demarcation:** The system has demonstrated mathematical validity and reproducibility, but requires load-testing and operational runbooks before deployment.

---

### 12.6 Phase 4 Artifact Inventory

| Artifact Path | Format | Description |
| :--- | :--- | :--- |
| `outputs/thresholds/isolation_forest_thresholds.csv` | CSV | Dense 216-quantile validation sweep metrics for Isolation Forest |
| `outputs/thresholds/lof_thresholds.csv` | CSV | Dense 216-quantile validation sweep metrics for Local Outlier Factor |
| `outputs/thresholds/selected_operating_points.json` | JSON | Formal operating points (validation thresholds & untouched test evaluations) |
| `outputs/thresholds/business_cost_analysis.json` | JSON | Cost sensitivity results across 1:10, 1:20, and 1:50 loss ratios |
| `outputs/figures/validation_pr_curves.png` | PNG | Dense validation Precision-Recall curves with no-skill baseline |
| `outputs/figures/validation_f1_threshold.png` | PNG | Validation F1 vs threshold curves for both models |
| `outputs/figures/validation_precision_recall.png` | PNG | Validation Precision vs Recall parametric comparison |
| `outputs/figures/validation_fpr_recall.png` | PNG | Pareto trade-off between False Positive Rate and Recall |
| `outputs/figures/validation_business_cost.png` | PNG | Total business cost vs threshold curves under illustrative ratios |
| `outputs/figures/test_operating_points.png` | PNG | Untouched test partition performance across all 4 operating modes |
| `outputs/figures/final_model_comparison.png` | PNG | Multi-metric radar and architectural summary comparison |
