#!/usr/bin/env python3
"""
Simple script to run the Concert Scout AI Streamlit application.
"""

import subprocess
import sys
import os

def main():
    """Run the Streamlit application."""
    # Change to the ConcertScoutAI directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Run streamlit
    cmd = [
        sys.executable, "-m", "streamlit", "run", 
        "streamlit_app.py",
        "--server.port", "8501",
        "--server.address", "localhost",
        "--browser.gatherUsageStats", "false"
    ]
    
    print("🎤 Starting Concert Scout AI Streamlit App...")
    print("📱 The app will open in your browser at: http://localhost:8501")
    print("🛑 Press Ctrl+C to stop the application")
    print("-" * 50)
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n👋 Concert Scout AI stopped. Goodbye!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running Streamlit app: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 