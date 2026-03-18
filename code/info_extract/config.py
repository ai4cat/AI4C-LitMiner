import os
import re
from google import genai

# API Configuration
API_KEY = "GEMINI_API_KEY" 
CLIENT = genai.Client(api_key=API_KEY)

# Path Configuration (Adjust for Cross-Platform)
I_ROOT_DIRECTORY = r"IN_PATH"
OUTPUT_BASE = r"OUT_PATH"

# Final output paths
OUTPUT_FILENAME = os.path.join(OUTPUT_BASE, 'extracted_catalyst_data_aggregated_v9.xlsx')
IMAGE_OUTPUT_DIR = os.path.join(OUTPUT_BASE, 'extracted_images')

# Constants and Keywords
# Keywords to filter out Supplementary Information files based on filename
SI_FILE_KEYWORDS = ["supp", "sup", "si", "supporting", "synthesis_method"]
# Keywords to stop text extraction (filtering out references/bibliography)
REFERENCE_KEYWORDS = ["references", "bibliography", "acknowledgement", "acknowledgments", "author contributions"]

# Processing limits
PAGES_TO_ANALYZE = 6 # Max pages to analyze for experimental data extraction
MAX_TEXT_PAGES = 15  # Max pages to read for full text descriptor analysis

# Regex for string cleaning
CONTROL_CHARS_RE = re.compile(r'[\x00-\x1F]+')
