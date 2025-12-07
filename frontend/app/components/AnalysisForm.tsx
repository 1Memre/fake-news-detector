import { motion } from 'framer-motion';
import { AlignLeft, Link as LinkIcon, Search, Loader2 } from 'lucide-react';

interface AnalysisFormProps {
  inputType: 'text' | 'url';
  setInputType: (type: 'text' | 'url') => void;
  text: string;
  setText: (text: string) => void;
  url: string;
  setUrl: (url: string) => void;
  onAnalyze: () => void;
  loading: boolean;
}

export default function AnalysisForm({
  inputType,
  setInputType,
  text,
  setText,
  url,
  setUrl,
  onAnalyze,
  loading
}: AnalysisFormProps) {
  
  const isInputEmpty = inputType === 'text' ? !text.trim() : !url.trim();

  return (
    <div className="space-y-6">
      {/* Input Toggle */}
      <div className="flex bg-gray-800/50 p-1 rounded-xl w-fit mx-auto border border-gray-700/50">
        <button
          onClick={() => setInputType('text')}
          className={`flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
            inputType === 'text' 
            ? 'bg-blue-600 text-white shadow-lg' 
            : 'text-gray-400 hover:text-white hover:bg-gray-800'
          }`}
        >
          <AlignLeft className="h-4 w-4" />
          <span>Text</span>
        </button>
        <button
          onClick={() => setInputType('url')}
          className={`flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
            inputType === 'url' 
            ? 'bg-blue-600 text-white shadow-lg' 
            : 'text-gray-400 hover:text-white hover:bg-gray-800'
          }`}
        >
          <LinkIcon className="h-4 w-4" />
          <span>URL Link</span>
        </button>
      </div>

      <div className="relative">
        {inputType === 'text' ? (
          <>
            <textarea
              className="w-full h-40 p-5 bg-gray-800/50 border border-gray-700 rounded-xl focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 focus:outline-none transition-all text-gray-200 placeholder-gray-500 resize-none text-lg leading-relaxed shadow-inner"
              placeholder="Paste a news headline or article snippet here..."
              value={text}
              onChange={(e) => setText(e.target.value)}
            />
            <div className="absolute bottom-4 right-4 text-gray-600 text-xs pointer-events-none">
              {text.length} chars
            </div>
          </>
        ) : (
          <div className="relative">
            <input
              type="url"
              className="w-full p-5 pl-12 bg-gray-800/50 border border-gray-700 rounded-xl focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 focus:outline-none transition-all text-gray-200 placeholder-gray-500 text-lg leading-relaxed shadow-inner"
              placeholder="https://example.com/news-article"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
            />
            <LinkIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-500 h-5 w-5" />
          </div>
        )}
      </div>

      <motion.button
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        onClick={onAnalyze}
        disabled={loading || isInputEmpty}
        className={`w-full py-4 px-6 rounded-xl font-bold text-lg shadow-lg flex items-center justify-center space-x-2 transition-all ${
          loading || isInputEmpty
            ? 'bg-gray-800 text-gray-500 cursor-not-allowed border border-gray-700'
            : 'bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white shadow-blue-900/20'
        }`}
      >

        {loading ? (
          <>
            <Loader2 className="animate-spin h-5 w-5" />
            <span>Analyzing...</span>
          </>
        ) : (
          <>
            <Search className="h-5 w-5" />
            <span>Analyze Credibility</span>
          </>
        )}
      </motion.button>
    </div>
  );
}
