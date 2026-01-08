import { CheckCircle, XCircle, AlertCircle, Info } from "lucide-react";
import type { PredictionResponse } from "../types";

type PredictionResultProps = {
  result: PredictionResponse | null;
  error: string | null;
};

const PredictionResult = ({ result, error }: PredictionResultProps) => {
  if (error) {
    return (
      <div className="card bg-red-50 dark:bg-red-900/20 border-2 border-red-300 dark:border-red-700">
        <div className="flex items-start gap-3">
          <AlertCircle className="w-6 h-6 text-red-600 dark:text-red-400 mt-1" />
          <div>
            <h3 className="text-lg font-semibold text-red-800 dark:text-red-300 mb-2">
              Classification Error
            </h3>
            <p className="text-red-700 dark:text-red-400">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="card bg-gray-50 dark:bg-gray-700/50 border-2 border-dashed border-gray-300 dark:border-gray-600">
        <div className="flex flex-col items-center justify-center py-12 text-center">
          <Info className="w-12 h-12 text-gray-400 mb-4" />
          <p className="text-gray-600 dark:text-gray-400">
            Enter an email message to classify it as spam or ham
          </p>
        </div>
      </div>
    );
  }

  const isSpam = result.is_spam;
  const confidence = result.confidence;

  return (
    <div className="card">
      <div className="flex items-center gap-3 mb-6">
        {isSpam ? (
          <XCircle className="w-8 h-8 text-red-600" />
        ) : (
          <CheckCircle className="w-8 h-8 text-green-600" />
        )}
        <h2 className="text-2xl font-bold text-gray-800 dark:text-white">
          Classification Result
        </h2>
      </div>

      {/* Prediction Badge */}
      <div
        className={`bg-gradient-to-br rounded-lg p-6 mb-6 ${
          isSpam
            ? "from-red-50 to-red-100 dark:from-red-900/30 dark:to-red-800/30"
            : "from-green-50 to-green-100 dark:from-green-900/30 dark:to-green-800/30"
        }`}
      >
        <div className="text-center">
          <p className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-2">
            Classification
          </p>
          <div
            className={`inline-block px-6 py-3 rounded-full text-2xl font-bold ${
              isSpam
                ? "bg-red-600 text-white"
                : "bg-green-600 text-white"
            }`}
          >
            {isSpam ? "SPAM" : "HAM"}
          </div>
          <p className="mt-3 text-sm text-gray-600 dark:text-gray-400">
            Confidence: {(confidence * 100).toFixed(1)}%
          </p>
          <div className="mt-2 text-xs text-gray-500 dark:text-gray-400">
            Spam: {(result.probability_spam * 100).toFixed(1)}% | 
            Ham: {(result.probability_ham * 100).toFixed(1)}%
          </div>
        </div>
      </div>

      {/* Model Info */}
      {result.model_info && (
        <div className="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-4">
          <div className="flex items-center gap-2 mb-3">
            <Info className="w-5 h-5 text-gray-600 dark:text-gray-400" />
            <p className="text-sm font-medium text-gray-700 dark:text-gray-300">
              Model Information
            </p>
          </div>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <p className="text-gray-500 dark:text-gray-400">Model Type</p>
              <p className="font-semibold text-gray-800 dark:text-white">
                {result.model_info.type}
              </p>
            </div>
            <div>
              <p className="text-gray-500 dark:text-gray-400">Vectorizer</p>
              <p className="font-semibold text-gray-800 dark:text-white">
                {result.model_info.vectorizer}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PredictionResult;

