'use client';

import { useState } from 'react';
import axios from 'axios';
import dynamic from 'next/dynamic';
import Link from 'next/link';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { Send, Code2, BarChart3, Database, Loader2, LayoutDashboard } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

// Dynamically import Plotly to avoid SSR issues
const Plot = dynamic(() => import('react-plotly.js'), { ssr: false });

interface QueryResponse {
  answer: string;
  code?: string;
  visualization?: string;
  statistics?: Record<string, any>;
  citations?: string[];
}

export default function Home() {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState<QueryResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showCode, setShowCode] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!question.trim()) return;

    setLoading(true);
    setError('');
    setResponse(null);

    try {
      const res = await axios.post<QueryResponse>('http://localhost:8005/query', {
        question: question.trim()
      });

      setResponse(res.data);
      setShowCode(false);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'An error occurred while processing your question.');
    } finally {
      setLoading(false);
    }
  };

  const renderVisualization = () => {
    if (!response?.visualization) return null;

    try {
      const plotData = JSON.parse(response.visualization);
      return (
        <div className="mt-6">
          <div className="flex items-center gap-2 mb-3">
            <BarChart3 className="w-5 h-5 text-blue-600" />
            <h3 className="text-lg font-semibold text-gray-800">Visualization</h3>
          </div>
          <div className="bg-white p-4 rounded-lg border border-gray-200">
            <Plot
              data={plotData.data}
              layout={{
                ...plotData.layout,
                autosize: true,
                width: undefined,
                height: 400
              }}
              config={{ responsive: true }}
              style={{ width: '100%' }}
            />
          </div>
        </div>
      );
    } catch (e) {
      return null;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Database className="w-8 h-8 text-blue-600" />
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Mining Data Analytics</h1>
                <p className="text-sm text-gray-600">Intelligent Data Exploration System</p>
              </div>
            </div>
            <Link 
              href="/dashboard"
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
            >
              <LayoutDashboard className="w-4 h-4" />
              Dashboard
            </Link>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Input Section */}
        <div className="bg-white rounded-xl shadow-md border border-gray-200 p-6 mb-6">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="question" className="block text-sm font-medium text-gray-700 mb-2">
                Ask a question about the mining data
              </label>
              <textarea
                id="question"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Example: Why is NOx the dominant pollutant at Point 9?"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                rows={3}
                disabled={loading}
              />
            </div>

            <button
              type="submit"
              disabled={loading || !question.trim()}
              className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-medium py-3 px-6 rounded-lg transition-colors flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Analyzing...
                </>
              ) : (
                <>
                  <Send className="w-5 h-5" />
                  Analyze
                </>
              )}
            </button>
          </form>

          {error && (
            <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-800 text-sm">{error}</p>
            </div>
          )}
        </div>

        {/* Response Section */}
        {response && (
          <div className="space-y-6">
            {/* Main Answer */}
            <div className="bg-white rounded-xl shadow-md border border-gray-200 p-6">
              <h2 className="text-xl font-semibold text-gray-800 mb-4">Analysis Result</h2>
              <div className="prose prose-slate max-w-none">
                <ReactMarkdown 
                  remarkPlugins={[remarkGfm]}
                  className="text-gray-700 leading-relaxed"
                  components={{
                    h1: ({node, ...props}) => <h1 className="text-2xl font-bold mt-4 mb-2 text-gray-900" {...props} />,
                    h2: ({node, ...props}) => <h2 className="text-xl font-bold mt-3 mb-2 text-gray-900" {...props} />,
                    h3: ({node, ...props}) => <h3 className="text-lg font-semibold mt-2 mb-1 text-gray-900" {...props} />,
                    p: ({node, ...props}) => <p className="mb-3" {...props} />,
                    ul: ({node, ...props}) => <ul className="list-disc list-inside mb-3 space-y-1" {...props} />,
                    ol: ({node, ...props}) => <ol className="list-decimal list-inside mb-3 space-y-1" {...props} />,
                    li: ({node, ...props}) => <li className="ml-4" {...props} />,
                    strong: ({node, ...props}) => <strong className="font-semibold text-gray-900" {...props} />,
                    em: ({node, ...props}) => <em className="italic" {...props} />,
                    code: ({node, inline, ...props}: any) => 
                      inline ? (
                        <code className="bg-gray-100 px-1.5 py-0.5 rounded text-sm font-mono text-red-600" {...props} />
                      ) : (
                        <code className="block bg-gray-100 p-3 rounded text-sm font-mono overflow-x-auto" {...props} />
                      ),
                  }}
                >
                  {response.answer}
                </ReactMarkdown>
              </div>

              {response.citations && response.citations.length > 0 && (
                <div className="mt-4 pt-4 border-t border-gray-200">
                  <p className="text-xs text-gray-500 font-medium mb-1">Data Sources:</p>
                  {response.citations.map((citation, idx) => (
                    <p key={idx} className="text-xs text-gray-600">
                      {citation}
                    </p>
                  ))}
                </div>
              )}
            </div>

            {/* Visualization */}
            {renderVisualization()}

            {/* Code Section */}
            {response.code && (
              <div className="bg-white rounded-xl shadow-md border border-gray-200 overflow-hidden">
                <button
                  onClick={() => setShowCode(!showCode)}
                  className="w-full px-6 py-4 flex items-center justify-between hover:bg-gray-50 transition-colors"
                >
                  <div className="flex items-center gap-2">
                    <Code2 className="w-5 h-5 text-gray-600" />
                    <h3 className="text-lg font-semibold text-gray-800">Generated Analysis Code</h3>
                  </div>
                  <span className="text-sm text-gray-500">
                    {showCode ? 'Hide' : 'Show'}
                  </span>
                </button>
                
                {showCode && (
                  <div className="border-t border-gray-200">
                    <SyntaxHighlighter
                      language="python"
                      style={vscDarkPlus}
                      customStyle={{
                        margin: 0,
                        borderRadius: 0,
                        fontSize: '0.875rem'
                      }}
                    >
                      {response.code}
                    </SyntaxHighlighter>
                  </div>
                )}
              </div>
            )}

            {/* Statistics */}
            {response.statistics && Object.keys(response.statistics).length > 0 && (
              <div className="bg-white rounded-xl shadow-md border border-gray-200 p-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-3">Analysis Statistics</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {Object.entries(response.statistics).map(([key, value]) => (
                    <div key={key} className="bg-gray-50 rounded-lg p-3">
                      <p className="text-xs text-gray-600 mb-1">{key.replace(/_/g, ' ')}</p>
                      <p className="text-lg font-semibold text-gray-900">{value}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Sample Questions */}
        {!response && !loading && (
          <div className="bg-white rounded-xl shadow-md border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Sample Questions</h3>
            <div className="space-y-2">
              {[
                "Why is NOx the dominant pollutant at most locations?",
                "What is the trend of Fire Risk Score over time?",
                "Which monitoring points have the highest AQI values?",
                "Why is the O2 percentage lower at certain points?",
                "Is the working environment safe based on current data?",
                "What mitigation strategies are recommended for high NOx levels?"
              ].map((q, idx) => (
                <button
                  key={idx}
                  onClick={() => setQuestion(q)}
                  className="w-full text-left px-4 py-3 bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors text-sm text-gray-700"
                >
                  {q}
                </button>
              ))}
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-6 py-4 text-center text-sm text-gray-600">
          <p>Powered by Multi-Agent AI System | OpenAI GPT-4o | FastAPI + Next.js</p>
        </div>
      </footer>
    </div>
  );
}

