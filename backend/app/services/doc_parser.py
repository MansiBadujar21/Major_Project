from __future__ import annotations

import os
import io
from pathlib import Path
import pdfplumber
import fitz  # PyMuPDF
from docx import Document
from pdf2image import convert_from_bytes
import pytesseract
import pandas as pd
import camelot
import tabula
import tempfile
import time


def parse_document(filename: str, content: bytes) -> str:
    suffix = Path(filename).suffix.lower()
    if suffix == ".pdf":
        return _parse_pdf(content)
    if suffix == ".docx":
        return _parse_docx(content)
    if suffix in {".txt", ""}:
        return content.decode("utf-8", errors="ignore")
    raise ValueError(f"Unsupported file type: {suffix}")


def _parse_pdf(content: bytes) -> str:
    text_parts: list[str] = []
    try:
        # Prefer pdfplumber for layout; fallback to PyMuPDF
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            for page in pdf.pages:
                text_parts.append(page.extract_text() or "")
    except Exception:
        with fitz.open(stream=content, filetype="pdf") as doc:
            for page in doc:
                text_parts.append(page.get_text())

    # Table-aware extraction for better accuracy on tabular PDFs
    # Temporarily disabled due to JPype issues
    table_text_parts: list[str] = []
    
    # TODO: Re-enable table extraction once JPype is properly configured
    # try:
    #     # Create temporary file with unique name to avoid conflicts
    #     tmp_fd, tmp_path = tempfile.mkstemp(suffix=".pdf")
    #     os.close(tmp_fd)  # Close the file descriptor
    #     
    #     # Write content to temporary file
    #     with open(tmp_path, 'wb') as tmpf:
    #         tmpf.write(content)
    #         tmpf.flush()
    #     
    #     # Add small delay to ensure file is fully written
    #     time.sleep(0.1)
    #     
    #     # Try Camelot first
    #     try:
    #         tables = camelot.read_pdf(tmp_path, pages="all", flavor="stream")
    #         for t in tables:
    #             df = t.df
    #             if isinstance(df, pd.DataFrame) and not df.empty:
    #                 table_text_parts.append(df.to_csv(index=False))
    #     except Exception as e:
    #         print(f"Camelot table extraction failed: {e}")
    #         pass
    #         
    #     # Try Tabula as fallback
    #     try:
    #         dfs = tabula.read_pdf(tmp_path, pages="all", multiple_tables=True, lattice=True, stream=True)
    #         for df in dfs or []:
    #             if isinstance(df, pd.DataFrame) and not df.empty:
    #                 table_text_parts.append(df.to_csv(index=False))
    #     except Exception as e:
    #         print(f"Tabula table extraction failed: {e}")
    #         pass
    #         
    # except Exception as e:
    #     print(f"Table extraction setup failed: {e}")
    #     pass
    # finally:
    #     # Clean up temporary file
    #     if tmp_path and os.path.exists(tmp_path):
    #         try:
    #             os.unlink(tmp_path)
    #         except Exception as e:
    #             print(f"Failed to clean up temp file {tmp_path}: {e}")

    if table_text_parts:
        text_parts.append("\n".join(table_text_parts))
        
    # If still too little text, try OCR for scanned PDFs with guardrails
    if len("".join(text_parts).strip()) < 50:
        ocr_enabled = os.getenv("OCR_ENABLED", "true").strip().lower() in {"1", "true", "yes"}
        if ocr_enabled:
            dpi = int(os.getenv("OCR_DPI", "200"))
            max_pages = int(os.getenv("OCR_MAX_PAGES", "3"))
            try:
                total_pages = 0
                try:
                    with fitz.open(stream=content, filetype="pdf") as d:
                        total_pages = d.page_count
                except Exception:
                    total_pages = 0
                last_page = max_pages if max_pages > 0 else None
                images = convert_from_bytes(
                    content,
                    dpi=dpi,
                    first_page=1 if last_page else None,
                    last_page=last_page,
                )
                for img in images:
                    text_parts.append(pytesseract.image_to_string(img) or "")
            except Exception:
                # OCR dependencies (poppler/tesseract) may be missing; skip silently
                pass
    return "\n".join(text_parts)


def _parse_docx(content: bytes) -> str:
    bio = io.BytesIO(content)
    doc = Document(bio)
    return "\n".join(p.text for p in doc.paragraphs)


