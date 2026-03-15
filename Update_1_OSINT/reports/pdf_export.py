"""
pdf_export.py
-------------
Generates PDF reports for OSINT / SOC dashboard
Unicode-safe, professional layout
"""

import os
import sqlite3
from datetime import datetime
from fpdf import FPDF

# ✅ SINGLE SOURCE OF TRUTH FOR DB
from data.db_config import DB_PATH


# ================= REPORT OUTPUT DIR =================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_DIR = os.path.join(BASE_DIR, "reports", "generated")
os.makedirs(REPORT_DIR, exist_ok=True)


# ================= PDF CLASS =================
class SOCReportPDF(FPDF):

    def header(self):
        # Dark Blue Header Banner
        self.set_fill_color(15, 23, 42) # slate-900
        self.rect(0, 0, 210, 35, style='F')
        
        self.set_y(15)
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, "OSINT Threat Intelligence Report", ln=True, align="L")
        self.set_y(17)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(148, 163, 184) # slate-400
        self.cell(0, 10, f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC", align="R")
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", size=8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

# ================= MAIN FUNCTION =================
def generate_pdf_report(target_filter=None):
    """
    Generate SOC PDF report from analysis_logs table
    Returns generated file path
    """

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    query = """
        SELECT
            target,
            threat_level,
            threat_type,
            risk_score,
            vt_score,
            abuse_score,
            open_ports,
            created_at
        FROM analysis_logs
    """
    
    if target_filter:
        query += " WHERE target = ? ORDER BY created_at DESC"
        cur.execute(query, (target_filter,))
    else:
        query += " ORDER BY created_at DESC"
        cur.execute(query)

    rows = cur.fetchall()
    conn.close()

    pdf = SOCReportPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    if not rows:
        pdf.set_y(50)
        pdf.set_font("Helvetica", size=12)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 10, "No data available for this report.", align="C")
        
        filename = f"osint_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.pdf"
        file_path = os.path.join(REPORT_DIR, filename)
        pdf.output(file_path)
        return file_path

    # Compute overall stats if multiple targets, or focus on the single target
    overall_title = f"Executive Summary: {target_filter}" if target_filter else "Platform Executive Summary"
    
    pdf.set_y(40)
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 10, overall_title, ln=True)

    # ---------------- SUMMARY STATS ----------------
    high_count = sum(1 for r in rows if "high" in str(r[1]).lower() or "critical" in str(r[1]).lower())
    med_count = sum(1 for r in rows if "medium" in str(r[1]).lower())
    low_count = len(rows) - high_count - med_count
    
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(71, 85, 105)
    
    summary_text = f"Total Scanned: {len(rows)}    |    High Risk: {high_count}    |    Medium Risk: {med_count}    |    Low Risk: {low_count}"
    pdf.cell(0, 8, summary_text, ln=True)
    pdf.ln(5)

    # ---------------- REPORT BODY ----------------
    for row in rows:
        (
            target,
            level,
            threat_type,
            risk_score,
            vt_score,
            abuse_score,
            open_ports,
            created_at
        ) = row

        # Card Box
        start_y = pdf.get_y()
        if start_y > 230:
            pdf.add_page()
            start_y = pdf.get_y()

        pdf.set_fill_color(248, 250, 252) # slate-50
        pdf.set_draw_color(226, 232, 240) # slate-200
        pdf.rect(10, start_y, 190, 50, style='FD')
        
        # Determine Color based on Risk
        level = str(level).lower()
        if "high" in level:
            r, g, b = 239, 68, 68 # red
        elif "medium" in level:
            r, g, b = 245, 158, 11 # amber
        else:
            r, g, b = 16, 185, 129 # emerald

        # Left Accent Line
        pdf.set_fill_color(r, g, b)
        pdf.rect(10, start_y, 3, 50, style='F')

        # Target Name
        pdf.set_xy(15, start_y + 5)
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(100, 8, f"{target}")

        # Date
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(100, 100, 100)
        pdf.set_xy(150, start_y + 5)
        pdf.cell(45, 8, f"{created_at}", align="R")

        # Visual Risk Bar
        pdf.set_xy(15, start_y + 15)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(r, g, b)
        pdf.cell(40, 6, f"THREAT: {level.upper()}")
        
        # Draw Bar empty
        pdf.set_fill_color(226, 232, 240)
        pdf.rect(55, start_y + 17, 100, 4, style='F')
        # Fill Bar based on risk score (0-100)
        score = min(max(int(risk_score), 0), 100)
        pdf.set_fill_color(r, g, b)
        pdf.rect(55, start_y + 17, score, 4, style='F')
        
        # Details row
        pdf.set_xy(15, start_y + 25)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(71, 85, 105)
        
        details = (
            f"Type: {threat_type}   |   "
            f"VirusTotal: {vt_score} hits   |   "
            f"AbuseIPDB: {abuse_score}   |   "
            f"Ports: {open_ports if open_ports else 'None'}"
        )
        pdf.cell(0, 10, details)

        pdf.set_y(start_y + 60)

    # ---------------- SAVE FILE ----------------
    filename = f"osint_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.pdf"
    file_path = os.path.join(REPORT_DIR, filename)

    pdf.output(file_path)

    return file_path
