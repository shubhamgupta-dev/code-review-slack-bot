#!/bin/bash

# Generate QR Code for Mobile Access
# This creates a QR code pointing to the local network URL

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                                                                  ║"
echo "║           📱 MOBILE ACCESS QR CODE 📱                           ║"
echo "║                                                                  ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# Get local IP
LOCAL_IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "localhost")

if [ "$LOCAL_IP" == "localhost" ]; then
    echo "❌ Could not detect local IP address"
    echo "   Please check your network connection"
    exit 1
fi

echo "🌐 Local Network Access:"
echo "   http://${LOCAL_IP}:8000/dashboard/login"
echo ""
echo "🔑 Login Credentials:"
echo "   Username: shubham-dev"
echo "   Password: yourlaptop"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Generate QR code
python3 << PYTHON_EOF
import qrcode
import sys

local_url = "http://${LOCAL_IP}:8000/dashboard/login"

qr = qrcode.QRCode(version=1, box_size=1, border=2)
qr.add_data(local_url)
qr.make(fit=True)

print("📱 SCAN THIS QR CODE TO ACCESS ON MOBILE:")
print("")
qr.print_ascii(invert=True)
print("")
PYTHON_EOF

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ SETUP INSTRUCTIONS:"
echo ""
echo "   1. Scan the QR code with your mobile camera"
echo "   2. Make sure mobile is on SAME WiFi network"
echo "   3. You'll be taken to the login page"
echo "   4. BOOKMARK the page before login 📌"
echo "   5. After bookmark, login with credentials above"
echo ""
echo "   The bookmarked page will always show the latest"
echo "   public URL even when tunnel restarts!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 TIP: If QR scan doesn't work, manually type:"
echo "   http://${LOCAL_IP}:8000/dashboard/login"
echo ""

