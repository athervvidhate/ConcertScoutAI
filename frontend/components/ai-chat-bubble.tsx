import { Sparkles, Bot } from "lucide-react"

interface AiChatBubbleProps {
  message: string;
  title: string;
}

export function AiChatBubble({ message, title }: AiChatBubbleProps) {
  if (!message.trim()) return null;

  return (
    <div className="mb-8 animate-fade-in">
      <div className="flex items-start gap-4">
        {/* Enhanced AI Avatar */}
        <div className="flex-shrink-0 relative">
          <div className="w-12 h-12 bg-gradient-to-br from-purple-500 via-pink-500 to-blue-500 rounded-full flex items-center justify-center shadow-lg shadow-purple-500/25">
            <Bot className="h-6 w-6 text-white" />
          </div>
          {/* Glow effect */}
          <div className="absolute inset-0 bg-gradient-to-br from-purple-500 via-pink-500 to-blue-500 rounded-full blur-md opacity-30"></div>
        </div>
        
        {/* Enhanced Chat Bubble */}
        <div className="flex-1 relative">
          {/* Main bubble with gradient background */}
          <div className="bg-gradient-to-r from-gray-900/90 via-gray-800/90 to-gray-900/90 backdrop-blur-sm border border-gray-700/50 rounded-2xl p-6 shadow-xl shadow-black/20 relative overflow-hidden">
            {/* Gradient overlay */}
            <div className="absolute inset-0 bg-gradient-to-r from-purple-500/5 via-transparent to-blue-500/5"></div>
            
            {/* Content */}
            <div className="relative z-10">
              {/* Title with enhanced styling */}
              <div className="flex items-center gap-2 mb-3">
                <Sparkles className="h-4 w-4 text-purple-400" />
                <h4 className="text-lg font-semibold bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 bg-clip-text text-transparent">
                  {title}
                </h4>
                <div className="flex gap-1">
                  <div className="w-1 h-1 bg-purple-400 rounded-full"></div>
                  <div className="w-1 h-1 bg-pink-400 rounded-full"></div>
                  <div className="w-1 h-1 bg-blue-400 rounded-full"></div>
                </div>
              </div>
              
              {/* Message with better typography */}
              <p className="text-gray-200 text-base leading-relaxed whitespace-pre-line font-medium">
                {message}
              </p>
            </div>
            
            {/* Decorative corner accent */}
            <div className="absolute top-0 right-0 w-16 h-16 bg-gradient-to-bl from-purple-500/20 to-transparent rounded-bl-full"></div>
          </div>
          
          {/* Chat bubble tail */}
          <div className="absolute left-0 top-6 w-0 h-0 border-l-8 border-l-transparent border-r-8 border-r-transparent border-t-8 border-t-gray-800/90 transform -translate-x-2"></div>
        </div>
      </div>
    </div>
  );
} 