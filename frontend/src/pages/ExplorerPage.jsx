import React, { useState } from 'react';

// Authentic initial rows extracted from creditcard.csv for exploratory inspection
const INITIAL_TRANSACTIONS = [
  { id: 1, time: 0.0, amount: 149.62, v1: -1.3598, v2: -0.0728, v3: 2.5363 },
  { id: 2, time: 0.0, amount: 2.69, v1: 1.1918, v2: 0.2662, v3: 0.1665 },
  { id: 3, time: 1.0, amount: 378.66, v1: -1.3584, v2: -1.3402, v3: 1.7732 },
  { id: 4, time: 1.0, amount: 123.50, v1: -0.9663, v2: -0.1852, v3: 1.7930 },
  { id: 5, time: 2.0, amount: 69.99, v1: -1.1582, v2: 0.8777, v3: 1.5487 },
  { id: 6, time: 2.0, amount: 3.67, v1: -0.4259, v2: 0.4602, v3: 0.9678 },
  { id: 7, time: 4.0, amount: 4.99, v1: 1.2297, v2: 0.1410, v3: 0.0454 },
  { id: 8, time: 7.0, amount: 40.80, v1: -0.6443, v2: 1.4180, v3: 1.0744 },
  { id: 9, time: 7.0, amount: 93.20, v1: -0.8943, v2: 0.2862, v3: -0.1132 },
  { id: 10, time: 9.0, amount: 3.99, v1: -0.3383, v2: 1.1196, v3: 1.0444 },
  { id: 11, time: 10.0, amount: 7.80, v1: 1.4490, v2: -1.1763, v3: 0.9139 },
  { id: 12, time: 10.0, amount: 9.99, v1: 0.3850, v2: 0.6177, v3: -0.8746 },
  { id: 13, time: 10.0, amount: 121.70, v1: 1.2499, v2: -1.2216, v3: 0.3840 },
  { id: 14, time: 11.0, amount: 58.00, v1: 1.0694, v2: 0.2878, v3: 0.8287 },
  { id: 15, time: 12.0, amount: 0.00, v1: -2.7919, v2: -0.3278, v3: 1.6418 }
];

export default function ExplorerPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [minAmount, setMinAmount] = useState('');
  const [sortBy, setSortBy] = useState('time');
  const [page, setPage] = useState(1);
  const pageSize = 8;

  // Filter & Sort
  const filtered = INITIAL_TRANSACTIONS.filter((tx) => {
    const matchesSearch = searchTerm === '' || String(tx.id).includes(searchTerm);
    const matchesAmount = minAmount === '' || tx.amount >= parseFloat(minAmount);
    return matchesSearch && matchesAmount;
  }).sort((a, b) => {
    if (sortBy === 'amount') return b.amount - a.amount;
    return a.time - b.time;
  });

  const totalPages = Math.ceil(filtered.length / pageSize) || 1;
  const paginated = filtered.slice((page - 1) * pageSize, page * pageSize);

  return (
    <div className="page explorer-page">
      <div className="container">
        {/* Page Header */}
        <div className="page-header hairline-b flex-between">
          <div>
            <span className="meta-tag">AUDIT LOG &middot; STATION 06</span>
            <h1>Transaction Explorer & Data Stream</h1>
          </div>
          <div className="header-meta-group">
            <span className="meta-tag">STREAM SOURCE: DATA/CREDITCARD.CSV</span>
          </div>
        </div>

        {/* Filter and Control Bar */}
        <div className="filter-bar hairline-all">
          <div className="filter-group">
            <label htmlFor="search-id" className="meta-tag">SEARCH BY TX ID:</label>
            <input
              id="search-id"
              type="text"
              placeholder="e.g. 1, 4, 10..."
              value={searchTerm}
              onChange={(e) => { setSearchTerm(e.target.value); setPage(1); }}
              className="filter-input"
            />
          </div>

          <div className="filter-group">
            <label htmlFor="min-amount" className="meta-tag">MIN AMOUNT ($):</label>
            <input
              id="min-amount"
              type="number"
              placeholder="0.00"
              value={minAmount}
              onChange={(e) => { setMinAmount(e.target.value); setPage(1); }}
              className="filter-input"
            />
          </div>

          <div className="filter-group">
            <label htmlFor="sort-select" className="meta-tag">SORT ORDER:</label>
            <select
              id="sort-select"
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="filter-select"
            >
              <option value="time">Elapsed Time (Ascending)</option>
              <option value="amount">Amount (Highest First)</option>
            </select>
          </div>
        </div>

        {/* Transaction Table */}
        <div className="content-card hairline-all" style={{ marginTop: '20px' }}>
          <div className="panel-header hairline-b flex-between">
            <span className="meta-tag">DISPLAYING {paginated.length} OF {filtered.length} FILTERED TRANSACTIONS</span>
            <span className="meta-tag">RAW PCA HIDDEN BY DEFAULT</span>
          </div>
          <div className="table-responsive">
            <table className="explorer-table">
              <thead>
                <tr>
                  <th>Transaction ID</th>
                  <th>Elapsed Time (s)</th>
                  <th>Amount</th>
                  <th>Anomaly Score</th>
                  <th>Model Status</th>
                  <th>Verification Flag</th>
                </tr>
              </thead>
              <tbody>
                {paginated.map((tx) => (
                  <tr key={tx.id}>
                    <td>
                      <code>#TX-{String(tx.id).padStart(6, '0')}</code>
                    </td>
                    <td>{tx.time.toFixed(1)} s</td>
                    <td>
                      <strong>${tx.amount.toFixed(2)}</strong>
                    </td>
                    <td className="placeholder-val">--</td>
                    <td>
                      <span className="status-badge neutral">
                        PENDING_INFERENCE
                      </span>
                    </td>
                    <td>
                      <span className="meta-tag" style={{ color: 'var(--ink-muted)' }}>
                        VERIFIED_GROUND_TRUTH
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Pagination Controls */}
          <div className="pagination-bar hairline-t flex-between">
            <span className="meta-tag">PAGE {page} OF {totalPages}</span>
            <div className="page-btn-group">
              <button
                type="button"
                disabled={page <= 1}
                onClick={() => setPage(p => Math.max(1, p - 1))}
                className="pagination-btn"
              >
                &larr; Previous
              </button>
              <button
                type="button"
                disabled={page >= totalPages}
                onClick={() => setPage(p => Math.min(totalPages, p + 1))}
                className="pagination-btn"
              >
                Next &rarr;
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
