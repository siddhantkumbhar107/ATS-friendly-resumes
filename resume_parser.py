try:
    from xhtml2pdf import pisa
    from io import BytesIO

    def convert_html_to_pdf(source_html):
        output = BytesIO()
        pisa_status = pisa.CreatePDF(source_html, dest=output)
        if pisa_status.err:
            return None
        return output.getvalue()

except ImportError:
    def convert_html_to_pdf(source_html):
        return None
