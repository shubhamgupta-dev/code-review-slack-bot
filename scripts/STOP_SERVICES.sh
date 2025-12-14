#!/bin/bash

# Stop all ReviewFlow services

echo "=================================================="
echo "🛑 STOPPING REVIEWFLOW SERVICES"
echo "=================================================="
echo ""

# Stop auto-sync service
if pgrep -f "auto_sync_service.py" > /dev/null; then
    echo "🔄 Stopping auto-sync service..."
    pkill -f auto_sync_service.py
    sleep 1
    echo "✅ Auto-sync service stopped"
else
    echo "ℹ️  Auto-sync service not running"
fi

echo ""

# Stop server
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo "🔄 Stopping FastAPI server..."
    lsof -ti:8000 | xargs kill
    sleep 1
    echo "✅ Server stopped"
else
    echo "ℹ️  Server not running"
fi

echo ""
echo "=================================================="
echo "✅ ALL SERVICES STOPPED"
echo "=================================================="
echo ""
echo "🔄 To start again: ./START_SERVICES.sh"
echo ""
