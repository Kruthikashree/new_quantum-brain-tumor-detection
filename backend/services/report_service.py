import base64
import io
import os
from datetime import datetime

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
)

from database.mongodb import users
from services.email_service import send_email

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
DISCLAIMER = (
    "This report is an AI-assisted analysis intended to support, not replace, "
    "clinical judgment. It is not a confirmed medical diagnosis. Please consult "
    "your doctor for interpretation."
)


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


def build_pdf(report, include_result=True):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=18 * mm,
                            rightMargin=18 * mm, topMargin=16 * mm,
                            bottomMargin=16 * mm)
    styles = getSampleStyleSheet()
    p, d = report["patient"], report["doctor"]
    result = (report.get("result") or {}) if include_result else {}
    generated_at = datetime.now().strftime("%d %b %Y, %I:%M %p")

    story = [
        Paragraph("MRI ANALYSIS REPORT", styles["Title"]),
        Paragraph("Quantum-Enhanced Brain Tumor Detection", styles["Normal"]),
        Paragraph(f"Report generated on: {generated_at}", styles["Normal"]),
        Spacer(1, 8 * mm),
    ]

    def table(rows):
        t = Table(rows, colWidths=[45 * mm, 120 * mm])
        t.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.lightgrey),
            ("BACKGROUND", (0, 0), (0, -1), colors.whitesmoke),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
        return t

    story += [
        Paragraph("Patient", styles["Heading3"]),
        table([
            ["Name", p["full_name"]], ["Patient ID", p["patient_id"]],
            ["Age", str(p["age"])], ["Gender", p["gender"]],
        ]),
        Spacer(1, 5 * mm),
        Paragraph("Referring Doctor", styles["Heading3"]),
        table([["Doctor", d["full_name"]], ["Hospital / Clinic", d["hospital"]]]),
        Spacer(1, 5 * mm),
    ]

    info_rows = [["MRI Scan Date & Time", _format_scan_datetime(report["scan_date"])]]
    if include_result and result.get("tumor") is not None:
        info_rows += [
            ["AI Prediction", str(result.get("tumor", "-"))],
            ["Confidence", f'{result.get("confidence", "-")}%'],
        ]
    info_rows.append(["Referral Code", report["referral_code"]])

    story += [Paragraph("Report Details", styles["Heading3"]), table(info_rows), Spacer(1, 5 * mm)]

    if report.get("clinical_notes"):
        story += [Paragraph("Clinical Notes", styles["Heading3"]),
                  Paragraph(report["clinical_notes"], styles["Normal"]),
                  Spacer(1, 5 * mm)]

    # MRI scan image — included for both lab and doctor versions
    mri_flowable = _image_flowable(_read_file_bytes(report["image_path"]), 90 * mm, 90 * mm)
    if mri_flowable:
        story += [Paragraph("MRI Scan", styles["Heading3"]), mri_flowable, Spacer(1, 5 * mm)]

    if include_result:
        heatmap = _image_flowable(decode_image(result.get("heatmap")), 90 * mm, 90 * mm)
        if heatmap:
            story += [Paragraph("Explainability Heatmap (Grad-CAM style)", styles["Heading3"]),
                      heatmap, Spacer(1, 5 * mm)]
    else:
        story += [Paragraph(
            "AI analysis has not been generated for this report yet. "
            "It will be available once the assigned doctor reviews it.",
            styles["Normal"])]

    story.append(Paragraph(DISCLAIMER, styles["Italic"]))
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