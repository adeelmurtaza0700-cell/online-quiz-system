from reportlab.pdfgen import canvas

def generate_certificate(name, quiz_title, score, file_path):
    c = canvas.Canvas(file_path)
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(300, 500, "Certificate of Completion")
    c.setFont("Helvetica", 18)
    c.drawCentredString(300, 450, f"Presented to: {name}")
    c.drawCentredString(300, 400, f"For completing the quiz: {quiz_title}")
    c.drawCentredString(300, 350, f"Score: {score}")
    c.save()
