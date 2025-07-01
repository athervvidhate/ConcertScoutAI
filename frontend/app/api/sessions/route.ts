import { NextRequest, NextResponse } from 'next/server';

const getBackendUrl = () => {
  let backendUrl = process.env.BACKEND_URL || 'http://localhost:8000';
  
  // Ensure the URL has a protocol
  if (!backendUrl.startsWith('http://') && !backendUrl.startsWith('https://')) {
    backendUrl = `https://${backendUrl}`;
  }
  
  return backendUrl;
};

const BACKEND_URL = getBackendUrl();

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    console.log(`Proxying session request to: ${BACKEND_URL}/sessions`);
    
    // Add timeout to prevent hanging requests
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 second timeout for sessions
    
    const response = await fetch(`${BACKEND_URL}/sessions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'ConcertScout-Frontend/1.0',
      },
      body: JSON.stringify(body),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Backend error' }));
      console.error('Backend session error:', errorData);
      return NextResponse.json(
        { error: errorData.detail || 'Backend error' },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Sessions API route error:', error);
    
    let errorMessage = 'Internal server error';
    let statusCode = 500;
    
    if (error instanceof Error) {
      if (error.name === 'AbortError') {
        errorMessage = 'Request timeout - backend took too long to respond';
        statusCode = 408;
      } else if (error.message.includes('ECONNRESET')) {
        errorMessage = 'Connection to backend was reset';
        statusCode = 503;
      } else if (error.message.includes('ENOTFOUND')) {
        errorMessage = 'Backend host not found';
        statusCode = 503;
      } else if (error.message.includes('ECONNREFUSED')) {
        errorMessage = 'Backend connection refused';
        statusCode = 503;
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