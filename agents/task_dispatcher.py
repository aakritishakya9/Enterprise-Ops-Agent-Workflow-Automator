"""
Task & Ticket Dispatcher Agent for SyncOps AI
Converts extracted action items into production-ready Jira, Linear, and GitHub issues,
and provides CSV / JSON export formats for enterprise project management tools.
"""

from typing import Dict, Any, List
import pandas as pd
import json

class TaskDispatcherAgent:
    def __init__(self):
        pass

    def dispatch(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        action_items = extracted_data.get("action_items", [])
        title = extracted_data.get("meeting_title", "General Project")
        
        tickets = []
        rows_for_csv = []
        
        for idx, item in enumerate(action_items, 1):
            ticket_id = item.get("id", f"TASK-{idx:03d}")
            task_name = item.get("task", f"Task item {idx}")
            assignee = item.get("assignee", "Unassigned")
            role = item.get("role", "Engineer")
            priority = item.get("priority", "Medium")
            deadline = item.get("deadline", "Next Sprint")
            category = item.get("category", "Operations")
            
            # Acceptance Criteria Generation
            acceptance_criteria = [
                f"Verify '{task_name}' meets delivery criteria established in {title}.",
                f"Peer review and signoff completed by {assignee} ({role}).",
                f"All configuration changes or schema updates tested against staging environment prior to {deadline}."
            ]
            
            ticket = {
                "key": ticket_id,
                "summary": task_name,
                "assignee": assignee,
                "role": role,
                "priority": priority,
                "deadline": deadline,
                "category": category,
                "issue_type": "Task" if priority in ["Medium", "Low"] else "Story",
                "epic": title[:30],
                "description": (
                    f"**Context:** Originates from {title}.\n\n"
                    f"**Objective:** {task_name}\n\n"
                    f"**Assignee:** {assignee} ({role})\n"
                    f"**Deadline Target:** {deadline}\n\n"
                    f"**Acceptance Criteria:**\n"
                    + "\n".join([f"- [ ] {ac}" for ac in acceptance_criteria])
                )
            }
            tickets.append(ticket)
            
            rows_for_csv.append({
                "Issue Key": ticket_id,
                "Issue Type": ticket["issue_type"],
                "Summary": task_name,
                "Assignee": assignee,
                "Priority": priority,
                "Due Date": deadline,
                "Component/Category": category,
                "Description": ticket["description"]
            })
            
        df = pd.DataFrame(rows_for_csv)
        csv_string = df.to_csv(index=False)
        
        return {
            "tickets": tickets,
            "dataframe": df,
            "csv_string": csv_string,
            "total_tickets": len(tickets),
            "critical_count": sum(1 for t in tickets if t["priority"] in ["Critical", "High"])
        }
