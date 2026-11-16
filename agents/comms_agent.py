"""
Executive Communications Agent for SyncOps AI
Drafts formal C-Suite / Client briefing emails and Slack/Teams broadcasts based on extracted intelligence.
"""

from typing import Dict, Any

class CommsAgent:
    def __init__(self):
        pass

    def generate_comms(self, extracted_data: Dict[str, Any], sop_data: Dict[str, Any]) -> Dict[str, str]:
        title = extracted_data.get("meeting_title", "Operational Sync")
        go_live = extracted_data.get("target_go_live", "Upcoming Milestone")
        decisions = extracted_data.get("decisions", [])
        actions = extracted_data.get("action_items", [])
        risks = extracted_data.get("risks_and_blockers", [])
        sop_id = sop_data.get("sop_id", "SOP-OPS-2026")

        # Client Briefing Email Draft
        decisions_bullet = "\n".join([f"  • {d.get('decision')}: {d.get('impact')}" for d in decisions])
        actions_bullet = "\n".join([f"  • [{a.get('id')}] {a.get('task')} — Owner: {a.get('assignee')} (Target: {a.get('deadline')})" for a in actions])
        
        email_body = f"""Subject: Executive Briefing & Action Register: {title}

Hi Team & Stakeholders,

Thank you for your focused participation in today's alignment session regarding {title}. 

Our target delivery milestone remains firmly set for: {go_live}.

Below is an executive summary of key decisions reached, binding action items, and governance protocols.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. KEY DECISIONS ALIGNED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{decisions_bullet}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2. ACTION REGISTER & COMMITMENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{actions_bullet}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3. GOVERNANCE & OPERATIONAL SAFEGUARDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Standard Operating Procedure {sop_id} has been formally generated and archived in our compliance repository. 

Key Risk Mitigation:
"""
        for r in risks:
            email_body += f"  • Risk: {r.get('risk')} | Mitigation: {r.get('mitigation')}\n"

        email_body += f"""
Our next governance check-in will review closed deliverables against the action register. If you identify any blocking dependencies, please escalate immediately.

Best regards,

SyncOps AI Executive Orchestrator
On Behalf of Project Leadership
"""

        # Slack / Teams Broadcast Markdown
        slack_msg = f"""🚨 *OPERATIONAL BROADCAST: {title.upper()}* 🚨
*Target Go-Live:* `{go_live}` | *SOP Reference:* `{sop_id}`

*🔑 Key Decisions:*
"""
        for d in decisions:
            slack_msg += f"• *{d.get('decision')}*: {d.get('impact')}\n"

        slack_msg += "\n*📋 Action Register & Deadlines:*\n"
        for a in actions:
            p_badge = "🔥" if a.get("priority") in ["Critical", "High"] else "📌"
            slack_msg += f"{p_badge} *{a.get('assignee')}* ({a.get('deadline')}): {a.get('task')}\n"

        if risks:
            slack_msg += "\n*⚠️ Open Risks & Mitigations:*\n"
            for r in risks:
                slack_msg += f"• *{r.get('risk')}*: {r.get('mitigation')}\n"

        slack_msg += "\n_Full SOP documentation and Jira tickets have been auto-dispatched._ 🚀"

        return {
            "email_subject": f"Executive Briefing & Action Register: {title}",
            "email_body": email_body.strip(),
            "slack_message": slack_msg.strip()
        }
