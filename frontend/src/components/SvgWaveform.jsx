import React from 'react';

/**
 * Metaphorical SVG line animation representing anomaly detection / transaction signal.
 * Draws itself on entry using the accent blue (#2C4A8F), remaining thin and mathematically restrained.
 */
export default function SvgWaveform({ height = 70, className = "" }) {
  return (
    <div className={`svg-waveform-container ${className}`} role="img" aria-label="Transaction signal wave trace">
      <svg
        viewBox="0 0 1000 120"
        preserveAspectRatio="none"
        className="waveform-svg"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        style={{ height: `${height}px`, width: '100%' }}
      >
        {/* Baseline grid guides */}
        <line x1="0" y1="60" x2="1000" y2="60" stroke="rgba(20, 28, 43, 0.1)" strokeWidth="1" strokeDasharray="4 4" />
        <line x1="0" y1="20" x2="1000" y2="20" stroke="rgba(20, 28, 43, 0.06)" strokeWidth="1" />
        <line x1="0" y1="100" x2="1000" y2="100" stroke="rgba(20, 28, 43, 0.06)" strokeWidth="1" />

        {/* Drawn signal path */}
        <path
          d="M0,60 L120,60 L140,56 L160,63 L180,59 L220,60 L240,48 L255,75 L270,30 L285,92 L300,18 L315,85 L330,60 L440,60 L470,55 L490,64 L520,60 L620,60 L640,42 L655,78 L670,60 L780,60 L800,52 L815,68 L830,60 L1000,60"
          stroke="#2C4A8F"
          strokeWidth="1.75"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="waveform-path"
        />

        {/* Anomaly inspection target marker */}
        <circle cx="300" cy="18" r="3" fill="#2C4A8F" />
        <circle cx="300" cy="18" r="8" stroke="#2C4A8F" strokeWidth="1" strokeDasharray="2 2" />
        <text x="312" y="16" fill="#2C4A8F" fontFamily="var(--font-mono)" fontSize="10" letterSpacing="0.05em">
          [TARGET_ANOMALY_TRACE]
        </text>
      </svg>
    </div>
  );
}
