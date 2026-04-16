import markdown
from weasyprint import HTML
import os

class PDFGenerator:
    def generate(self, md_content, output_path):
        """
        Converts Markdown content to a PDF file.
        """
        # Convert Markdown to HTML
        html_content = markdown.markdown(md_content, extensions=['extra', 'smarty'])
        
        # Add some basic styling
        styled_html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: 'Helvetica', 'Arial', sans-serif; line-height: 1.6; color: #333; margin: 2cm; }}
                h1 {{ color: #d32f2f; border-bottom: 2px solid #d32f2f; padding-bottom: 10px; }}
                h2 {{ color: #1976d2; margin-top: 30px; border-bottom: 1px solid #ccc; }}
                ul {{ margin-bottom: 20px; }}
                li {{ margin-bottom: 10px; }}
                blockquote {{ font-style: italic; color: #555; border-left: 5px solid #ccc; padding-left: 15px; }}
                p {{ margin-bottom: 15px; text-align: justify; }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        # Generate PDF
        HTML(string=styled_html).write_pdf(output_path)
        return output_path

if __name__ == "__main__":
    # Test stub
    gen = PDFGenerator()
    test_md = """
# Test Summary
## Narrative Summary
This is a test summary. It should look nice in a PDF.
Second paragraph of the narrative.
## Key Points
- Point 1
- Point 2
## Notable Quotes
- "Hello world" (00:01)
    """
    gen.generate(test_md, "test_summary.pdf")
    print("Generated test_summary.pdf")
