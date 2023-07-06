from fastapi import APIRouter, Response, Query
from fitz import Font

from source.exceptions.font_exceptions import validate_font, FontException
from source.models.Arabic_Fonts.fonts import fonts, FontEnum
from source.services.doc_generation_service import Aradocgen

router = APIRouter()



@router.post("/generate-doc",
             description="Generate a PDF document with the specified font type, number of pages, font size, and Wiki URL.")
async def generate_document(
        font_type: FontEnum = Query(..., description="Font type"),
        n_pages: int = Query(10, description="Number of pages"),
        font_size: int = Query(12, description="Font size (greater than 10 and less than 20)", gt=10, lt=20),
        url: str = Query(..., description="URL of the Wikipedia article")
):
    try:
        selected_font = Font(fontfile=fonts.get(font_type.name))
    except KeyError as e:
        return Response(
            content=str(e),
            media_type="text/plain",
            status_code=400
        )
    try:
        pdf_buffer = Aradocgen().generate_pdf(selected_font, url, n_pages, font_size)
        return Response(
            content=pdf_buffer.getvalue(),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={font_type.name}_{font_size}_{n_pages}.pdf"},
        )
    #fstring
    except FontException as e:
        return Response(
            content=str(e),
            media_type="text/plain",
            status_code=400
        )


@router.get("/get-available", description="Get the available font types.")
async def get_available_types():
    return Aradocgen().get_available()


@router.get("/extract-content", description="Extract content from a given URL.")
async def extract_content(
        url: str = Query(..., description="URL")
):
    return Aradocgen().extract_content_from_website(url)
