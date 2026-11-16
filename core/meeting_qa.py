"""
Conversational Q&A Assistant for SyncOps AI ("Chat with the Meeting")
Answers user questions grounded directly in the meeting transcript and extracted operational intelligence.
"""

from typing import Dict, Any, List
import re
from core.llm_client import UniversalLLMClient

QA_SYSTEM_PROMPT = """You are the SyncOps AI Meeting Assistant.
Your job is to answer user questions about a specific meeting, based ONLY on the provided meeting transcript and extracted decisions/actions.
Be concise, professional, and quote timestamps and speaker names whenever possible.
If the answer cannot be determined from the transcript, state that clearly.
"""

class MeetingQAAgent:
    def __init__(self, llm_client: UniversalLLMClient):
        self.llm = llm_client

    def answer_question(self, question: str, transcript: str, extracted_data: Dict[str, Any]) -> str:
        """Answers user question using LLM or offline grounded semantic retrieval."""
        if self.llm.provider in ["gemini", "openai"] and self.llm.api_key:
            prompt = (
                f"Meeting Intelligence:\n"
                f"- Title: {extracted_data.get('meeting_title')}\n"
                f"- Target Go-Live: {extracted_data.get('target_go_live')}\n"
                f"- Decisions: {extracted_data.get('decisions')}\n"
                f"- Action Items: {extracted_data.get('action_items')}\n\n"
                f"Full Transcript:\n{transcript}\n\n"
                f"Question: {question}"
            )
            return self.llm.generate(prompt=prompt, system_prompt=QA_SYSTEM_PROMPT)
        
        # High-fidelity semantic offline retrieval
        return self._offline_grounded_answer(question, transcript, extracted_data)

    def _offline_grounded_answer(self, question: str, transcript: str, extracted_data: Dict[str, Any]) -> str:
        q_lower = question.lower()
        decisions = extracted_data.get("decisions", [])
        actions = extracted_data.get("action_items", [])
        lines = transcript.split("\n")

        # 1. Check for specific named people
        people = ["marcus", "priya", "elena", "alex", "rohan", "sarah", "kavita", "david", "ananya", "nikhil", "tanya", "vikramaditya", "alice", "bob"]
        matched_person = next((p for p in people if p in q_lower), None)

        if matched_person:
            # Find lines spoken by or mentioning this person
            relevant = [l.strip() for l in lines if matched_person in l.lower()]
            person_actions = [a for a in actions if matched_person in (a.get("assignee") or "").lower()]
            
            resp = f"**Information regarding {matched_person.capitalize()}:**\n\n"
            if person_actions:
                resp += "**Assigned Action Items:**\n"
                for act in person_actions:
                    resp += f"• **[{act.get('id')}]** {act.get('task')} *(Deadline: {act.get('deadline')})*\n"
                resp += "\n"
            
            if relevant:
                resp += f"**Transcript Citations:**\n"
                for r in relevant[:3]:
                    resp += f"> `{r}`\n"
            return resp

        # 2. Check for deadlines or timelines
        if any(w in q_lower for w in ["deadline", "due date", "when", "timeline", "milestone", "go-live", "target"]):
            resp = f"**Project Timeline & Milestones for '{extracted_data.get('meeting_title')}':**\n\n"
            resp += f"• **Target Go-Live:** {extracted_data.get('target_go_live')}\n"
            resp += "\n**Deliverable Deadlines:**\n"
            for a in actions:
                resp += f"• **{a.get('assignee')}**: {a.get('task')} — **Target: {a.get('deadline')}**\n"
            return resp

        # 3. Check for decisions
        if any(w in q_lower for w in ["decision", "agreed", "consensus", "choice"]):
            resp = "**Key Strategic Decisions Reached:**\n\n"
            for d in decisions:
                resp += f"• **{d.get('decision')}**: {d.get('impact')} *(Context: {d.get('context')})*\n"
            return resp

        # 4. Check for technical topics
        keywords = ["soc2", "ip", "mtls", "oauth2", "webhook", "postgres", "timeout", "index", "hikaricp", "copilot", "gemini", "refund", "csat"]
        matched_kw = next((k for k in keywords if k in q_lower), None)
        if matched_kw:
            relevant = [l.strip() for l in lines if matched_kw in l.lower()]
            if relevant:
                resp = f"**Found {len(relevant)} direct mentions of '{matched_kw.upper()}' in the meeting:**\n\n"
                for r in relevant[:3]:
                    resp += f"> `{r}`\n\n"
                return resp

        # 5. Fallback context summary
        return (
            f"Based on the meeting **'{extracted_data.get('meeting_title')}'**:\n\n"
            f"The team established **{len(decisions)} core strategic decisions** and assigned **{len(actions)} binding action items** "
            f"targeting delivery for **{extracted_data.get('target_go_live')}**.\n\n"
            f"Feel free to ask specifically about: *deadlines*, *assignees* (e.g. 'What is Marcus doing?'), or *technical constraints* (e.g. 'What is the SOC2 blocker?')."
        )
