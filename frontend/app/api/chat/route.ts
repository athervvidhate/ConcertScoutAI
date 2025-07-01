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
    
    console.log(`Proxying request to: ${BACKEND_URL}/chat`);
    
    const response = await fetch(`${BACKEND_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Backend error' }));
      console.error('Backend error:', errorData);
      return NextResponse.json(
        { error: errorData.detail || 'Backend error' },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('API route error:', error);
    return NextResponse.json(
      { error: 'Internal server error', details: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
} 