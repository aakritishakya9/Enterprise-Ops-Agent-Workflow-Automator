"""
Multi-Platform Export Formatter for SyncOps AI
Formats meeting intelligence into native Notion Markdown, Jira Wiki Markup, and Confluence HTML.
"""

from typing import Dict, Any, List


class MultiPlatformExportFormatter:
    @staticmethod
    def to_notion(extracted: Dict[str, Any], sop: Dict[str, Any]) -> str:
        """Formats output into Notion-optimized Markdown with callouts and toggle blocks."""
        title = extracted.get("meeting_title", "Enterprise Alignment")
        target = extracted.get("target_go_live", "Upcoming Milestone")
        decisions = extracted.get("decisions", [])
        actions = extracted.get("action_items", [])
        risks = extracted.get("risks_and_blockers", [])

        lines = [
            f"# ⚡ {title}",
            f"> 🎯 **Target Go-Live:** {target} | **SOP Reference:** `{sop.get('sop_id', 'SOP-2026')}`",
            "",
            "## 📌 Key Decisions & Strategic Baseline",
            ""
        ]
        for d in decisions:
            lines.append(f"> 💡 **{d.get('decision')}**")
            lines.append(f"> *Context:* {d.get('context')} | *Impact:* {d.get('impact')}")
            lines.append("")

        lines.extend([
            "## 📋 Action Item Backlog",
            "| ID | Task | Assignee | Priority | Deadline |",
            "| :--- | :--- | :--- | :--- | :--- |"
        ])
        for a in actions:
            p_icon = "🔴" if a.get("priority") in ["Critical", "High"] else "🟡"
            lines.append(f"| `{a.get('id')}` | {a.get('task')} | **{a.get('assignee')}** | {p_icon} {a.get('priority')} | {a.get('deadline')} |")

        lines.extend([
            "",
            "## ⚠️ Risk & Blocker Registry",
            "<details>",
            "<summary>Click to view active mitigations</summary>",
            ""
        ])
        for r in risks:
            lines.append(f"- **Risk:** {r.get('risk')} *(Severity: {r.get('severity', 'Medium')})*")
            lines.append(f"  - *Mitigation:* {r.get('mitigation')}")
        lines.append("</details>")

        return "\n".join(lines)

    @staticmethod
    def to_jira_markup(extracted: Dict[str, Any], sop: Dict[str, Any]) -> str:
        """Formats output into Jira Wiki Markup format (native h1., ||table||, {panel})."""
        title = extracted.get("meeting_title", "Enterprise Alignment")
        target = extracted.get("target_go_live", "Upcoming Milestone")
        decisions = extracted.get("decisions", [])
        actions = extracted.get("action_items", [])

        lines = [
            f"h1. (flag) {title}",
            f"{{panel:title=Delivery Milestone: {target}|borderStyle=solid|borderColor=#38BDF8|titleBGColor=#0F172A|bgColor=#1E293B}}",
            f"SOP Document: *{sop.get('sop_id')}* | Automated by SyncOps AI",
            "{panel}",
            "",
            "h2. Key Operational Decisions",
        ]
        for d in decisions:
            lines.append(f"* *{d.get('decision')}*: {d.get('impact')} _(Context: {d.get('context')})_")

        lines.extend([
            "",
            "h2. Action Items Register",
            "||Issue Key||Summary||Assignee||Priority||Due Date||"
        ])
        for a in actions:
            lines.append(f"|{a.get('id')}|{a.get('task')}|{a.get('assignee')}|{a.get('priority')}|{a.get('deadline')}|")

        return "\n".join(lines)

    @staticmethod
    def to_confluence_html(extracted: Dict[str, Any], sop: Dict[str, Any]) -> str:
        """Formats output into clean Confluence HTML Storage Format."""
        title = extracted.get("meeting_title", "Enterprise Alignment")
        target = extracted.get("target_go_live", "Upcoming Milestone")
        actions = extracted.get("action_items", [])
        decisions = extracted.get("decisions", [])

        html = f"""<div style="font-family: -apple-system, BlinkMacSystemFont, sans-serif; line-height: 1.6;">
    <div style="background-color: #0F172A; color: #FFFFFF; padding: 16px 20px; border-radius: 8px; border-left: 6px solid #38BDF8; margin-bottom: 20px;">
        <h2 style="margin: 0 0 6px 0; color: #FFFFFF;">{title}</h2>
        <p style="margin: 0; color: #94A3B8; font-size: 14px;"><strong>Target Go-Live:</strong> {target} | <strong>SOP ID:</strong> {sop.get('sop_id')}</p>
    </div>

    <h3>1. Core Decisions</h3>
    <ul>
"""
        for d in decisions:
            html += f"        <li><strong>{d.get('decision')}</strong>: {d.get('impact')} <span style='color:#64748B;'>({d.get('context')})</span></li>\n"

        html += """    </ul>

    <h3>2. Action Item Ownership Matrix</h3>
    <table style="width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 14px;">
        <thead>
            <tr style="background-color: #1E293B; color: #FFFFFF; text-align: left;">
                <th style="padding: 10px; border: 1px solid #334155;">ID</th>
                <th style="padding: 10px; border: 1px solid #334155;">Task Description</th>
                <th style="padding: 10px; border: 1px solid #334155;">Assignee</th>
                <th style="padding: 10px; border: 1px solid #334155;">Priority</th>
                <th style="padding: 10px; border: 1px solid #334155;">Target Deadline</th>
            </tr>
        </thead>
        <tbody>
"""
        for a in actions:
            html += f"""            <tr>
                <td style="padding: 8px 10px; border: 1px solid #E2E8F0; font-weight: bold;">{a.get('id')}</td>
                <td style="padding: 8px 10px; border: 1px solid #E2E8F0;">{a.get('task')}</td>
                <td style="padding: 8px 10px; border: 1px solid #E2E8F0;"><strong>{a.get('assignee')}</strong></td>
                <td style="padding: 8px 10px; border: 1px solid #E2E8F0;">{a.get('priority')}</td>
                <td style="padding: 8px 10px; border: 1px solid #E2E8F0;">{a.get('deadline')}</td>
            </tr>\n"""

        html += """        </tbody>
    </table>
</div>"""
        return html
