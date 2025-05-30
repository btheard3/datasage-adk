from fpdf import FPDF
import io

def generate_pdf_report(results: dict) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, "DataSage Report", ln=True, align="C")

    for section, content in results.items():
        pdf.ln(10)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, txt=section.replace("_", " ").title(), ln=True)

        pdf.set_font("Arial", size=11)
        if isinstance(content, dict):
            for key, value in content.items():
                value_str = str(value).replace("\n", " ").strip()
                pdf.multi_cell(0, 8, f"{key}: {value_str}")
        else:
            pdf.multi_cell(0, 8, str(content))

    output = io.BytesIO()
    pdf.output(output)
    output.seek(0)
    return output.read()













