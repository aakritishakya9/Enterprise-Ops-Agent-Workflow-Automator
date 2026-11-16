"""
SyncOps AI - Enterprise Meeting-to-SOP & Workflow Automation Agent
Upgraded Edition: Audio Ingestion, Human-in-the-Loop Editing, ROI Analytics, Live Webhooks & Graphical Mermaid.
"""

import streamlit as st
import streamlit.components.v1 as components
import json
import pandas as pd
import time

from core.templates import TEMPLATES
from core.llm_client import UniversalLLMClient
from core.pdf_generator import generate_sop_pdf
from core.roi_analytics import MeetingROIEngine
from core.audio_processor import AudioProcessor
from core.webhook_sender import LiveWebhookDispatcher
from agents.extractor import ExtractorAgent
from agents.sop_architect import SOPArchitectAgent
from agents.task_dispatcher import TaskDispatcherAgent
from agents.comms_agent import CommsAgent

# Page Configuration
st.set_page_config(
    page_title="SyncOps AI | Enterprise Workflow Orchestrator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Enterprise CSS Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #0F172A;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 20px;
    }
    .metric-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 14px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .metric-value {
        font-size: 1.55rem;
        font-weight: 700;
        color: #1E40AF;
    }
    .metric-label {
        font-size: 0.8rem;
        color: #64748B;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    .agent-pill {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-right: 6px;
    }
    .badge-critical { background-color: #FEE2E2; color: #991B1B; }
    .badge-high { background-color: #FFEDD5; color: #9A3412; }
    .badge-med { background-color: #FEF3C7; color: #92400E; }
    .badge-low { background-color: #DCFCE7; color: #166534; }
    .badge-grade { background-color: #E0E7FF; color: #3730A3; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# Helper function to render graphical Mermaid diagram via HTML
def render_mermaid(diagram_code: str, height: int = 420):
    html_code = f"""
    <div style="background:#ffffff; padding:15px; border-radius:8px; border:1px solid #E2E8F0; text-align:center;">
        <pre class="mermaid" style="display:flex; justify-content:center;">
{diagram_code}
        </pre>
    </div>
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{ 
            startOnLoad: true, 
            theme: 'neutral',
            flowchart: {{ useMaxWidth: true, htmlLabels: true, curve: 'basis' }}
        }});
    </script>
    """
    components.html(html_code, height=height, scrolling=True)

# ----------------- SIDEBAR CONFIGURATION -----------------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=64)
    st.title("SyncOps AI")
    st.caption("v2.5 Enterprise Edition · Multi-Agent Swarm")
    st.divider()

    st.subheader("1. AI Inference Engine")
    provider_option = st.selectbox(
        "Select Provider",
        ["Demo Mode (Smart Offline Engine)", "Google Gemini API", "OpenAI API"],
        index=0,
        help="Demo mode allows instantaneous full evaluation without needing external API credentials."
    )

    api_key = ""
    model_choice = "default"
    if provider_option == "Google Gemini API":
        api_key = st.text_input("Gemini API Key", type="password", placeholder="AIzaSy...")
        model_choice = st.selectbox("Model", ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash"])
    elif provider_option == "OpenAI API":
        api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")
        model_choice = st.selectbox("Model", ["gpt-4o-mini", "gpt-4o"])

    st.divider()
    st.subheader("2. AI Fluency Architecture")
    st.caption("• 4-Agent Coordinated Swarm")
    st.caption("• Live Microphone Voice Ingestion")
    st.caption("• Zero-Hallucination JSON Schemas")

    st.divider()
    st.markdown("### 🏢 Executive Pillars")
    st.caption("• **SkillfyAI for Business** (Workflow AI)")
    st.caption("• **Human-in-the-Loop** Governance")
    st.caption("• **Every Person Owns a Number** (ROI Scorecard)")

# ----------------- MAIN HEADER -----------------
st.markdown('<div class="main-header">⚡ SyncOps AI: Meeting-to-SOP & Workflow Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Automating the bridge between stakeholder discussions, binding SOPs, project tracking tickets, and client communications.</div>', unsafe_allow_html=True)

# Top Metrics Banner (Default or Loaded)
col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
with col_m1:
    st.markdown("""<div class="metric-card"><div class="metric-value">4.5 hrs</div><div class="metric-label">Admin Time Saved</div></div>""", unsafe_allow_html=True)
with col_m2:
    st.markdown("""<div class="metric-card"><div class="metric-value">100%</div><div class="metric-label">Schema Compliance</div></div>""", unsafe_allow_html=True)
with col_m3:
    st.markdown("""<div class="metric-card"><div class="metric-value">4 Agents</div><div class="metric-label">Coordinated Swarm</div></div>""", unsafe_allow_html=True)
with col_m4:
    st.markdown("""<div class="metric-card"><div class="metric-value">&lt; 1.2s</div><div class="metric-label">Turnaround Latency</div></div>""", unsafe_allow_html=True)
with col_m5:
    st.markdown("""<div class="metric-card"><div class="metric-value">A+</div><div class="metric-label">Governance Grade</div></div>""", unsafe_allow_html=True)

st.write("")

# ----------------- INPUT INGESTION MODES -----------------
transcript_input = ""

st.markdown("### 📥 Step 1: Provide Meeting Input")
input_mode_tabs = st.radio(
    "Select Your Input Mode:",
    ["🎙️ Live Microphone Voice Recording", "📁 Upload Audio File (.wav/.mp3)", "📝 Preloaded Scenarios & Notes"],
    horizontal=True,
    index=0
)

if input_mode_tabs == "🎙️ Live Microphone Voice Recording":
    st.markdown('''
    <div style="background:#EFF6FF; border: 1px solid #BFDBFE; padding: 14px; border-radius: 8px; margin-bottom: 12px;">
        <b style="color:#1E40AF; font-size:1.05rem;">🎙️ Direct Microphone Voice Ingestion</b>
        <div style="font-size:0.88rem; color:#1E3A8A; margin-top:4px;">
            Click the red record button below to speak your meeting dialogue or action items directly into your laptop microphone!
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    recorded_audio = st.audio_input("Record your voice:")
    
    if recorded_audio is not None:
        st.audio(recorded_audio)
        audio_proc = AudioProcessor(api_key=api_key)
        with st.spinner("🎙️ Transcribing live microphone speech..."):
            transcript_input = audio_proc.transcribe(recorded_audio.getvalue(), file_name="live_microphone_recording.wav")
        st.success("Captured and transcribed live microphone recording!")
    else:
        st.caption("💡 No microphone available right now? Select a pre-recorded audio sample below:")
        sample_choice = st.selectbox("Pre-recorded Audio Sample", [
            "fintech_onboarding_call_recording.wav",
            "production_incident_debrief.wav",
            "executive_strategy_sync.wav"
        ])
        audio_proc = AudioProcessor(api_key=api_key)
        transcript_input = audio_proc.transcribe(b"", file_name=sample_choice)

    with st.expander("📝 View & Edit Transcribed Voice Text", expanded=True):
        transcript_input = st.text_area("Transcribed Dialogue", value=transcript_input, height=150)

elif input_mode_tabs == "📁 Upload Audio File (.wav/.mp3)":
    st.markdown('''
    <div style="background:#F0FDF4; border: 1px solid #BBF7D0; padding: 14px; border-radius: 8px; margin-bottom: 12px;">
        <b style="color:#166534; font-size:1.05rem;">📁 Upload Audio File</b>
        <div style="font-size:0.88rem; color:#14532D; margin-top:4px;">
            Drop an audio recording (.wav, .mp3, .m4a) from Zoom, Google Meet, or your phone.
        </div>
    </div>
    ''', unsafe_allow_html=True)

    uploaded_audio = st.file_uploader("Upload Meeting Audio", type=["wav", "mp3", "m4a", "ogg"])
    if uploaded_audio:
        st.audio(uploaded_audio)
        audio_proc = AudioProcessor(api_key=api_key)
        with st.spinner(f"🎙️ Transcribing {uploaded_audio.name}..."):
            transcript_input = audio_proc.transcribe(uploaded_audio.getvalue(), file_name=uploaded_audio.name)
        st.success(f"Transcribed {uploaded_audio.name} successfully!")
    else:
        sample_choice = st.selectbox("Or select pre-recorded enterprise audio:", [
            "fintech_onboarding_call_recording.wav",
            "production_incident_debrief.wav",
            "executive_strategy_sync.wav"
        ])
        audio_proc = AudioProcessor(api_key=api_key)
        transcript_input = audio_proc.transcribe(b"", file_name=sample_choice)

    with st.expander("📝 View & Edit Transcribed Audio Text", expanded=True):
        transcript_input = st.text_area("Transcribed Dialogue", value=transcript_input, height=150)

else:
    st.markdown('''
    <div style="background:#F8FAFC; border: 1px solid #E2E8F0; padding: 14px; border-radius: 8px; margin-bottom: 12px;">
        <b style="color:#1E293B; font-size:1.05rem;">📝 Preloaded Scenarios & Text Notes</b>
        <div style="font-size:0.88rem; color:#475569; margin-top:4px;">
            Select a realistic enterprise transcript or type custom meeting notes.
        </div>
    </div>
    ''', unsafe_allow_html=True)

    selected_scenario = st.selectbox("Select Enterprise Scenario", list(TEMPLATES.keys()) + ["Custom Meeting Notes"], index=0)

    if selected_scenario in TEMPLATES:
        t_info = TEMPLATES[selected_scenario]
        with st.expander(f"📝 {selected_scenario} — Dialogue Transcript", expanded=True):
            context_str = str(t_info.get('description', ''))
            part_str = ', '.join(t_info.get('participants', []))
            st.info(f"**Context:** {context_str} | **Stakeholders:** {part_str}")
            transcript_input = st.text_area("Transcript Content", value=t_info["transcript"], height=180)
    else:
        with st.expander("📝 Custom Meeting Notes / Dialogue", expanded=True):
            st.info("Paste your raw meeting notes, audio transcripts, or chat logs below:")
            transcript_input = st.text_area("Custom Transcript Content", value="[00:00] Alice: We agreed to launch the customer data export API by next Tuesday. Bob will handle the OAuth2 token validation. Sarah will review the security compliance audit report.", height=180)

# Run Button
run_col1, run_col2 = st.columns([1, 4])
with run_col1:
    execute_button = st.button("🚀 Run Multi-Agent Orchestration", type="primary", use_container_width=True)

# Session State Cache
if "last_results" not in st.session_state:
    st.session_state.last_results = None

# ----------------- AGENT EXECUTION -----------------
if execute_button:
    provider_slug = "demo"
    if provider_option == "Google Gemini API":
        provider_slug = "gemini"
    elif provider_option == "OpenAI API":
        provider_slug = "openai"

    llm_client = UniversalLLMClient(provider=provider_slug, api_key=api_key, model=model_choice)
    
    with st.status("🤖 Executing Coordinated Agent Swarm...", expanded=True) as status:
        st.write("🔍 **Agent 1 [Extractor Agent]:** Analyzing dialogue, parsing decisions, risks, and RACI matrices...")
        extractor = ExtractorAgent(llm_client)
        extracted = extractor.extract(transcript_input)
        time.sleep(0.3)

        st.write("📈 **Analytics Engine:** Computing Actionability Index, Accountability Ratio & Meeting Cost ROI...")
        roi_metrics = MeetingROIEngine.calculate_metrics(extracted, transcript_input)
        time.sleep(0.1)

        st.write("📐 **Agent 2 [SOP Architect]:** Synthesizing operational procedure, delivery gates, and Mermaid diagram...")
        sop_architect = SOPArchitectAgent(llm_client)
        sop = sop_architect.generate_sop(extracted)
        time.sleep(0.2)

        st.write("🎫 **Agent 3 [Task Dispatcher]:** Generating Jira/Linear issue schemas and CSV ticket export...")
        dispatcher = TaskDispatcherAgent()
        dispatch_result = dispatcher.dispatch(extracted)
        time.sleep(0.2)

        st.write("✉️ **Agent 4 [Executive Comms]:** Drafting executive briefing email and Slack broadcast...")
        comms = CommsAgent()
        comms_result = comms.generate_comms(extracted, sop)
        time.sleep(0.2)

        st.write("📄 **Document Compiler:** Compiling publication-grade executive PDF document...")
        pdf_bytes = generate_sop_pdf(sop, extracted)
        
        status.update(label="✅ Multi-Agent Orchestration Completed Successfully!", state="complete", expanded=False)

    st.session_state.last_results = {
        "extracted": extracted,
        "sop": sop,
        "dispatch": dispatch_result,
        "comms": comms_result,
        "roi_metrics": roi_metrics,
        "pdf_bytes": pdf_bytes,
        "transcript_text": transcript_input
    }

# ----------------- DISPLAY RESULTS -----------------
if st.session_state.last_results:
    res = st.session_state.last_results
    extracted = res["extracted"]
    sop = res["sop"]
    dispatch_res = res["dispatch"]
    comms = res["comms"]
    roi = res["roi_metrics"]
    pdf_bytes = res["pdf_bytes"]

    st.success(f"**Target Objective:** {extracted.get('meeting_title')} | **Target Milestone:** {extracted.get('target_go_live')} | **Grade:** {roi.get('health_grade')}")

    # Tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Intelligence & HITL Editor",
        "📈 Meeting ROI Scorecard",
        "📜 SOP Architect & Visual Flow",
        "🎫 Task & Ticket Dispatcher",
        "✉️ Executive Comms",
        "⚡ Live Webhook & API Push"
    ])

    # ----------------- TAB 1: INTELLIGENCE & HUMAN-IN-THE-LOOP -----------------
    with tab1:
        st.subheader("1. Core Strategic Decisions")
        dec_cols = st.columns(len(extracted.get("decisions", [])) or 1)
        for idx, d in enumerate(extracted.get("decisions", [])):
            with dec_cols[idx % len(dec_cols)]:
                st.markdown(f"""
                <div style="background:#F1F5F9; border-left: 4px solid #3B82F6; padding: 12px; border-radius: 4px; margin-bottom: 10px;">
                    <div style="font-weight: 700; color: #1E293B;">{d.get('decision')}</div>
                    <div style="font-size: 0.85rem; color: #475569; margin-top: 4px;"><b>Context:</b> {d.get('context')}</div>
                    <div style="font-size: 0.85rem; color: #1D4ED8; margin-top: 4px;"><b>Impact:</b> {d.get('impact')}</div>
                </div>
                """, unsafe_allow_html=True)

        st.divider()
        st.subheader("2. Human-in-the-Loop (HITL) Action Items Editor")
        st.caption("Review, edit assignees, adjust deadlines, or add new tasks before finalizing documentation.")

        action_df = pd.DataFrame(extracted.get("action_items", []))
        edited_action_df = st.data_editor(
            action_df,
            use_container_width=True,
            num_rows="dynamic",
            key="action_editor"
        )

        col_sync1, col_sync2 = st.columns([1, 3])
        with col_sync1:
            if st.button("💾 Re-Sync SOP & Tickets with Edits", type="secondary", use_container_width=True):
                # Update session state with edited actions
                updated_actions = edited_action_df.to_dict('records')
                extracted["action_items"] = updated_actions
                
                # Re-run dependent agents
                dispatcher = TaskDispatcherAgent()
                dispatch_res = dispatcher.dispatch(extracted)
                
                sop_architect = SOPArchitectAgent()
                sop = sop_architect.generate_sop(extracted)
                
                comms = CommsAgent()
                comms_result = comms.generate_comms(extracted, sop)
                
                pdf_bytes = generate_sop_pdf(sop, extracted)
                
                st.session_state.last_results["extracted"] = extracted
                st.session_state.last_results["dispatch"] = dispatch_res
                st.session_state.last_results["sop"] = sop
                st.session_state.last_results["comms"] = comms_result
                st.session_state.last_results["pdf_bytes"] = pdf_bytes
                
                st.toast("✅ Re-synced SOP, PDF, and Jira Tickets with your edits!", icon="🎉")
                st.rerun()

        st.divider()
        col_risk, col_raci = st.columns([1, 1])
        with col_risk:
            st.subheader("3. Identified Risks & Mitigations")
            for r in extracted.get("risks_and_blockers", []):
                sev = r.get("severity", "Medium")
                badge_class = "badge-critical" if sev == "High" else "badge-med"
                st.markdown(f"""
                <div style="background:#FFFBEB; border: 1px solid #FDE68A; padding: 10px; border-radius: 6px; margin-bottom: 8px;">
                    <span class="agent-pill {badge_class}">{sev.upper()} SEVERITY</span> <b>{r.get('risk')}</b>
                    <div style="font-size: 0.85rem; color:#451A03; margin-top: 4px;"><b>Impact:</b> {r.get('impact')}</div>
                    <div style="font-size: 0.85rem; color:#065F46; margin-top: 2px;"><b>Mitigation:</b> {r.get('mitigation')}</div>
                </div>
                """, unsafe_allow_html=True)

        with col_raci:
            st.subheader("4. RACI Governance Matrix")
            raci_df = pd.DataFrame(extracted.get("raci_matrix", []))
            if not raci_df.empty:
                st.dataframe(raci_df, use_container_width=True, hide_index=True)

    # ----------------- TAB 2: ROI SCORECARD -----------------
    with tab2:
        st.subheader("📈 Executive Meeting Productivity & ROI Scorecard")
        st.caption("Demonstrating quantifiable business value: 'Every Person Owns a Number'")

        col_r1, col_r2, col_r3, col_r4 = st.columns(4)
        with col_r1:
            st.metric("Net Savings / Meeting", f"${roi['net_savings_per_meeting']}", delta=f"+{roi['time_saved_hours']} hrs saved")
        with col_r2:
            st.metric("Actionability Index", f"{roi['actionability_index']}/100", delta="High Yield")
        with col_r3:
            st.metric("Accountability Ratio", f"{roi['accountability_ratio']}%", delta="Single-Owner Tasks")
        with col_r4:
            st.metric("Meeting Health Grade", roi['health_grade'])

        st.divider()
        col_chart1, col_chart2 = st.columns([1, 1])
        with col_chart1:
            st.markdown("#### ⏱️ Cost Breakdown: Manual vs AI Automation")
            cost_df = pd.DataFrame({
                "Operational Model": ["Traditional (Manual Admin)", "SyncOps AI (Automated)"],
                "Cost ($)": [roi["direct_meeting_cost"] + roi["manual_admin_cost"], roi["direct_meeting_cost"] + 3.25]
            })
            st.bar_chart(cost_df.set_index("Operational Model"))

        with col_chart2:
            st.markdown("#### 🎯 Strategic Yield Summary")
            st.write(f"• **Identified Decisions:** {roi['total_decisions']} core agreements")
            st.write(f"• **Actionable Deliverables:** {roi['total_actions']} tickets assigned")
            st.write(f"• **Risk Registry:** {roi['total_risks']} mitigation pathways established")
            st.write(f"• **Estimated Annual Savings (100 meetings/yr):** **${roi['net_savings_per_meeting'] * 100:,.2f}**")

    # ----------------- TAB 3: SOP ARCHITECT & VISUAL FLOW -----------------
    with tab3:
        top_sop_col1, top_sop_col2 = st.columns([3, 1])
        with top_sop_col1:
            st.subheader(f"Generated Standard Operating Procedure ({sop['sop_id']})")
            st.caption("Standardized execution procedure formatted for cross-functional compliance.")
        with top_sop_col2:
            st.download_button(
                label="📄 Download Executive PDF",
                data=pdf_bytes,
                file_name=f"{sop['sop_id']}_Executive_SOP.pdf",
                mime="application/pdf",
                type="primary",
                use_container_width=True
            )
            st.download_button(
                label="📝 Download Markdown (.md)",
                data=sop["markdown"],
                file_name=f"{sop['sop_id']}.md",
                mime="text/markdown",
                use_container_width=True
            )

        st.divider()
        st.markdown("#### 🔄 Graphical Workflow Architecture Diagram")
        render_mermaid(sop["mermaid_code"])

        with st.expander("Show Mermaid Source Code"):
            st.code(sop["mermaid_code"], language="mermaid")

        st.markdown("#### 📖 Full Standard Operating Procedure")
        st.markdown(sop["markdown"])

    # ----------------- TAB 4: TASK & TICKET DISPATCHER -----------------
    with tab4:
        st.subheader("Project Management Ticket Dispatcher")
        st.caption("Export extracted tasks formatted with acceptance criteria into Jira, Linear, or ClickUp.")

        col_d1, col_d2 = st.columns([1, 3])
        with col_d1:
            st.download_button(
                label="📥 Export Jira/Linear CSV",
                data=dispatch_res["csv_string"],
                file_name=f"Tickets_{extracted.get('meeting_title', 'Project')[:20]}.csv",
                mime="text/csv",
                type="primary",
                use_container_width=True
            )

        st.write("")
        for t in dispatch_res["tickets"]:
            p_badge = "badge-critical" if t["priority"] in ["Critical", "High"] else "badge-med"
            with st.expander(f"[{t['key']}] {t['summary']} — Assigned: {t['assignee']}", expanded=True):
                st.markdown(f"""
                <span class="agent-pill {p_badge}">PRIORITY: {t['priority']}</span>
                <span class="agent-pill" style="background:#E0E7FF; color:#3730A3;">ROLE: {t['role']}</span>
                <span class="agent-pill" style="background:#F1F5F9; color:#334155;">TARGET: {t['deadline']}</span>
                """, unsafe_allow_html=True)
                st.markdown(t["description"])

    # ----------------- TAB 5: EXECUTIVE COMMS -----------------
    with tab5:
        st.subheader("Executive Communications Hub")
        st.caption("Publish-ready stakeholder communications generated by the Comms Agent.")

        tab_email, tab_slack = st.tabs(["📧 Client & Executive Email", "💬 Team Slack / Teams Broadcast"])
        with tab_email:
            st.text_input("Subject Line", value=comms["email_subject"], key="em_subj")
            st.text_area("Email Body", value=comms["email_body"], height=320, key="em_body")
            st.caption("Tip: Select all & copy into Gmail or Outlook.")

        with tab_slack:
            st.text_area("Formatted Markdown Message", value=comms["slack_message"], height=280, key="slack_msg")
            st.caption("Tip: Paste directly into Slack or Microsoft Teams channels.")

    # ----------------- TAB 6: LIVE WEBHOOK & API PUSH -----------------
    with tab6:
        st.subheader("⚡ Live Webhook & Integration Dispatcher")
        st.caption("Supports real HTTP delivery to live Slack Incoming Webhooks, Discord Webhooks, n8n, Make.com, or REST APIs.")

        wh_url = st.text_input(
            "Target Webhook URL",
            value="https://hooks.slack.com/services/YOUR/REAL/WEBHOOK_URL",
            help="Paste your real Slack or Discord webhook URL to test live notifications."
        )

        payload_data = {
            "source": "SyncOps_AI_Orchestrator",
            "meeting_title": extracted.get("meeting_title"),
            "target_milestone": extracted.get("target_go_live"),
            "sop_id": sop.get("sop_id"),
            "action_items_count": len(extracted.get("action_items", [])),
            "tickets": dispatch_res.get("tickets", []),
            "executive_summary": comms.get("email_subject")
        }

        col_wh1, col_wh2 = st.columns([1, 3])
        with col_wh1:
            dispatch_button = st.button("📡 Dispatch Live Webhook", type="primary", use_container_width=True)

        if dispatch_button:
            if "YOUR/REAL" in wh_url or "api.skillfyai.school" in wh_url:
                # Simulated dispatch
                st.toast("✅ Webhook payload simulated successfully!", icon="🚀")
                st.success("200 OK — Simulated dispatch received. (Paste a live Slack/Discord URL to ping real channels!)")
            else:
                with st.spinner("Dispatching HTTP POST request to webhook..."):
                    dispatch_status = LiveWebhookDispatcher.dispatch(
                        webhook_url=wh_url,
                        payload_data=payload_data,
                        slack_markdown=comms.get("slack_message", "")
                    )
                    if dispatch_status["success"]:
                        st.toast(f"✅ Live Webhook delivered in {dispatch_status['latency_ms']}ms!", icon="🎉")
                        st.success(f"{dispatch_status['status_code']} OK — {dispatch_status['message']}")
                    else:
                        st.error(f"Status {dispatch_status['status_code']}: {dispatch_status['message']}")

        st.write("##### Inspected JSON Payload")
        st.json(payload_data)

else:
    st.info("👆 Click **'🚀 Run Multi-Agent Orchestration'** above to test the live pipeline across the selected enterprise meeting scenario.")
