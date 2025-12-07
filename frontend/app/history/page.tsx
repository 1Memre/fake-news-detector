'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { ArrowLeft, Clock, Search, ExternalLink } from 'lucide-react';

interface PredictionRecord {
  id: number;
  text: string;
  prediction: string;
  confidence: string;
  timestamp: string;
}

export default function HistoryPage() {
  const [history, setHistory] = useState<PredictionRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
        const response = await fetch(`${apiUrl}/history?limit=50`);
        if (!response.ok) {
          throw new Error('Failed to fetch history');
        }
        const data = await response.json();
        setHistory(data);
      } catch (err) {
        console.error(err);
        setError('Could not load history. Is the backend running?');
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, []);

  return (
    <div className="min-h-screen bg-gray-950 text-white p-6 font-sans selection:bg-blue-500/30">
      <div className="max-w-4xl mx-auto">
        <header className="flex items-center justify-between mb-8">
          <div className="flex items-center space-x-4">
            <Link 
              href="/"
              className="p-2 bg-gray-800/50 rounded-lg hover:bg-gray-700 transition-colors text-gray-400 hover:text-white"
            >
              <ArrowLeft className="h-5 w-5" />
            </Link>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
              Analysis History
            </h1>
          </div>
        </header>

        {loading ? (
          <div className="flex flex-col items-center justify-center py-20 text-gray-500">
             <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-blue-500 mb-4"></div>
             <p>Loading records...</p>
          </div>
        ) : error ? (
           <div className="p-8 bg-red-900/10 border border-red-800/30 rounded-xl text-center">
             <p className="text-red-400">{error}</p>
           </div>
        ) : history.length === 0 ? (
          <div className="text-center py-20 bg-gray-900/50 rounded-2xl border border-gray-800 border-dashed">
            <Search className="h-12 w-12 text-gray-600 mx-auto mb-4" />
            <h3 className="text-xl font-medium text-gray-400 mb-2">No History Found</h3>
            <p className="text-gray-500 mb-6">You haven't analyzed any news yet.</p>
            <Link 
              href="/"
              className="inline-flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg transition-colors"
            >
              Start Analyzing
            </Link>
          </div>
        ) : (
          <div className="space-y-4">
            {history.map((item, index) => (
              <motion.div
                key={item.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.05 }}
                className="bg-gray-900/60 border border-gray-800 rounded-xl p-5 hover:bg-gray-800/80 transition-all group"
              >
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center space-x-3 mb-2">
                       <span className={`px-2 py-0.5 rounded text-xs font-bold uppercase tracking-wider ${
                         item.prediction === 'REAL' 
                           ? 'bg-green-500/10 text-green-400 border border-green-500/20' 
                           : item.prediction === 'FAKE'
                           ? 'bg-red-500/10 text-red-500 border border-red-500/20'
                           : 'bg-gray-700 text-gray-400'
                       }`}>
                         {item.prediction}
                       </span>
                       <span className="text-xs text-gray-500 font-mono">
                         {new Date(item.timestamp).toLocaleString()}
                       </span>
                    </div>
                    <p className="text-gray-300 line-clamp-2 md:line-clamp-1 font-medium">
                      {item.text}
                    </p>
                  </div>

                  <div className="flex items-center justify-between md:justify-end gap-6 flex-shrink-0 min-w-[150px]">
                     <div className="text-right">
                       <div className="text-xs text-gray-500">Confidence</div>
                       <div className={`font-mono font-bold ${
                          item.prediction === 'REAL' ? 'text-green-400' : 'text-red-400'
                       }`}>
                         {item.confidence}
                       </div>
                     </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
