"""
Database setup and models for notification dashboard
"""
import aiosqlite
import json
from datetime import datetime
from pathlib import Path

DATABASE_PATH = Path("data/notifications.db")


async def init_db():
    """Initialize the database with required tables."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        # Notifications table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pr_number INTEGER NOT NULL,
                pr_title TEXT NOT NULL,
                pr_url TEXT NOT NULL,
                pr_body TEXT,
                repository TEXT NOT NULL,
                author TEXT NOT NULL,
                author_avatar TEXT,
                branch_from TEXT,
                branch_to TEXT,
                summary TEXT,
                ai_analysis TEXT,  -- JSON string
                files_changed INTEGER,
                additions INTEGER,
                deletions INTEGER,
                complexity TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # User actions table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS user_actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                notification_id INTEGER,
                action TEXT NOT NULL,
                comment TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (notification_id) REFERENCES notifications(id)
            )
        """)

        await db.commit()


async def save_notification(pr_event, pr_summary: dict) -> int:
    """Save a PR notification to the database."""
    pr = pr_event.pull_request
    repo = pr_event.repository

    ai_analysis_json = json.dumps(pr_summary.get('ai_analysis', {}))

    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute("""
            INSERT INTO notifications (
                pr_number, pr_title, pr_url, pr_body,
                repository, author, author_avatar,
                branch_from, branch_to,
                summary, ai_analysis,
                files_changed, additions, deletions, complexity
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            pr.number,
            pr.title,
            pr.html_url,
            pr.body,
            repo.full_name,
            pr.user.login,
            pr.user.avatar_url,
            pr.head['ref'],
            pr.base['ref'],
            pr_summary.get('summary_text', ''),
            ai_analysis_json,
            pr_summary.get('files_changed', 0),
            pr_summary.get('additions', 0),
            pr_summary.get('deletions', 0),
            pr_summary.get('complexity', 'Unknown')
        ))

        await db.commit()
        return cursor.lastrowid


async def get_all_notifications(status_filter: str = None, limit: int = 50):
    """Get all notifications, optionally filtered by status."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row

        if status_filter:
            cursor = await db.execute("""
                SELECT * FROM notifications
                WHERE status = ?
                ORDER BY created_at DESC
                LIMIT ?
            """, (status_filter, limit))
        else:
            cursor = await db.execute("""
                SELECT * FROM notifications
                ORDER BY created_at DESC
                LIMIT ?
            """, (limit,))

        rows = await cursor.fetchall()
        return [dict(row) for row in rows]


async def get_notification_by_id(notification_id: int):
    """Get a single notification by ID."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row

        cursor = await db.execute("""
            SELECT * FROM notifications WHERE id = ?
        """, (notification_id,))

        row = await cursor.fetchone()
        return dict(row) if row else None


async def update_notification_status(notification_id: int, status: str):
    """Update the status of a notification."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            UPDATE notifications
            SET status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (status, notification_id))

        await db.commit()


async def save_user_action(notification_id: int, action: str, comment: str = None):
    """Save a user action on a notification."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            INSERT INTO user_actions (notification_id, action, comment)
            VALUES (?, ?, ?)
        """, (notification_id, action, comment))

        await db.commit()


async def get_notification_stats():
    """Get summary statistics about notifications."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row

        cursor = await db.execute("""
            SELECT
                status,
                COUNT(*) as count
            FROM notifications
            GROUP BY status
        """)

        rows = await cursor.fetchall()
        stats = {row['status']: row['count'] for row in rows}

        return {
            'pending': stats.get('pending', 0),
            'approved': stats.get('approved', 0),
            'changes_requested': stats.get('changes_requested', 0),
            'commented': stats.get('commented', 0),
            'total': sum(stats.values())
        }
