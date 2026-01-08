import { Mail, Github } from "lucide-react";
import APIStatus from "./APIStatus";

type HeaderProps = {
  apiStatus: "checking" | "online" | "offline";
};

const Header = ({ apiStatus }: HeaderProps) => {
  return (
    <header className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex items-center justify-between">
          {/* Logo and Title */}
          <div className="flex items-center gap-3">
            <Mail className="w-8 h-8 text-blue-600" />
            <div>
              <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                ML Spam Classifier
              </h1>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                Email Classification with Machine Learning
              </p>
            </div>
          </div>

          {/* Status and Links */}
          <div className="flex items-center gap-4">
            <APIStatus status={apiStatus} />
            <a
              href="https://github.com/LucasBiason/ml-spam-classifier-api"
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white transition-colors"
              aria-label="GitHub Repository"
            >
              <Github className="w-5 h-5" />
            </a>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;

