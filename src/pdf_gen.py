import os
from fpdf import FPDF

class PDFGenerator:
    def generate(self, md_content, output_path):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        for line in md_content.split("\n"):
            if line.startswith("# "):
                pdf.set_font("Helvetica", "B", 18)
                pdf.multi_cell(0, 10, line[2:])
                pdf.ln(2)
            elif line.startswith("## "):
                pdf.set_font("Helvetica", "B", 14)
                pdf.multi_cell(0, 8, line[3:])
                pdf.ln(1)
            elif line.startswith("### "):
                pdf.set_font("Helvetica", "B", 12)
                pdf.multi_cell(0, 7, line[4:])
            elif line.startswith("- ") or line.startswith("* "):
                pdf.set_font("Helvetica", "", 11)
                pdf.multi_cell(0, 7, f"  • {line[2:]}")
            elif line.startswith("**") and line.endswith("**"):
                pdf.set_font("Helvetica", "B", 11)
                pdf.multi_cell(0, 7, line.strip("*"))
            elif line.strip() == "":
                pdf.ln(3)
            else:
                pdf.set_font("Helvetica", "", 11)
                pdf.multi_cell(0, 7, line)

        pdf.output(output_path)
        return output_path
