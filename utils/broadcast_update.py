#!/usr/bin/env python3
"""
Broadcast WebSocket update to all connected clients
Called by auto-sync service when changes are detected
"""
import asyncio
import sys
import requests


async def broadcast_update(notification_id: int = None, action: str = "update"):
    """
    Trigger WebSocket broadcast by calling the API
    Since we can't directly access the FastAPI app from external scripts,
    we'll use HTTP API to trigger broadcasts
    """
    try:
        # For now, we'll just log the update
        # The dashboard clients will poll for updates
        print(f"📡 Update detected: {action} notification #{notification_id}")

    except Exception as e:
        print(f"Error broadcasting update: {e}")


if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "update"
    notification_id = int(sys.argv[2]) if len(sys.argv) > 2 else None

    asyncio.run(broadcast_update(notification_id, action))
