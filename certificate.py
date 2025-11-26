from fpdf import FPDF

def generate_certificate(name, quiz, score):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=24)
    pdf.cell(200, 20, txt="Certificate of Achievement", ln=1, align="C")

    pdf.set_font("Arial", size=16)
    pdf.cell(200, 10, txt=f"This is awarded to {name}", ln=1, align="C")
    pdf.cell(200, 10, txt=f"For scoring {score} in {quiz}", ln=1, align="C")

    file_path = f"certificate_{name}.pdf"
    pdf.output(file_path)
    return file_path
