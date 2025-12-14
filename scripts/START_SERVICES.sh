#!/bin/bash

# Start all ReviewFlow services

echo "=================================================="
echo "🚀 STARTING REVIEWFLOW SERVICES"
echo "=================================================="
echo ""

# Check if server is already running
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo "✅ Server already running on port 8000"
else
    echo "🔄 Starting FastAPI server..."
    nohup python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > server.log 2>&1 &
    sleep 2
    echo "✅ Server started on port 8000"
fi

echo ""

# Check if auto-sync is already running
if pgrep -f "auto_sync_service.py" > /dev/null; then
    echo "⚠️  Auto-sync service already running"
    echo "   Stop it with: pkill -f auto_sync_service"
    echo "   Or use: ./RESTART_SERVICES.sh"
else
    echo "🔄 Starting auto-sync service (30-second interval)..."
    nohup python3 -u utils/auto_sync_service.py 30 > auto_sync.log 2>&1 &
    sleep 2
    echo "✅ Auto-sync service started"
fi

echo ""
echo "=================================================="
echo "✅ REVIEWFLOW IS READY!"
echo "=================================================="
echo ""
echo "📊 Dashboard: http://localhost:8000/dashboard/login"
echo "   Login with: shubham-dev / yourlaptop"
echo ""
echo "🔍 Service Status:"
echo "   Server: $(lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null && echo '✅ Running' || echo '❌ Stopped')"
echo "   Auto-sync: $(pgrep -f 'auto_sync_service.py' >/dev/null && echo '✅ Running (checks every 30 seconds)' || echo '❌ Stopped')"
echo ""
echo "📋 View Logs:"
echo "   Server: tail -f server.log"
echo "   Auto-sync: tail -f auto_sync.log"
echo ""
echo "🛑 Stop Services:"
echo "   ./stop.sh (or ./scripts/STOP_SERVICES.sh)"
echo ""
echo "=================================================="
