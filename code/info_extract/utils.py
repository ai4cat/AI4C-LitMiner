import fitz
import base64
import pandas as pd
import os
import re
from config import CONTROL_CHARS_RE, REFERENCE_KEYWORDS, MAX_TEXT_PAGES

# --- 1. String Cleaning Function (For Excel Writing) ---
def clean_excel_string(text):
    """
    Removes illegal control characters from strings to prevent Pandas/Excel writing errors.
    """
    if pd.isna(text) or text is None:
        return text
    if isinstance(text, str):
        # 1. Remove control characters (fixes IllegalCharacterError)
        text = CONTROL_CHARS_RE.sub('', text)
        # 2. Clean leading/trailing whitespace
        text = text.strip()
        return text
    return text

# --- 2. PDF Page to Base64 Image (For Multimodal Input) ---
def pdf_page_to_base64(doc, page_number, zoom=2.0):
    """Converts a specific PDF page to a base64 encoded PNG image."""
    if page_number >= len(doc):
        return None
    
    page = doc.load_page(page_number)
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    
    img_data = pix.tobytes("png")
    base64_str = base64.b64encode(img_data).decode("utf-8")
    return base64_str

# --- 3. Extract Main Text Content (Filtering References) ---
def extract_main_text(doc):
    """
    Extracts main text content from the PDF, stopping when reference keywords are detected.
    """
    full_text = []
    max_pages_to_read = min(len(doc), MAX_TEXT_PAGES) 
    
    for page_num in range(max_pages_to_read):
        page = doc.load_page(page_num)
        text = page.get_text("text").lower()
        
        # Check for stop keywords
        if any(keyword in text for keyword in REFERENCE_KEYWORDS):
            print(f"    [Text Extraction Stopped] Detected reference keyword on Page {page_num + 1}.")
            break 
        
        full_text.append(text)
        
    return "\n".join(full_text)
