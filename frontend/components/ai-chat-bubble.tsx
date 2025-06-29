import { MessageCircle } from "lucide-react"

interface AiChatBubbleProps {
  message: string;
  title: string;
}

export function AiChatBubble({ message, title }: AiChatBubbleProps) {
  if (!message.trim()) return null;

  return (
    <div className="mb-6">
      <div className="flex items-start gap-3">
        <div className="flex-shrink-0 w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center">
          <MessageCircle className="h-4 w-4 text-white" />
        </div>
        <div className="flex-1 bg-gray-800/50 border border-gray-700 rounded-lg p-4">
          <h4 className="text-sm font-medium text-purple-400 mb-2">{title}</h4>
          <p className="text-gray-300 text-sm leading-relaxed whitespace-pre-line">
            {message}
          </p>
        </div>
      </div>
    </div>
  );
} 