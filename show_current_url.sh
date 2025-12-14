#!/bin/bash

# Show Current Public URL with QR Code
# Run this anytime to see the latest active URL

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                                                                  ║"
echo "║              📱 CURRENT REVIEWFLOW PUBLIC URL 📱                ║"
echo "║                                                                  ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# Get current URL from log
CURRENT_URL=$(grep -a "tunneled with tls termination" localhostrun.log 2>/dev/null | tail -1 | grep -oE "https://[a-z0-9]+\.lhr\.life")

if [ -z "$CURRENT_URL" ]; then
    echo "❌ No tunnel URL found!"
    echo "   Run: ./start.sh to start services"
    exit 1
fi

# Test if URL is active
HTTP_CODE=$(curl -s --max-time 5 "${CURRENT_URL}/health" -o /dev/null -w "%{http_code}" 2>&1)

if [ "$HTTP_CODE" == "200" ]; then
    STATUS="✅ ACTIVE"
    STATUS_COLOR="\033[0;32m"
else
    STATUS="⚠️  DEAD (restarting...)"
    STATUS_COLOR="\033[0;33m"
fi

echo "🌐 Dashboard URL:"
echo "   ${CURRENT_URL}/dashboard/login"
echo ""
echo -e "📊 Status: ${STATUS_COLOR}${STATUS}\033[0m"
echo ""
echo "🔑 Login Credentials:"
echo "   Username: shubham-dev"
echo "   Password: yourlaptop"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Get local IP for mobile access
LOCAL_IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "localhost")

# Generate QR code for mobile (local network URL)
python3 << PYTHON_EOF
import qrcode
import sys

# Use local network URL for mobile access (same WiFi)
local_url = "http://${LOCAL_IP}:8000/dashboard/login"

qr = qrcode.QRCode(version=1, box_size=1, border=2)
qr.add_data(local_url)
qr.make(fit=True)

print("📱 SCAN THIS QR CODE ON YOUR MOBILE (SAME WiFi):")
print("")
print(f"   URL: {local_url}")
print("")
qr.print_ascii(invert=True)
print("")
print("   ⚠️  This QR code points to local network URL")
print("   → Works only when mobile is on SAME WiFi")
print("   → Bookmark the page to always get public URL")
print("")
PYTHON_EOF

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 TIPS:"
echo "   • This URL changes when tunnel restarts"
echo "   • Run this script anytime to get latest URL"
echo "   • Bookmark: ${CURRENT_URL} (redirects to login)"
echo "   • Or always go to root URL and it will redirect"
echo ""
echo "📋 Share with team:"
echo "   ${CURRENT_URL}/dashboard/login"
echo ""
