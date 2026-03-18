import fitz
import pandas as pd
import os
import time

# Import configuration, helpers, and tasks
from config import (
    CLIENT, SI_FILE_KEYWORDS, PAGES_TO_ANALYZE, 
    OUTPUT_FILENAME, IMAGE_OUTPUT_DIR
)
from utils import extract_main_text, pdf_page_to_base64, clean_excel_string
from prompt import analyze_descriptors_from_text, extract_catalyst_data

def process_all_pdfs(root_dir):
    all_catalyst_results = []
    
    # Ensure the image output directory exists
    os.makedirs(IMAGE_OUTPUT_DIR, exist_ok=True)
    print(f"-> Extracted images will be saved to: {IMAGE_OUTPUT_DIR}")

    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            
            if not filename.lower().endswith('.pdf'):
                continue

            # File-level SI filter (efficiently skips whole SI files)
            if any(kw in filename.lower() for kw in SI_FILE_KEYWORDS):
                print(f"--- Skipping File: {filename} (Detected SI filename keyword) ---")
                continue
            
            pdf_path = os.path.join(dirpath, filename)
            print("\n" + "=" * 80)
            print(f"-> Processing File: {pdf_path}")
            
            try:
                doc = fitz.open(pdf_path)
                
                # 1. Task 2: Text Mining (Descriptor Analysis)
                main_text = extract_main_text(doc)
                if not main_text:
                    descriptor_data = {"descriptor_justification": None, "top_co_occurring_pairs": []}
                else:
                    descriptor_data = analyze_descriptors_from_text(main_text, CLIENT)
                    print("    [Descriptor Analysis Complete] Justification generated.")

                
                # 2. Task 1: Multimodal Extraction (Experimental Data)
                doc_name_base = os.path.splitext(filename)[0].replace(' ', '_')
                
                for page_num in range(PAGES_TO_ANALYZE):
                    b64_img = pdf_page_to_base64(doc, page_num)
                    
                    try:
                        data = extract_catalyst_data(b64_img, CLIENT)
                        
                        if data and "catalysts" in data:
                            for item in data["catalysts"]:
                                # Only save if key data (E1/2 or Configuration) was extracted
                                if item.get('E_1_2') is not None or item.get('Configuration') is not None:
                                    
                                    # --- Image Saving Logic ---
                                    img_filename = f"{doc_name_base}_Page_{page_num + 1}.png"
                                    img_save_path = os.path.join(IMAGE_OUTPUT_DIR, img_filename)
                                    
                                    page = doc.load_page(page_num)
                                    # Use a fixed zoom (e.g., 2.0) for consistent image quality
                                    pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0)) 
                                    pix.save(img_save_path)
                                    # --------------------------
                                    
                                    item['File_Path'] = pdf_path.replace(root_dir, '').lstrip(os.sep)
                                    item['Page'] = page_num + 1
                                    item['Image_File'] = img_filename # Record the image file name
                                    item['Descriptor_Analysis'] = descriptor_data.get('descriptor_justification', None)
                                    all_catalyst_results.append(item)
                                    print(f"    -> Data Extracted & Image Saved (Page {page_num+1}): {item.get('System')} | E1/2: {item.get('E_1_2')}")
                    
                    except Exception as e:
                        # Failures in page-level extraction are ignored
                        pass 

                doc.close()

            except Exception as e:
                print(f"-> FATAL ERROR: Failed to open or process file {pdf_path}: {e}")

    # Data Consolidation and Saving
    if all_catalyst_results:
        df_catalyst = pd.DataFrame(all_catalyst_results)
        
        # Aggregation Step: Combine multiple page extractions into one complete record per catalyst
        agg_funcs = {
            'E_1_2': 'max',  # Retain the highest E_1_2 value (best performance)
            # Retain the first non-null value for descriptive fields
            'Configuration': lambda x: x.dropna().iloc[0] if not x.dropna().empty else None, 
            'Structure_Description': lambda x: x.dropna().iloc[0] if not x.dropna().empty else None, 
            'DOI': lambda x: x.dropna().iloc[0] if not x.dropna().empty else None,
            'Descriptor_Analysis': 'first', # Analysis is the same for the whole file
            'Page': 'min', # Keep track of the first page where data was found
            'Image_File': lambda x: sorted(list(set(x.dropna().tolist()))), # Collect all unique, relevant image file names
        }
        
        # Group by File_Path and Catalyst System Name
        df_aggregated = df_catalyst.groupby(['File_Path', 'System'], dropna=False).agg(agg_funcs).reset_index()
        df_final = df_aggregated.rename(columns={'E_1_2': 'E_1_2_Max'})
        
        # --- Apply String Cleaning (Prevents Excel errors) ---
        string_cols = ['System', 'Configuration', 'DOI', 'Structure_Description', 'Descriptor_Analysis']
        for col in string_cols:
            if col in df_final.columns:
                df_final[col] = df_final[col].apply(clean_excel_string)
        
        cols = ['File_Path', 'System', 'E_1_2_Max', 'Configuration', 'DOI', 'Structure_Description', 'Descriptor_Analysis', 'Page', 'Image_File']
        
        # Select and order columns. 
        df_final = df_final[[c for c in cols if c in df_final.columns]]
        
        # Write to Excel
        df_final.to_excel(OUTPUT_FILENAME, index=False)
        
        print("\n" + "=" * 80)
        print(f"Aggregation Complete! Extracted {len(df_final)} unique catalyst records.")
        print(f"Results saved to {OUTPUT_FILENAME}")
        print(f"Associated images saved to: {IMAGE_OUTPUT_DIR}")
        print("=" * 80)
    else:
        print("No valid catalyst experimental data was extracted.")
        