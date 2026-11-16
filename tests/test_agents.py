"""
End-to-End Unit & Integration Tests for SyncOps AI
Tests Extractor, SOP Architect, Task Dispatcher, Comms, ROI Analytics, Audio Processor, 
Webhooks, Calendar Export, Dependency Analyzer, Multi-Platform Formatter, and Q&A Engine.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.llm_client import UniversalLLMClient
from core.templates import TEMPLATES
from core.pdf_generator import generate_sop_pdf
from core.roi_analytics import MeetingROIEngine
from core.audio_processor import AudioProcessor
from core.webhook_sender import LiveWebhookDispatcher
from core.calendar_export import CalendarExportEngine
from core.dependency_analyzer import DependencyAnalyzer
from core.export_formatter import MultiPlatformExportFormatter
from core.meeting_qa import MeetingQAAgent
from agents.extractor import ExtractorAgent
from agents.sop_architect import SOPArchitectAgent
from agents.task_dispatcher import TaskDispatcherAgent
from agents.comms_agent import CommsAgent


def test_full_platform_capabilities():
    client = UniversalLLMClient(provider="demo")
    extractor = ExtractorAgent(client)
    sop_architect = SOPArchitectAgent(client)
    dispatcher = TaskDispatcherAgent()
    comms = CommsAgent()
    audio_proc = AudioProcessor()
    qa_agent = MeetingQAAgent(client)

    # 1. Test Audio Processor
    audio_transcript = audio_proc.transcribe(b"", file_name="fintech_onboarding_call_recording.wav")
    assert len(audio_transcript) > 50, "Audio transcription failed"
    print("  [PASS] Audio Processor fallback verified.")

    # 2. Test Live Webhook Dispatcher
    dummy_payload = {"meeting_title": "Test Sync", "action_items_count": 2}
    invalid_dispatch = LiveWebhookDispatcher.dispatch("", dummy_payload)
    assert not invalid_dispatch["success"], "Empty URL should fail gracefully"
    print("  [PASS] Live Webhook Dispatcher validation verified.")

    # 3. Test Templates & Core Pipeline
    for name, t_data in TEMPLATES.items():
        print(f"Testing template: {name}...")
        transcript = t_data["transcript"]
        
        # 1. Extraction Agent
        extracted = extractor.extract(transcript)
        assert "meeting_title" in extracted, "Missing meeting_title in extraction"
        assert len(extracted.get("action_items", [])) > 0, "No action items extracted"
        assert len(extracted.get("decisions", [])) > 0, "No decisions extracted"

        # 2. ROI Analytics Engine
        roi = MeetingROIEngine.calculate_metrics(extracted, transcript)
        assert roi["net_savings_per_meeting"] > 0, "ROI calculation error"

        # 3. SOP Architect Agent
        sop = sop_architect.generate_sop(extracted)
        assert "sop_id" in sop, "Missing sop_id"

        # 4. Task Dispatcher Agent
        dispatch_result = dispatcher.dispatch(extracted)
        assert dispatch_result["total_tickets"] > 0, "No tickets dispatched"

        # 5. Dependency & Critical Path Analyzer (Upgrade 3)
        dep = DependencyAnalyzer.analyze(extracted.get("action_items", []), extracted.get("meeting_title", "Project"))
        assert "gantt" in dep["mermaid_gantt"], "Gantt generation error"
        assert dep["parallelizability_score"] > 0, "Parallelizability error"

        # 6. Calendar Export Engine (Upgrade 2)
        ics_text = CalendarExportEngine.generate_ics(extracted.get("action_items", []), extracted.get("meeting_title", "Project"))
        assert "BEGIN:VCALENDAR" in ics_text and "END:VCALENDAR" in ics_text, "Invalid iCalendar syntax"
        gcal_url = CalendarExportEngine.generate_google_calendar_url(extracted["action_items"][0], extracted["meeting_title"])
        assert "calendar.google.com" in gcal_url, "Invalid Google Calendar URL"

        # 7. Multi-Platform Export Hub (Upgrade 4)
        notion_md = MultiPlatformExportFormatter.to_notion(extracted, sop)
        assert "# ⚡" in notion_md, "Notion formatting error"
        jira_wiki = MultiPlatformExportFormatter.to_jira_markup(extracted, sop)
        assert "h1." in jira_wiki, "Jira markup formatting error"
        conf_html = MultiPlatformExportFormatter.to_confluence_html(extracted, sop)
        assert "<table>" in conf_html or "<table" in conf_html, "Confluence HTML formatting error"

        # 8. Meeting Q&A Agent (Upgrade 1)
        ans_deadline = qa_agent.answer_question("When is the deadline?", transcript, extracted)
        assert len(ans_deadline) > 20, "Q&A answer empty"
        ans_risk = qa_agent.answer_question("What is the blocker?", transcript, extracted)
        assert len(ans_risk) > 20, "Q&A blocker empty"

        # 9. PDF Generator
        pdf_bytes = generate_sop_pdf(sop, extracted)
        assert len(pdf_bytes) > 500, f"PDF generation failed, size {len(pdf_bytes)}"

        print(f"  [PASS] {name} passed with all 4 advanced features (Q&A, Calendar, Critical Path, Export Hub)!")

    print("\nAll end-to-end upgrade tests passed with 100% success!")


if __name__ == "__main__":
    test_full_platform_capabilities()
