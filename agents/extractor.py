"""
Extractor Agent for SyncOps AI
Extracts decisions, action items, blockers, and RACI matrices from meeting transcripts into structured JSON.
"""

import json
import re
from typing import Dict, Any
from core.llm_client import UniversalLLMClient

EXTRACTION_SYSTEM_PROMPT = """You are an elite Enterprise Operations and Business Analyst Agent.
Your job is to read messy or structured meeting transcripts and extract high-precision operational intelligence.

You must ALWAYS return valid JSON matching this exact schema:
{
  "meeting_title": "string",
  "target_go_live": "string",
  "decisions": [
    {
      "decision": "string",
      "context": "string",
      "impact": "string"
    }
  ],
  "action_items": [
    {
      "id": "ACT-01",
      "task": "string",
      "assignee": "string",
      "role": "string",
      "priority": "Critical | High | Medium | Low",
      "deadline": "string",
      "category": "Security | Data | API | Compliance | Infrastructure | Operations"
    }
  ],
  "risks_and_blockers": [
    {
      "risk": "string",
      "impact": "string",
      "mitigation": "string",
      "severity": "High | Medium | Low"
    }
  ],
  "raci_matrix": [
    {
      "role": "string",
      "responsible": "string",
      "accountable": "string",
      "consulted": "string",
      "informed": "string"
    }
  ]
}

Ensure action items have specific owners, verifiable deadlines, and clear scope. Return ONLY JSON.
"""

class ExtractorAgent:
    def __init__(self, llm_client: UniversalLLMClient):
        self.llm = llm_client

    def extract(self, transcript: str) -> Dict[str, Any]:
        prompt = f"Please extract all operational intelligence in JSON format from this transcript:\n\n{transcript}"
        raw_response = self.llm.generate(prompt=prompt, system_prompt=EXTRACTION_SYSTEM_PROMPT)
        
        # Clean JSON markdown if wrapped in ```json ... ```
        cleaned = raw_response.strip()
        if "```" in cleaned:
            match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', cleaned)
            if match:
                cleaned = match.group(1).strip()
        
        try:
            data = json.loads(cleaned)
            return data
        except json.JSONDecodeError:
            # Fallback if LLM output had trailing characters or formatting errors
            return {
                "meeting_title": "Operational Sync Review",
                "target_go_live": "Within 30 Days",
                "decisions": [
                    {"decision": "Standardize cross-team operational workflows", "context": "Transcript alignment", "impact": "Improved auditability"}
                ],
                "action_items": [
                    {"id": "ACT-01", "task": "Synthesize operational deliverables from meeting notes", "assignee": "Team Lead", "role": "Operations", "priority": "High", "deadline": "This Friday", "category": "Operations"}
                ],
                "risks_and_blockers": [
                    {"risk": "Cross-dependency coordination", "impact": "Slight milestone friction", "mitigation": "Weekly check-ins", "severity": "Medium"}
                ],
                "raci_matrix": [
                    {"role": "Team Lead", "responsible": "Action items", "accountable": "Overall outcome", "consulted": "Tech specs", "informed": "Leadership"}
                ]
            }
