import { NextResponse } from 'next/server';

const getBackendUrl = () => {
  let backendUrl = process.env.BACKEND_URL || 'http://localhost:8000';
  
  // Ensure the URL has a protocol
  if (!backendUrl.startsWith('http://') && !backendUrl.startsWith('https://')) {
    backendUrl = `https://${backendUrl}`;
  }
  
  return backendUrl;
};

const BACKEND_URL = getBackendUrl();

export async function GET() {
  try {
    console.log(`Checking backend health at: ${BACKEND_URL}/health`);
    
    // Add timeout to prevent hanging requests
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 second timeout
    
    const response = await fetch(`${BACKEND_URL}/health`, {
      signal: controller.signal,
      headers: {
        'User-Agent': 'ConcertScout-Frontend/1.0',
      },
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      console.error('Backend health check failed:', response.status);
      return NextResponse.json(
        { error: 'Backend health check failed', status: response.status },
        { status: response.status }
      );
    }

    const data = await response.json();
    console.log('Backend health check successful:', data.status);
    return NextResponse.json(data);
  } catch (error) {
    console.error('Health check error:', error);
    
    let errorMessage = 'Backend unavailable';
    let statusCode = 503;
    
    if (error instanceof Error) {
      if (error.name === 'AbortError') {
        errorMessage = 'Backend request timeout';
      } else if (error.message.includes('ECONNRESET')) {
        errorMessage = 'Backend connection reset';
      } else if (error.message.includes('ENOTFOUND')) {
        errorMessage = 'Backend host not found';
      } else if (error.message.includes('ECONNREFUSED')) {
        errorMessage = 'Backend connection refused';
      }
    }
    
    return NextResponse.json(
      { 
        error: errorMessage, 
        details: error instanceof Error ? error.message : 'Unknown error',
        backendUrl: BACKEND_URL,
        timestamp: new Date().toISOString()
      },
      { status: statusCode }
    );
  }
} 