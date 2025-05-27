from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "DataSage Report Summary", ln=True, align="C")

    def add_section(self, title, content):
        self.ln(10)
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, ln=True)
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 8, content)

def generate_pdf_report(results: dict) -> bytes:
    pdf = PDF()
    pdf.add_page()

    if "estimate_cost" in results:
        c = results["estimate_cost"]
        section = f"""
        - Average Cost: ${c.get('avg_cost', 0):,.2f}
        - Median Cost: ${c.get('median_cost', 0):,.2f}
        - Min Cost: ${c.get('min_cost', 0):,.2f}
        - Max Cost: ${c.get('max_cost', 0):,.2f}
        """
        pdf.add_section("Estimate Cost", section)

    if "interpret_benefits" in results:
        b = results["interpret_benefits"]
        section = f"""
        Coverage: {b.get('coverage', '')}
        Copay: {b.get('copay', '')}
        Summary: {b.get('summary', '')}
        """
        pdf.add_section("Benefit Interpretation", section)

    if "detect_anomalies" in results:
        a = results["detect_anomalies"]
        pdf.add_section("Anomaly Detection", a.get("message", ""))

    if "generate_insights" in results:
        insight = results["generate_insights"].get("insight", "")
        pdf.add_section("Insights", insight)

    return bytes(pdf.output(dest="S"))








