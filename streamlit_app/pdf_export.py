# streamlit_app/pdf_export.py

from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "DataSage Healthcare Cost Report", ln=True, align="C")  # ⛔ Removed emoji

    def chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.set_fill_color(240, 240, 240)
        clean_title = str(title).encode("latin-1", "replace").decode("latin-1")
        self.cell(0, 10, clean_title, ln=True, fill=True)

    def chapter_body(self, content_dict):
        self.set_font("Arial", "", 11)
        for key, value in content_dict.items():
            try:
                key_str = str(key).encode("latin-1", "replace").decode("latin-1")
                value_str = str(value).encode("latin-1", "replace").decode("latin-1")
                self.multi_cell(0, 8, f"{key_str}: {value_str}")
            except Exception as e:
                self.multi_cell(0, 8, f"{key}: [Encoding Error]")
        self.ln()


def generate_pdf_report(results: dict) -> bytes:
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    for section, content in results.items():
        section_title = section.replace("_", " ").title()
        pdf.chapter_title(section_title)
        if isinstance(content, dict):
            pdf.chapter_body(content)
        else:
            value_str = str(content).encode("latin-1", "replace").decode("latin-1")
            pdf.set_font("Arial", "", 11)
            pdf.multi_cell(0, 8, value_str)
            pdf.ln()

    return pdf.output(dest="S").encode("latin-1")









