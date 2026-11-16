"""
End-to-End Unit & Integration Tests for SyncOps AI
Tests Extractor, SOP Architect, Task Dispatcher, Comms, ROI Analytics, Audio Processor, and Webhooks.
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
from agents.extractor import ExtractorAgent
from agents.sop_architect import SOPArchitectAgent
from agents.task_dispatcher import TaskDispatcherAgent
from agents.comms_agent import CommsAgent


def test_pipeline_on_all_templates():
    client = UniversalLLMClient(provider="demo")
    extractor = ExtractorAgent(client)
    sop_architect = SOPArchitectAgent(client)
    dispatcher = TaskDispatcherAgent()
    comms = CommsAgent()
    audio_proc = AudioProcessor()

    # 1. Test Audio Processor
    audio_transcript = audio_proc.transcribe(b"", file_name="fintech_onboarding_call_recording.wav")
    assert len(audio_transcript) > 50, "Audio transcription failed"
    print("  [PASS] Audio Processor fallback transcription verified.")

    # 2. Test Live Webhook Dispatcher validation
    dummy_payload = {"meeting_title": "Test Sync", "action_items_count": 2}
    invalid_dispatch = LiveWebhookDispatcher.dispatch("", dummy_payload)
    assert not invalid_dispatch["success"], "Empty URL should fail gracefully"
    print("  [PASS] Live Webhook Dispatcher validation verified.")

    # 3. Test Templates
    for name, t_data in TEMPLATES.items():
        print(f"Testing template: {name}...")
        transcript = t_data["transcript"]
        
        # 1. Extraction Agent
        extracted = extractor.extract(transcript)
        assert "meeting_title" in extracted, "Missing meeting_title in extraction"
        assert len(extracted.get("action_items", [])) > 0, "No action items extracted"
        assert len(extracted.get("decisions", [])) > 0, "No decisions extracted"
        assert len(extracted.get("raci_matrix", [])) > 0, "No RACI matrix extracted"

        # 2. Meeting ROI Engine
        roi = MeetingROIEngine.calculate_metrics(extracted, transcript)
        assert roi["net_savings_per_meeting"] > 0, "ROI calculation error"
        assert roi["actionability_index"] > 0, "Actionability index calculation error"
        assert roi["accountability_ratio"] > 0, "Accountability ratio calculation error"

        # 3. SOP Architect Agent
        sop = sop_architect.generate_sop(extracted)
        assert "sop_id" in sop, "Missing sop_id"
        assert "markdown" in sop, "Missing markdown in SOP"
        assert "mermaid_code" in sop, "Missing mermaid diagram in SOP"
        assert "graph TD" in sop["mermaid_code"], "Invalid Mermaid diagram syntax"

        # 4. Task Dispatcher Agent
        dispatch_result = dispatcher.dispatch(extracted)
        assert dispatch_result["total_tickets"] > 0, "No tickets dispatched"
        assert not dispatch_result["dataframe"].empty, "Dataframe is empty"
        assert "Issue Key" in dispatch_result["csv_string"], "CSV format error"

        # 5. Comms Agent
        comms_result = comms.generate_comms(extracted, sop)
        assert "email_body" in comms_result, "Missing email body"
        assert "slack_message" in comms_result, "Missing slack message"

        # 6. PDF Generator
        pdf_bytes = generate_sop_pdf(sop, extracted)
        assert len(pdf_bytes) > 500, f"PDF generation failed, size {len(pdf_bytes)}"

        print(f"  [PASS] {name} passed! Generated {dispatch_result['total_tickets']} tickets, Grade: {roi['health_grade']}, PDF: {len(pdf_bytes)} bytes.")

    print("\nAll integration and upgrade tests passed with 100% success!")


if __name__ == "__main__":
    test_pipeline_on_all_templates()
