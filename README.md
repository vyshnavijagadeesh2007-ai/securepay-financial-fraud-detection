# SecurePay AI — Real-Time Anomaly Detection in Financial Transactions

[![Phase](https://img.shields.io/badge/Project%20Status-Phase%204%20(Calibrated%20%26%20Complete)-2C4A8F)](#development-phases)
[![Architecture](https://img.shields.io/badge/Architecture-FastAPI%20%7C%20React%20%7C%20Scikit--Learn-141C2B)](#planned-technology-stack)
[![Design](https://img.shields.io/badge/Aesthetic-Editorial%20FinTech%20Instrument-E5DED0)](#visual-design-system)

---

## 1. Problem Statement

Financial payment rails process millions of electronic transactions every hour. Within these massive data streams, fraudulent transactions occur with extreme scarcity (~$0.173\%$ prevalence in European cardholder datasets), forming an **extreme class imbalance** scenario (~$578:1$ legitimate-to-fraudulent ratio).

Traditional supervised classification models struggle when minority class events evolve rapidly or where ground-truth labels are heavily delayed. **SecurePay AI** addresses this challenge through an unsupervised anomaly and novelty detection paradigm:
- Establishing an empirical mathematical baseline of legitimate transaction behavior ($\text{Class} = 0$).
- Identifying structural departures using **Isolation Forest** (tree-based recursive space partitioning) and **Local Outlier Factor (LOF)** (local density-based $k$-NN comparison).
- Providing calibrated threshold tuning, contamination hyperparameter sensitivity analysis, and real-time inference via a high-performance REST API.

---

## 2. Dataset Specification & Location

- **Dataset Location:** `data/creditcard.csv` (150,828,752 bytes, ~143.84 MiB)
- **Observations:** 284,807 transactions recorded over 48 hours in September 2013 by European cardholders.
- **Dimensionality:** 31 features:
  - `Time`: Elapsed seconds from the initial recorded transaction.
  - `Amount`: Monetary transaction amount (heavily right-skewed, range $\$0.00$ to $\$25,691.16$).
  - `V1` through `V28`: 28 numerical principal components resulting from PCA transformation for confidentiality.
  - `Class`: Ground-truth label ($0$ = Legitimate, $1$ = Fraud).
- **Class Balance:**
  - Legitimate ($\text{Class} = 0$): 284,315 observations ($99.827\%$)
  - Fraudulent ($\text{Class} = 1$): 492 observations ($0.173\%$)
- **Data Integrity:** 0 null values across all 31 features. 1,081 identical rows audited (1,062 in Class 0, 19 in Class 1).
- **Integrity Rule:** The raw dataset `data/creditcard.csv` remains strictly untouched. The `Class` column is **never passed as an input feature** during unsupervised model training; it is reserved exclusively for evaluation metrics.

---

## 3. Current Architecture

```
                    ┌───────────────────────────┐
                    │    data/creditcard.csv    │
                    │   (284,807 rows × 31 cols)│
                    └─────────────┬─────────────┘
                                  │ (Phase 0: Verified Read-Only)
                                  ▼
                    ┌───────────────────────────┐
                    │    Data / ML Pipeline     │
                    │  (Phase 1 & 2: Planned)   │
                    │  - RobustScaler Preproc   │
                    │  - Normal Baseline Split  │
                    │  - Isolation Forest & LOF │
                    └─────────────┬─────────────┘
                                  │ (Phase 2: Saved Artifacts)
                                  ▼
                    ┌───────────────────────────┐
                    │      FastAPI Backend      │
                    │    (Phase 0: Scaffolding) │
                    │  - REST Endpoints (/api)  │
                    │  - Pydantic v2 Contracts  │
                    │  - Status & Health Checks │
                    └─────────────┬─────────────┘
                                  │ (REST JSON via HTTP/CORS)
                                  ▼
                    ┌───────────────────────────┐
                    │    React + Vite Client    │
                    │    (Phase 0: Scaffolding) │
                    │  - Editorial FinTech UI   │
                    │  - Zero Fabricated Stats  │
                    │  - SVG Line Trace Metaphor│
                    └───────────────────────────┘
```

---

## 4. Planned Technology Stack

| Layer | Component | Version / Specification | Role |
| :--- | :--- | :--- | :--- |
| **Data Engine** | Python 3.14 + Pandas / NumPy | `pandas>=2.2`, `numpy>=1.26` | Ingestion, data hygiene, exploratory data analysis |
| **ML Engine** | Scikit-Learn + SciPy + Joblib | `scikit-learn>=1.4`, `joblib>=1.3` | RobustScaler, Isolation Forest, Local Outlier Factor, PR curves |
| **API Backend** | FastAPI + Uvicorn + Pydantic v2 | `fastapi>=0.110`, `uvicorn>=0.28` | High-throughput asynchronous REST inference & analytics server |
| **Frontend** | React 19 + Vite | `react>=19.0`, `vite>=6.0` | Modular component architecture, client-side routing |
| **Styling** | Vanilla CSS (Custom Design System) | Tokenized CSS variables | "Editorial FinTech research instrument" aesthetic |
| **Testing** | Pytest + FastAPI TestClient | `pytest>=8.0`, `httpx>=0.28` | Unit, schema contract, and regression testing |

---

## 5. Visual Design System

The application visual language rejects generic dark-neon "AI dashboard" templates in favor of a **scholarly, editorial FinTech research instrument**:

- **Color Palette:**
  - Primary Background: `#EFE9DD` (warm archival paper)
  - Secondary Background: `#E5DED0` (stationery card tone)
  - Primary Ink: `#141C2B` (deep analytical slate)
  - Secondary Ink: `#4A5364` (muted technical text)
  - Muted: `#767E8C` (subtle captions and metadata)
  - Accent Blue: `#2C4A8F` (*Accent only* — rules, hairline drawing vectors, active states, key tags)
  - Hairline: `rgba(20, 28, 43, 0.16)` (sharp mathematical dividers)
- **Typography:**
  - Headings & Statements: **Newsreader** (classic editorial serif with italic emphasis)
  - Body, Numerics, Metadata: **Courier Prime** (clean tabular monospaced)
- **Stylistic Directives:**
  - No gradients, no glassmorphism, no neon glows.
  - Zero border-radius (`border-radius: 0`) for sharp instrument edges.
  - Restrained SVG line drawing animation representing anomaly scoring traces.
  - Strict compliance with `prefers-reduced-motion`.

---

## 6. Planned Frontend Pages

All 8 pages are scaffolded with data integrity safeguards. Metric placeholders (`--`) are rendered until empirical models are executed in Phase 2.

1. **Home / Project Introduction:** Problem context, anomaly detection overview, directional CTAs, signature wordmark `SECUREPAY AI.`.
2. **Dashboard:** High-level operational metrics (`Total`, `Legitimate`, `Fraud`, `Precision`, `Recall`, `F1`). *(ML performance metrics marked `--` in Phase 0)*.
3. **Transaction Detection:** Single-transaction feature submission form ($Time$, $V_1$–$V_{28}$, $Amount$) with model selector and anomaly score readout. *(Status: `MODEL_NOT_TRAINED` in Phase 0)*.
4. **Analytics:** Exploratory distributions, skewness reports, PCA projection space, and extreme class imbalance visualizations.
5. **Model Lab:** Side-by-side empirical comparison between **Isolation Forest** and **Local Outlier Factor** (precision, recall, false positive rates, execution latency).
6. **Threshold Analysis:** Precision-Recall tradeoff curves, contamination grid experiments, and optimal boundary calibration.
7. **Transaction Explorer:** Filterable, paginated audit table for real transactions from `creditcard.csv`.
8. **Methodology / About:** In-depth technical documentation covering mathematical foundations, `RobustScaler`, assumptions, limitations, and future work.

---

## 7. Machine Learning Methodology (Planned)

1. **Feature Transformation:**
   - $V_1$ through $V_{28}$ are already zero-centered orthogonal PCA components.
   - $Time$ and $Amount$ are normalized using **`RobustScaler`**:
     $$x' = \frac{x - \text{median}(x)}{\text{IQR}(x)}$$
     Preventing extreme monetary outliers from corrupting scale parameters.
2. **Novelty Baseline Training Strategy:**
   - Train set: Composed exclusively of legitimate transactions ($\text{Class} = 0$).
   - The model learns the multidimensional boundary of legitimate customer purchasing behavior.
3. **Unsupervised Algorithms:**
   - **Isolation Forest:** Exploits the property that anomalous points require fewer recursive random splits to isolate.
   - **Local Outlier Factor (LOF):** Measures local density deviation relative to $k$-nearest neighbors (with `novelty=True` for test inference).
4. **Evaluation Protocol:**
   - Test set: Real-world mixed stream containing both legitimate and fraudulent transactions.
   - Metrics: Precision, Recall, $F_1$-score, Area under Precision-Recall Curve (PR-AUC), and Confusion Matrix.
   - Accuracy is explicitly rejected as an optimization criterion.

---

## 8. Development Phases

- [x] **Phase 0 — Architecture & Design Foundation:** *(Completed)*
  - Verified `data/creditcard.csv` presence and integrity ($284,807 \times 31$).
  - Established project structure, API contracts, domain models, and schemas.
  - Designed the stationery/editorial FinTech UI system.
  - Built verified test suite enforcing Phase 0 contracts.
- [x] **Phase 1 — Exploratory Data Analysis & Preprocessing Pipeline:** *(Completed)*
  - Rigorous EDA on class asymmetry ($99.827\%$ legit vs $0.173\%$ fraud, $1 : 578$ ratio).
  - Investigated 1,081 duplicate rows ($0.38\%$), verifying 0 conflicting class labels.
  - Analyzed 48-hour cyclical diurnal time dynamics and extreme positive monetary skewness ($16.98$, max $\$25,691.16$).
  - Generated and exported 5 publication-grade figures to `outputs/figures/`.
  - Computed and serialized structured metrics to `outputs/metrics/`.
  - Implemented and unit-tested reusable `TransactionPreprocessor` (`RobustScaler` on Amount & Time, zero PCA distortion, strict Class target isolation).
  - Updated research notebook `notebooks/fraud_detection_analysis.ipynb` through Sections 1–13.
- [x] **Phase 2 — Unsupervised Isolation Forest Anomaly Detection Baseline:** *(Completed)*
  - Trained Isolation Forest on clean legitimate cardholder partition (`Class == 0`, 283,253 samples deduplicated).
  - Evaluated contamination hyperparameter grid ($c \in [0.001, 0.002, 0.005, 0.01, 0.02, 0.03, 0.05]$) across out-of-sample population.
  - Selected optimal baseline $c = 0.002$ ($F_1 = 0.2163$, Precision = $18.40\%$, Recall = $26.22\%$, PR-AUC = $0.1554$, 572 FP).
  - Serialized pipeline artifacts (`preprocessor.joblib`, `isolation_forest.joblib`) to `outputs/models/`.
  - Exported confusion matrix figure to `outputs/figures/isolation_forest_confusion_matrix.png`.
  - Saved full experiment results and metadata to `outputs/metrics/`.
  - Integrated dynamic artifact loading into FastAPI backend (`ISOLATION_FOREST: READY`).
  - Updated research notebook `notebooks/fraud_detection_analysis.ipynb` (Sections 14–22).
  - Achieved 100% test pass rate across 34 unit tests.
- [x] **Phase 3 — Local Outlier Factor (LOF) & Unsupervised Density Comparison:** *(Completed)*
  - Implemented reusable Local Outlier Factor detector with `novelty=True` in `backend/ml/lof/model.py`.
  - Executed controlled hyperparameter grid across 16 configurations ($k \in [10, 20, 35, 50]$, $c \in [0.001, 0.002, 0.005, 0.010]$).
  - Selected optimal LOF baseline: $k=50, c=0.010$ ($F_1 = 0.0691$, Recall = $22.76\%$, Precision = $4.07\%$, PR-AUC = $0.0271$, 2,638 FP).
  - Serialized model artifact to `outputs/models/local_outlier_factor.joblib` (185.8 MB).
  - Generated and exported evaluation figures (`lof_confusion_matrix.png`, `lof_precision_recall_curve.png`, `lof_score_distribution.png`, `model_comparison.png`).
  - Conducted head-to-head empirical comparison: Isolation Forest proved superior ($3.13\times$ higher $F_1$, $5.73\times$ higher PR-AUC, $4.6\times$ fewer false alarms, $11.4\times$ faster runtime).
  - Integrated LOF serving into FastAPI backend (`LOCAL_OUTLIER_FACTOR: READY`).
  - Added unit test suite in `tests/test_lof.py` (45/45 total tests passing).
  - Updated research notebook `notebooks/fraud_detection_analysis.ipynb` (Sections 23–30).
- [x] **Phase 4 — Dynamic Threshold Calibration, Operating Points & Final Recommendation:** *(Completed)*
  - Implemented leak-free 60/20/20 stratified holdout protocol (`random_state = 42`); validation partition (N=56,961) used strictly for calibration.
  - Performed dense 216-quantile validation sweep across continuous anomaly scores for both Isolation Forest and Local Outlier Factor.
  - Calibrated 4 canonical operating points (`Low False Alarm`, `Balanced / Peak F1`, `Controlled Low FPR <= 0.25%`, `High Recall >= 70%`).
  - Evaluated selected thresholds once on untouched test partition (N=56,962; 99 fraud cases):
    - Isolation Forest: Test PR-AUC = **0.1081** ($62.2\times$ base), Balanced F1 = **0.1993** (Recall = $29.29\%$, 163 FP), Low FA = 44 FP ($0.077\%$ FPR).
    - Local Outlier Factor: Test PR-AUC = **0.2186** ($125.8\times$ base), Balanced F1 = **0.3455** (Recall = $57.58\%$, 174 FP), High Recall = $81.82\%$ (537 FP).
  - Executed configurable business cost sensitivity analysis across 1:10, 1:20, and 1:50 loss ratios.
  - Proposed a defensible **Two-Tier Architecture**:
    - **Tier 1 (Isolation Forest):** Proposed as the lightweight first-stage screening model because it has a substantially smaller model footprint (1.84 MB vs 185.8 MB) and lower batch scoring cost than LOF. A conservative operating point such as Controlled Low FPR (τ = 0.634134) can be used when false-alert reduction is important.
    - **Tier 2 (LOF):** Proposed as a secondary investigation or audit model because it achieved stronger test PR-AUC (0.2186 vs 0.1081) and higher recall at sensitive operating points, at the cost of greater computational and memory requirements.
  - Clarified performance metrics: Earlier batch benchmarking showed approximately 11.3× lower batch scoring time for Isolation Forest than LOF (approximately 1.01 s vs 11.36 s on the evaluated test partition). Verified live API request measurements were 83.47 ms for Isolation Forest and 190.43 ms for LOF (per-request API timings, not pure inference latency).
  - Integrated dynamic operating modes into FastAPI `/api/predict` and exposed calibrated metrics via `/api/threshold/operating-points`.
  - Added operating points matrix and interactive sensitivity controls to React frontend.
  - Exported all 11 Phase 4 artifacts and generated publication figures in `outputs/figures/`.
  - Comprehensive documentation compiled in `reports/performance_analysis_report.md` (Sections 1–20) and `reports/dataset_validation_report.md` (Section 12).
  - Achieved 100% test pass rate across all 60 tests in `pytest tests/`.

---

## 9. Data Integrity Notice

Before Phase 2 execution, all ML metrics in the interface display strictly as:
$$\text{Precision} \to -- \quad \text{Recall} \to -- \quad \text{F1} \to -- \quad \text{Status} \to \text{NOT TRAINED}$$
No synthetic or fabricated performance numbers are ever generated.
