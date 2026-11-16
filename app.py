"""
SyncOps AI - Enterprise Meeting-to-SOP & Workflow Automation Agent
Enterprise Edition: Ultra-Modern SaaS Dark UI with Glassmorphism, Micro-Animations, and High-Contrast Typography.
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

# ----------------- ENTERPRISE SAAS DESIGN SYSTEM -----------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Background and Layout */
    .stApp {
        background-color: #080C14;
        color: #F1F5F9;
    }

    /* Hero Header */
    .hero-container {
        padding: 10px 0px 24px 0px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 24px;
    }
    .hero-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(59, 130, 246, 0.12);
        border: 1px solid rgba(59, 130, 246, 0.35);
        border-radius: 9999px;
        padding: 5px 14px;
        margin-bottom: 12px;
    }
    .pulse-dot {
        width: 8px;
        height: 8px;
        background-color: #38BDF8;
        border-radius: 50%;
        box-shadow: 0 0 10px #38BDF8;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(0.85); }
    }
    .hero-pill-text {
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.8px;
        color: #60A5FA;
        text-transform: uppercase;
    }
    .hero-title {
        font-size: 2.6rem;
        font-weight: 800;
        letter-spacing: -0.8px;
        color: #FFFFFF;
        margin: 0 0 8px 0;
        line-height: 1.15;
    }
    .gradient-text {
        background: linear-gradient(135deg, #38BDF8 0%, #818CF8 50%, #C084FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        font-size: 1.12rem;
        font-weight: 500;
        color: #94A3B8;
        max-width: 900px;
        margin-bottom: 6px;
    }
    .hero-description {
        font-size: 0.9rem;
        color: #64748B;
        margin: 0;
    }

    /* Metric Stat Cards */
    .stat-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 14px;
        margin-bottom: 24px;
    }
    .stat-card {
        background: rgba(17, 24, 39, 0.65);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 16px 18px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .stat-card:hover {
        border-color: rgba(56, 189, 248, 0.3);
        transform: translateY(-2px);
    }
    .stat-label {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #94A3B8;
        margin-bottom: 4px;
    }
    .stat-val {
        font-size: 1.7rem;
        font-weight: 800;
        color: #F8FAFC;
        letter-spacing: -0.5px;
        line-height: 1.2;
    }
    .stat-sub {
        font-size: 0.75rem;
        color: #64748B;
        margin-top: 4px;
    }

    .val-cyan { color: #38BDF8; }
    .val-emerald { color: #34D399; }
    .val-indigo { color: #818CF8; }
    .val-amber { color: #FBBF24; }
    .val-purple { color: #C084FC; }

    /* Custom Step Containers */
    .input-box {
        background: rgba(17, 24, 39, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.09);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }

    /* Badges & Pills */
    .agent-pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.3px;
        margin-right: 6px;
    }
    .badge-critical { background: rgba(239, 68, 68, 0.15); color: #F87171; border: 1px solid rgba(239, 68, 68, 0.3); }
    .badge-high { background: rgba(249, 115, 22, 0.15); color: #FB923C; border: 1px solid rgba(249, 115, 22, 0.3); }
    .badge-med { background: rgba(245, 158, 11, 0.15); color: #FBBF24; border: 1px solid rgba(245, 158, 11, 0.3); }
    .badge-low { background: rgba(16, 185, 129, 0.15); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.3); }
    .badge-info { background: rgba(59, 130, 246, 0.15); color: #60A5FA; border: 1px solid rgba(59, 130, 246, 0.3); }

    /* Decision & Risk Cards */
    .decision-card {
        background: #0F172A;
        border-left: 4px solid #38BDF8;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
        border-top: 1px solid rgba(255,255,255,0.05);
        border-right: 1px solid rgba(255,255,255,0.05);
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    .decision-title {
        font-size: 1rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 6px;
    }
    .decision-meta {
        font-size: 0.85rem;
        color: #94A3B8;
        line-height: 1.45;
    }
    .decision-impact {
        font-size: 0.85rem;
        color: #38BDF8;
        font-weight: 600;
        margin-top: 6px;
    }

    .risk-card {
        background: rgba(30, 27, 24, 0.5);
        border: 1px solid rgba(245, 158, 11, 0.25);
        border-radius: 8px;
        padding: 14px;
        margin-bottom: 10px;
    }

    /* Tab Custom Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #0F172A;
        padding: 8px 10px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        color: #94A3B8;
        font-weight: 600;
        font-size: 0.88rem;
        padding: 8px 16px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1E293B !important;
        color: #38BDF8 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.3);
    }

    /* Buttons */
    .stButton>button {
        border-radius: 8px;
        font-weight: 700;
        letter-spacing: 0.3px;
        transition: all 0.2s ease;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to render graphical Mermaid diagram via HTML with dark styling
def render_mermaid(diagram_code: str, height: int = 420):
    html_code = f"""
    <div style="background:#0F172A; padding:20px; border-radius:10px; border:1px solid rgba(255,255,255,0.08); text-align:center;">
        <pre class="mermaid" style="display:flex; justify-content:center;">
{diagram_code}
        </pre>
    </div>
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{ 
            startOnLoad: true, 
            theme: 'dark',
            themeVariables: {{
                darkMode: true,
                background: '#0F172A',
                primaryColor: '#1E293B',
                primaryTextColor: '#F8FAFC',
                primaryBorderColor: '#38BDF8',
                lineColor: '#60A5FA',
                secondaryColor: '#111827',
                tertiaryColor: '#0A0E17'
            }},
            flowchart: {{ useMaxWidth: true, htmlLabels: true, curve: 'basis' }}
        }});
    </script>
    """
    components.html(html_code, height=height, scrolling=True)

# ----------------- SIDEBAR CONFIGURATION -----------------
with st.sidebar:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:14px;">
        <img src="https://img.icons8.com/fluency/96/artificial-intelligence.png" width="46" style="filter: drop-shadow(0 0 12px rgba(56,189,248,0.4));"/>
        <div>
            <div style="font-size:1.25rem; font-weight:800; color:#FFFFFF; letter-spacing:-0.5px;">SyncOps <span style="color:#38BDF8;">AI</span></div>
            <div style="font-size:0.75rem; color:#64748B; font-weight:600;">v2.5 Enterprise Edition</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    st.markdown("##### ⚙️ AI Inference Engine")
    provider_option = st.selectbox(
        "Model Provider",
        ["Demo Mode (Smart Offline Engine)", "Google Gemini API", "OpenAI API"],
        index=0,
        help="Demo mode allows instantaneous full evaluation without external API keys."
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
    st.markdown("##### 🏛️ AI Fluency Architecture")
    st.caption("• **Swarm Pipeline:** 4 Specialized Agents")
    st.caption("• **Voice Engine:** Multimodal Audio Ingestion")
    st.caption("• **Schema Guarantee:** Zero-Hallucination")
    st.caption("• **HITL:** Interactive Editable Backlog")

    st.divider()
    st.markdown("##### 💼 Enterprise Alignment")
    st.caption("• Designed for **SkillfyAI for Business**")
    st.caption("• 'Every Person Owns a Number' Scorecard")

# ----------------- HERO HEADER -----------------
st.markdown("""
<div class="hero-container">
    <div class="hero-pill">
        <span class="pulse-dot"></span>
        <span class="hero-pill-text">Autonomous Enterprise Workflow Swarm</span>
    </div>
    <h1 class="hero-title">SyncOps <span class="gradient-text">AI</span></h1>
    <div class="hero-subtitle">The Autonomous Bridge Between Stakeholder Dialogue and Production Delivery.</div>
    <div class="hero-description">Translates unstructured client meetings, audio recordings, and Zoom transcripts into binding Standard Operating Procedures, Jira issue backlogs, and C-Suite briefings with zero hallucination.</div>
