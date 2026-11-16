"""
Meeting Efficiency & ROI Analytics Engine for SyncOps AI
Calculates Actionability Index, Accountability Ratio, Meeting Cost, and Time Saved.
Aligned with SkillfyAI's "Every person owns a number" principle.
"""

from typing import Dict, Any, List


class MeetingROIEngine:
    @staticmethod
    def calculate_metrics(
        extracted_data: Dict[str, Any],
        transcript_text: str,
        avg_hourly_rate: float = 65.0,
        meeting_duration_minutes: int = 30
    ) -> Dict[str, Any]:
        """Calculates executive metrics on meeting productivity, cost, and automated savings."""
        decisions = extracted_data.get("decisions", [])
        actions = extracted_data.get("action_items", [])
        risks = extracted_data.get("risks_and_blockers", [])
        raci = extracted_data.get("raci_matrix", [])

        # 1. Total Participant Count (from RACI or unique assignees)
        unique_stakeholders = set()
        for a in actions:
            if a.get("assignee") and a.get("assignee") != "Unassigned":
                unique_stakeholders.add(a.get("assignee"))
        for r in raci:
            if r.get("role"):
                unique_stakeholders.add(r.get("role"))
        
        participant_count = max(len(unique_stakeholders), 4)

        # 2. Meeting Cost Calculation
        meeting_hours = meeting_duration_minutes / 60.0
        direct_meeting_cost = round(participant_count * meeting_hours * avg_hourly_rate, 2)

        # 3. Post-Meeting Admin Hours (Without AI: ~4.5 hours across team)
        manual_admin_hours = 4.5
        manual_admin_cost = round(manual_admin_hours * avg_hourly_rate, 2)
        total_traditional_cost = direct_meeting_cost + manual_admin_cost

        # With SyncOps AI: turnaround is <2 minutes (0.03 hours)
        automated_admin_hours = 0.05
        ai_cost = round(automated_admin_hours * avg_hourly_rate, 2)
        total_ai_cost = direct_meeting_cost + ai_cost
        net_savings_per_meeting = round(manual_admin_cost - ai_cost, 2)

        # 4. Actionability Index (Decisions + Actions per 100 words of dialogue)
        word_count = max(len(transcript_text.split()), 100)
        actionable_events = len(decisions) + len(actions)
        actionability_index = min(round((actionable_events / (word_count / 100)) * 10, 1), 100.0)

        # 5. Accountability Ratio (% of actions with single named individuals, not vague groups)
        vague_terms = ["team", "everyone", "unassigned", "leadership", "all"]
        named_owners = 0
        for act in actions:
            assignee = (act.get("assignee") or "").lower()
            if assignee and not any(v in assignee for v in vague_terms):
                named_owners += 1
        
        accountability_ratio = round((named_owners / max(len(actions), 1)) * 100, 1)

        # 6. Overall Meeting Health Grade (A+, A, B, C)
        if accountability_ratio >= 85 and actionability_index >= 40:
            health_grade = "A+ (Executive Grade)"
        elif accountability_ratio >= 70:
            health_grade = "A (High Actionability)"
        elif accountability_ratio >= 50:
            health_grade = "B (Moderate Alignment)"
        else:
            health_grade = "C (Needs Better Ownership)"

        return {
            "participant_count": participant_count,
            "meeting_duration_minutes": meeting_duration_minutes,
            "direct_meeting_cost": direct_meeting_cost,
            "manual_admin_cost": manual_admin_cost,
            "net_savings_per_meeting": net_savings_per_meeting,
            "time_saved_hours": manual_admin_hours,
            "actionability_index": actionability_index,
            "accountability_ratio": accountability_ratio,
            "health_grade": health_grade,
            "total_decisions": len(decisions),
            "total_actions": len(actions),
            "total_risks": len(risks)
        }
