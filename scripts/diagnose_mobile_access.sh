#!/bin/bash
# Mobile Access Diagnostic Script
# Run this to check your setup for mobile access

echo "======================================"
echo "📱 MOBILE ACCESS DIAGNOSTIC REPORT"
echo "======================================"
echo ""

echo "✅ 1. SERVER STATUS"
echo "-------------------"
SERVER_CHECK=$(lsof -i :8000 | grep LISTEN)
if [ -n "$SERVER_CHECK" ]; then
    echo "✓ Server is RUNNING on port 8000"
    echo "  PID: $(echo $SERVER_CHECK | awk '{print $2}')"
else
    echo "✗ Server is NOT running on port 8000"
    echo "  Run: ./START_SERVICES.sh"
fi
echo ""

echo "✅ 2. NETWORK INFORMATION"
echo "-------------------------"
LOCAL_IP=$(ipconfig getifaddr en0 2>/dev/null)
if [ -n "$LOCAL_IP" ]; then
    echo "✓ Local IP (WiFi): $LOCAL_IP"
else
    echo "✗ Could not detect WiFi IP"
    echo "  Make sure WiFi is enabled"
fi

WIFI_NETWORK=$(networksetup -getairportnetwork en0 2>/dev/null | cut -d ':' -f 2 | xargs)
if [ -n "$WIFI_NETWORK" ]; then
    echo "✓ Connected to WiFi: $WIFI_NETWORK"
else
    echo "✗ Not connected to WiFi"
fi
echo ""

echo "✅ 3. ACCESS URL"
echo "----------------"
if [ -n "$LOCAL_IP" ]; then
    ACCESS_URL="http://$LOCAL_IP:8000/dashboard/?token=demo-token-123"
    echo "📱 Mobile URL: $ACCESS_URL"
    echo ""
    echo "🔗 To access from mobile:"
    echo "   1. Connect your mobile to WiFi: $WIFI_NETWORK"
    echo "   2. Open browser and go to:"
    echo "      $ACCESS_URL"
    echo ""
fi

echo "✅ 4. LOCAL ACCESS TEST"
echo "-----------------------"
if [ -n "$LOCAL_IP" ]; then
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "http://$LOCAL_IP:8000/dashboard/?token=demo-token-123" 2>/dev/null)
    if [ "$HTTP_STATUS" = "200" ]; then
        echo "✓ Server is accessible locally (HTTP $HTTP_STATUS)"
    else
        echo "✗ Server returned HTTP $HTTP_STATUS"
    fi
fi
echo ""

echo "✅ 5. FIREWALL CHECK"
echo "--------------------"
echo "ℹ️  To check firewall status, run manually:"
echo "   sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate"
echo ""
echo "ℹ️  If firewall is ON, temporarily disable it:"
echo "   sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate off"
echo ""
echo "ℹ️  Re-enable firewall after testing:"
echo "   sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on"
echo ""

echo "✅ 6. COMMON ISSUES CHECKLIST"
echo "------------------------------"
echo "On your MOBILE device, verify:"
echo "  [ ] Connected to SAME WiFi network: $WIFI_NETWORK"
echo "  [ ] Cellular data is TURNED OFF"
echo "  [ ] VPN is DISABLED"
echo "  [ ] Using HTTP (not HTTPS) in browser"
echo "  [ ] Tried clearing browser cache"
echo ""
echo "On your COMPUTER, verify:"
echo "  [ ] Firewall is temporarily DISABLED (or Python allowed)"
echo "  [ ] VPN is DISABLED"
echo "  [ ] Server is running"
echo ""

echo "======================================"
echo "📚 For detailed troubleshooting:"
echo "   Read: MOBILE_TROUBLESHOOTING.md"
echo "======================================"
echo ""

echo "💡 QUICK FIX (Most common solution):"
echo ""
echo "1. Disable firewall temporarily:"
echo "   sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate off"
echo ""
echo "2. On mobile, ensure you're on WiFi: $WIFI_NETWORK"
echo ""
echo "3. Try accessing: http://$LOCAL_IP:8000/dashboard/?token=demo-token-123"
echo ""
echo "4. Re-enable firewall after testing:"
echo "   sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on"
echo ""
