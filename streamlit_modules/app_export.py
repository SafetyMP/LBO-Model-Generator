"""
Export functions for Streamlit app.

Includes PDF export and other export formats.
"""

import streamlit as st
import pandas as pd
from typing import Dict, Optional
import io
import tempfile
import os

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.platypus import (
        SimpleDocTemplate,
        Table,
        TableStyle,
        Paragraph,
        Spacer,
        PageBreak,
        Image,
    )
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


def generate_pdf_summary(
    results: Dict, inputs: Dict, company_name: str = "LBO Deal Screener"
) -> Optional[bytes]:
    """
    Generate PDF summary report with key metrics and charts.

    Returns:
        PDF file as bytes, or None if reportlab not available
    """
    if not REPORTLAB_AVAILABLE:
        return None

    # Create PDF in memory
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5 * inch, bottomMargin=0.5 * inch)

    # Container for PDF elements
    elements = []
    styles = getSampleStyleSheet()

    # Title
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Heading1"],
        fontSize=24,
        textColor=colors.HexColor("#1f77b4"),
        spaceAfter=30,
        alignment=TA_CENTER,
    )
    elements.append(Paragraph(f"<b>{company_name}</b>", title_style))
    elements.append(Paragraph("LBO Model Summary Report", styles["Heading2"]))
    elements.append(Spacer(1, 0.3 * inch))

    # Executive Summary
    elements.append(Paragraph("<b>Executive Summary</b>", styles["Heading2"]))
    elements.append(Spacer(1, 0.1 * inch))

    # Key Metrics Table
    metrics_data = [
        ["Metric", "Value"],
        ["Equity IRR", f"{results.get('irr', 0):.1%}"],
        ["MOIC", f"{results.get('moic', 0):.2f}x"],
        ["Exit EV", f"${results.get('exit_ev', 0)/1_000_000:.1f}M"],
        ["Exit Equity Value", f"${results.get('exit_equity_value', 0)/1_000_000:.1f}M"],
        ["Equity Invested", f"${results.get('equity_invested', 0)/1_000_000:.1f}M"],
        ["Total Debt Paydown", f"${results.get('debt_paid', 0):.1f}M"],
    ]

    metrics_table = Table(metrics_data, colWidths=[3 * inch, 2 * inch])
    metrics_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f77b4")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 12),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("FONTSIZE", (0, 1), (-1, -1), 10),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ]
        )
    )
    elements.append(metrics_table)
    elements.append(Spacer(1, 0.2 * inch))

    # Assumptions Section
    elements.append(Paragraph("<b>Key Assumptions</b>", styles["Heading2"]))
    elements.append(Spacer(1, 0.1 * inch))

    assumptions_data = [
        ["Assumption", "Value"],
        ["Entry Multiple", f"{inputs.get('entry_multiple', 0):.1f}x"],
        ["Exit Multiple", f"{inputs.get('exit_multiple', 0):.1f}x"],
        ["Leverage Ratio", f"{inputs.get('leverage_ratio', 0):.1f}x"],
        ["Revenue Growth", f"{inputs.get('rev_growth', 0):.1%}"],
        ["EBITDA Margin", f"{inputs.get('ebitda_margin', 0):.1%}"],
        ["Entry EBITDA", f"${inputs.get('entry_ebitda', 0)/1_000_000:.1f}M"],
        ["Interest Rate", f"{inputs.get('interest_rate', 0):.1%}"],
        ["Tax Rate", f"{inputs.get('tax_rate', 0):.1%}"],
    ]

    assumptions_table = Table(assumptions_data, colWidths=[3 * inch, 2 * inch])
    assumptions_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2ca02c")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 12),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("FONTSIZE", (0, 1), (-1, -1), 10),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ]
        )
    )
    elements.append(assumptions_table)
    elements.append(Spacer(1, 0.2 * inch))

    # Entry vs Exit Comparison
    elements.append(Paragraph("<b>Entry vs Exit Comparison</b>", styles["Heading2"]))
    elements.append(Spacer(1, 0.1 * inch))

    entry_ev = results.get("entry_ev", 0)
    exit_ev = results.get("exit_ev", 0)
    entry_ebitda = results.get("entry_ebitda", 0)
    exit_ebitda = results.get("exit_ebitda", 0)

    ev_change = ((exit_ev - entry_ev) / entry_ev * 100) if entry_ev > 0 else 0
    ebitda_change = ((exit_ebitda - entry_ebitda) / entry_ebitda * 100) if entry_ebitda > 0 else 0

    comparison_data = [
        ["Metric", "Entry", "Exit", "Change"],
        [
            "Enterprise Value",
            f"${entry_ev/1_000_000:.1f}M",
            f"${exit_ev/1_000_000:.1f}M",
            f"{ev_change:+.1f}%",
        ],
        [
            "EBITDA",
            f"${entry_ebitda/1_000_000:.1f}M",
            f"${exit_ebitda/1_000_000:.1f}M",
            f"{ebitda_change:+.1f}%",
        ],
    ]

    comparison_table = Table(
        comparison_data, colWidths=[2 * inch, 1.5 * inch, 1.5 * inch, 1 * inch]
    )
    comparison_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#ff7f0e")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 12),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("FONTSIZE", (0, 1), (-1, -1), 10),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ]
        )
    )
    elements.append(comparison_table)
    elements.append(Spacer(1, 0.2 * inch))

    # Financial Statements Summary
    if "financial_statements" in results and not results["financial_statements"].empty:
        elements.append(PageBreak())
        elements.append(Paragraph("<b>Financial Statements Summary</b>", styles["Heading2"]))
        elements.append(Spacer(1, 0.1 * inch))

        fs = results["financial_statements"]

        # Create summary table
        summary_cols = ["Year"]
        if "Revenue" in fs.columns:
            summary_cols.append("Revenue")
        if "Ebitda" in fs.columns:
            summary_cols.append("EBITDA")
        if "Fcf" in fs.columns:
            summary_cols.append("FCF")

        if len(summary_cols) > 1:
            fs_data = [summary_cols]
            for idx, row in fs.iterrows():
                row_data = [str(idx)]
                if "Revenue" in fs.columns:
                    row_data.append(f"${row.get('Revenue', 0)/1_000_000:.1f}M")
                if "Ebitda" in fs.columns:
                    row_data.append(f"${row.get('Ebitda', 0)/1_000_000:.1f}M")
                if "Fcf" in fs.columns:
                    row_data.append(f"${row.get('Fcf', 0)/1_000_000:.1f}M")
                fs_data.append(row_data)

            fs_table = Table(fs_data, colWidths=[1 * inch] + [1.5 * inch] * (len(summary_cols) - 1))
            fs_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#9467bd")),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 11),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                        ("FONTSIZE", (0, 1), (-1, -1), 9),
                        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
                    ]
                )
            )
            elements.append(fs_table)

    # Footer
    elements.append(Spacer(1, 0.3 * inch))
    footer_style = ParagraphStyle(
        "Footer", parent=styles["Normal"], fontSize=8, textColor=colors.grey, alignment=TA_CENTER
    )
    elements.append(Paragraph("Generated by LBO Deal Screener", footer_style))
    elements.append(
        Paragraph(
            f"Report generated on {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}", footer_style
        )
    )

    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()


def export_pdf_button(results: Dict, inputs: Dict, company_name: str = "LBO Deal Screener"):
    """Display PDF export button in Streamlit."""
    if not REPORTLAB_AVAILABLE:
        st.warning("⚠️ PDF export requires reportlab. Install with: `pip install reportlab`")
        return

    if st.button("📄 Export PDF Summary", type="secondary"):
        with st.spinner("Generating PDF report..."):
            try:
                pdf_bytes = generate_pdf_summary(results, inputs, company_name)
                if pdf_bytes:
                    st.download_button(
                        label="📥 Download PDF Report",
                        data=pdf_bytes,
                        file_name=f"lbo_summary_{pd.Timestamp.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf",
                    )
                    st.success("✅ PDF report generated successfully!")
                else:
                    st.error("Failed to generate PDF report.")
            except Exception as e:
                st.error(f"Error generating PDF: {str(e)}")
                st.exception(e)
