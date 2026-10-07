import React, { useState, useEffect } from 'react';
import Navigation from './components/Navigation';
import SignalTrace from './components/SignalTrace';
import FooterWordmark from './components/FooterWordmark';

import HomePage from './pages/HomePage';
import DashboardPage from './pages/DashboardPage';
import DetectionPage from './pages/DetectionPage';
import AnalyticsPage from './pages/AnalyticsPage';
import ModelLabPage from './pages/ModelLabPage';
import ThresholdPage from './pages/ThresholdPage';
import ExplorerPage from './pages/ExplorerPage';
import MethodologyPage from './pages/MethodologyPage';

import './App.css';

export default function App() {
  const [activePage, setActivePage] = useState('home');

  // Scroll to top upon page navigation
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, [activePage]);

  const renderPage = () => {
    switch (activePage) {
      case 'home':
        return <HomePage onNavigate={setActivePage} />;
      case 'dashboard':
        return <DashboardPage onNavigate={setActivePage} />;
      case 'detection':
        return <DetectionPage />;
      case 'analytics':
        return <AnalyticsPage />;
      case 'model-lab':
        return <ModelLabPage onNavigate={setActivePage} />;
      case 'threshold':
        return <ThresholdPage />;
      case 'explorer':
        return <ExplorerPage />;
      case 'methodology':
        return <MethodologyPage />;
      default:
        return <HomePage onNavigate={setActivePage} />;
    }
  };

  return (
    <div className="app-shell">
      {/* Primary Navigation Masthead */}
      <Navigation activePage={activePage} setActivePage={setActivePage} />

      {/* Travelling Visual Element: Anomaly Trace Progress */}
      <SignalTrace activePage={activePage} onNavigate={setActivePage} />

      {/* Main Page Viewport */}
      <main id="main-content" className="app-main" tabIndex="-1">
        {renderPage()}
      </main>

      {/* Editorial Footer with Signature Wordmark */}
      <FooterWordmark />
    </div>
  );
}
