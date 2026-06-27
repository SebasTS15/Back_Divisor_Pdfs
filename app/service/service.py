from pypdf import PdfReader, PdfWriter


class Pdfservice:

    def __init__(self, file) -> None:
        self.pdf = PdfReader(file)

    @classmethod
    def get_title(self):
        return self.pdf.metadata.title

