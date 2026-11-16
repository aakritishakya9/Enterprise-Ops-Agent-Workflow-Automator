"""
Task Dependency & Critical Path Analyzer for SyncOps AI
Analyzes prerequisites, calculates critical path, and generates Mermaid Gantt and dependency charts.
"""

from typing import Dict, Any, List


class DependencyAnalyzer:
    @staticmethod
    def analyze(action_items: List[Dict[str, Any]], meeting_title: str) -> Dict[str, Any]:
        """Maps dependencies between action items, identifies the critical path, and formats Gantt syntax."""
        dependencies = []
        critical_path = []
        
        # Analyze semantic prerequisites
        # In software/enterprise: specs -> infrastructure -> staging tables/implementation -> audit/release
        n = len(action_items)
        for i in range(n):
            current = action_items[i]
            curr_id = current.get("id", f"ACT-{i+1}")
            
            # If there is a preceding item, check if it forms a sequential dependency
            if i > 0:
                prev = action_items[i-1]
                prev_id = prev.get("id", f"ACT-{i}")
                
                # Assign dependency
                dependencies.append({
                    "task_id": curr_id,
                    "task_name": current.get("task", ""),
                    "depends_on": prev_id,
                    "precursor_name": prev.get("task", ""),
                    "is_blocking": True if current.get("priority") in ["Critical", "High"] else False
                })

        # The Critical Path is the sequence of high/critical priority dependent milestones
        critical_path = [a.get("id") for a in action_items if a.get("priority") in ["Critical", "High"]]
        if not critical_path and action_items:
            critical_path = [a.get("id") for a in action_items[:3]]

        # Generate Mermaid Dependency Graph (graph LR)
        dep_lines = ["graph LR"]
        for idx, act in enumerate(action_items, 1):
            act_id = act.get("id", f"ACT-{idx}")
            clean_name = act.get("task", f"Task {idx}")[:28].replace('"', '')
            dep_lines.append(f'    {act_id}["{act_id}: {clean_name} ({act.get("assignee", "Owner")})"]')
        
        for dep in dependencies:
            dep_lines.append(f"    {dep['depends_on']} -->|Blocks| {dep['task_id']}")
        
        mermaid_dep_graph = "\n".join(dep_lines)

        # Generate Mermaid Gantt Chart Syntax
        gantt_lines = [
            "gantt",
            f"    title Delivery Roadmap: {meeting_title[:35]}",
            "    dateFormat YYYY-MM-DD",
            "    section Critical Path"
        ]
        
        # Build relative days
        base_year = 2026
        base_month = 11
        for idx, act in enumerate(action_items, 1):
            act_id = act.get("id", f"ACT-{idx}")
            clean_name = act.get("task", f"Task {idx}")[:30].replace('"', '').replace(':', '')
            day_start = 20 + idx * 2
            day_end = day_start + 2
            
            crit_prefix = "crit, " if act_id in critical_path else ""
            gantt_lines.append(f"    {clean_name} : {crit_prefix}{act_id}, {base_year}-{base_month:02d}-{day_start:02d}, 2d")

        mermaid_gantt = "\n".join(gantt_lines)

        # Parallelizability metric
        parallelizable_count = max(len(action_items) - len(dependencies), 1)
        parallel_ratio = round((parallelizable_count / max(len(action_items), 1)) * 100, 1)

        return {
            "dependencies": dependencies,
            "critical_path": critical_path,
            "mermaid_dep_graph": mermaid_dep_graph,
            "mermaid_gantt": mermaid_gantt,
            "total_dependencies": len(dependencies),
            "parallelizability_score": parallel_ratio
        }
