"""
Live Webhook Dispatcher for SyncOps AI
Sends formatted notifications directly to real Slack, Discord, n8n, Make.com, or enterprise endpoints.
"""

from typing import Dict, Any
import json
import time

try:
    import requests
except ImportError:
    requests = None


class LiveWebhookDispatcher:
    @staticmethod
    def dispatch(
        webhook_url: str,
        payload_data: Dict[str, Any],
        slack_markdown: str = "",
        timeout_seconds: int = 10
    ) -> Dict[str, Any]:
        """Dispatches payload to a live webhook endpoint or simulates execution."""
        start_time = time.time()
        
        if not webhook_url or not webhook_url.startswith("http"):
            return {
                "success": False,
                "status_code": 400,
                "message": "Invalid or missing Webhook URL. Please provide a valid HTTP/HTTPS endpoint.",
                "latency_ms": 0
            }

        is_slack = "hooks.slack.com" in webhook_url
        is_discord = "discord.com/api/webhooks" in webhook_url

        # Format specialized payloads
        if is_slack:
            body = {
                "text": f"⚡ SyncOps AI Broadcast: {payload_data.get('meeting_title', 'Operational Sync')}",
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": f"🚨 {payload_data.get('meeting_title', 'Operational Broadcast')[:140]}",
                            "emoji": True
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*Target Go-Live:* `{payload_data.get('target_milestone', 'Upcoming')}`\n*SOP ID:* `{payload_data.get('sop_id', 'SOP-2026')}`"
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": slack_markdown[:2900] if slack_markdown else "Operational deliverables dispatched."
                        }
                    }
                ]
            }
        elif is_discord:
            body = {
                "content": f"⚡ **SyncOps AI Broadcast: {payload_data.get('meeting_title')}**",
                "embeds": [
                    {
                        "title": f"SOP Generated: {payload_data.get('sop_id')}",
                        "description": (slack_markdown[:2000] if slack_markdown else "Operational deliverables dispatched."),
                        "color": 3901686, # Hex #3B82F6 in decimal
                        "fields": [
                            {"name": "Target Milestone", "value": str(payload_data.get("target_milestone")), "inline": True},
                            {"name": "Action Items Count", "value": str(payload_data.get("action_items_count")), "inline": True}
                        ]
                    }
                ]
            }
        else:
            # Generic / n8n / Make.com JSON payload
            body = payload_data

        if not requests:
            return {
                "success": False,
                "status_code": 500,
                "message": "requests library is required for live network dispatch.",
                "latency_ms": 0
            }

        try:
            resp = requests.post(webhook_url, json=body, timeout=timeout_seconds)
            latency = round((time.time() - start_time) * 1000, 1)
            
            if resp.status_code in [200, 201, 204]:
                return {
                    "success": True,
                    "status_code": resp.status_code,
                    "message": f"Successfully delivered to {resp.url} in {latency}ms.",
                    "latency_ms": latency
                }
            else:
                return {
                    "success": False,
                    "status_code": resp.status_code,
                    "message": f"Server returned error code {resp.status_code}: {resp.text[:200]}",
                    "latency_ms": latency
                }
        except Exception as e:
            latency = round((time.time() - start_time) * 1000, 1)
            return {
                "success": False,
                "status_code": 500,
                "message": f"Network delivery error: {str(e)}",
                "latency_ms": latency
            }
