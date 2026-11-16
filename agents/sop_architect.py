"""
SOP Architect Agent for SyncOps AI
Transforms extracted meeting intelligence into publication-ready Standard Operating Procedures (SOPs)
complete with Mermaid workflow diagrams and audit checklists.
"""

from typing import Dict, Any, List

class SOPArchitectAgent:
    def __init__(self, llm_client=None):
        self.llm = llm_client

    def generate_sop(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        title = extracted_data.get("meeting_title", "Enterprise Standard Operating Procedure")
        go_live = extracted_data.get("target_go_live", "Immediate")
        actions = extracted_data.get("action_items", [])
        decisions = extracted_data.get("decisions", [])
        risks = extracted_data.get("risks_and_blockers", [])
        
        # Build Mermaid Workflow Diagram
        mermaid_lines = [
            "graph TD",
            "    A[Stakeholder Alignment & Meeting Output] --> B[Phase 1: Prerequisites & Security Gate]",
            "    B --> C[Phase 2: Execution & Core Workflows]",
            "    C --> D[Phase 3: QA Verification & Milestone Check]",
            "    D --> E{Criteria Met?}",
            "    E -- Yes --> F[Approved Production Go-Live]",
            "    E -- No --> G[Severity Escalation & Rollback Plan]"
        ]
        
        # Add dynamic nodes based on actions
        for i, a in enumerate(actions[:4], 1):
            task_clean = a.get("task", f"Task {i}")[:35].replace('"', '')
            mermaid_lines.append(f'    C --> T{i}["{a.get("assignee", "Owner")}: {task_clean}"]')
        
        mermaid_code = "\n".join(mermaid_lines)

        sop_id = "SOP-OPS-2026-X1"
        if "Fintech" in title:
            sop_id = "SOP-INT-FINTECH-01"
        elif "Incident" in title or "INC-" in title:
            sop_id = "SOP-INC-DB-8902"
        elif "Copilot" in title or "AI" in title:
            sop_id = "SOP-AI-COPILOT-Q1"

        # Construct Execution Steps from Actions
        execution_steps = []
        phase_map = {
            0: "Phase 1: Environment & Credential Provisioning",
            1: "Phase 2: Technical Implementation & Schema Integration",
            2: "Phase 3: Verification, Staging & Test Execution",
            3: "Phase 4: Final Signoff & Production Enablement"
        }
        
        for idx, act in enumerate(actions):
            p_name = phase_map.get(idx, f"Phase {idx + 1}: Execution Step")
            execution_steps.append({
                "phase": p_name,
                "owner": act.get("assignee", "Responsible Lead"),
                "deadline": act.get("deadline", "TBD"),
                "details": f"{act.get('task')} (Category: {act.get('category', 'Operations')}). Must be verified by designated stakeholder prior to gate transition."
            })

        # Construct Full Markdown Document
        markdown_content = f"""# {sop_id}: {title}

**Effective Date:** November 2026  
**Document ID:** `{sop_id}`  
**Target Milestone:** {go_live}  
**Classification:** Confidential / Enterprise Operations  

---

## 1. Purpose & Scope
This Standard Operating Procedure (SOP) formalizes the operational protocols, security mandates, and cross-functional responsibilities established during stakeholder alignment. 
It establishes deterministic execution gates to guarantee delivery reliability, zero-trust security compliance, and rapid error resolution.

## 2. Core Decisions & Operating Baseline
"""
        for d in decisions:
            markdown_content += f"- **{d.get('decision')}:** {d.get('context')} *(Impact: {d.get('impact')})*\n"

        markdown_content += "\n## 3. Workflow Architecture Diagram\n```mermaid\n" + mermaid_code + "\n```\n\n"

        markdown_content += "## 4. Step-by-Step Procedure & Delivery Gates\n"
        for s in execution_steps:
            markdown_content += f"### {s['phase']}\n"
            markdown_content += f"- **Responsible Lead:** {s['owner']}\n"
            markdown_content += f"- **Target Milestone:** {s['deadline']}\n"
            markdown_content += f"- **Procedure:** {s['details']}\n\n"

        markdown_content += "## 5. Risk Mitigation & Exception Handling\n"
        for r in risks:
            markdown_content += f"- **Risk:** {r.get('risk')} *(Severity: {r.get('severity', 'Medium')})*\n"
            markdown_content += f"  - *Impact:* {r.get('impact')}\n"
            markdown_content += f"  - *Mitigation Protocol:* {r.get('mitigation')}\n"

        markdown_content += """
---
## 6. Audit & Verification Checklist
- [ ] Static credentials and mTLS certs verified against zero-trust policy.
- [ ] End-to-end integration tests validated in non-production staging.
- [ ] Automated monitoring webhooks and alert thresholds activated in PagerDuty.
- [ ] Stakeholder signoff recorded in executive audit log.
"""

        return {
            "sop_id": sop_id,
            "title": title,
            "effective_date": "November 2026",
            "purpose": f"Establishes binding operational procedures and verification gates for {title}.",
            "scope": "Applies across client engineering, DevOps, SecOps, and Project Management teams.",
            "prerequisites": [
                "Zero-trust credential verification and IP CIDR provisioning completed.",
                "Schema contracts and Postman API specifications distributed to all engineers.",
                "Service Level Agreement (SLA) terms confirmed by authorized leadership."
            ],
            "execution_steps": execution_steps,
            "mermaid_code": mermaid_code,
            "markdown": markdown_content
        }
