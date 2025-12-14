#!/bin/bash

# Start persistent localhost.run tunnel with auto-restart
# This tunnel will stay active as long as this script is running

LOGFILE="localhostrun.log"
PIDFILE="tunnel.pid"

echo "🚀 Starting persistent public tunnel..."
echo "⏰ This tunnel will auto-restart if it drops"
echo "📝 Logs: $LOGFILE"
echo ""

# Kill any existing tunnel
pkill -f "ssh.*localhost.run" 2>/dev/null

# Function to start tunnel
start_tunnel() {
    echo "[$(date)] Starting tunnel..." | tee -a "$LOGFILE"
    ssh -o StrictHostKeyChecking=no \
        -o UserKnownHostsFile=/dev/null \
        -o ServerAliveInterval=60 \
        -o ServerAliveCountMax=3 \
        -o ExitOnForwardFailure=yes \
        -R 80:localhost:8000 \
        nokey@localhost.run >> "$LOGFILE" 2>&1 &

    TUNNEL_PID=$!
    echo $TUNNEL_PID > "$PIDFILE"
    echo "[$(date)] Tunnel started with PID: $TUNNEL_PID" | tee -a "$LOGFILE"
}

# Monitor and restart if needed
monitor_tunnel() {
    while true; do
        if [ -f "$PIDFILE" ]; then
            TUNNEL_PID=$(cat "$PIDFILE")
            if ! ps -p $TUNNEL_PID > /dev/null 2>&1; then
                echo "[$(date)] ⚠️  Tunnel died! Restarting..." | tee -a "$LOGFILE"
                sleep 5
                start_tunnel
            fi
        else
            start_tunnel
        fi

        # Check every 30 seconds
        sleep 30

        # Extract and display current URL
        if [ -f "$LOGFILE" ]; then
            CURRENT_URL=$(grep -oE "https://[a-z0-9]+\.lhr\.life" "$LOGFILE" | tail -1)
            if [ ! -z "$CURRENT_URL" ]; then
                echo "[$(date)] ✅ Active URL: $CURRENT_URL"
            fi
        fi
    done
}

# Trap SIGINT and SIGTERM to cleanup
cleanup() {
    echo ""
    echo "[$(date)] 🛑 Stopping tunnel..."
    if [ -f "$PIDFILE" ]; then
        TUNNEL_PID=$(cat "$PIDFILE")
        kill $TUNNEL_PID 2>/dev/null
        rm "$PIDFILE"
    fi
    pkill -f "ssh.*localhost.run" 2>/dev/null
    echo "[$(date)] Tunnel stopped"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start monitoring
echo "🔄 Starting tunnel monitor (Press Ctrl+C to stop)"
echo ""
monitor_tunnel
