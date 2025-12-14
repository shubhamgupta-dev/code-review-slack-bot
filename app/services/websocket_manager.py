"""
WebSocket Manager for Live Dashboard Updates
Manages WebSocket connections and broadcasts updates to connected clients
"""
import asyncio
import json
import logging
from typing import List, Set
from fastapi import WebSocket

logger = logging.getLogger(__name__)


class WebSocketManager:
    """Manages WebSocket connections for real-time updates"""

    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        """Accept a new WebSocket connection"""
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"✅ WebSocket connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection"""
        self.active_connections.discard(websocket)
        logger.info(f"👋 WebSocket disconnected. Total connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send a message to a specific client"""
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")

    async def broadcast(self, message: dict):
        """Broadcast a message to all connected clients"""
        if not self.active_connections:
            logger.debug("No active connections to broadcast to")
            return

        disconnected = set()
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
                disconnected.add(connection)

        # Clean up disconnected clients
        for connection in disconnected:
            self.disconnect(connection)

    async def broadcast_notification_update(self, notification_id: int, action: str, data: dict = None):
        """Broadcast a notification update to all clients"""
        message = {
            "type": "notification_update",
            "notification_id": notification_id,
            "action": action,  # 'new', 'update', 'delete'
            "data": data or {}
        }
        await self.broadcast(message)
        logger.info(f"📡 Broadcast: {action} notification #{notification_id}")

    async def broadcast_stats_update(self, stats: dict):
        """Broadcast updated statistics to all clients"""
        message = {
            "type": "stats_update",
            "stats": stats
        }
        await self.broadcast(message)
        logger.info(f"📊 Broadcast: Stats update")

    async def broadcast_sync_status(self, status: str, details: str = None):
        """Broadcast sync status to all clients"""
        message = {
            "type": "sync_status",
            "status": status,  # 'syncing', 'synced', 'error'
            "details": details
        }
        await self.broadcast(message)
        logger.info(f"🔄 Broadcast: Sync status - {status}")


# Global WebSocket manager instance
ws_manager = WebSocketManager()
