"use client"

import React, { useState } from 'react';
import { UploadCloud, Wand2, FileText, Briefcase, AlertCircle, CheckCircle, Loader2 } from 'lucide-react';
import UploadZone from './components/UploadZone';
import ScoreGauge from './components/ScoreGauge';
import PersonalityBars from './components/PersonalityBars';
import TailorView from './components/TailorView';
import RejectionRiskCard from './components/RejectionRiskCard';
import GapAnalysis from './components/GapAnalysis';
import RecommendationsList from './components/RecommendationsList';
import { analyzeResume, tailorResume, AnalyzeResponse, TailorResponse } from './services/api';

export default function Home() {
  const [resumeText, setResumeText] = useState("");
  const [resumeFileName, setResumeFileName] = useState("");
  const [jdText, setJdText] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<AnalyzeResponse | null>(null);
  const [tailoredResult, setTailoredResult] = useState<TailorResponse | null>(null);
  const [tab, setTab] = useState<'analyze' | 'tailor'>('analyze');

  const handleAnalyze = async () => {
    if (!resumeText || !jdText) return;
    setLoading(true);
    setError(null);
    setTailoredResult(null);
    try {
      const data = await analyzeResume(resumeText, jdText);
      setResult(data);
    } catch (err: any) {
      // Graceful error handling
      if (err.response && err.response.status === 400) {
        // Expected validation error - use warn to avoid Next.js error overlay
        console.warn("Input Validation Error:", err.response.data.detail);
        setError(err.response.data.detail);
      } else {
        // Unexpected system error
        console.error("Analysis Error:", err);
        setError("Analysis failed. Please check the backend connection.");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleTailor = async () => {
    if (!resumeText || !jdText || !result) return;
    setLoading(true);
    setError(null);
    try {
      // Pass the detected design style from the analysis result
      const data = await tailorResume(resumeText, jdText, result.design_style);
      setTailoredResult(data);
      setTab('tailor');
    } catch (err) {
      console.error(err);
      setError("Tailoring failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-50 pb-20 font-sans">
      {/* Header */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2 cursor-pointer" onClick={() => { setResult(null); setError(null); setJdText(""); }}>
            <div className={`p-2 rounded-lg transition-colors ${result ? 'bg-slate-100' : 'bg-blue-600'}`}>
              <FileText className={`w-5 h-5 ${result ? 'text-slate-600' : 'text-white'}`} />
            </div>
            <h1 className="text-xl font-bold text-slate-900">REZUAI</h1>
          </div>
          {result && (
            <button onClick={() => { setResult(null); setError(null); setJdText(""); }} className="text-sm text-slate-500 hover:text-slate-800 font-medium">
              Start New Analysis
            </button>
          )}
        </div>
      </header>

      {/* VIEW 1: INPUT MODE */}
      {!result ? (
        <div className="max-w-3xl mx-auto px-4 py-12 animate-in fade-in slide-in-from-bottom-4 duration-500">
          <div className="text-center mb-10">
            <h2 className="text-3xl font-bold text-slate-900 mb-3">Optimize your resume for any job</h2>
            <p className="text-slate-600 text-lg">Paste your specific job description and we'll tailor your resume instantly.</p>
          </div>

          {error && (
            <div className="mb-6 bg-red-50 border border-red-200 text-red-700 p-4 rounded-xl flex items-start gap-3">
              <AlertCircle className="w-5 h-5 mt-0.5 shrink-0" />
              <div>
                <h3 className="font-semibold">Analysis Failed</h3>
                <p className="text-sm opacity-90">{error}</p>
              </div>
            </div>
          )}

          <div className="space-y-6">
            <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
              <div className="flex items-center justify-between mb-4">
                <h2 className="font-semibold text-slate-800 flex items-center gap-2">
                  <FileText className="w-4 h-4 text-blue-500" /> Your Resume
                </h2>
              </div>
              <UploadZone
                onFileLoaded={(text, fileName) => {
                  setResumeText(text);
                  setResumeFileName(fileName);
                  setError(null);
                }}
                fileName={resumeFileName}
                onClear={() => {
                  setResumeText("");
                  setResumeFileName("");
                }}
              />
            </div>

            <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
              <div className="flex items-center justify-between mb-4">
                <h2 className="font-semibold text-slate-800 flex items-center gap-2">
                  <Briefcase className="w-4 h-4 text-purple-500" /> Job Description
                </h2>
              </div>
              <textarea
                className="w-full h-40 p-3 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all font-mono resize-y"
                placeholder="Paste the job description here..."
                value={jdText}
                onChange={(e) => { setJdText(e.target.value); setError(null); }}
              />
            </div>

            <button
              onClick={handleAnalyze}
              disabled={loading || !resumeText || !jdText}
              className="w-full bg-slate-900 hover:bg-black text-white font-semibold py-4 px-6 rounded-xl shadow-xl shadow-slate-900/10 transition-all flex items-center justify-center gap-3 text-lg disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? <Loader2 className="animate-spin" /> : <Wand2 className="w-5 h-5" />}
              {loading ? "Analyzing..." : "Analyze Match"}
            </button>
          </div>
        </div>
      ) : (

        /* VIEW 2: RESULTS DASHBOARD */
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-in fade-in zoom-in-95 duration-500">

          <div className="flex flex-col md:flex-row gap-6 mb-8 items-start justify-between">
            <div>
              <h2 className="text-2xl font-bold text-slate-900">Analysis Results</h2>
              <div className="flex items-center gap-2 text-sm text-slate-500 mt-1">
                <span className="capitalize px-2 py-0.5 bg-slate-100 rounded text-slate-700 font-medium">
                  {result.detected_domain} Domain
                </span>
                <span>•</span>
                <span className="capitalize px-2 py-0.5 bg-slate-100 rounded text-slate-700 font-medium">
                  {result.design_style} Style Detected
                </span>
              </div>
            </div>

            <div className="flex gap-1 bg-white p-1 rounded-lg border border-slate-200 shadow-sm">
              <button
                onClick={() => setTab('analyze')}
                className={`px-4 py-2 rounded-md text-sm font-medium transition-all ${tab === 'analyze' ? 'bg-slate-100 text-slate-900' : 'text-slate-500 hover:text-slate-700'}`}
              >
                Match Report
              </button>
              <button
                onClick={() => {
                  if (!tailoredResult) handleTailor();
                  else setTab('tailor');
                }}
                disabled={loading}
                className={`px-4 py-2 rounded-md text-sm font-medium transition-all flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed ${tab === 'tailor' ? 'bg-purple-50 text-purple-700' : 'text-slate-500 hover:text-slate-700'}`}
              >
                <Wand2 className="w-3 h-3" />
                {tailoredResult ? "Tailored Resume" : "Generate Tailored Resume"}
              </button>
            </div>
          </div>

          {error && (
            <div className="mb-6 bg-red-50 border border-red-200 text-red-700 p-4 rounded-xl flex items-start gap-3">
              <AlertCircle className="w-5 h-5 mt-0.5 shrink-0" />
              <div>
                <h3 className="font-semibold">Action Failed</h3>
                <p className="text-sm opacity-90">{error}</p>
              </div>
            </div>
          )}

          {/* DASHBOARD CONTENT */}
          {tab === 'analyze' ? (
            <div className="space-y-6">
              {/* Rejection Risk - Top Priority */}
              {result.rejection_risk && (
                <RejectionRiskCard risk={result.rejection_risk} />
              )}

              {/* Scores */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <ScoreGauge score={result.overall_score} label="Overall Match" color={result.overall_score > 70 ? "#16a34a" : "#ca8a04"} />
                <div className="md:col-span-2 grid grid-cols-2 gap-6">
                  <ScoreGauge score={result.technical_score} label="Technical" />
                  <ScoreGauge score={result.personality_score} label="Cultural Fit" color="#ec4899" />
                </div>
              </div>

              {/* Gap Analysis */}
              {result.gaps && result.gaps.length > 0 && (
                <GapAnalysis gaps={result.gaps} />
              )}

              {/* Recommendations */}
              {result.recommendations && result.recommendations.length > 0 && (
                <RecommendationsList recommendations={result.recommendations} />
              )}

              {/* Existing Components - Personality Bars & Suggestions */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <PersonalityBars traits={result.traits} />
                <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
                  <h3 className="font-semibold text-slate-800 mb-4 flex items-center gap-2">
                    <AlertCircle className="w-4 h-4 text-amber-500" /> Additional Insights
                  </h3>
                  <div className="space-y-3 max-h-60 overflow-y-auto pr-2 custom-scrollbar">
                    {result.suggestions.map((s, i) => (
                      <div key={i} className="text-sm p-3 bg-amber-50 text-amber-900 rounded-lg border border-amber-100 leading-relaxed">
                        {s}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="animate-in fade-in slide-in-from-right-8 duration-300">
              {loading ? (
                <div className="h-96 flex flex-col items-center justify-center text-slate-400">
                  <Loader2 className="w-10 h-10 animate-spin mb-4 text-purple-500" />
                  <p>Optimizing your resume content...</p>
                </div>
              ) : tailoredResult ? (
                <TailorView data={tailoredResult} />
              ) : null}
            </div>
          )}
        </div>
      )}
    </main>
  );
}
