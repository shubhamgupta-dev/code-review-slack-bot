#!/bin/bash

# Start public tunnel using localhost.run
# Makes your ReviewFlow dashboard accessible from anywhere

echo "🌐 Starting public tunnel for ReviewFlow Dashboard..."
echo ""

# Kill any existing tunnel
pkill -f "localhost.run" 2>/dev/null

# Start new tunnel
echo "📡 Establishing SSH tunnel to localhost.run..."
ssh -o StrictHostKeyChecking=no \
    -o UserKnownHostsFile=/dev/null \
    -o ServerAliveInterval=60 \
    -o ServerAliveCountMax=3 \
    -R 80:localhost:8000 \
    nokey@localhost.run > localhostrun.log 2>&1 &

TUNNEL_PID=$!
echo "✅ Tunnel started with PID: $TUNNEL_PID"
echo ""

# Wait for tunnel to establish
echo "⏳ Waiting for tunnel to establish..."
sleep 5

# Display public URL
echo ""
python3 utils/show_public_url.py

echo ""
echo "💡 Keep this terminal open or run in background"
echo "   To run in background: nohup ./scripts/start_public_tunnel.sh &"
echo ""
