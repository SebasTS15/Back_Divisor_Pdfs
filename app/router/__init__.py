from fastapi import APIRouter
from .router import router

router_pdf_service = APIRouter(prefix='/pdf_service', tags=['Splitter/Estract Pdf Service'])
router_pdf_service.include_router(router)

