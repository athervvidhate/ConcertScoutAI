#!/bin/bash

# Concert Scout AI Deployment Script
echo "🎵 Concert Scout AI Deployment Script"
echo "====================================="

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

echo "📋 This script will help you deploy your Concert Scout AI application"
echo ""
echo "1. Deploy backend to Render"
echo "2. Deploy frontend to Vercel"
echo "3. Full deployment guide"
echo ""

read -p "Choose an option (1-3): " choice

case $choice in
    1)
        echo "🚀 Deploying to Render..."
        echo ""
        echo "1. Go to https://render.com"
        echo "2. Create a new Web Service"
        echo "3. Connect your GitHub repository"
        echo "4. Set the root directory to: /api"
        echo "5. Set build command to: pip install -r requirements.txt"
        echo "6. Set start command to: uvicorn app:app --host 0.0.0.0 --port \$PORT"
        echo "7. Add your environment variables (same as Railway)"
        echo "8. Deploy and copy the generated URL"
        ;;
    2)
        echo "🚀 Deploying to Vercel..."
        echo ""
        echo "1. Go to https://vercel.com"
        echo "2. Import your GitHub repository"
        echo "3. Set the root directory to: /frontend"
        echo "4. Add environment variable: BACKEND_URL=https://your-backend-url"
        echo "5. Deploy"
        echo ""
        echo "After deployment, add your custom domain in Vercel settings"
        ;;
    3)
        echo "📖 Opening deployment guide..."
        if command -v open &> /dev/null; then
            open DEPLOYMENT.md
        elif command -v xdg-open &> /dev/null; then
            xdg-open DEPLOYMENT.md
        else
            echo "Please open DEPLOYMENT.md manually"
        fi
        ;;
    *)
        echo "❌ Invalid option. Please choose 1-5."
        exit 1
        ;;
esac

echo ""
echo "✅ Deployment instructions provided!"
echo "📖 For detailed instructions, see DEPLOYMENT.md" 