from fpdf import FPDF

def generate_pdf_report(results: dict) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="DataSage Report", ln=True, align="C")
    pdf.ln(10)

    for section, data in results.items():
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt=section.replace("_", " ").title(), ln=True)
        pdf.set_font("Arial", size=11)

        if isinstance(data, dict):
            for key, value in data.items():
                pdf.multi_cell(0, 10, f"{key}: {value}")
        else:
            pdf.multi_cell(0, 10, str(data))
        pdf.ln(5)

        return pdf.output(dest="S").encode("utf-8")


