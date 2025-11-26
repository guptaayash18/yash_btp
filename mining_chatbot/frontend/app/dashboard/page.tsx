'use client';

import { useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { 
  TrendingUp, 
  Wind, 
  Flame, 
  MapPin, 
  Calendar, 
  BarChart3, 
  Home,
  AlertTriangle,
  Activity,
  Thermometer,
  Database
} from 'lucide-react';

export default function Dashboard() {
  const [selectedCategory, setSelectedCategory] = useState<'overview' | 'pollutant' | 'risk' | 'aqi'>('overview');

  const sections = [
    { id: 'overview', label: 'Overview', icon: BarChart3 },
    { id: 'pollutant', label: 'Pollutant Analysis', icon: Wind },
    { id: 'risk', label: 'Fire Risk', icon: Flame },
    { id: 'aqi', label: 'AQI Heatmaps', icon: AlertTriangle },
  ];

  const pollutantAnalyses = [
    { id: '01', title: 'Overall Distribution', file: '01_overall_distribution.png' },
    { id: '02', title: 'Monthly Trend (Stacked)', file: '02_monthly_trend_stacked.png' },
    { id: '03', title: 'Monthly Trend (Percentage)', file: '03_monthly_trend_percentage.png' },
    { id: '04', title: 'Flight Pattern Heatmap', file: '04_flight_pattern_heatmap.png' },
    { id: '05', title: 'Spatial Distribution', file: '05_spatial_distribution.png' },
    { id: '06', title: 'Day of Week Pattern', file: '06_day_of_week_pattern.png' },
    { id: '07', title: 'Temperature Correlation', file: '07_temperature_correlation.png' },
    { id: '08', title: 'Oxygen Correlation', file: '08_oxygen_correlation.png' },
    { id: '09', title: 'Weekly Time Series', file: '09_weekly_timeseries.png' },
    { id: '10', title: 'AQI Comparison', file: '10_aqi_comparison.png' },
    { id: '11', title: 'Seasonal Analysis', file: '11_seasonal_analysis.png' },
  ];

  const riskHeatmaps = [
    { title: 'Fire Risk Score - Maximum', file: 'FL01_FRS_Maximum_Risk_Heatmap.png', description: 'Maximum FRS over the entire year for each monitoring point' },
    { title: 'Fire Risk Score - 95th Percentile', file: 'FL01_FRS_P95_Heatmap.png', description: '95th percentile FRS showing consistent high-risk zones' },
  ];

  const aqiHeatmaps = [
    { title: 'AQI Gradient Heatmap', file: 'FL01_Beautiful_Gradient_Heatmap.png', description: 'Spatial distribution of dominant pollutants with smooth gradients' },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 shadow-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Database className="w-8 h-8 text-blue-600" />
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Mining Analytics Dashboard</h1>
                <p className="text-sm text-gray-600">Comprehensive Data Analysis & Visualizations</p>
              </div>
            </div>
            <Link 
              href="/"
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
            >
              <Home className="w-4 h-4" />
              Chatbot
            </Link>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <div className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex gap-2 overflow-x-auto">
            {sections.map((section) => {
              const Icon = section.icon;
              return (
                <button
                  key={section.id}
                  onClick={() => setSelectedCategory(section.id as any)}
                  className={`flex items-center gap-2 px-6 py-4 font-medium border-b-2 transition-colors whitespace-nowrap ${
                    selectedCategory === section.id
                      ? 'border-blue-600 text-blue-600'
                      : 'border-transparent text-gray-600 hover:text-gray-900'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  {section.label}
                </button>
              );
            })}
          </div>
        </div>
      </div>

      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Overview Section */}
        {selectedCategory === 'overview' && (
          <div className="space-y-6">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-2">Dashboard Overview</h2>
              <p className="text-gray-600">Comprehensive analysis of mining site air quality, pollutants, and fire risk data</p>
            </div>

            {/* Key Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="bg-white rounded-xl shadow-md border border-gray-200 p-6">
                <div className="flex items-center gap-3 mb-2">
                  <div className="p-2 bg-blue-100 rounded-lg">
                    <MapPin className="w-6 h-6 text-blue-600" />
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Monitoring Points</p>
                    <p className="text-2xl font-bold text-gray-900">15</p>
                  </div>
                </div>
                <p className="text-xs text-gray-500">Across mining site</p>
              </div>

              <div className="bg-white rounded-xl shadow-md border border-gray-200 p-6">
                <div className="flex items-center gap-3 mb-2">
                  <div className="p-2 bg-green-100 rounded-lg">
                    <Calendar className="w-6 h-6 text-green-600" />
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Data Coverage</p>
                    <p className="text-2xl font-bold text-gray-900">1 Year</p>
                  </div>
                </div>
                <p className="text-xs text-gray-500">65,700+ records</p>
              </div>

              <div className="bg-white rounded-xl shadow-md border border-gray-200 p-6">
                <div className="flex items-center gap-3 mb-2">
                  <div className="p-2 bg-orange-100 rounded-lg">
                    <Wind className="w-6 h-6 text-orange-600" />
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Pollutants Tracked</p>
                    <p className="text-2xl font-bold text-gray-900">5</p>
                  </div>
                </div>
                <p className="text-xs text-gray-500">PM10, PM2.5, CO, NOx, SO2</p>
              </div>

              <div className="bg-white rounded-xl shadow-md border border-gray-200 p-6">
                <div className="flex items-center gap-3 mb-2">
                  <div className="p-2 bg-red-100 rounded-lg">
                    <Flame className="w-6 h-6 text-red-600" />
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Risk Metrics</p>
                    <p className="text-2xl font-bold text-gray-900">FRS</p>
                  </div>
                </div>
                <p className="text-xs text-gray-500">Fire Risk Score + GR</p>
              </div>
            </div>

            {/* Key Insights */}
            <div className="bg-white rounded-xl shadow-md border border-gray-200 p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <TrendingUp className="w-6 h-6 text-blue-600" />
                Key Insights
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                  <h4 className="font-semibold text-gray-900 mb-2">Dominant Pollutant: NOx</h4>
                  <p className="text-sm text-gray-700">NOx is the dominant pollutant at most monitoring points, indicating significant combustion activities from mining operations and diesel vehicles.</p>
                </div>
                <div className="p-4 bg-orange-50 rounded-lg border border-orange-200">
                  <h4 className="font-semibold text-gray-900 mb-2">Seasonal Patterns</h4>
                  <p className="text-sm text-gray-700">Clear seasonal variations observed with higher pollutant concentrations during dry winter months (November-February).</p>
                </div>
                <div className="p-4 bg-red-50 rounded-lg border border-red-200">
                  <h4 className="font-semibold text-gray-900 mb-2">Fire Risk Hotspots</h4>
                  <p className="text-sm text-gray-700">Points 4, 8, and 11 show consistently high Fire Risk Scores, requiring enhanced safety monitoring and mitigation measures.</p>
                </div>
                <div className="p-4 bg-green-50 rounded-lg border border-green-200">
                  <h4 className="font-semibold text-gray-900 mb-2">Oxygen Correlation</h4>
                  <p className="text-sm text-gray-700">Inverse correlation between O2 percentage and combustion pollutants (CO, NOx) confirms combustion as primary pollution source.</p>
                </div>
              </div>
            </div>

            {/* Quick Access */}
            <div className="bg-white rounded-xl shadow-md border border-gray-200 p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Quick Access</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {sections.slice(1).map((section) => {
                  const Icon = section.icon;
                  return (
                    <button
                      key={section.id}
                      onClick={() => setSelectedCategory(section.id as any)}
                      className="p-4 bg-gradient-to-br from-gray-50 to-gray-100 hover:from-blue-50 hover:to-blue-100 rounded-lg border border-gray-200 hover:border-blue-300 transition-all text-left"
                    >
                      <Icon className="w-8 h-8 text-blue-600 mb-2" />
                      <h4 className="font-semibold text-gray-900">{section.label}</h4>
                      <p className="text-sm text-gray-600 mt-1">
                        {section.id === 'pollutant' && 'View detailed pollutant trends and distributions'}
                        {section.id === 'risk' && 'Analyze fire risk patterns and hotspots'}
                        {section.id === 'aqi' && 'Explore spatial AQI distributions'}
                      </p>
                    </button>
                  );
                })}
              </div>
            </div>
          </div>
        )}

        {/* Pollutant Analysis Section */}
        {selectedCategory === 'pollutant' && (
          <div className="space-y-6">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-2 flex items-center gap-3">
                <Wind className="w-8 h-8 text-blue-600" />
                Dominant Pollutant Analysis
              </h2>
              <p className="text-gray-600">Comprehensive trend analysis of dominant pollutants across the mining site</p>
            </div>

            <div className="grid grid-cols-1 gap-6">
              {pollutantAnalyses.map((analysis) => (
                <div key={analysis.id} className="bg-white rounded-xl shadow-md border border-gray-200 overflow-hidden">
                  <div className="p-6">
                    <h3 className="text-xl font-semibold text-gray-900 mb-4">{analysis.title}</h3>
                    <div className="relative w-full" style={{ minHeight: '400px' }}>
                      <Image
                        src={`/analysis/${analysis.file}`}
                        alt={analysis.title}
                        width={1200}
                        height={600}
                        className="w-full h-auto rounded-lg"
                        priority={analysis.id === '01'}
                      />
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Analysis Summary */}
            <div className="bg-white rounded-xl shadow-md border border-gray-200 p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Analysis Summary</h3>
              <div className="prose prose-slate max-w-none">
                <ul className="space-y-2 text-gray-700">
                  <li><strong>NOx Dominance:</strong> NOx is the dominant pollutant at 70-80% of monitoring points throughout the year.</li>
                  <li><strong>Spatial Patterns:</strong> Points 1, 2, 5, 6, 8, 9, 10, 14 show consistent NOx dominance, indicating proximity to diesel equipment and blasting zones.</li>
                  <li><strong>Temporal Variations:</strong> CO dominance increases during early morning hours (6-8 AM) due to cold starts and equipment operation.</li>
                  <li><strong>Seasonal Trends:</strong> Winter months show 20-30% higher pollutant concentrations due to temperature inversions and reduced atmospheric dispersion.</li>
                  <li><strong>Temperature Correlation:</strong> Moderate positive correlation (r=0.3-0.4) between temperature and pollutant levels during summer months.</li>
                  <li><strong>Oxygen Depletion:</strong> Strong inverse correlation (r=-0.7) between O2 percentage and combustion pollutants (CO, NOx).</li>
                </ul>
              </div>
            </div>
          </div>
        )}

        {/* Fire Risk Section */}
        {selectedCategory === 'risk' && (
          <div className="space-y-6">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-2 flex items-center gap-3">
                <Flame className="w-8 h-8 text-red-600" />
                Fire Risk Analysis
              </h2>
              <p className="text-gray-600">Intelligent analysis of fire risk patterns over time and space</p>
            </div>

            {/* Risk Categories */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="bg-green-50 border-2 border-green-300 rounded-lg p-4">
                <div className="flex items-center gap-2 mb-2">
                  <div className="w-4 h-4 bg-green-500 rounded"></div>
                  <h4 className="font-semibold text-gray-900">Low Risk</h4>
                </div>
                <p className="text-sm text-gray-700">FRS &lt; 0.3</p>
              </div>
              <div className="bg-yellow-50 border-2 border-yellow-300 rounded-lg p-4">
                <div className="flex items-center gap-2 mb-2">
                  <div className="w-4 h-4 bg-yellow-500 rounded"></div>
                  <h4 className="font-semibold text-gray-900">Moderate Risk</h4>
                </div>
                <p className="text-sm text-gray-700">0.3 ≤ FRS &lt; 0.5</p>
              </div>
              <div className="bg-orange-50 border-2 border-orange-300 rounded-lg p-4">
                <div className="flex items-center gap-2 mb-2">
                  <div className="w-4 h-4 bg-orange-500 rounded"></div>
                  <h4 className="font-semibold text-gray-900">High Risk</h4>
                </div>
                <p className="text-sm text-gray-700">0.5 ≤ FRS &lt; 0.7</p>
              </div>
              <div className="bg-red-50 border-2 border-red-300 rounded-lg p-4">
                <div className="flex items-center gap-2 mb-2">
                  <div className="w-4 h-4 bg-red-600 rounded"></div>
                  <h4 className="font-semibold text-gray-900">Critical Risk</h4>
                </div>
                <p className="text-sm text-gray-700">FRS ≥ 0.7</p>
              </div>
            </div>

            {/* Heatmaps */}
            <div className="grid grid-cols-1 gap-6">
              {riskHeatmaps.map((heatmap, idx) => (
                <div key={idx} className="bg-white rounded-xl shadow-md border border-gray-200 overflow-hidden">
                  <div className="p-6">
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">{heatmap.title}</h3>
                    <p className="text-sm text-gray-600 mb-4">{heatmap.description}</p>
                    <div className="relative w-full" style={{ minHeight: '400px' }}>
                      <Image
                        src={`/heatmaps/${heatmap.file}`}
                        alt={heatmap.title}
                        width={1200}
                        height={600}
                        className="w-full h-auto rounded-lg"
                        priority={idx === 0}
                      />
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Risk Mitigation */}
            <div className="bg-white rounded-xl shadow-md border border-gray-200 p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <AlertTriangle className="w-6 h-6 text-orange-600" />
                Risk Mitigation Recommendations
              </h3>
              <div className="space-y-4">
                <div className="p-4 bg-red-50 rounded-lg border-l-4 border-red-500">
                  <h4 className="font-semibold text-gray-900 mb-2">High-Risk Points (4, 8, 11)</h4>
                  <ul className="text-sm text-gray-700 space-y-1 list-disc list-inside">
                    <li>Install continuous gas monitoring systems with automated alerts</li>
                    <li>Implement enhanced ventilation and air circulation protocols</li>
                    <li>Restrict hot work activities during high-risk periods</li>
                    <li>Deploy portable fire suppression equipment at strategic locations</li>
                  </ul>
                </div>
                <div className="p-4 bg-orange-50 rounded-lg border-l-4 border-orange-500">
                  <h4 className="font-semibold text-gray-900 mb-2">Moderate-Risk Points (1, 2, 6)</h4>
                  <ul className="text-sm text-gray-700 space-y-1 list-disc list-inside">
                    <li>Regular gas detection surveys (weekly frequency)</li>
                    <li>Maintain proper equipment grounding and bonding</li>
                    <li>Enforce strict no-smoking policies in elevated risk zones</li>
                  </ul>
                </div>
                <div className="p-4 bg-blue-50 rounded-lg border-l-4 border-blue-500">
                  <h4 className="font-semibold text-gray-900 mb-2">General Recommendations</h4>
                  <ul className="text-sm text-gray-700 space-y-1 list-disc list-inside">
                    <li>Conduct quarterly fire risk assessments</li>
                    <li>Maintain Graham's Ratio below critical thresholds (GR &lt; 0.1)</li>
                    <li>Ensure CH4 concentrations remain below 1.25% (LEL)</li>
                    <li>Optimize diesel equipment operation to reduce CO emissions</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* AQI Section */}
        {selectedCategory === 'aqi' && (
          <div className="space-y-6">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-2 flex items-center gap-3">
                <AlertTriangle className="w-8 h-8 text-orange-600" />
                AQI Spatial Distribution
              </h2>
              <p className="text-gray-600">Air Quality Index visualization across monitoring points</p>
            </div>

            {/* AQI Categories */}
            <div className="grid grid-cols-2 md:grid-cols-6 gap-3">
              {[
                { label: 'Good', color: 'bg-green-500', range: '0-50' },
                { label: 'Satisfactory', color: 'bg-lime-500', range: '51-100' },
                { label: 'Moderate', color: 'bg-yellow-500', range: '101-200' },
                { label: 'Poor', color: 'bg-orange-500', range: '201-300' },
                { label: 'Very Poor', color: 'bg-red-500', range: '301-400' },
                { label: 'Severe', color: 'bg-purple-600', range: '401-500' },
              ].map((category) => (
                <div key={category.label} className="bg-white border border-gray-200 rounded-lg p-3">
                  <div className="flex items-center gap-2 mb-1">
                    <div className={`w-4 h-4 ${category.color} rounded`}></div>
                    <p className="font-semibold text-sm text-gray-900">{category.label}</p>
                  </div>
                  <p className="text-xs text-gray-600">{category.range}</p>
                </div>
              ))}
            </div>

            {/* Heatmaps */}
            <div className="grid grid-cols-1 gap-6">
              {aqiHeatmaps.map((heatmap, idx) => (
                <div key={idx} className="bg-white rounded-xl shadow-md border border-gray-200 overflow-hidden">
                  <div className="p-6">
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">{heatmap.title}</h3>
                    <p className="text-sm text-gray-600 mb-4">{heatmap.description}</p>
                    <div className="relative w-full" style={{ minHeight: '400px' }}>
                      <Image
                        src={`/heatmaps/${heatmap.file}`}
                        alt={heatmap.title}
                        width={1200}
                        height={600}
                        className="w-full h-auto rounded-lg"
                        priority
                      />
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* AQI Insights */}
            <div className="bg-white rounded-xl shadow-md border border-gray-200 p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">AQI Insights</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-4 bg-purple-50 rounded-lg border border-purple-200">
                  <h4 className="font-semibold text-gray-900 mb-2 flex items-center gap-2">
                    <Activity className="w-5 h-5 text-purple-600" />
                    NOx AQI Patterns
                  </h4>
                  <p className="text-sm text-gray-700">Most monitoring points show "Very Poor" to "Severe" NOx AQI levels (300-500+), indicating critical need for NOx emission controls and enhanced ventilation.</p>
                </div>
                <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                  <h4 className="font-semibold text-gray-900 mb-2 flex items-center gap-2">
                    <Thermometer className="w-5 h-5 text-blue-600" />
                    Spatial Variations
                  </h4>
                  <p className="text-sm text-gray-700">Points closer to active mining operations (1, 2, 8, 9) consistently show higher AQI values across all pollutants, suggesting localized pollution sources.</p>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-6 py-4 text-center text-sm text-gray-600">
          <p>Mining Analytics Dashboard | Data-Driven Insights for Safe Operations</p>
        </div>
      </footer>
    </div>
  );
}

