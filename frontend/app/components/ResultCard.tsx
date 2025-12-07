import { motion, AnimatePresence } from 'framer-motion';
import { 
  AlertTriangle, 
  CheckCircle, 
  XCircle, 
  ExternalLink,
  FileText,
  Lightbulb,
  Info,
  Heart,
  AlignLeft
} from 'lucide-react';

interface ResultCardProps {
  result: string;
  data: any; // Ideally strictly typed
}

export default function ResultCard({ result, data }: ResultCardProps) {
  return (
    <AnimatePresence mode="wait">
      <motion.div 
        key="result"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -20 }}
        transition={{ duration: 0.4, ease: "easeOut" }}
        className="mt-10 space-y-6"
      >
        {result === 'INVALID' ? (
          // Invalid Input Warning
          <div className="p-8 bg-yellow-900/10 border border-yellow-600/30 rounded-2xl text-center backdrop-blur-sm">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-yellow-900/30 mb-4">
              <AlertTriangle className="h-8 w-8 text-yellow-500" />
            </div>
            <h2 className="text-2xl font-bold text-yellow-500 mb-2">
              Not a News Article
            </h2>
            <p className="text-gray-300 text-lg">
              {data?.explanation || "The input text does not appear to be a valid news headline."}
            </p>
          </div>
        ) : (
          // Standard Result (Real/Fake)
          <div
            className={`p-8 rounded-2xl border backdrop-blur-sm relative overflow-hidden ${
              result === 'REAL'
                ? 'bg-green-950/30 border-green-500/30 shadow-[0_0_40px_-10px_rgba(34,197,94,0.2)]'
                : 'bg-red-950/30 border-red-500/30 shadow-[0_0_40px_-10px_rgba(239,68,68,0.2)]'
            }`}
          >
            <div className="flex flex-col md:flex-row items-center justify-between mb-8">
              <div className="flex items-center space-x-4 mb-4 md:mb-0">
                <div className={`p-3 rounded-full ${result === 'REAL' ? 'bg-green-500/20' : 'bg-red-500/20'}`}>
                  {result === 'REAL' ? (
                    <CheckCircle className="h-10 w-10 text-green-500" />
                  ) : (
                    <XCircle className="h-10 w-10 text-red-500" />
                  )}
                </div>
                <div>
                  <h2 className={`text-3xl font-bold tracking-tight ${
                    result === 'REAL' ? 'text-green-400' : 'text-red-500'
                  }`}>
                    {result} NEWS
                  </h2>
                  <p className="text-gray-400 text-sm">
                    {result === 'REAL' ? 'High Credibility Detected' : 'Low Credibility Detected'}
                  </p>
                </div>
              </div>
              
              <div className="text-right">
                 <div className="text-sm text-gray-400 mb-1 uppercase tracking-wider font-semibold">Confidence</div>
                 <div className={`text-3xl font-mono font-bold ${
                   result === 'REAL' ? 'text-green-400' : 'text-red-500'
                 }`}>
                   {data?.confidence}
                 </div>
              </div>
            </div>

            {/* Confidence Bar */}
            <div className="w-full bg-gray-800/50 rounded-full h-3 mb-6 overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ 
                  width: data?.confidence.includes('%') 
                    ? data.confidence.split('%')[0] + '%' 
                    : '100%' 
                }}
                transition={{ duration: 1, ease: "circOut" }}
                className={`h-full rounded-full ${
                  result === 'REAL' 
                    ? 'bg-gradient-to-r from-green-600 to-green-400' 
                    : 'bg-gradient-to-r from-red-600 to-red-400'
                }`}
              />
            </div>
          </div>
        )}

        {/* Sentiment Analysis Section (New) */}
        {result !== 'INVALID' && data?.sentiment_label && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
             <motion.div 
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.1 }}
              className="p-5 bg-gray-800/40 rounded-xl border border-gray-700/50"
            >
              <h3 className="text-gray-400 text-xs font-bold uppercase tracking-wider mb-2 flex items-center">
                <Heart className="h-4 w-4 mr-2 text-pink-500" />
                Emotional Tone
              </h3>
              <div className="flex items-end justify-between">
                <span className={`text-2xl font-bold ${
                  data.sentiment_label === 'Positive' ? 'text-green-400' : 
                  data.sentiment_label === 'Negative' ? 'text-red-400' : 'text-gray-300'
                }`}>
                  {data.sentiment_label}
                </span>
                <div className="text-right">
                  <span className="text-xs text-gray-500 block">Score</span>
                  <span className="font-mono text-sm text-gray-400">
                    {data.sentiment_score.toFixed(2)}
                  </span>
                </div>
              </div>
              
              {/* Sentiment Bar */}
              <div className="w-full bg-gray-700/50 h-1.5 mt-3 rounded-full relative overflow-hidden">
                <div className="absolute left-1/2 top-0 bottom-0 w-0.5 bg-gray-500 h-full z-10"></div>
                <motion.div 
                  initial={{ width: '0%' }}
                  animate={{ 
                    width: `${Math.abs(data.sentiment_score) * 50}%`,
                    x: data.sentiment_score > 0 ? '0%' : '-100%',
                    left: '50%'
                  }}
                  className={`h-full absolute ${data.sentiment_score > 0 ? 'bg-green-500' : 'bg-red-500'}`}
                />
              </div>
            </motion.div>

            <motion.div 
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.15 }}
              className="p-5 bg-gray-800/40 rounded-xl border border-gray-700/50"
            >
              <h3 className="text-gray-400 text-xs font-bold uppercase tracking-wider mb-2 flex items-center">
                <AlignLeft className="h-4 w-4 mr-2 text-purple-500" />
                Subjectivity
              </h3>
              <div className="flex items-end justify-between">
                <span className="text-2xl font-bold text-gray-200">
                  {data.subjectivity_score > 0.5 ? 'Opinionated' : 'Objective'}
                </span>
                <div className="text-right">
                  <span className="text-xs text-gray-500 block">Score</span>
                  <span className="font-mono text-sm text-gray-400">
                    {data.subjectivity_score.toFixed(2)}
                  </span>
                </div>
              </div>
               <div className="w-full bg-gray-700/50 h-1.5 mt-3 rounded-full overflow-hidden">
                <motion.div 
                  initial={{ width: 0 }}
                  animate={{ width: `${data.subjectivity_score * 100}%` }}
                  className="h-full bg-purple-500"
                />
              </div>
            </motion.div>
          </div>
        )}

        {/* Auto-Correction Notice (New) */}
        {data?.corrected_text && (
          <motion.div 
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="p-4 bg-purple-900/10 border border-purple-500/20 rounded-xl flex items-start space-x-3"
          >
            <div className="flex-shrink-0 mt-0.5">
               <span className="flex items-center justify-center h-5 w-5 rounded-full bg-purple-500/20 text-purple-400 font-bold text-xs">A</span>
            </div>
            <div>
              <h4 className="text-sm font-bold text-purple-400 uppercase tracking-wider mb-1">
                Auto-Corrected Input
              </h4>
              <p className="text-gray-400 text-sm">
                <span className="text-gray-500 line-through mr-2">{data.original_text}</span>
                <span className="text-gray-200">{data.corrected_text}</span>
              </p>
            </div>
          </motion.div>
        )}


        {/* Explanation Section */}
        {result !== 'INVALID' && data?.explanation && (
          <motion.div 
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="p-6 bg-gray-800/40 rounded-xl border border-gray-700/50 backdrop-blur-sm"
          >
            <div className="flex items-start space-x-3">
              <Info className="h-6 w-6 text-blue-400 mt-0.5 flex-shrink-0" />
              <div>
                <h3 className="text-sm font-bold text-blue-400 mb-2 uppercase tracking-wider">
                  Analysis Report
                </h3>
                <p className="text-gray-300 leading-relaxed">
                  {data.explanation}
                </p>
              </div>
            </div>
          </motion.div>
        )}

        {/* Correction Section */}
        {data?.correction && (
          <motion.div 
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="p-6 bg-blue-900/20 rounded-xl border border-blue-500/30 backdrop-blur-sm"
          >
            <div className="flex items-start space-x-3">
              <Lightbulb className="h-6 w-6 text-yellow-400 mt-0.5 flex-shrink-0" />
              <div className="w-full">
                <h3 className="text-sm font-bold text-blue-300 mb-2 uppercase tracking-wider">
                  Related Trusted Context
                </h3>
                <p className="text-gray-400 text-sm mb-3">
                  We found a related story from a trusted source that might provide the correct context:
                </p>
                <a
                  href={data.correction.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center justify-between p-3 bg-blue-950/40 rounded-lg border border-blue-800/50 hover:bg-blue-900/40 transition-colors group"
                >
                  <div>
                    <div className="font-medium text-blue-200 group-hover:text-white transition-colors">
                      {data.correction.title}
                    </div>
                    <div className="text-xs text-blue-400 mt-1">
                      {data.correction.domain}
                    </div>
                  </div>
                  <ExternalLink className="h-4 w-4 text-blue-400 group-hover:text-white transition-colors" />
                </a>
              </div>
            </div>
          </motion.div>
        )}

        {/* Trusted Sources Section */}
        {result !== 'INVALID' && (
          <motion.div 
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="pt-6 border-t border-gray-800"
          >
            <h3 className="text-lg font-semibold text-gray-300 mb-4 text-center flex items-center justify-center">
              <FileText className="h-5 w-5 mr-2 text-gray-500" />
              Source Verification
            </h3>
            
            {data?.sources && data.sources.length > 0 ? (
              <div className="grid gap-3">
                {data.sources.map((source: any, index: number) => (
                  <a
                    key={index}
                    href={source.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center justify-between p-4 bg-gray-800/60 rounded-xl hover:bg-gray-700/80 transition-all border border-gray-700 group"
                  >
                    <span className="text-blue-400 font-medium group-hover:text-blue-300">
                      {source.domain}
                    </span>
                    <span className="text-xs text-gray-500 flex items-center group-hover:text-gray-300">
                      View Source <ExternalLink className="h-3 w-3 ml-1" />
                    </span>
                  </a>
                ))}
              </div>
            ) : (
              <div className="text-center p-6 bg-gray-800/30 rounded-xl border border-gray-700/50 border-dashed">
                <p className="text-gray-400 text-sm">
                  ⚠️ We couldn't find this exact story on our list of trusted news sites.
                </p>
                <p className="text-gray-500 text-xs mt-1">
                  This doesn't guarantee it's fake, but please verify with other sources.
                </p>
              </div>
            )}
          </motion.div>
        )}
      </motion.div>
    </AnimatePresence>
  );
}
