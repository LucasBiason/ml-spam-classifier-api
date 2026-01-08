import { Activity } from "lucide-react";

type APIStatusProps = {
  status: "checking" | "online" | "offline";
};

const APIStatus = ({ status }: APIStatusProps) => {
  const getStatusColor = () => {
    switch (status) {
      case "online":
        return "text-green-500";
      case "offline":
        return "text-red-500";
      default:
        return "text-yellow-500";
    }
  };

  const getStatusText = () => {
    switch (status) {
      case "checking":
        return "Checking...";
      case "online":
        return "online";
      case "offline":
        return "offline";
    }
  };

  return (
    <div className="flex items-center gap-2">
      <Activity className={`w-4 h-4 ${getStatusColor()}`} />
      <span className="text-sm text-gray-600 dark:text-gray-400">
        API: {getStatusText()}
      </span>
    </div>
  );
};

export default APIStatus;

