import { useState, useEffect } from "react";
import {
  Header,
  Footer,
  OfflineAlert,
  EmailForm,
  PredictionResult,
} from "./components";
import { healthCheck, classifyEmail } from "./services/api";
import type { EmailInput, PredictionResponse } from "./types";

const App = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<PredictionResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [apiStatus, setApiStatus] = useState<"checking" | "online" | "offline">(
    "checking"
  );

  useEffect(() => {
    const checkAPI = async () => {
      try {
        await healthCheck();
        setApiStatus("online");
      } catch {
        setApiStatus("offline");
      }
    };
    checkAPI();
  }, []);

  const handleClassify = async (data: EmailInput) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const prediction = await classifyEmail(data);
      setResult(prediction);
    } catch (err: any) {
      const errorMessage =
        err.response?.data?.detail || "Failed to classify email. Please try again.";
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
      <Header apiStatus={apiStatus} />

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {apiStatus === "offline" && <OfflineAlert />}

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Form */}
          <div>
            <EmailForm onSubmit={handleClassify} loading={loading} />
          </div>

          {/* Result */}
          <div>
            <PredictionResult result={result} error={error} />
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default App;

