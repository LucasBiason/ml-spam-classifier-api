import { AlertTriangle } from "lucide-react";

const OfflineAlert = () => {
  return (
    <div className="mb-6 p-4 bg-red-50 dark:bg-red-900/20 border-2 border-red-300 dark:border-red-700 rounded-lg">
      <div className="flex items-start gap-3">
        <AlertTriangle className="w-5 h-5 text-red-600 dark:text-red-400 mt-0.5" />
        <div>
          <p className="text-red-800 dark:text-red-300 font-medium">
            API is offline. Please make sure the backend is running.
          </p>
          <p className="text-sm text-red-600 dark:text-red-400 mt-1">
            Run:{" "}
            <code className="bg-red-100 dark:bg-red-900/40 px-2 py-1 rounded">
              make dev
            </code>
          </p>
        </div>
      </div>
    </div>
  );
};

export default OfflineAlert;

