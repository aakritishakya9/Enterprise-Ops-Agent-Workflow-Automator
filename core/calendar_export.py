"""
Calendar & Deadline Export Engine for SyncOps AI
Generates RFC 5545 .ics iCalendar files and Google Calendar quick-add URLs for meeting action items.
"""

from typing import Dict, Any, List
import urllib.parse
from datetime import datetime, timedelta


class CalendarExportEngine:
    @staticmethod
    def generate_ics(action_items: List[Dict[str, Any]], meeting_title: str) -> str:
        """Generates standard RFC 5545 .ics file content containing all action items as calendar events."""
        lines = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//SyncOps AI//Enterprise Meeting Calendar//EN",
            "CALSCALE:GREGORIAN",
            "METHOD:PUBLISH"
        ]

        # Base timestamp for demo: upcoming business days
        base_date = datetime.now() + timedelta(days=2)

        for idx, act in enumerate(action_items, 1):
            task_id = act.get("id", f"ACT-{idx}")
            summary = f"[{task_id}] {act.get('task', 'Action Item')}"
            assignee = act.get("assignee", "Unassigned")
            priority = act.get("priority", "Medium")
            deadline = act.get("deadline", "Upcoming")
            
            # Create a mock scheduled target time based on index
            event_date = base_date + timedelta(days=idx)
            start_str = event_date.strftime("%Y%m%dT090000Z")
            end_str = event_date.strftime("%Y%m%dT100000Z")
            created_str = datetime.now().strftime("%Y%m%dT%H%M%SZ")

            desc = f"Action Item: {act.get('task')}\\nAssignee: {assignee}\\nPriority: {priority}\\nTarget Deadline: {deadline}\\nSource Meeting: {meeting_title}"

            lines.extend([
                "BEGIN:VEVENT",
                f"UID:{task_id}-{created_str}@syncops.ai",
                f"DTSTAMP:{created_str}",
                f"DTSTART:{start_str}",
                f"DTEND:{end_str}",
                f"SUMMARY:{summary[:70]}",
                f"DESCRIPTION:{desc}",
                f"STATUS:CONFIRMED",
                f"PRIORITY:{1 if priority in ['Critical', 'High'] else 5}",
                "END:VEVENT"
            ])

        lines.append("END:VCALENDAR")
        return "\r\n".join(lines)

    @staticmethod
    def generate_google_calendar_url(act: Dict[str, Any], meeting_title: str) -> str:
        """Generates a direct one-click Google Calendar event creation URL."""
        task_id = act.get("id", "ACT")
        title = urllib.parse.quote(f"[{task_id}] {act.get('task', 'Task')[:50]}")
        details = urllib.parse.quote(
            f"Action Item: {act.get('task')}\n"
            f"Assignee: {act.get('assignee')}\n"
            f"Priority: {act.get('priority')}\n"
            f"Deadline: {act.get('deadline')}\n"
            f"Source Meeting: {meeting_title}"
        )
        
        # Target date
        target = datetime.now() + timedelta(days=3)
        dates = f"{target.strftime('%Y%m%d')}T090000Z/{target.strftime('%Y%m%d')}T100000Z"

        return f"https://calendar.google.com/calendar/render?action=TEMPLATE&text={title}&dates={dates}&details={details}"
