import json
import base64
from google.genai import types

# --- 1. Task 1: Multimodal Extraction (Experimental/Structural Data) ---
def extract_catalyst_data(base64_image, client):
    """Uses Gemini to extract structured experimental data from a page image."""
    
    image_part = types.Part.from_bytes(data=base64.b64decode(base64_image), mime_type='image/png')
    
    system_prompt = "You are a materials science expert specializing in single-atom catalysts (SACs) literature mining. Your task is to accurately extract key catalyst parameters from the provided research paper images."
    
    user_prompt = """
    Analyze the provided research paper page image, which typically contains a performance Table and/or a structural Figure.
    
    Extract the following fields. If the information is not present on the page, fill the field with null:
    1. **System**: The catalyst system name (e.g., Fe SAC/N-C).
    2. **Configuration**: The coordination configuration (e.g., FeN5, MnN3O1).
    3. **E_1_2**: The Half-wave potential value in Volts (V).
    4. **DOI**: The Digital Object Identifier of the paper (if visible).
    5. **Structure_Description**: A single sentence describing the key microscopic structure observed.
    
    Strictly output the results in the following JSON format. E_1_2 must be a number or null; others are strings or null.
    { "catalysts": [ { "System": "...", "Configuration": "...", "E_1_2": "...", "DOI": "...", "Structure_Description": "..." } ] }
    """
    
    contents = [image_part, user_prompt]

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.1,
            response_mime_type="application/json",
            response_schema=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "catalysts": types.Schema(
                        type=types.Type.ARRAY,
                        items=types.Schema(
                            type=types.Type.OBJECT,
                            properties={
                                "System": types.Schema(type=types.Type.STRING),
                                "Configuration": types.Schema(type=types.Type.STRING),
                                "E_1_2": types.Schema(type=types.Type.NUMBER),
                                "DOI": types.Schema(type=types.Type.STRING),
                                "Structure_Description": types.Schema(type=types.Type.STRING),
                            }
                        )
                    )
                }
            )
        )
    )
    return json.loads(response.text)

# --- 2. Task 2: Text Mining (Descriptor Validation and Justification) ---
def analyze_descriptors_from_text(text_content, client):
    """Analyzes the main text once per document to validate and justify the 20 core descriptors."""
    
    system_prompt = """
    You are a leading materials informatics scientist. Your task is to analyze the provided SACs paper text and systematically justify the key physicochemical descriptors that influence O2 adsorption and activation.
    """

    user_prompt = f"""
    Analyze the following main text content extracted from a single-atom catalyst research paper.

    Core Task:
    1. **Co-occurrence Analysis**: Identify the **three** pairs of descriptors most frequently discussed together within the text.
    2. **Importance Justification**: Write a single, concise paragraph (in English, about 70-100 words) that systemically summarizes why the research emphasizes these descriptors across the four dimensions (Structure, Electron, Spin, and Adsorption Thermodynamics) for O2 activation.
    
    20 Core Descriptor Categories (Analyze the concepts corresponding to these groups):
    1. **Intrinsic Electronic Structure & Coordination Environment (X0-X2)**:
        - X0: Phi (Electronegativity-Based Descriptor)
        - X1: Coordination Number
        - X2: Charge of the Central Metal Atom (Before O2 Adsorption)
        
    2. **Pre-Adsorption Spin & Band Structure (X3-X7)**:
        - X3, X4: Magnetic Moment (from OSZICAR & OUTCAR)
        - X5, X6: d-Band Center (Spin-Up & Spin-Down)
        - X7: d-Band Center Gap of Spin State
        
    3. **Post-Adsorption Electronic Restructuring (X8-X13)**:
        - X8: Charge of the Central Metal Atom (After O2 Adsorption)
        - X9, X10: Magnetic Moment (from OSZICAR & OUTCAR, After O2 Adsorption)
        - X11, X12: d-Band Center (Spin-Up & Spin-Down, After O2 Adsorption)
        - X13: d-Band Center Gap of Spin State (After O2 Adsorption)
        
    4. **Geometric & Oxygen Molecular Metrics/Thermodynamics (X14-X19)**:
        - X14: Bond Length of M–O
        - X15: Bond Length of O–O
        - X16, X17: Magnetic Moment of Oxygen Atoms
        - X18: Total Magnetic Moment of O2
        - X19: Adsorption Energy of O2
    
    --- TEXT CONTENT ---
    {text_content[:20000]} 
    ---
    
    Strictly output the results in the following JSON format. If a DOI is not explicitly found, fill with null.
    
    {{
        "DOI_Text_Search": "...",
        "top_co_occurring_pairs": [
            {{"pair": "Coordination Number and d-Band Center", "count_simulation": 5}},
            {{"pair": "...", "count_simulation": 3}}
        ],
        "descriptor_justification_en": "Your conclusive summary paragraph (English)"
    }}
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=[user_prompt],
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.2,
            response_mime_type="application/json",
        )
    )
    return json.loads(response.text)
