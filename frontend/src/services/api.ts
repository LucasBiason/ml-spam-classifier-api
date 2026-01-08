import axios from "axios";
import type { EmailInput, PredictionResponse, HealthResponse } from "../types";

const getApiBaseUrl = (): string => {
  if (typeof window === 'undefined') {
    return import.meta.env.VITE_API_URL || "http://localhost:8000";
  }
  
  // In production, use the same domain with /ml-spam-classifier-api path
  if (window.location.hostname === 'lucasbiason.com' || window.location.hostname === 'www.lucasbiason.com') {
    return `${window.location.origin}/ml-spam-classifier-api`;
  }
  
  // Development
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    return import.meta.env.VITE_API_URL || "http://localhost:8000";
  }
  
  return import.meta.env.VITE_API_URL || window.location.origin;
};

const API_BASE_URL = getApiBaseUrl();

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 10000, // 10 seconds timeout
});

// Add response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Log error for debugging
    console.error('API Error:', error.message, error.config?.url);
    return Promise.reject(error);
  }
);

export const healthCheck = async (): Promise<HealthResponse> => {
  try {
    const response = await api.get<HealthResponse>("/health");
    return response.data;
  } catch (error: any) {
    // Log detailed error information
    console.error('Health check failed:', {
      url: error.config?.url,
      baseURL: API_BASE_URL,
      message: error.message,
      response: error.response?.data,
      status: error.response?.status,
    });
    throw error;
  }
};

export const classifyEmail = async (
  data: EmailInput
): Promise<PredictionResponse> => {
  const response = await api.post<PredictionResponse>("/api/v1/predict", data);
  return response.data;
};

export default api;

