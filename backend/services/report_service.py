import base64
import io
import os
from datetime import datetime

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, HRFlowable
)

from database.mongodb import users
from services.email_service import send_email

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
DISCLAIMER = (
    "This report is an AI-assisted analysis intended to support, not replace, "
    "clinical judgment. It is not a confirmed medical diagnosis. Please consult "
    "your doctor for interpretation."
)

NEGATIVE_CLASS = "No Tumor"

# --- Theme colors ---
BRAND_DARK = colors.HexColor("#1e3a8a")
BRAND_BLUE = colors.HexColor("#2563eb")
BRAND_LIGHT = colors.HexColor("#eff6ff")
TEXT_MUTED = colors.HexColor("#64748b")
LINE_LIGHT = colors.HexColor("#e2e8f0")

POSITIVE_BG = colors.HexColor("#fee2e2")
POSITIVE_BORDER = colors.HexColor("#dc2626")
POSITIVE_TEXT = colors.HexColor("#991b1b")
NEGATIVE_BG = colors.HexColor("#dcfce7")
NEGATIVE_BORDER = colors.HexColor("#16a34a")
NEGATIVE_TEXT = colors.HexColor("#166534")


def _styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "ReportTitle", parent=base["Title"],
            fontName="Helvetica-Bold", fontSize=22, leading=26,
            textColor=colors.white, alignment=TA_CENTER, spaceAfter=0,
        ),
        "subtitle": ParagraphStyle(
            "ReportSubtitle", parent=base["Normal"],
            fontName="Helvetica", fontSize=10.5, leading=14,
            textColor=colors.HexColor("#dbeafe"), alignment=TA_CENTER,
        ),
        "timestamp": ParagraphStyle(
            "ReportTimestamp", parent=base["Normal"],
            fontName="Helvetica-Oblique", fontSize=9, leading=12,
            textColor=colors.HexColor("#bfdbfe"), alignment=TA_CENTER,
        ),
        "section": ParagraphStyle(
            "SectionHeading", parent=base["Heading3"],
            fontName="Helvetica-Bold", fontSize=12.5, leading=16,
            textColor=BRAND_DARK, spaceBefore=4, spaceAfter=6,
        ),
        "normal": base["Normal"],
        "italic": ParagraphStyle(
            "DisclaimerStyle", parent=base["Normal"],
            fontName="Helvetica-Oblique", fontSize=8.5, leading=12,
            textColor=TEXT_MUTED,
        ),
        "small_muted": ParagraphStyle(
            "SmallMuted", parent=base["Normal"],
            fontName="Helvetica", fontSize=8.5, leading=11,
            textColor=TEXT_MUTED, alignment=TA_CENTER,
        ),
    }


def _impression_box(tumor, focus_region, s):
    """A single colored impression box: positive/negative, tumor type,
    and the general image region the AI focused on most."""
    if not tumor:
        return None

    is_negative = tumor == NEGATIVE_CLASS
    bg = NEGATIVE_BG if is_negative else POSITIVE_BG
    border = NEGATIVE_BORDER if is_negative else POSITIVE_BORDER
    text_color = NEGATIVE_TEXT if is_negative else POSITIVE_TEXT

    style = ParagraphStyle(
        "ImpressionBox", parent=s["normal"],
        fontName="Helvetica-Bold", fontSize=11.5, leading=16,
        textColor=text_color,
    )
    label_style = ParagraphStyle(
        "ImpressionLabel", parent=s["normal"],
        fontName="Helvetica-Bold", fontSize=8.5, leading=11,
        textColor=text_color,
    )

    if is_negative:
        label = "NEGATIVE FINDING"
        text = (
            "No tumor characteristics were detected by AI analysis. "
            "Please consult the referring doctor for clinical correlation."
        )
    else:
        label = "POSITIVE FINDING"
        region_note = (
            f" The AI's attention was concentrated in the {focus_region} region of the scan."
            if focus_region else ""
        )
        text = (
            f"Characteristics consistent with {tumor} were detected.{region_note} "
            f"Please consult the referring doctor for clinical correlation."
        )

    box = Table(
        [[Paragraph(label, label_style)], [Paragraph(text, style)]],
        colWidths=[165 * mm],
    )
    box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LINEBEFORE", (0, 0), (0, -1), 3, border),
        ("TOPPADDING", (0, 0), (-1, 0), 8),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 2),
        ("TOPPADDING", (0, 1), (-1, 1), 2),
        ("BOTTOMPADDING", (0, 1), (-1, 1), 9),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
    ]))
    return box


