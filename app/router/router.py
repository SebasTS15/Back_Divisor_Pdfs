from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from fastapi.responses import StreamingResponse
from app.service.service import Pdfservice

router = APIRouter()


@router.post('/splitter_pdf')
def splitter_pdf(
    name_pdf: str = Form(),
    pages_splitter: int = Form(), 
    file: UploadFile = File()
    ):

    if file.content_type != 'application/pdf':
        raise HTTPException(status_code=400, detail = 'El archivo debe ser un PDF')
    
    pdf_service = Pdfservice(file)
    
    try:
        new_pdfs  =  pdf_service.splitter_pdf(pages_splitter)
        zip_file = pdf_service.create_zip_pdf(new_pdfs,name_pdf)
        return StreamingResponse(
            zip_file,
            media_type='application/zip',
            headers={
                "Content-Disposition": f'attachment; filename="{name_pdf}.zip"'
                }
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@goruter.get('/estrac_pdf')
def estract_pd():
    pass


