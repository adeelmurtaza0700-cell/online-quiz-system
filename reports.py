from fpdf import FPDF
from database import fetch_all
import csv

def generate_certificate(name, quiz_title, score):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial",'B',16)
    pdf.cell(0,10,"Certificate of Achievement",ln=True,align="C")
    pdf.ln(10)
    pdf.set_font("Arial",'',12)
    pdf.multi_cell(0,10,f"This certifies that {name} has successfully completed the quiz '{quiz_title}' with a score of {score}%.")
    pdf.output(f"certificate_{name}.pdf")

def export_results_csv():
    results = fetch_all("SELECT * FROM results")
    if results:
        keys = results[0].keys()
        with open("results.csv","w",newline="") as f:
            dict_writer = csv.DictWriter(f,keys)
            dict_writer.writeheader()
            dict_writer.writerows(results)
