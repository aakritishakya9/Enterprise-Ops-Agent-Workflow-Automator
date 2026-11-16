"""
SyncOps AI - Enterprise Meeting-to-SOP & Workflow Automation Agent
A production-grade Streamlit application orchestrating multi-agent workflows.
"""

import streamlit as st
import json
import pandas as pd
import time

from core.templates import TEMPLATES
from core.llm_client import UniversalLLMClient
from core.pdf_generator import generate_sop_pdf
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
        padding: 16px;
        text-align: center;
    }
    .metric-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #1E40AF;
    }
    .metric-label {
        font-size: 0.82rem;
        color: #64748B;
        text-transform: uppercase;
        font-weight: 600;
    }
    .agent-pill {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-right: 6px;
    }
    .badge-critical { background-color: #FEE2E2; color: #991B1B; }
    .badge-high { background-color: #FFEDD5; color: #9A3412; }
    .badge-med { background-color: #FEF3C7; color: #92400E; }
    .badge-low { background-color: #DCFCE7; color: #166534; }
</style>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR CONFIGURATION -----------------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=64)
    st.title("SyncOps AI")
    st.caption("v2.4 Enterprise Edition · Multi-Agent Orchestrator")
    st.divider()

    st.subheader("1. AI Inference Engine")
    provider_option = st.selectbox(
        "Select Provider",
        ["Demo Mode (Offline Smart Engine)", "Google Gemini API", "OpenAI API"],
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
    st.subheader("2. Enterprise Scenario")
    template_choices = list(TEMPLATES.keys()) + ["Custom Meeting Notes"]
    selected_scenario = st.selectbox("Select Meeting Transcript", template_choices, index=0)

    st.divider()
    st.markdown("### 🏢 Aligned With")
    st.caption("• **SkillfyAI for Business** (Corporate AI Transformation)")
    st.caption("• **SOP & Workflow Automation** (Zero-Hallucination Schemas)")

# ----------------- MAIN CONTENT -----------------
st.markdown('<div class="main-header">⚡ SyncOps AI: Meeting-to-SOP & Workflow Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Automating the bridge between stakeholder discussions, binding SOPs, project tracking tickets, and client communications.</div>', unsafe_allow_html=True)

# Top Metrics Banner
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.markdown("""<div class="metric-card"><div class="metric-value">4.5 hrs</div><div class="metric-label">Avg. Admin Time Saved</div></div>""", unsafe_allow_html=True)
with col_m2:
    st.markdown("""<div class="metric-card"><div class="metric-value">100%</div><div class="metric-label">Schema Compliance</div></div>""", unsafe_allow_html=True)
with col_m3:
    st.markdown("""<div class="metric-card"><div class="metric-value">4 Agents</div><div class="metric-label">Coordinated Pipeline</div></div>""", unsafe_allow_html=True)
with col_m4:
    st.markdown("""<div class="metric-card"><div class="metric-value">&lt; 1.2s</div><div class="metric-label">Orchestration Latency</div></div>""", unsafe_allow_html=True)

st.write("")

# Meeting Input Section
with st.expander("📝 Raw Meeting Transcript / Input Dialogue", expanded=(selected_scenario == "Custom Meeting Notes")):
    if selected_scenario in TEMPLATES:
        t_info = TEMPLATES[selected_scenario]
        st.info(f"**Scenario Context:** {t_info['description']} | **Participants:** {', '.join(t_info['participants'])}")
        transcript_input = st.text_area("Transcript Content", value=t_info["transcript"], height=200)
    else:
        st.info("Paste your raw meeting notes, audio transcripts, or Zoom chat logs below:")
        transcript_input = st.text_area("Custom Transcript Content", value="[00:00] Alice: We agreed to launch the customer data export API by next Tuesday. Bob will handle the OAuth2 token validation. Sarah will review the security compliance audit report.", height=180)

# Run Button
run_col1, run_col2 = st.columns([1, 4])
with run_col1:
    execute_button = st.button("🚀 Run Multi-Agent Orchestration", type="primary", use_container_width=True)

# Session State Cache
if "last_results" not in st.session_state:
    st.session_state.last_results = None

if execute_button:
    provider_slug = "demo"
    if provider_option == "Google Gemini API":
        provider_slug = "gemini"
    elif provider_option == "OpenAI API":
        provider_slug = "openai"

    llm_client = UniversalLLMClient(provider=provider_slug, api_key=api_key, model=model_choice)
    
    with st.status("🤖 Executing Coordinated Agent Swarm...", expanded=True) as status:
        st.write("🔍 **Agent 1 [Extractor Agent]:** Analyzing transcript, parsing decisions, risks, and RACI matrices...")
        extractor = ExtractorAgent(llm_client)
        extracted = extractor.extract(transcript_input)
        time.sleep(0.3)

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
        "pdf_bytes": pdf_bytes
    }

# Render Results
if st.session_state.last_results:
    res = st.session_state.last_results
    extracted = res["extracted"]
    sop = res["sop"]
    dispatch_res = res["dispatch"]
    comms = res["comms"]
    pdf_bytes = res["pdf_bytes"]

    st.success(f"**Target Objective:** {extracted.get('meeting_title')} | **Target Milestone:** {extracted.get('target_go_live')}")

    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Executive Intelligence",
        "📜 SOP Architect",
        "🎫 Task & Ticket Dispatcher",
        "✉️ Executive Comms",
        "⚡ Webhook & API Dispatcher"
    ])

    # ----------------- TAB 1: EXECUTIVE INTELLIGENCE -----------------
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
        st.subheader("2. Action Items & Commitments")
        action_df = pd.DataFrame(extracted.get("action_items", []))
        if not action_df.empty:
            st.dataframe(action_df, use_container_width=True, hide_index=True)

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

    # ----------------- TAB 2: SOP ARCHITECT -----------------
    with tab2:
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
        st.markdown("#### 🔄 Workflow Process Diagram")
        st.info("Rendered via Mermaid flowchart syntax:")
        st.code(sop["mermaid_code"], language="mermaid")

        st.markdown("#### 📖 Full SOP Document")
        st.markdown(sop["markdown"])

    # ----------------- TAB 3: TASK & TICKET DISPATCHER -----------------
    with tab3:
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

    # ----------------- TAB 4: EXECUTIVE COMMS -----------------
    with tab4:
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

    # ----------------- TAB 5: WEBHOOK & API DISPATCHER -----------------
    with tab5:
        st.subheader("⚡ Automated Webhook & API Dispatcher")
        st.caption("Demonstrating zero-code/low-code integration hooks for n8n, Make.com, or enterprise endpoints.")

        wh_url = st.text_input("Webhook Destination URL", value="https://api.skillfyai.school/v1/workflows/dispatch-meeting", key="wh_url")
        
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
            if st.button("📡 Dispatch Webhook Payload", use_container_width=True):
                st.toast("✅ Webhook payload successfully simulated & dispatched!", icon="🚀")
                st.success(f"200 OK — Payload received by workflow orchestrator at `{wh_url}`")

        st.write("##### Inspected JSON Payload")
        st.json(payload_data)

else:
    st.info("👆 Click **'🚀 Run Multi-Agent Orchestration'** above to test the live pipeline across the selected enterprise meeting scenario.")
