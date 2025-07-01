import { NextResponse } from 'next/server';

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000';

export async function GET() {
  try {
    console.log(`Checking backend health at: ${BACKEND_URL}/health`);
    
    const response = await fetch(`${BACKEND_URL}/health`);

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
    return NextResponse.json(
      { 
        error: 'Backend unavailable', 
        details: error instanceof Error ? error.message : 'Unknown error',
        timestamp: new Date().toISOString()
      },
      { status: 503 }
    );
  }
} 