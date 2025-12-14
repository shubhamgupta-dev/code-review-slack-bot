#!/bin/bash
# Setup Public Access via ngrok

clear
echo "=========================================="
echo "🌐 PUBLIC ACCESS SETUP via ngrok"
echo "=========================================="
echo ""

echo "Step 1: Get ngrok Auth Token"
echo "-----------------------------"
echo "1. Go to: https://dashboard.ngrok.com/get-started/setup"
echo "2. Sign up (free) or log in"
echo "3. Copy your authtoken"
echo ""
read -p "Paste your ngrok authtoken here: " AUTH_TOKEN
echo ""

if [ -z "$AUTH_TOKEN" ]; then
    echo "❌ No token provided. Exiting."
    exit 1
fi

echo "Step 2: Configure ngrok"
echo "-----------------------"
ngrok config add-authtoken "$AUTH_TOKEN"

if [ $? -eq 0 ]; then
    echo "✅ ngrok configured successfully!"
else
    echo "❌ Failed to configure ngrok"
    exit 1
fi
echo ""

echo "Step 3: Starting ngrok tunnel"
echo "-----------------------------"
echo "Creating public URL for port 8000..."
echo ""
echo "⏳ Starting ngrok (Press Ctrl+C to stop)"
echo "📱 Your public URL will appear below:"
echo ""
echo "=========================================="
echo ""

# Start ngrok
ngrok http 8000
