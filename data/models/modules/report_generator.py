from reportlab.pdfgen import canvas

def generate_report():

    c = canvas.Canvas("reports/report.pdf")

    c.drawString(
        100,
        750,
        "CyberLens AI Report"
    )

    c.save()
