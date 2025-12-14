#!/bin/bash

# Tunnel Keep-Alive Monitor
# Checks tunnel every 60 seconds and restarts if needed
# This script will keep your tunnel alive for days

LOGFILE="tunnel_keepalive.log"

echo "[$(date)] 🔄 Tunnel Keep-Alive Monitor Started" | tee -a "$LOGFILE"
echo "Checking every 60 seconds..." | tee -a "$LOGFILE"
echo ""

while true; do
    # Get current tunnel URL
    CURRENT_URL=$(grep -a "tunneled with tls termination" localhostrun.log 2>/dev/null | tail -1 | grep -oE "https://[a-z0-9]+\.lhr\.life")

    if [ -z "$CURRENT_URL" ]; then
        echo "[$(date)] ⚠️  No tunnel URL found, waiting..." | tee -a "$LOGFILE"
        sleep 60
        continue
    fi

    # Test tunnel with timeout
    HTTP_CODE=$(curl -s --max-time 10 "${CURRENT_URL}/health" -o /dev/null -w "%{http_code}" 2>&1)

    if [ "$HTTP_CODE" == "200" ]; then
        echo "[$(date)] ✅ Tunnel healthy: $CURRENT_URL (HTTP $HTTP_CODE)" | tee -a "$LOGFILE"
    else
        echo "[$(date)] ❌ Tunnel dead: $CURRENT_URL (HTTP $HTTP_CODE)" | tee -a "$LOGFILE"
        echo "[$(date)] 🔄 Restarting tunnel..." | tee -a "$LOGFILE"

        # Kill old tunnel
        pkill -f "ssh.*localhost.run" 2>/dev/null
        sleep 3

        # The persistent_tunnel script will auto-restart
        echo "[$(date)] ⏳ Waiting for tunnel to restart..." | tee -a "$LOGFILE"
        sleep 15

        # Get new URL
        NEW_URL=$(grep -a "tunneled with tls termination" localhostrun.log 2>/dev/null | tail -1 | grep -oE "https://[a-z0-9]+\.lhr\.life")
        echo "[$(date)] 🆕 New URL: $NEW_URL" | tee -a "$LOGFILE"
    fi

    # Wait 60 seconds before next check
    sleep 60
done
