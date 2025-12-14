#!/bin/bash
# Fix SSL certificates for Python 3.13 on macOS

echo "=================================="
echo "Fixing SSL Certificates for Python 3.13"
echo "=================================="
echo ""
echo "This script will install SSL certificates for Python 3.13"
echo "You will be prompted for your password (sudo required)"
echo ""

sudo /Applications/Python\ 3.13/Install\ Certificates.command

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ SSL certificates installed successfully!"
    echo ""
    echo "Now you can run the webhook test:"
    echo "  python3 test_webhook_endpoint.py"
else
    echo ""
    echo "❌ SSL certificate installation failed"
    echo ""
    echo "Alternative: Try running this command directly:"
    echo "  sudo /Applications/Python\ 3.13/Install\ Certificates.command"
fi