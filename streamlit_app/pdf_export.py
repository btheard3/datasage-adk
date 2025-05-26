from fpdf import FPDF

def generate_pdf_report(results: dict) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "DataSage Cost Report", ln=True, align='C')
    pdf.ln(5)

    for section, content in results.items():
        pdf.set_font("Arial", 'B', size=12)
        pdf.cell(200, 10, section.replace("_", " ").title(), ln=True)
        pdf.set_font("Arial", size=11)

        if isinstance(content, dict):
            for key, value in content.items():
                pdf.multi_cell(0, 10, f"{key}: {value}")
        else:
            pdf.multi_cell(0, 10, str(content))

        pdf.ln(5)

    return pdf.output(dest="S").encode("latin1", "replace")