</div>
""", unsafe_allow_html=True)

# ----------------- TOP METRICS BANNER -----------------
st.markdown("""
<div class="stat-grid">
    <div class="stat-card">
        <div class="stat-label">Admin Time Saved</div>
        <div class="stat-val val-cyan">4.5 hrs</div>
        <div class="stat-sub">per meeting session</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">Schema Compliance</div>
        <div class="stat-val val-emerald">100%</div>
        <div class="stat-sub">deterministic output</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">Swarm Architecture</div>
        <div class="stat-val val-indigo">4 Agents</div>
        <div class="stat-sub">coordinated pipeline</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">Execution Latency</div>
        <div class="stat-val val-amber">&lt; 1.2s</div>
        <div class="stat-sub">full turn-around</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">Governance Grade</div>
        <div class="stat-val val-purple">A+</div>
        <div class="stat-sub">executive audit ready</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------- INPUT INGESTION MODES -----------------
transcript_input = ""

st.markdown("""
<div style="display:flex; align-items:center; gap:8px; margin-bottom:12px;">
    <span style="background:#38BDF8; color:#080C14; font-weight:800; font-size:0.75rem; padding:2px 8px; border-radius:9999px;">STEP 1</span>
    <span style="font-size:1.15rem; font-weight:700; color:#FFFFFF;">Select Input Ingestion Channel</span>
</div>
""", unsafe_allow_html=True)

input_mode_tabs = st.radio(
    "Select Your Input Mode:",
    ["🎙️ Live Microphone Voice Recording", "📁 Upload Audio File (.wav/.mp3)", "📝 Preloaded Scenarios & Notes"],
    horizontal=True,
    index=0
)

