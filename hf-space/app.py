"""
  Docling REST API — Hugging Face Spaces deployment
  FastAPI wrapper around DocumentConverter with Swagger UI.
  """
  from __future__ import annotations
  import os
  import tempfile
  from pathlib import Path
  from typing import Literal

  import httpx
  from docling.document_converter import DocumentConverter
  from fastapi import FastAPI, File, Form, HTTPException, UploadFile
  from fastapi.responses import RedirectResponse

  app = FastAPI(
      title="Docling API",
      description="Convert PDF, DOCX, PPTX, HTML and more to Markdown / plain text via Docling.",
      version="1.0.0",
  )

  _converter: DocumentConverter | None = None


  def get_converter() -> DocumentConverter:
      global _converter
      if _converter is None:
          _converter = DocumentConverter()
      return _converter


  @app.get("/", include_in_schema=False)
  async def root():
      return RedirectResponse(url="/docs")


  @app.get("/health")
  async def health():
      return {"status": "ok"}


  @app.post("/convert")
  async def convert_file(
      file: UploadFile = File(..., description="Document to convert (PDF, DOCX, PPTX, HTML…)"),
      format: Literal["markdown", "text", "json"] = Form("markdown"),
  ):
      """Upload a document and receive its content as Markdown, plain text, or JSON.
      Handles scanned PDFs via OCR automatically."""
      data = await file.read()
      suffix = Path(file.filename or "upload").suffix or ".pdf"
      with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
          tmp.write(data)
          tmp_path = tmp.name
      try:
          result = get_converter().convert(tmp_path)
          doc = result.document
          if format == "json":
              return {"content": doc.export_to_dict(), "format": "json"}
          return {"content": doc.export_to_markdown(), "format": format}
      except Exception as exc:
          raise HTTPException(status_code=422, detail=str(exc)) from exc
      finally:
          os.unlink(tmp_path)


  @app.post("/convert-url")
  async def convert_url(
      url: str = Form(..., description="Public URL of the document"),
      format: Literal["markdown", "text", "json"] = Form("markdown"),
  ):
      """Provide a public URL to a document and receive its content."""
      try:
          async with httpx.AsyncClient(follow_redirects=True, timeout=60) as client:
              resp = await client.get(url)
              resp.raise_for_status()
      except Exception as exc:
          raise HTTPException(status_code=400, detail=f"Could not fetch URL: {exc}") from exc
      suffix = Path(url.split("?")[0]).suffix or ".pdf"
      with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
          tmp.write(resp.content)
          tmp_path = tmp.name
      try:
          result = get_converter().convert(tmp_path)
          doc = result.document
          if format == "json":
              return {"content": doc.export_to_dict(), "format": "json"}
          return {"content": doc.export_to_markdown(), "format": format}
      except Exception as exc:
          raise HTTPException(status_code=422, detail=str(exc)) from exc
      finally:
          os.unlink(tmp_path)
  