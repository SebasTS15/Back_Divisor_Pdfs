from fastapi import APIRouter, File, UploadFile, HTTPException, Query, Form
from fastapi.responses import StreamingResponse
from app.service.service import Pdfservice

router = APIRouter()


@router.post('/splitter_pdf')
def splitter_pdf(
    nuevo_nombre_pdf: str = Form(...),
    paginas_dividir: int = Form(...),
    archivo: UploadFile = File(...)
    ):

    if archivo.content_type != 'application/pdf':
        raise HTTPException(status_code=400, detail = 'El archivo debe ser un PDF')
    
    pdf_service = Pdfservice(archivo)
    
    try:
        new_pdfs  =  pdf_service.splitter_pdf(paginas_dividir)
        zip_file = pdf_service.create_zip_pdf(new_pdfs,nuevo_nombre_pdf)
        return StreamingResponse(
            zip_file,
            media_type='application/zip',
            headers={
                "Content-Disposition": f'attachment; filename="{nuevo_nombre_pdf}.zip"'
                }
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post('/estrac_pdf')
def estract_pd(
    nuevo_nombre_pdf: str = Form(...),
    paginas_estraer: str = Form(...),
    archivo: UploadFile = File(...)
):
    if archivo.content_type != 'application/pdf':
        raise HTTPException(status_code=400, detail= 'El archivo debe ser un PDF')
    
    pdf_service = Pdfservice(archivo)

    try:
        list_pages = pdf_service.convercion_list_pdfs(paginas_estraer)
        new_pdf = pdf_service.estract_and_create_new_pdf(list_pages)
        return StreamingResponse(
            new_pdf,
            media_type='application/pdf',
            headers={
                'Content-Disposition': f'attachment; filename="{nuevo_nombre_pdf}.pdf"'
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