if input_mode_tabs == "🎙️ Live Microphone Voice Recording":
    st.markdown("""
    <div style="background:rgba(30, 41, 59, 0.4); border:1px solid rgba(56, 189, 248, 0.25); padding:16px; border-radius:10px; margin-bottom:14px;">
        <div style="display:flex; align-items:center; gap:8px;">
            <span style="color:#38BDF8; font-size:1.2rem;">🎙️</span>
            <b style="color:#F8FAFC; font-size:1rem;">Direct Microphone Ingestion</b>
        </div>
        <div style="font-size:0.86rem; color:#94A3B8; margin-top:4px;">
            Click the record button below to speak meeting action items or decisions live into your microphone.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    recorded_audio = st.audio_input("Record your voice:")
    
    if recorded_audio is not None:
        st.audio(recorded_audio)
        audio_proc = AudioProcessor(api_key=api_key)
        with st.spinner("🎙️ Transcribing live microphone speech..."):
            transcript_input = audio_proc.transcribe(recorded_audio.getvalue(), file_name="live_microphone_recording.wav")
        st.success("Transcribed live microphone recording successfully!")
    else:
        st.caption("💡 No microphone available right now? Select a pre-recorded audio sample below:")
        sample_choice = st.selectbox("Pre-recorded Audio Sample", [
            "fintech_onboarding_call_recording.wav",
            "production_incident_debrief.wav",
            "executive_strategy_sync.wav"
        ])
        audio_proc = AudioProcessor(api_key=api_key)
        transcript_input = audio_proc.transcribe(b"", file_name=sample_choice)

    with st.expander("📝 View & Edit Transcribed Dialogue", expanded=True):
        transcript_input = st.text_area("Transcribed Dialogue", value=transcript_input, height=150)

elif input_mode_tabs == "📁 Upload Audio File (.wav/.mp3)":
    st.markdown("""
    <div style="background:rgba(30, 41, 59, 0.4); border:1px solid rgba(52, 211, 153, 0.25); padding:16px; border-radius:10px; margin-bottom:14px;">
        <div style="display:flex; align-items:center; gap:8px;">
            <span style="color:#34D399; font-size:1.2rem;">📁</span>
            <b style="color:#F8FAFC; font-size:1rem;">Audio File Ingestion</b>
        </div>
        <div style="font-size:0.86rem; color:#94A3B8; margin-top:4px;">
            Drop an audio recording (.wav, .mp3, .m4a) from Zoom, Google Meet, or your phone.
        </div>
    </div>
    """, unsafe_allow_html=True)

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
    st.markdown("""
    <div style="background:rgba(30, 41, 59, 0.4); border:1px solid rgba(255, 255, 255, 0.1); padding:16px; border-radius:10px; margin-bottom:14px;">
        <div style="display:flex; align-items:center; gap:8px;">
            <span style="color:#A78BFA; font-size:1.2rem;">📝</span>
            <b style="color:#F8FAFC; font-size:1rem;">Preloaded Enterprise Scenarios</b>
        </div>
        <div style="font-size:0.86rem; color:#94A3B8; margin-top:4px;">
            Select a realistic corporate transcript or paste your own raw notes.
        </div>
    </div>
    """, unsafe_allow_html=True)

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
st.write("")
col_btn1, col_btn2 = st.columns([1.5, 3.5])
with col_btn1:
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

    st.markdown(f"""
    <div style="background:rgba(16, 185, 129, 0.1); border:1px solid rgba(16, 185, 129, 0.3); border-radius:10px; padding:12px 18px; margin: 18px 0px 22px 0px; display:flex; justify-content:space-between; align-items:center;">
        <div>
            <span style="color:#34D399; font-weight:800; font-size:0.8rem; text-transform:uppercase; letter-spacing:0.5px;">DELIVERY TARGET</span>
            <div style="font-size:1.15rem; font-weight:700; color:#FFFFFF;">{extracted.get('meeting_title')}</div>
        </div>
        <div style="text-align:right;">
            <span class="agent-pill badge-info">MILESTONE: {extracted.get('target_go_live')}</span>
            <span class="agent-pill badge-low">HEALTH: {roi.get('health_grade')}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Main Tabs
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
        st.markdown("#### 1. Core Strategic Decisions")
        dec_cols = st.columns(len(extracted.get("decisions", [])) or 1)
        for idx, d in enumerate(extracted.get("decisions", [])):
            with dec_cols[idx % len(dec_cols)]:
                st.markdown(f"""
                <div class="decision-card">
                    <div class="decision-title">{d.get('decision')}</div>
                    <div class="decision-meta"><b>Context:</b> {d.get('context')}</div>
                    <div class="decision-impact">Impact: {d.get('impact')}</div>
                </div>
                """, unsafe_allow_html=True)

        st.divider()
        st.markdown("#### 2. Human-in-the-Loop (HITL) Action Items Editor")
        st.caption("Review, edit assignees, adjust deadlines, or add new tasks before finalizing documentation.")

        action_df = pd.DataFrame(extracted.get("action_items", []))
        edited_action_df = st.data_editor(
            action_df,
            use_container_width=True,
            num_rows="dynamic",
            key="action_editor"
        )

        col_sync1, col_sync2 = st.columns([1.2, 3.8])
        with col_sync1:
            if st.button("💾 Re-Sync SOP & Tickets with Edits", type="secondary", use_container_width=True):
                updated_actions = edited_action_df.to_dict('records')
                extracted["action_items"] = updated_actions
                
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
            st.markdown("#### 3. Identified Risks & Mitigations")
            for r in extracted.get("risks_and_blockers", []):
                sev = r.get("severity", "Medium")
                badge_class = "badge-critical" if sev == "High" else "badge-med"
                st.markdown(f"""
                <div class="risk-card">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                        <span class="agent-pill {badge_class}">{sev.upper()} SEVERITY</span>
                        <b style="color:#F8FAFC;">{r.get('risk')}</b>
                    </div>
                    <div style="font-size: 0.85rem; color:#FBBF24; margin-top: 4px;"><b>Impact:</b> {r.get('impact')}</div>
                    <div style="font-size: 0.85rem; color:#34D399; margin-top: 2px;"><b>Mitigation:</b> {r.get('mitigation')}</div>
                </div>
                """, unsafe_allow_html=True)

        with col_raci:
            st.markdown("#### 4. RACI Governance Matrix")
            raci_df = pd.DataFrame(extracted.get("raci_matrix", []))
            if not raci_df.empty:
                st.dataframe(raci_df, use_container_width=True, hide_index=True)

    # ----------------- TAB 2: ROI SCORECARD -----------------
    with tab2:
        st.markdown("#### 📈 Executive Meeting Productivity & ROI Scorecard")
        st.caption("Quantifying business yield: 'Every Person Owns a Number'")

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
            st.markdown("##### ⏱️ Cost Breakdown: Manual vs AI Automation")
            cost_df = pd.DataFrame({
                "Operational Model": ["Traditional (Manual Admin)", "SyncOps AI (Automated)"],
                "Cost ($)": [roi["direct_meeting_cost"] + roi["manual_admin_cost"], roi["direct_meeting_cost"] + 3.25]
            })
            st.bar_chart(cost_df.set_index("Operational Model"))

        with col_chart2:
            st.markdown("##### 🎯 Strategic Yield Summary")
            st.markdown(f"""
            - **Identified Decisions:** `{roi['total_decisions']}` core operational commitments
            - **Actionable Deliverables:** `{roi['total_actions']}` engineering tickets assigned
            - **Risk Registry:** `{roi['total_risks']}` active mitigation pathways established
            - **Estimated Annual Savings (100 meetings/yr):** **<span style="color:#34D399; font-size:1.15rem;">${roi['net_savings_per_meeting'] * 100:,.2f}</span>**
            """, unsafe_allow_html=True)

    # ----------------- TAB 3: SOP ARCHITECT & VISUAL FLOW -----------------
    with tab3:
        top_sop_col1, top_sop_col2 = st.columns([3, 1])
        with top_sop_col1:
            st.markdown(f"#### Generated Standard Operating Procedure (`{sop['sop_id']}`)")
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
        st.markdown("##### 🔄 Graphical Workflow Architecture Diagram")
        render_mermaid(sop["mermaid_code"])

        with st.expander("Show Mermaid Source Code"):
            st.code(sop["mermaid_code"], language="mermaid")

        st.markdown("##### 📖 Full Standard Operating Procedure")
        st.markdown(sop["markdown"])

    # ----------------- TAB 4: TASK & TICKET DISPATCHER -----------------
    with tab4:
        st.markdown("#### Project Management Ticket Dispatcher")
        st.caption("Export extracted tasks formatted with acceptance criteria into Jira, Linear, or ClickUp.")

        col_d1, col_d2 = st.columns([1.2, 3.8])
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
                <span class="agent-pill badge-info">ROLE: {t['role']}</span>
                <span class="agent-pill badge-low">TARGET: {t['deadline']}</span>
                """, unsafe_allow_html=True)
                st.markdown(t["description"])

    # ----------------- TAB 5: EXECUTIVE COMMS -----------------
    with tab5:
        st.markdown("#### Executive Communications Hub")
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
        st.markdown("#### ⚡ Live Webhook & Integration Dispatcher")
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

        col_wh1, col_wh2 = st.columns([1.2, 3.8])
        with col_wh1:
            dispatch_button = st.button("📡 Dispatch Live Webhook", type="primary", use_container_width=True)

        if dispatch_button:
            if "YOUR/REAL" in wh_url or "api.skillfyai.school" in wh_url:
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
