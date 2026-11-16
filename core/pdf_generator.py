"""
Executive PDF Generator for SyncOps AI
Generates formatted, publication-grade Standard Operating Procedure (SOP) PDF documents using ReportLab.
"""

import io
from typing import Dict, Any, List

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable


def generate_sop_pdf(sop_data: Dict[str, Any], extracted_data: Dict[str, Any]) -> bytes:
    """Generates an executive-ready PDF report of the SOP and returns bytes."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    
    # Custom Paragraph Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#64748B'),
        spaceAfter=14
    )
    
    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=14,
        spaceAfter=6
    )
    
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155'),
        spaceAfter=6
    )
    
    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#1E293B')
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.white
    )

    elements = []

    # Title & Metadata Block
    title = sop_data.get("title", "Standard Operating Procedure")
    elements.append(Paragraph(title, title_style))
    elements.append(Paragraph(f"Document ID: {sop_data.get('sop_id', 'SOP-OPS-2026')} | Effective Date: {sop_data.get('effective_date', 'November 2026')} | Status: APPROVED FOR EXECUTION", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#3B82F6'), spaceAfter=14))

    # Purpose & Scope
    elements.append(Paragraph("1. Purpose & Scope", h2_style))
    purpose_text = sop_data.get("purpose", "Defines the operating procedures, operational safeguards, and execution gates derived from stakeholder requirements.")
    elements.append(Paragraph(purpose_text, body_style))
    
    scope_text = sop_data.get("scope", "Applies to cross-functional engineering, operations, security, and client success workstreams.")
    elements.append(Paragraph(f"<b>Scope:</b> {scope_text}", body_style))

    # Prerequisites & Access
    elements.append(Paragraph("2. Prerequisites & Governance Gates", h2_style))
    prereqs = sop_data.get("prerequisites", [
        "Verified stakeholder approval and mutual NDA/SLA execution",
        "Configured environment credentials with zero-trust role-based access",
        "Whitelisted communication endpoints and monitoring alerting webhooks"
    ])
    for idx, p in enumerate(prereqs, 1):
        elements.append(Paragraph(f"• <b>Gate {idx}:</b> {p}", body_style))

    # Step-by-Step Procedure
    elements.append(Paragraph("3. Step-by-Step Execution Procedure", h2_style))
    steps = sop_data.get("execution_steps", [])
    if not steps:
        steps = [
            {"phase": "Phase 1: Environment Provisioning", "details": "Validate static IP allocations and distribute signed OAuth2/mTLS client specifications."},
            {"phase": "Phase 2: Schema Mapping & Staging", "details": "Execute delta synchronization pipelines and confirm HMAC-SHA256 webhook callbacks."},
            {"phase": "Phase 3: Acceptance Testing & Go-Live", "details": "Perform end-to-end integration verification, review latency SLOs, and sign off for production release."}
        ]

    for s in steps:
        phase = s.get("phase", "Phase")
        details = s.get("details", "")
        elements.append(Paragraph(f"<b>{phase}</b>", body_style))
        elements.append(Paragraph(details, body_style))
        elements.append(Spacer(1, 4))

    # Action Items Table
    action_items = extracted_data.get("action_items", [])
    if action_items:
        elements.append(Paragraph("4. Action Item & Ownership Matrix", h2_style))
        table_data = [
            [
                Paragraph("ID", table_header_style),
                Paragraph("Task Description", table_header_style),
                Paragraph("Assignee", table_header_style),
                Paragraph("Priority", table_header_style),
                Paragraph("Deadline", table_header_style)
            ]
        ]
        for a in action_items:
            table_data.append([
                Paragraph(a.get("id", "ACT"), table_cell_style),
                Paragraph(a.get("task", ""), table_cell_style),
                Paragraph(a.get("assignee", "Unassigned"), table_cell_style),
                Paragraph(a.get("priority", "Medium"), table_cell_style),
                Paragraph(a.get("deadline", "TBD"), table_cell_style)
            ])

        t = Table(table_data, colWidths=[45, 230, 105, 55, 95])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E293B')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 10))

    # RACI Matrix Table
    raci_list = extracted_data.get("raci_matrix", [])
    if raci_list:
        elements.append(Paragraph("5. RACI Governance Matrix", h2_style))
        raci_table_data = [
            [
                Paragraph("Stakeholder Role", table_header_style),
                Paragraph("Responsible (R)", table_header_style),
                Paragraph("Accountable (A)", table_header_style),
                Paragraph("Consulted (C)", table_header_style),
                Paragraph("Informed (I)", table_header_style)
            ]
        ]
        for r in raci_list:
            raci_table_data.append([
                Paragraph(r.get("role", ""), table_cell_style),
                Paragraph(r.get("responsible", ""), table_cell_style),
                Paragraph(r.get("accountable", ""), table_cell_style),
                Paragraph(r.get("consulted", ""), table_cell_style),
                Paragraph(r.get("informed", ""), table_cell_style)
            ])

        r_table = Table(raci_table_data, colWidths=[110, 110, 110, 100, 100])
        r_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3B82F6')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
        ]))
        elements.append(r_table)
        elements.append(Spacer(1, 10))

    # Exception Handling & Quality Checklist
    elements.append(Paragraph("6. Exception Handling & Incident Escalation", h2_style))
    elements.append(Paragraph("If any milestone or verification criteria breaches acceptable tolerance by >24 hours, the designated Accountable lead triggers an immediate Severity-2 escalation to the Steering Committee. Rollback procedures must be executed within 30 minutes of SLA degradation.", body_style))

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()
