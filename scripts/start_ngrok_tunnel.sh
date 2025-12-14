#!/bin/bash

# Start ngrok tunnel with auto-restart
LOGFILE="ngrok_tunnel.log"
PIDFILE="ngrok.pid"

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                                                                  ║"
echo "║        🚀 STARTING NGROK TUNNEL (STABLE ANYWHERE ACCESS) 🚀     ║"
echo "║                                                                  ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# Kill any existing ngrok processes
pkill -f ngrok 2>/dev/null
sleep 2

# Start ngrok
echo "[$(date)] Starting ngrok tunnel..." | tee -a "$LOGFILE"
ngrok http 8000 --log=stdout --log-level=info > "$LOGFILE" 2>&1 &

NGROK_PID=$!
echo $NGROK_PID > "$PIDFILE"
echo "[$(date)] Ngrok started with PID: $NGROK_PID" | tee -a "$LOGFILE"

# Wait for ngrok to establish tunnel
echo ""
echo "⏳ Waiting for ngrok tunnel to establish..."
sleep 5

# Get the public URL
NGROK_URL=""
for i in {1..10}; do
    NGROK_URL=$(curl -s http://localhost:4040/api/tunnels 2>/dev/null | grep -o '"public_url":"https://[^"]*' | head -1 | cut -d'"' -f4)
    
    if [ ! -z "$NGROK_URL" ]; then
        break
    fi
    
    echo "Attempt $i/10: Waiting for ngrok..."
    sleep 2
done

if [ -z "$NGROK_URL" ]; then
    echo "❌ Failed to get ngrok URL!"
    echo ""
    echo "⚠️  TROUBLESHOOTING:"
    echo "   1. Check if you have an ngrok auth token configured"
    echo "   2. Run: ngrok config check"
    echo "   3. If no token, get one at: https://dashboard.ngrok.com/get-started/your-authtoken"
    echo "   4. Add token: ngrok config add-authtoken YOUR_TOKEN"
    exit 1
fi

# Create URL info file
cat > NGROK_URL.txt << URLEOF
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║        🌐 STABLE PUBLIC URL (WORKS ANYWHERE) 🌐                 ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

📱 DASHBOARD (ANYWHERE ACCESS):
   ${NGROK_URL}/dashboard/login

🔑 CREDENTIALS:
   Username: shubham-dev
   Password: yourlaptop

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ ADVANTAGES:

   • Works from ANY WiFi or mobile data
   • Stable - doesn't change URL randomly
   • Much more reliable than localhost.run
   • Professional tunneling service

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📱 FOR MOBILE:

   1. Open browser on mobile (ANY network)
   2. Go to: ${NGROK_URL}/dashboard/login
   3. Login and use dashboard

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔧 NGROK DASHBOARD:
   http://localhost:4040

   View live requests, replays, and tunnel status

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Last Updated: $(date)

URLEOF

echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                                                                  ║"
echo "║              ✅ NGROK TUNNEL READY - ANYWHERE ACCESS ✅         ║"
echo "║                                                                  ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
echo "🌐 PUBLIC URL (works from any WiFi/mobile data):"
echo "   ${NGROK_URL}/dashboard/login"
echo ""
echo "🔑 Login:"
echo "   Username: shubham-dev"
echo "   Password: yourlaptop"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 TIPS:"
echo "   • This URL is stable and won't change randomly"
echo "   • Works from ANY network (not just your WiFi)"
echo "   • View tunnel status: http://localhost:4040"
echo "   • Check URL anytime: cat NGROK_URL.txt"
echo ""
echo "🔧 Ngrok PID: $NGROK_PID"
echo "📝 Logs: tail -f $LOGFILE"
echo ""

# Generate QR code
python3 << PYEOF
import qrcode
import sys

url = "${NGROK_URL}/dashboard/login"

try:
    qr = qrcode.QRCode(version=1, box_size=1, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    
    print("📱 SCAN THIS QR CODE ON YOUR MOBILE:")
    print("")
    qr.print_ascii(invert=True)
    print("")
except Exception as e:
    print(f"⚠️  Could not generate QR code: {e}")
    print("")
PYEOF

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ Tunnel is running in the background!"
echo "   To stop: pkill -f ngrok"
echo ""

# Monitor tunnel in background
(
    while true; do
        if ! ps -p $NGROK_PID > /dev/null 2>&1; then
            echo "[$(date)] ⚠️  Ngrok died! Restarting..." | tee -a "$LOGFILE"
            exec "$0"
        fi
        sleep 30
    done
) &

