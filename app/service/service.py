import ast
from io import BytesIO
import zipfile 
from pypdf import PdfReader, PdfWriter
import os


class Pdfservice:

    def __init__(self, file) -> None:
        pdf_file = getattr(file, "file", file)
        pdf_file.seek(0)
        self.pdf = PdfReader(pdf_file)

    def get_title(self):
        return self.pdf.metadata.title if self.pdf.metadata else None
    
    def get_pages(self):
        return len(self.pdf.pages)

    def validate_token(self, token:str):

        if not token:
            raise ValueError('Hay un elemento vacio')
        
        if token.count('-')>1:
            raise ValueError(f"El token '{token}' tiene más de un '-'")

        if '-' in token:
            
            inicio, fin = token.split('-')

            if not inicio.isdigit() or not fin.isdigit():
                raise ValueError(f"El rango '{token}' no es valido")
            if int(fin) > int(inicio):
                raise ValueError (f"El rango del '{token}' está invertido")
        else:

            if not token.isdigit():
                raise ValueError(f"El '{token}' no es un número válido")

    
    def validate_pages_per_pdf(self, pages_per_pdf: int):
        total_pages = self.get_pages()

        if not isinstance(pages_per_pdf, int):
            raise TypeError("El número de páginas por PDF debe ser un entero.")

        if pages_per_pdf <= 0:
            raise ValueError("El número de páginas por PDF debe ser mayor que cero.")

        if pages_per_pdf > total_pages:
            raise ValueError(
                f"El PDF solo tiene {total_pages} páginas y no puede dividirse en bloques de {pages_per_pdf}."
            )

    
    def convercion_list_pdfs(self,text: str):
        
        pages = []

        tokens = text.replace(" ","").split(",")

        for token in tokens:
            
            self.validate_token(token)

            if "-" in token:
                
                inicio, fin = token.split('-')

                for page in range(int(inicio), int(fin) +1 ):

                    pages.append(page)

            else:

                pages.append(int(token))

        return pages

    
    def estract_and_create_new_pdf(self,pages:list[int]):

        for i in range(len(pages)):

            self.validate_pages_per_pdf(pages[i])

        new_pdf = PdfWriter()

        total_pages = len(self.pdf.pages)

        pages = list(dict.fromkeys(pages))

        for page in pages:
            if not 1 <= page <= total_pages:
                raise  ValueError(f'La pagina {page} no existe')
            
            new_pdf.add_page(self.pdf.pages[page - 1])

        output = BytesIO()
        new_pdf.write(output)
        output.seek(0)

        return output
    
    def splitter_pdf(self, pages_per_pdf: int):

        self.validate_pages_per_pdf(pages_per_pdf)

        total_pages = self.get_pages()

        new_pdfs = []

        for start_block in range(1, total_pages + 1, pages_per_pdf ):

            new_pdf = PdfWriter()

            end_block = start_block + pages_per_pdf - 1
            
            if end_block > total_pages:
                end_block = total_pages
                
            for page_current in range(start_block, end_block + 1):

                new_pdf.add_page(self.pdf.pages[page_current -1])

            output = BytesIO()
            new_pdf.write(output)
            output.seek(0)
            new_pdfs.append(output)
        
        return new_pdfs

    def create_zip_pdf(self, new_pdfs: list[BytesIO], name_zip: str):

        memoria_zip = BytesIO()

        with zipfile.ZipFile(memoria_zip,'w',zipfile.ZIP_DEFLATED) as zip_f:
            
            for indice, archivo in enumerate(new_pdfs):

                zip_f.writestr(f'{name_zip}_{indice + 1}.pdf',archivo.getvalue())

        memoria_zip.seek(0)
        
        return memoria_zip


