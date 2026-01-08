export type EmailInput = {
  message: string;
};

export type PredictionResponse = {
  prediction: "spam" | "ham";
  is_spam: boolean;
  confidence: number;
  probability_spam: number;
  probability_ham: number;
  model_info: {
    type: string;
    vectorizer: string;
  };
};

export type HealthResponse = {
  status: string;
  timestamp?: string;
  classifier_ready?: boolean;
  version?: string;
};

