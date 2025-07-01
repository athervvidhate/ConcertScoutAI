// API configuration for different environments
const getApiBaseUrl = () => {
  // In production (Vercel), use relative URLs that will be proxied
  if (typeof window !== 'undefined' && window.location.hostname !== 'localhost') {
    return '/api';
  }
  
  // In development, use localhost
  return 'http://localhost:8000';
};

const API_BASE_URL = getApiBaseUrl();

export interface ChatRequest {
  message: string;
  user_id?: string;
  session_id?: string;
}

export interface ChatResponse {
  response: string;
  session_id: string;
  user_id: string;
  events: Array<{
    author: string;
    timestamp: string;
    type: string;
    content?: string;
    function_name?: string;
    function_args?: any;
    response?: any;
  }>;
}

export interface SessionResponse {
  session_id: string;
  user_id: string;
  message: string;
}

export interface ApiError {
  status: number;
  statusText: string;
  message: string;
  isQuotaExceeded: boolean;
  isServerError: boolean;
}

class ApiService {
  private baseUrl: string;

  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  private async handleErrorResponse(response: Response): Promise<ApiError> {
    let errorDetails = '';
    let isQuotaExceeded = false;

    try {
      const errorData = await response.json();
      errorDetails = errorData.detail || errorData.message || 'Unknown error';
      
      // Check if it's a quota exceeded error
      if (errorDetails.includes('429 RESOURCE_EXHAUSTED') || 
          errorDetails.includes('exceeded your current quota') ||
          errorDetails.includes('rate limit') ||
          response.status === 429) {
        isQuotaExceeded = true;
      }
    } catch {
      errorDetails = response.statusText;
    }

    return {
      status: response.status,
      statusText: response.statusText,
      message: errorDetails,
      isQuotaExceeded,
      isServerError: response.status >= 500
    };
  }

  async chat(request: ChatRequest): Promise<ChatResponse> {
    const response = await fetch(`${this.baseUrl}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const errorInfo = await this.handleErrorResponse(response);
      const error = new Error(`API request failed: ${response.status} ${response.statusText}`) as any;
      error.apiError = errorInfo;
      throw error;
    }

    return response.json();
  }

  async createSession(userId: string = 'default_user'): Promise<SessionResponse> {
    const response = await fetch(`${this.baseUrl}/sessions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ user_id: userId }),
    });

    if (!response.ok) {
      const errorInfo = await this.handleErrorResponse(response);
      const error = new Error(`API request failed: ${response.status} ${response.statusText}`) as any;
      error.apiError = errorInfo;
      throw error;
    }

    return response.json();
  }

  async healthCheck(): Promise<{ status: string; service: string }> {
    const response = await fetch(`${this.baseUrl}/health`);
    
    if (!response.ok) {
      const errorInfo = await this.handleErrorResponse(response);
      const error = new Error(`Health check failed: ${response.status} ${response.statusText}`) as any;
      error.apiError = errorInfo;
      throw error;
    }

    return response.json();
  }
}

export const apiService = new ApiService(); 