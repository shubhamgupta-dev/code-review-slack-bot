#!/bin/bash
# MOBILE ACCESS FIX - Run this script to enable mobile access

clear
echo "========================================="
echo "📱 MOBILE ACCESS FIX"
echo "========================================="
echo ""

# Get local IP
LOCAL_IP=$(ipconfig getifaddr en0 2>/dev/null || echo "192.168.29.169")

echo "Step 1: DISABLE FIREWALL (Required)"
echo "-----------------------------------"
echo "Run this command and enter your password:"
echo ""
echo "  sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate off"
echo ""
read -p "Press ENTER after you've disabled the firewall..."
echo ""

# Check if firewall is off
echo "Checking firewall status..."
FW_STATUS=$(sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate 2>/dev/null)
echo "$FW_STATUS"
echo ""

echo "Step 2: VERIFY SERVER"
echo "-----------------------------------"
SERVER_CHECK=$(lsof -i :8000 | grep LISTEN)
if [ -n "$SERVER_CHECK" ]; then
    echo "✓ Server is RUNNING on port 8000"
else
    echo "✗ Server is NOT running!"
    echo "  Start it with: ./START_SERVICES.sh"
    exit 1
fi
echo ""

echo "Step 3: TEST LOCAL ACCESS"
echo "-----------------------------------"
echo "Testing connection to $LOCAL_IP:8000..."
if nc -zv $LOCAL_IP 8000 2>&1 | grep -q "succeeded"; then
    echo "✓ Port 8000 is ACCESSIBLE"
else
    echo "✗ Port 8000 is NOT accessible"
    exit 1
fi
echo ""

echo "Step 4: MOBILE INSTRUCTIONS"
echo "-----------------------------------"
echo "On your MOBILE device:"
echo ""
echo "1. Go to Settings → WiFi"
echo "2. Make sure you're on the SAME network as this computer"
echo "3. Turn OFF cellular data"
echo "4. Open any browser (Chrome, Safari)"
echo "5. Enter this URL exactly:"
echo ""
echo "   http://$LOCAL_IP:8000/dashboard/?token=demo-token-123"
echo ""
echo "========================================="
echo "📱 QR CODE FOR EASY ACCESS"
echo "========================================="
echo ""

# Generate QR code
if command -v python3 &> /dev/null; then
    python3 show_qr_code.py
    echo ""
    echo "✓ QR code generated above!"
    echo "✓ Image saved as: reviewflow_qr_code.png"
else
    echo "Python3 not found. Manually enter the URL on mobile."
fi

echo ""
echo "========================================="
echo "🔧 TROUBLESHOOTING"
echo "========================================="
echo ""
echo "If mobile still can't connect:"
echo ""
echo "1. Check both devices are on SAME WiFi:"
echo "   Computer: Check WiFi icon in menu bar"
echo "   Mobile: Settings → WiFi → Network name"
echo ""
echo "2. Disable VPN on both devices"
echo ""
echo "3. Try different browser on mobile"
echo ""
echo "4. Restart WiFi on mobile device"
echo ""
echo "5. Use Tailscale (works from anywhere):"
echo "   http://100.96.3.158:8000/dashboard/?token=demo-token-123"
echo ""
echo "========================================="
echo ""
echo "Press Ctrl+C to exit"
echo ""

# Keep script running and show server logs
echo "Watching for mobile connections..."
echo "(Server logs will appear below)"
echo ""
tail -f auto_sync.log 2>/dev/null || echo "Waiting for mobile connection..."
