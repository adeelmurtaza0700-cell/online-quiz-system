from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_certificate(name, quiz, score):
    filename = f"{name}_{quiz}_certificate.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica", 24)
    c.drawCentredString(300, 700, "Certificate of Completion")
    c.setFont("Helvetica", 18)
    c.drawCentredString(300, 650, f"Presented to {name}")
    c.drawCentredString(300, 600, f"For completing the quiz: {quiz}")
    c.drawCentredString(300, 550, f"Score: {score}")
    c.save()
    return filename
