from fpdf import FPDF

def generate_pdf_report(data: dict) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for key, value in data.items():
        pdf.set_font("Arial", style='B', size=12)
        pdf.cell(0, 10, f"{key}:", ln=True)

        pdf.set_font("Arial", size=11)

        if isinstance(value, dict):
            value_str = "\n".join(f"{k}: {v}" for k, v in value.items())
        else:
            value_str = str(value)

        # Split long lines manually to prevent fpdf width errors
        for line in value_str.splitlines():
            if not line.strip():
                pdf.ln()
                continue
            wrapped = [line[i:i+90] for i in range(0, len(line), 90)]
            for segment in wrapped:
                pdf.multi_cell(0, 8, segment)

        pdf.ln()

    return pdf.output(dest="S").encode("latin-1")














