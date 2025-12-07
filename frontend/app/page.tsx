'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { AlertTriangle, Clock } from 'lucide-react';
import Link from 'next/link';

import AnalysisForm from './components/AnalysisForm';
import ResultCard from './components/ResultCard';

export default function Home() {
  const [inputType, setInputType] = useState<'text' | 'url'>('text');
  const [text, setText] = useState('');
  const [url, setUrl] = useState('');

  const [result, setResult] = useState<string | null>(null);
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    const content = inputType === 'text' ? text : url;
    if (!content.trim()) return;
    
    setLoading(true);
    setError(null);
    setResult(null);
    setData(null);

    try {
      const payload = inputType === 'text' ? { text } : { text: "", url };
      
      // Use environment variable or default
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
         if (response.status === 503) {
            throw new Error('Service validation failed or model not ready.');
         }
        throw new Error('Failed to connect to the analysis service.');
      }

      const responseData = await response.json();
      setResult(responseData.prediction);
      setData(responseData);
    } catch (err: any) {
      setError(err.message || 'An error occurred while analyzing the text.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-950 text-white flex flex-col items-center justify-center p-4 font-sans selection:bg-blue-500/30">
        
       {/* History Link (Top Right) */}
       <div className="absolute top-6 right-6">
         <Link href="/history" className="flex items-center space-x-2 text-gray-400 hover:text-white transition-colors">
            <Clock className="w-5 h-5" />
            <span className="text-sm font-medium">History</span>
         </Link>
       </div>

      <main className="w-full max-w-3xl bg-gray-900/80 backdrop-blur-xl border border-gray-800 rounded-2xl shadow-2xl overflow-hidden mt-10 mb-10">
        <div className="p-8 md:p-10">
          <motion.div 
            initial={{ y: -20 }}
            animate={{ y: 0 }}
            transition={{ duration: 0.5 }}
            className="text-center mb-8"
          >
            <h1 className="text-4xl md:text-5xl font-extrabold mb-3 bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500 bg-clip-text text-transparent tracking-tight">
              AI Fake News Detector
            </h1>
            <p className="text-gray-400 text-lg">
              Analyze news credibility with advanced AI and real-time verification.
            </p>
          </motion.div>

          <AnalysisForm 
             inputType={inputType}
             setInputType={setInputType}
             text={text}
             setText={setText}
             url={url}
             setUrl={setUrl}
             onAnalyze={handleAnalyze}
             loading={loading}
          />

          <AnimatePresence>
            {error && (
              <motion.div 
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                className="mt-6 p-4 bg-red-900/20 border border-red-800/50 rounded-xl text-red-200 text-center flex items-center justify-center space-x-2"
              >
                <AlertTriangle className="h-5 w-5" />
                <span>{error}</span>
              </motion.div>
            )}
          </AnimatePresence>
            
          {result && (
              <ResultCard result={result} data={data} />
          )}

        </div>
        <div className="bg-gray-950/50 p-4 text-center text-xs text-gray-600 border-t border-gray-800/50 backdrop-blur-sm">
          Powered by Scikit-learn & FastAPI • v2.0
        </div>
      </main>
    </div>
  );
}
