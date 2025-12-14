#!/bin/bash

# Check status of ReviewFlow services

echo "=================================================="
echo "📊 REVIEWFLOW STATUS"
echo "=================================================="
echo ""

# Check server
echo "🌐 FastAPI Server:"
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    PID=$(lsof -ti:8000)
    echo "   Status: ✅ Running"
    echo "   PID: $PID"
    echo "   URL: http://localhost:8000"
    echo "   Dashboard: http://localhost:8000/dashboard/?token=demo-token-123"
else
    echo "   Status: ❌ Not running"
fi

echo ""

# Check auto-sync
echo "🔄 Auto-Sync Service:"
if pgrep -f "auto_sync_service.py" > /dev/null; then
    PID=$(pgrep -f "auto_sync_service.py")
    echo "   Status: ✅ Running"
    echo "   PID: $PID"
    echo "   Interval: 5 seconds"
    echo "   Next check: Within 5 seconds"
else
    echo "   Status: ❌ Not running"
fi

echo ""

# Check database
echo "💾 Database:"
PR_COUNT=$(sqlite3 notifications.db "SELECT COUNT(*) FROM notifications" 2>/dev/null || echo "0")
PENDING=$(sqlite3 notifications.db "SELECT COUNT(*) FROM notifications WHERE status='pending'" 2>/dev/null || echo "0")
echo "   Total PRs: $PR_COUNT"
echo "   Pending Reviews: $PENDING"

echo ""

# Show latest PRs
echo "📋 Latest PRs:"
sqlite3 notifications.db "SELECT '   PR #' || pr_number || ': ' || pr_title || ' [' || status || ']' FROM notifications ORDER BY id DESC LIMIT 3" 2>/dev/null || echo "   No PRs found"

echo ""

# Check logs
echo "📄 Recent Activity:"
if [ -f auto_sync.log ]; then
    echo "   Auto-sync log:"
    tail -3 auto_sync.log 2>/dev/null | sed 's/^/      /'
fi

echo ""
echo "=================================================="
echo ""
echo "💡 Commands:"
echo "   Start services: ./START_SERVICES.sh"
echo "   Stop services: ./STOP_SERVICES.sh"
echo "   View logs: tail -f auto_sync.log"
echo ""