def decode_image(value):
    """Accepts a data URL or raw base64 and returns bytes, or None."""
    if not value or not isinstance(value, str):
        return None
    try:
        if value.startswith("data:") and "," in value:
            value = value.split(",", 1)[1]
        return base64.b64decode(value)
    except Exception:
        return None


def _read_file_bytes(path):
    try:
        with open(path, "rb") as f:
            return f.read()
    except Exception:
        return None


def _image_flowable(data, max_w, max_h):
    if not data:
        return None
    try:
        with PILImage.open(io.BytesIO(data)) as im:
            w, h = im.size
        scale = min(max_w / w, max_h / h)
        return RLImage(io.BytesIO(data), width=w * scale, height=h * scale)
    except Exception:
        return None


def _format_scan_datetime(value):
    """value is stored as 'YYYY-MM-DDTHH:MM'. Falls back to raw value if parsing fails."""
    try:
        dt = datetime.strptime(value, "%Y-%m-%dT%H:%M")
        return dt.strftime("%d %b %Y, %I:%M %p")
    except (ValueError, TypeError):
        return value or "-"


def _info_table(rows, s):
    t = Table(rows, colWidths=[48 * mm, 117 * mm])
    style = [
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("TEXTCOLOR", (0, 0), (0, -1), BRAND_DARK),
        ("TEXTCOLOR", (1, 0), (1, -1), colors.HexColor("#1f2937")),
        ("BACKGROUND", (0, 0), (0, -1), BRAND_LIGHT),
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, LINE_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]
    t.setStyle(TableStyle(style))
    return t


