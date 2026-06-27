from pypdf import PdfReader, PdfWriter


class Pdfservice:

    def __init__(self, file) -> None:
        self.pdf = PdfReader(file)
        self.new = PdfWriter()

    def get_title(self):
        return self.pdf.metadata.title if self.pdf.metadata else None
    
    def get_pages(self):
        return len(self.pdf.pages) 

    def estract_page_pdf(self, page):
        input_page = self.pdf.pages[page]
        return self.new.add_page(input_page)

    

