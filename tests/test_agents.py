"""
End-to-End Unit & Integration Tests for SyncOps AI
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.llm_client import UniversalLLMClient
from core.templates import TEMPLATES
from core.pdf_generator import generate_sop_pdf
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

    for name, t_data in TEMPLATES.items():
        print(f"Testing template: {name}...")
        transcript = t_data["transcript"]
        
        # 1. Extraction Agent
        extracted = extractor.extract(transcript)
        assert "meeting_title" in extracted, "Missing meeting_title in extraction"
        assert len(extracted.get("action_items", [])) > 0, "No action items extracted"
        assert len(extracted.get("decisions", [])) > 0, "No decisions extracted"
        assert len(extracted.get("raci_matrix", [])) > 0, "No RACI matrix extracted"

        # 2. SOP Architect Agent
        sop = sop_architect.generate_sop(extracted)
        assert "sop_id" in sop, "Missing sop_id"
        assert "markdown" in sop, "Missing markdown in SOP"
        assert "mermaid_code" in sop, "Missing mermaid diagram in SOP"
        assert "graph TD" in sop["mermaid_code"], "Invalid Mermaid diagram syntax"

        # 3. Task Dispatcher Agent
        dispatch_result = dispatcher.dispatch(extracted)
        assert dispatch_result["total_tickets"] > 0, "No tickets dispatched"
        assert not dispatch_result["dataframe"].empty, "Dataframe is empty"
        assert "Issue Key" in dispatch_result["csv_string"], "CSV format error"

        # 4. Comms Agent
        comms_result = comms.generate_comms(extracted, sop)
        assert "email_body" in comms_result, "Missing email body"
        assert "slack_message" in comms_result, "Missing slack message"

        # 5. PDF Generator
        pdf_bytes = generate_sop_pdf(sop, extracted)
        assert len(pdf_bytes) > 500, f"PDF generation failed, size {len(pdf_bytes)}"

        print(f"  [PASS] {name} passed successfully! Generated {dispatch_result['total_tickets']} tickets and {len(pdf_bytes)} bytes PDF.")

    print("\nAll integration tests passed with 100% success!")

if __name__ == "__main__":
    test_pipeline_on_all_templates()
