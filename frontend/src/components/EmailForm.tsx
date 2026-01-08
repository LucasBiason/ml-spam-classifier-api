import { useState } from "react";
import { Mail } from "lucide-react";
import type { EmailInput } from "../types";

type EmailFormProps = {
  onSubmit: (data: EmailInput) => void;
  loading: boolean;
};

const EmailForm = ({ onSubmit, loading }: EmailFormProps) => {
  const [message, setMessage] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim()) {
      onSubmit({ message: message.trim() });
    }
  };

  return (
    <form onSubmit={handleSubmit} className="card space-y-6">
      <div className="flex items-center gap-3 mb-6">
        <Mail className="w-8 h-8 text-blue-600" />
        <h2 className="text-2xl font-bold text-gray-800 dark:text-white">
          Email Classification
        </h2>
      </div>

      {/* Email Message */}
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Email Message
        </label>
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Enter email message to classify..."
          className="input-field min-h-[200px] resize-y"
          required
          minLength={10}
          maxLength={5000}
        />
        <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
          {message.length} / 5000 characters
        </p>
      </div>

      {/* Submit Button */}
      <button
        type="submit"
        disabled={loading || !message.trim()}
        className="btn-primary w-full py-3 text-lg"
      >
        {loading ? (
          <span className="flex items-center justify-center gap-2">
            <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
                fill="none"
              />
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              />
            </svg>
            Classifying...
          </span>
        ) : (
          "Classify Email"
        )}
      </button>
    </form>
  );
};

export default EmailForm;