def build_pdf(report, include_result=True):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=18 * mm,
                            rightMargin=18 * mm, topMargin=0, bottomMargin=16 * mm)
    s = _styles()
    p, d = report["patient"], report["doctor"]
    result = (report.get("result") or {}) if include_result else {}
    generated_at = datetime.now().strftime("%d %b %Y, %I:%M %p")

    # --- Header band ---
    header_content = [
        [Paragraph("MRI ANALYSIS REPORT", s["title"])],
        [Paragraph("Quantum Brain AI", s["subtitle"])],
        [Paragraph(f"Report generated on: {generated_at}", s["timestamp"])],
    ]
    header = Table(header_content, colWidths=[174 * mm])
    header.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BRAND_DARK),
        ("TOPPADDING", (0, 0), (-1, 0), 16),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 2),
        ("TOPPADDING", (0, 1), (-1, 1), 2),
        ("BOTTOMPADDING", (0, 1), (-1, 1), 2),
        ("TOPPADDING", (0, 2), (-1, 2), 2),
        ("BOTTOMPADDING", (0, 2), (-1, 2), 16),
    ]))

    story = [header, Spacer(1, 10 * mm)]

    story += [
        Paragraph("PATIENT", s["section"]),
        _info_table([
            ["Name", p["full_name"]], ["Patient ID", p["patient_id"]],
            ["Age", str(p["age"])], ["Gender", p["gender"]],
        ], s),
        Spacer(1, 6 * mm),
        Paragraph("REFERRING DOCTOR", s["section"]),
        _info_table([["Doctor", d["full_name"]], ["Hospital / Clinic", d["hospital"]]], s),
        Spacer(1, 6 * mm),
    ]

    info_rows = [["MRI Scan Date & Time", _format_scan_datetime(report["scan_date"])]]
    if include_result and result.get("tumor") is not None:
        info_rows += [
            ["AI Prediction", str(result.get("tumor", "-"))],
            ["Confidence", f'{result.get("confidence", "-")}%'],
        ]
    info_rows.append(["Referral Code", report["referral_code"]])

    story += [
        Paragraph("REPORT DETAILS", s["section"]),
        _info_table(info_rows, s),
        Spacer(1, 5 * mm),
    ]

    impression_box = (
        _impression_box(result.get("tumor"), result.get("focus_region"), s)
        if include_result else None
    )
    if impression_box:
        story += [impression_box, Spacer(1, 7 * mm)]

    if report.get("clinical_notes"):
        story += [
            Paragraph("CLINICAL NOTES", s["section"]),
            Paragraph(report["clinical_notes"], s["normal"]),
            Spacer(1, 6 * mm),
        ]

    mri_flowable = _image_flowable(_read_file_bytes(report["image_path"]), 85 * mm, 85 * mm)
    if mri_flowable:
        story += [Paragraph("MRI SCAN", s["section"]), mri_flowable, Spacer(1, 6 * mm)]

    if include_result:
        heatmap = _image_flowable(decode_image(result.get("heatmap")), 85 * mm, 85 * mm)
        if heatmap:
            story += [
                Paragraph("EXPLAINABILITY HEATMAP (GRAD-CAM STYLE)", s["section"]),
                heatmap, Spacer(1, 6 * mm),
            ]
    else:
        story += [Paragraph(
            "AI analysis has not been generated for this report yet. "
            "It will be available once the assigned doctor reviews it.",
            s["normal"])]

    story += [
        HRFlowable(width="100%", thickness=0.6, color=LINE_LIGHT, spaceBefore=4, spaceAfter=8),
        Paragraph(DISCLAIMER, s["italic"]),
        Spacer(1, 4 * mm),
        Paragraph("Quantum Brain AI &bull; Automated AI-assisted MRI analysis", s["small_muted"]),
    ]

    doc.build(story)
    return buf.getvalue()


def send_report_emails(report):
    """Returns {"doctor": bool, "patient": bool}. Neither email contains the result."""
    p, d = report["patient"], report["doctor"]
    code = report["referral_code"]
    status = {"doctor": False, "patient": False}

    registered = users.find_one({"email": d["email"], "role": "doctor"}) is not None
    signup_hint = "" if registered else (
        f"\nYou do not have an account yet. Please sign up as a Doctor at "
        f"{FRONTEND_URL}/signup using this same email address ({d['email']}).\n"
    )

    doctor_body = (
        f"Hello Dr. {d['full_name']},\n\n"
        f"A new MRI analysis report is available for your patient {p['full_name']}.\n\n"
        f"Referral code: {code}\n\n"
        f"To view it, log in to the doctor portal at {FRONTEND_URL}/login with your "
        f"registered account, choose \"Enter Referral Code\", and enter the code above. "
        f"Only your account can open this report.\n"
        f"{signup_hint}\n"
        f"Sent by: {report['lab_name']}\n"
    )
    try:
        send_email(d["email"], "A new MRI report is available for your review", doctor_body)
        status["doctor"] = True
    except Exception as e:
        print("Doctor email error:", e)

    patient_body = (
        f"Hello {p['full_name']},\n\n"
        f"Your MRI analysis report has been generated and shared with your doctor, "
        f"Dr. {d['full_name']} ({d['hospital']}).\n\n"
        f"Reference code: {code}\n\n"
        f"Please contact your doctor for interpretation of the result. This analysis "
        f"is AI-assisted and is not a confirmed medical diagnosis.\n"
    )
    try:
        send_email(p["email"], "Your MRI report has been shared with your doctor", patient_body)
        status["patient"] = True
    except Exception as e:
        print("Patient email error:", e)

    return status