# import streamlit as st
# import google.generativeai as genai
# from PIL import Image
# import PyPDF2
# import fitz
# import io
# import base64
# import json
# import pandas as pd
# from typing import List, Optional, Dict, Any
# import re
# import uuid
# from datetime import datetime
# import gtts
# import pygame
# import tempfile
# import os

# st.set_page_config(
#     page_title="Using The OCR Multi-Function AI Processor",
#     page_icon="🤖",
#     layout="wide"
# )

# class AIProcessor:
#     def __init__(self, api_key: str):
#         genai.configure(api_key=api_key)
#         self.model = genai.GenerativeModel('gemini-1.5-flash')
#         pygame.mixer.init()
    
#     def captcha_handler(self, source, captcha_type: str = "auto") -> dict:
#         if isinstance(source, bytes):
#             return self._process_pdf_captcha(source, captcha_type)
#         else:
#             return self._process_image_captcha(source, captcha_type)
    
#     def _process_image_captcha(self, image: Image.Image, captcha_type: str) -> dict:
#         prompts = {
#             "alphabetical": "Extract only letters from this CAPTCHA. Format: Text: [letters], Type: alphabetical, Confidence: [High/Medium/Low]",
#             "numerical": "Extract only numbers from this CAPTCHA. Format: Text: [numbers], Type: numerical, Confidence: [High/Medium/Low]",
#             "arithmetic": "Solve this math CAPTCHA. Format: Text: [answer], Expression: [original], Type: arithmetic, Confidence: [High/Medium/Low]",
#             "auto": "Analyze and extract from this CAPTCHA. Format: Text: [result], Type: [type], Confidence: [High/Medium/Low]"
#         }
        
#         try:
#             response = self.model.generate_content([prompts[captcha_type], image])
#             return self._parse_captcha_response(response.text)
#         except Exception as e:
#             return {"error": str(e)}
    
#     def _process_pdf_captcha(self, pdf_bytes: bytes, captcha_type: str) -> List[dict]:
#         results = []
#         doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        
#         for page_num in range(len(doc)):
#             page = doc.load_page(page_num)
#             image_list = page.get_images()
            
#             for img_index, img in enumerate(image_list):
#                 xref = img[0]
#                 pix = fitz.Pixmap(doc, xref)
                
#                 if pix.n - pix.alpha < 4:
#                     img_data = pix.tobytes("png")
#                     pil_image = Image.open(io.BytesIO(img_data))
#                     result = self._process_image_captcha(pil_image, captcha_type)
#                     result['page'] = page_num + 1
#                     result['image_index'] = img_index + 1
#                     results.append(result)
                
#                 pix = None
        
#         doc.close()
#         return results
    
#     def handwritten_extractor(self, source) -> dict:
#         if isinstance(source, bytes):
#             return self._extract_handwritten_pdf(source)
#         else:
#             return self._extract_handwritten_image(source)
    
#     def _extract_handwritten_image(self, image: Image.Image) -> dict:
#         prompt = """Extract all handwritten text from this image. Provide detailed information about each text element found.
#         Format as JSON with fields: text, position, confidence, type, language"""
        
#         try:
#             response = self.model.generate_content([prompt, image])
#             extracted_data = self._parse_handwritten_response(response.text)
            
#             json_result = {
#                 "id": str(uuid.uuid4()),
#                 "timestamp": datetime.now().isoformat(),
#                 "source_type": "image",
#                 "extracted_content": extracted_data
#             }
            
#             return json_result
#         except Exception as e:
#             return {"error": str(e)}
    
#     def _extract_handwritten_pdf(self, pdf_bytes: bytes) -> dict:
#         results = []
#         doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        
#         for page_num in range(len(doc)):
#             page = doc.load_page(page_num)
#             image_list = page.get_images()
            
#             for img_index, img in enumerate(image_list):
#                 xref = img[0]
#                 pix = fitz.Pixmap(doc, xref)
                
#                 if pix.n - pix.alpha < 4:
#                     img_data = pix.tobytes("png")
#                     pil_image = Image.open(io.BytesIO(img_data))
                    
#                     prompt = """Extract all handwritten text from this image. Provide detailed information."""
#                     response = self.model.generate_content([prompt, pil_image])
                    
#                     extracted_data = self._parse_handwritten_response(response.text)
#                     results.append({
#                         "page": page_num + 1,
#                         "image_index": img_index + 1,
#                         "content": extracted_data
#                     })
                
#                 pix = None
        
#         doc.close()
        
#         json_result = {
#             "id": str(uuid.uuid4()),
#             "timestamp": datetime.now().isoformat(),
#             "source_type": "pdf",
#             "total_pages": len(doc),
#             "extracted_content": results
#         }
        
#         return json_result
    
#     def information_extractor(self, source) -> dict:
#         if isinstance(source, bytes):
#             return self._extract_info_pdf(source)
#         else:
#             return self._extract_info_image(source)
    
#     def _extract_info_image(self, image: Image.Image) -> dict:
#         prompt = """Extract all visible information from this image including text, numbers, symbols, objects, layouts, colors, and any other details."""
        
#         try:
#             response = self.model.generate_content([prompt, image])
            
#             info_data = {
#                 "id": str(uuid.uuid4()),
#                 "timestamp": datetime.now().isoformat(),
#                 "source_type": "image",
#                 "extracted_information": {
#                     "text_content": response.text,
#                     "analysis_type": "comprehensive",
#                     "processing_status": "completed"
#                 }
#             }
            
#             return info_data
#         except Exception as e:
#             return {"error": str(e)}
    
#     def _extract_info_pdf(self, pdf_bytes: bytes) -> dict:
#         results = []
#         doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        
#         for page_num in range(len(doc)):
#             page = doc.load_page(page_num)
            
#             text_content = page.get_text()
            
#             image_list = page.get_images()
#             page_images = []
            
#             for img_index, img in enumerate(image_list):
#                 xref = img[0]
#                 pix = fitz.Pixmap(doc, xref)
                
#                 if pix.n - pix.alpha < 4:
#                     img_data = pix.tobytes("png")
#                     pil_image = Image.open(io.BytesIO(img_data))
                    
#                     prompt = """Extract all information from this image."""
#                     response = self.model.generate_content([prompt, pil_image])
                    
#                     page_images.append({
#                         "image_index": img_index + 1,
#                         "extracted_content": response.text
#                     })
                
#                 pix = None
            
#             results.append({
#                 "page": page_num + 1,
#                 "text_content": text_content,
#                 "images": page_images
#             })
        
#         doc.close()
        
#         info_data = {
#             "id": str(uuid.uuid4()),
#             "timestamp": datetime.now().isoformat(),
#             "source_type": "pdf",
#             "total_pages": len(results),
#             "extracted_information": results
#         }
        
#         return info_data
    
#     def captcha_to_voice(self, captcha_text: str, language: str = "en") -> dict:
#         try:
#             tts = gtts.gTTS(text=captcha_text, lang=language, slow=False)
            
#             temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
#             tts.save(temp_audio.name)
            
#             pygame.mixer.music.load(temp_audio.name)
#             pygame.mixer.music.play()
            
#             with open(temp_audio.name, "rb") as audio_file:
#                 audio_data = base64.b64encode(audio_file.read()).decode()
            
#             voice_result = {
#                 "id": str(uuid.uuid4()),
#                 "timestamp": datetime.now().isoformat(),
#                 "input_text": captcha_text,
#                 "language": language,
#                 "audio_format": "mp3",
#                 "audio_data": audio_data,
#                 "file_path": temp_audio.name,
#                 "processing_status": "completed"
#             }
            
#             return voice_result
            
#         except Exception as e:
#             return {"error": str(e)}
#         finally:
#             if 'temp_audio' in locals():
#                 try:
#                     os.unlink(temp_audio.name)
#                 except:
#                     pass
    
#     def _parse_captcha_response(self, response_text: str) -> dict:
#         result = {"text": "", "expression": "", "type": "", "confidence": "", "raw_response": response_text}
        
#         lines = response_text.strip().split('\n')
#         for line in lines:
#             line = line.strip()
#             if line.startswith('Text:'):
#                 result['text'] = line.replace('Text:', '').strip()
#             elif line.startswith('Expression:'):
#                 result['expression'] = line.replace('Expression:', '').strip()
#             elif line.startswith('Type:'):
#                 result['type'] = line.replace('Type:', '').strip()
#             elif line.startswith('Confidence:'):
#                 result['confidence'] = line.replace('Confidence:', '').strip()
        
#         return result
    
#     def _parse_handwritten_response(self, response_text: str) -> dict:
#         try:
#             if response_text.strip().startswith('{'):
#                 return json.loads(response_text)
#             else:
#                 return {
#                     "extracted_text": response_text,
#                     "confidence": "medium",
#                     "type": "handwritten"
#                 }
#         except:
#             return {
#                 "extracted_text": response_text,
#                 "confidence": "medium",
#                 "type": "handwritten"
#             }
    
#     def save_json(self, data: dict, filename: str = None) -> str:
#         if not filename:
#             filename = f"result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
#         json_str = json.dumps(data, indent=2, ensure_ascii=False)
#         return json_str, filename
    
#     def json_to_excel(self, json_data: dict, filename: str = None) -> bytes:
#         if not filename:
#             filename = f"result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
#         def flatten_json(data, prefix=''):
#             items = []
#             if isinstance(data, dict):
#                 for key, value in data.items():
#                     new_key = f"{prefix}.{key}" if prefix else key
#                     if isinstance(value, (dict, list)):
#                         items.extend(flatten_json(value, new_key))
#                     else:
#                         items.append((new_key, value))
#             elif isinstance(data, list):
#                 for i, item in enumerate(data):
#                     new_key = f"{prefix}[{i}]" if prefix else f"item_{i}"
#                     if isinstance(item, (dict, list)):
#                         items.extend(flatten_json(item, new_key))
#                     else:
#                         items.append((new_key, item))
#             else:
#                 items.append((prefix, data))
#             return items
        
#         flattened_data = flatten_json(json_data)
#         df = pd.DataFrame(flattened_data, columns=['Field', 'Value'])
        
#         excel_buffer = io.BytesIO()
#         with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
#             df.to_excel(writer, sheet_name='Extracted_Data', index=False)
        
#         excel_buffer.seek(0)
#         return excel_buffer.getvalue(), filename

# def main():
#     st.title("🤖 Using The OCR Multi-Function AI Processor")
    
#     with st.sidebar:
#         api_key = st.text_input("Gemini API Key", type="password")
#         if not api_key:
#             st.warning("Enter API key")
#             return
        
#         processor = AIProcessor(api_key)
    
#     tab1, tab2, tab3, tab4 = st.tabs(["🔐 CAPTCHA Handler", "✍️ Handwritten Extractor", "📄 Information Extractor", "🔊 CAPTCHA Voice"])
    
#     with tab1:
#         st.header("CAPTCHA Handler")
        
#         captcha_type = st.selectbox("CAPTCHA Type", ["auto", "alphabetical", "numerical", "arithmetic"])
        
#         file_type = st.radio("Upload Type", ["Image", "PDF"])
        
#         if file_type == "Image":
#             image_file = st.file_uploader("Upload CAPTCHA Image", type=["png", "jpg", "jpeg", "gif", "bmp"])
            
#             if image_file and st.button("Process CAPTCHA"):
#                 image = Image.open(image_file)
#                 result = processor.captcha_handler(image, captcha_type)
                
#                 st.json(result)
                
#                 json_str, json_filename = processor.save_json(result)
#                 st.download_button("Download JSON", json_str, json_filename, "application/json")
        
#         else:
#             pdf_file = st.file_uploader("Upload PDF", type=["pdf"])
            
#             if pdf_file and st.button("Process PDF CAPTCHAs"):
#                 pdf_bytes = pdf_file.read()
#                 results = processor.captcha_handler(pdf_bytes, captcha_type)
                
#                 st.json(results)
                
#                 json_str, json_filename = processor.save_json(results)
#                 st.download_button("Download JSON", json_str, json_filename, "application/json")
    
#     with tab2:
#         st.header("Handwritten Text Extractor")
        
#         file_type = st.radio("Upload Type", ["Image", "PDF"], key="handwritten")
        
#         if file_type == "Image":
#             image_file = st.file_uploader("Upload Handwritten Image", type=["png", "jpg", "jpeg", "gif", "bmp"])
            
#             if image_file and st.button("Extract Handwritten Text"):
#                 image = Image.open(image_file)
#                 result = processor.handwritten_extractor(image)
                
#                 st.json(result)
                
#                 json_str, json_filename = processor.save_json(result)
#                 st.download_button("Download JSON", json_str, json_filename, "application/json")
                
#                 excel_data, excel_filename = processor.json_to_excel(result)
#                 st.download_button("Download Excel", excel_data, excel_filename, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        
#         else:
#             pdf_file = st.file_uploader("Upload PDF", type=["pdf"], key="handwritten_pdf")
            
#             if pdf_file and st.button("Extract from PDF"):
#                 pdf_bytes = pdf_file.read()
#                 result = processor.handwritten_extractor(pdf_bytes)
                
#                 st.json(result)
                
#                 json_str, json_filename = processor.save_json(result)
#                 st.download_button("Download JSON", json_str, json_filename, "application/json")
                
#                 excel_data, excel_filename = processor.json_to_excel(result)
#                 st.download_button("Download Excel", excel_data, excel_filename, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
#     with tab3:
#         st.header("Information Extractor")
        
#         file_type = st.radio("Upload Type", ["Image", "PDF"], key="info")
        
#         if file_type == "Image":
#             image_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg", "gif", "bmp"])
            
#             if image_file and st.button("Extract Information"):
#                 image = Image.open(image_file)
#                 result = processor.information_extractor(image)
                
#                 st.json(result)
                
#                 json_str, json_filename = processor.save_json(result)
#                 st.download_button("Download JSON", json_str, json_filename, "application/json")
        
#         else:
#             pdf_file = st.file_uploader("Upload PDF", type=["pdf"], key="info_pdf")
            
#             if pdf_file and st.button("Extract from PDF"):
#                 pdf_bytes = pdf_file.read()
#                 result = processor.information_extractor(pdf_bytes)
                
#                 st.json(result)
                
#                 json_str, json_filename = processor.save_json(result)
#                 st.download_button("Download JSON", json_str, json_filename, "application/json")
    
#     with tab4:
#         st.header("CAPTCHA to Voice")
        
#         captcha_text = st.text_input("Enter CAPTCHA Text")
#         language = st.selectbox("Language", ["en", "es", "fr", "de", "it", "pt", "ru", "ja", "ko", "zh"])
        
#         if captcha_text and st.button("Convert to Voice"):
#             result = processor.captcha_to_voice(captcha_text, language)
            
#             if "error" not in result:
#                 st.success("Voice generated successfully!")
#                 st.json(result)
                
#                 json_str, json_filename = processor.save_json(result)
#                 st.download_button("Download JSON", json_str, json_filename, "application/json")
#             else:
#                 st.error(result["error"])

# if __name__ == "__main__":
#     main()
import streamlit as st
import google.generativeai as genai
from PIL import Image
import PyPDF2
import fitz
import io
import base64
import json
import pandas as pd
from typing import List, Optional, Dict, Any
import re
import uuid
from datetime import datetime
import gtts
import pygame
import tempfile
import os

st.set_page_config(
    page_title="Enhanced OCR Multi-Function AI Processor",
    page_icon="🤖",
    layout="wide"
)

class AIProcessor:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        pygame.mixer.init()
    
    def ocr_extractor(self, source, extraction_type: str = "exact_text") -> dict:
        if isinstance(source, bytes):
            return self._process_pdf_ocr(source, extraction_type)
        else:
            return self._process_image_ocr(source, extraction_type)
    
    def _process_image_ocr(self, image: Image.Image, extraction_type: str) -> dict:
        prompts = {
            "exact_text": """Extract ALL visible text, numbers, symbols, and characters from this image EXACTLY as they appear. 
            Do NOT solve math problems, do NOT interpret content, do NOT add missing parts.
            Return only what you can see written/printed in the image.
            Format: Text: [exact content], Type: exact_text, Confidence: [High/Medium/Low]""",
            
            "alphabetical_only": """Extract ONLY alphabetical letters from this image exactly as they appear.
            Ignore numbers, symbols, and special characters.
            Format: Text: [letters only], Type: alphabetical, Confidence: [High/Medium/Low]""",
            
            "numerical_only": """Extract ONLY numbers and numerical digits from this image exactly as they appear.
            Ignore letters, words, and special characters except mathematical operators if they're part of number expressions.
            Format: Text: [numbers only], Type: numerical, Confidence: [High/Medium/Low]""",
            
            "mathematical_expressions": """Extract mathematical expressions, equations, and formulas EXACTLY as written.
            Do NOT solve them, just extract what's visible. Include all operators, equals signs, parentheses etc.
            Format: Text: [exact expression], Type: mathematical, Confidence: [High/Medium/Low]""",
            
            "mixed_content": """Extract all content from this image preserving the exact format and layout.
            Include text, numbers, symbols, spacing, and line breaks as they appear.
            Format: Text: [complete content], Type: mixed, Confidence: [High/Medium/Low]""",
            
            "handwritten_text": """Extract handwritten text exactly as written, preserving spelling and format.
            Do NOT correct spelling or grammar, extract exactly what's written.
            Format: Text: [handwritten content], Type: handwritten, Confidence: [High/Medium/Low]""",
            
            "printed_text": """Extract printed/typed text exactly as it appears.
            Maintain original formatting, spacing, and layout.
            Format: Text: [printed content], Type: printed, Confidence: [High/Medium/Low]""",
            
            "symbols_special": """Extract symbols, special characters, and non-alphanumeric content.
            Include punctuation, mathematical symbols, currency symbols, etc.
            Format: Text: [symbols], Type: symbols, Confidence: [High/Medium/Low]""",
            
            "structured_data": """Extract structured data like tables, lists, forms exactly as formatted.
            Preserve structure, alignment, and relationships between elements.
            Format: Text: [structured content], Type: structured, Confidence: [High/Medium/Low]""",
            
            "captcha_text": """Extract CAPTCHA text exactly as shown without solving or interpreting.
            Return only the visible characters, letters, or numbers in the CAPTCHA.
            Format: Text: [captcha content], Type: captcha, Confidence: [High/Medium/Low]"""
        }
        
        try:
            response = self.model.generate_content([prompts.get(extraction_type, prompts["exact_text"]), image])
            return self._parse_ocr_response(response.text, extraction_type)
        except Exception as e:
            return {"error": str(e), "extraction_type": extraction_type}
    
    def _process_pdf_ocr(self, pdf_bytes: bytes, extraction_type: str) -> List[dict]:
        results = []
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            
            text_content = page.get_text()
            if text_content.strip():
                results.append({
                    "page": page_num + 1,
                    "content_type": "text",
                    "extracted_content": text_content,
                    "extraction_type": extraction_type
                })
            
            image_list = page.get_images()
            
            for img_index, img in enumerate(image_list):
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                
                if pix.n - pix.alpha < 4:
                    img_data = pix.tobytes("png")
                    pil_image = Image.open(io.BytesIO(img_data))
                    result = self._process_image_ocr(pil_image, extraction_type)
                    result['page'] = page_num + 1
                    result['image_index'] = img_index + 1
                    result['content_type'] = "image"
                    results.append(result)
                
                pix = None
        
        doc.close()
        return results
    
    def captcha_handler(self, source, captcha_type: str = "exact_extraction") -> dict:
        if isinstance(source, bytes):
            return self._process_pdf_captcha(source, captcha_type)
        else:
            return self._process_image_captcha(source, captcha_type)
    
    def _process_image_captcha(self, image: Image.Image, captcha_type: str) -> dict:
        prompts = {
            "exact_extraction": """Extract the CAPTCHA content exactly as it appears. Do NOT solve or interpret.
            Just return what you see written in the image.
            Format: Text: [exact content], Type: exact, Confidence: [High/Medium/Low]""",
            
            "alphabetical": """Extract only the alphabetical letters from this CAPTCHA exactly as they appear.
            Format: Text: [letters], Type: alphabetical, Confidence: [High/Medium/Low]""",
            
            "numerical": """Extract only the numbers from this CAPTCHA exactly as they appear.
            Format: Text: [numbers], Type: numerical, Confidence: [High/Medium/Low]""",
            
            "arithmetic_expression": """Extract the mathematical expression from this CAPTCHA exactly as written.
            Do NOT solve it, just extract what's visible (like 1+2= or 5-3= etc).
            Format: Text: [expression], Type: arithmetic_expression, Confidence: [High/Medium/Low]""",
            
            "mixed_captcha": """Extract all content from this mixed CAPTCHA (letters, numbers, symbols) exactly as shown.
            Format: Text: [complete content], Type: mixed, Confidence: [High/Medium/Low]"""
        }
        
        try:
            response = self.model.generate_content([prompts.get(captcha_type, prompts["exact_extraction"]), image])
            return self._parse_captcha_response(response.text, captcha_type)
        except Exception as e:
            return {"error": str(e), "captcha_type": captcha_type}
    
    def _process_pdf_captcha(self, pdf_bytes: bytes, captcha_type: str) -> List[dict]:
        results = []
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            image_list = page.get_images()
            
            for img_index, img in enumerate(image_list):
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                
                if pix.n - pix.alpha < 4:
                    img_data = pix.tobytes("png")
                    pil_image = Image.open(io.BytesIO(img_data))
                    result = self._process_image_captcha(pil_image, captcha_type)
                    result['page'] = page_num + 1
                    result['image_index'] = img_index + 1
                    results.append(result)
                
                pix = None
        
        doc.close()
        return results
    
    def handwritten_extractor(self, source) -> dict:
        if isinstance(source, bytes):
            return self._extract_handwritten_pdf(source)
        else:
            return self._extract_handwritten_image(source)
    
    def _extract_handwritten_image(self, image: Image.Image) -> dict:
        prompt = """Extract all handwritten text from this image EXACTLY as written.
        Do NOT correct spelling, grammar, or formatting. Return exactly what you see written.
        Preserve line breaks, spacing, and layout as much as possible.
        Format the response as JSON with these fields: 
        - extracted_text: the exact handwritten content
        - confidence: High/Medium/Low
        - layout_preserved: true/false
        - notes: any relevant observations about the handwriting"""
        
        try:
            response = self.model.generate_content([prompt, image])
            extracted_data = self._parse_handwritten_response(response.text)
            
            json_result = {
                "id": str(uuid.uuid4()),
                "timestamp": datetime.now().isoformat(),
                "source_type": "image",
                "extraction_type": "handwritten_exact",
                "extracted_content": extracted_data
            }
            
            return json_result
        except Exception as e:
            return {"error": str(e)}
    
    def _extract_handwritten_pdf(self, pdf_bytes: bytes) -> dict:
        results = []
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            image_list = page.get_images()
            
            for img_index, img in enumerate(image_list):
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                
                if pix.n - pix.alpha < 4:
                    img_data = pix.tobytes("png")
                    pil_image = Image.open(io.BytesIO(img_data))
                    
                    prompt = """Extract handwritten content exactly as written, no corrections or interpretations."""
                    response = self.model.generate_content([prompt, pil_image])
                    
                    extracted_data = self._parse_handwritten_response(response.text)
                    results.append({
                        "page": page_num + 1,
                        "image_index": img_index + 1,
                        "content": extracted_data
                    })
                
                pix = None
        
        doc.close()
        
        json_result = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "source_type": "pdf",
            "extraction_type": "handwritten_exact",
            "total_pages": len(doc),
            "extracted_content": results
        }
        
        return json_result
    
    def information_extractor(self, source, extraction_mode: str = "comprehensive") -> dict:
        if isinstance(source, bytes):
            return self._extract_info_pdf(source, extraction_mode)
        else:
            return self._extract_info_image(source, extraction_mode)
    
    def _extract_info_image(self, image: Image.Image, extraction_mode: str) -> dict:
        prompts = {
            "comprehensive": """Extract ALL visible information from this image exactly as it appears.
            Include text, numbers, symbols, layouts, colors, objects, and any other details.
            Do NOT interpret or solve anything, just describe what you see.""",
            
            "text_only": """Extract only text content from this image exactly as written.""",
            
            "structured_data": """Extract structured information like tables, forms, lists exactly as formatted.""",
            
            "visual_elements": """Describe visual elements, layouts, colors, and non-text content."""
        }
        
        try:
            response = self.model.generate_content([prompts.get(extraction_mode, prompts["comprehensive"]), image])
            
            info_data = {
                "id": str(uuid.uuid4()),
                "timestamp": datetime.now().isoformat(),
                "source_type": "image",
                "extraction_mode": extraction_mode,
                "extracted_information": {
                    "content": response.text,
                    "processing_status": "completed"
                }
            }
            
            return info_data
        except Exception as e:
            return {"error": str(e)}
    
    def _extract_info_pdf(self, pdf_bytes: bytes, extraction_mode: str) -> dict:
        results = []
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            
            text_content = page.get_text()
            
            image_list = page.get_images()
            page_images = []
            
            for img_index, img in enumerate(image_list):
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                
                if pix.n - pix.alpha < 4:
                    img_data = pix.tobytes("png")
                    pil_image = Image.open(io.BytesIO(img_data))
                    
                    prompt = f"Extract information from this image using {extraction_mode} mode. Return exact content as visible."
                    response = self.model.generate_content([prompt, pil_image])
                    
                    page_images.append({
                        "image_index": img_index + 1,
                        "extracted_content": response.text
                    })
                
                pix = None
            
            results.append({
                "page": page_num + 1,
                "text_content": text_content,
                "images": page_images
            })
        
        doc.close()
        
        info_data = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "source_type": "pdf",
            "extraction_mode": extraction_mode,
            "total_pages": len(results),
            "extracted_information": results
        }
        
        return info_data
    
    def captcha_to_voice(self, captcha_text: str, language: str = "en") -> dict:
        try:
            tts = gtts.gTTS(text=captcha_text, lang=language, slow=False)
            
            temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tts.save(temp_audio.name)
            
            pygame.mixer.music.load(temp_audio.name)
            pygame.mixer.music.play()
            
            with open(temp_audio.name, "rb") as audio_file:
                audio_data = base64.b64encode(audio_file.read()).decode()
            
            voice_result = {
                "id": str(uuid.uuid4()),
                "timestamp": datetime.now().isoformat(),
                "input_text": captcha_text,
                "language": language,
                "audio_format": "mp3",
                "audio_data": audio_data,
                "file_path": temp_audio.name,
                "processing_status": "completed"
            }
            
            return voice_result
            
        except Exception as e:
            return {"error": str(e)}
        finally:
            if 'temp_audio' in locals():
                try:
                    os.unlink(temp_audio.name)
                except:
                    pass
    
    def _parse_ocr_response(self, response_text: str, extraction_type: str) -> dict:
        result = {
            "extracted_text": "",
            "extraction_type": extraction_type,
            "confidence": "",
            "raw_response": response_text
        }
        
        lines = response_text.strip().split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('Text:'):
                result['extracted_text'] = line.replace('Text:', '').strip()
            elif line.startswith('Confidence:'):
                result['confidence'] = line.replace('Confidence:', '').strip()
        
        if not result['extracted_text']:
            result['extracted_text'] = response_text.strip()
        
        return result
    
    def _parse_captcha_response(self, response_text: str, captcha_type: str) -> dict:
        result = {
            "extracted_text": "",
            "captcha_type": captcha_type,
            "confidence": "",
            "raw_response": response_text
        }
        
        lines = response_text.strip().split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('Text:'):
                result['extracted_text'] = line.replace('Text:', '').strip()
            elif line.startswith('Confidence:'):
                result['confidence'] = line.replace('Confidence:', '').strip()
        
        if not result['extracted_text']:
            result['extracted_text'] = response_text.strip()
        
        return result
    
    def _parse_handwritten_response(self, response_text: str) -> dict:
        try:
            if response_text.strip().startswith('{'):
                return json.loads(response_text)
            else:
                return {
                    "extracted_text": response_text,
                    "confidence": "medium",
                    "type": "handwritten_exact"
                }
        except:
            return {
                "extracted_text": response_text,
                "confidence": "medium",
                "type": "handwritten_exact"
            }
    
    def save_json(self, data: dict, filename: str = None) -> str:
        if not filename:
            filename = f"ocr_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        return json_str, filename
    
    def json_to_excel(self, json_data: dict, filename: str = None) -> bytes:
        if not filename:
            filename = f"ocr_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        def flatten_json(data, prefix=''):
            items = []
            if isinstance(data, dict):
                for key, value in data.items():
                    new_key = f"{prefix}.{key}" if prefix else key
                    if isinstance(value, (dict, list)):
                        items.extend(flatten_json(value, new_key))
                    else:
                        items.append((new_key, value))
            elif isinstance(data, list):
                for i, item in enumerate(data):
                    new_key = f"{prefix}[{i}]" if prefix else f"item_{i}"
                    if isinstance(item, (dict, list)):
                        items.extend(flatten_json(item, new_key))
                    else:
                        items.append((new_key, item))
            else:
                items.append((prefix, data))
            return items
        
        flattened_data = flatten_json(json_data)
        df = pd.DataFrame(flattened_data, columns=['Field', 'Value'])
        
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='OCR_Results', index=False)
        
        excel_buffer.seek(0)
        return excel_buffer.getvalue(), filename

def main():
    st.title("🤖 Enhanced OCR Multi-Function AI Processor")
    st.markdown("### Extract text exactly as it appears - No interpretation or solving")
    
    with st.sidebar:
        api_key = st.text_input("Gemini API Key", type="password")
        if not api_key:
            st.warning("Enter API key to continue")
            return
        
        processor = AIProcessor(api_key)
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔤 OCR Extractor", "🔐 CAPTCHA Handler", "✍️ Handwritten Extractor", "📄 Information Extractor", "🔊 Text to Voice"])
    
    with tab1:
        st.header("OCR Text Extractor")
        st.markdown("Extract text exactly as it appears in images or PDFs")
        
        extraction_type = st.selectbox("Extraction Type", [
            "exact_text", "alphabetical_only", "numerical_only", 
            "mathematical_expressions", "mixed_content", "handwritten_text",
            "printed_text", "symbols_special", "structured_data", "captcha_text"
        ])
        
        file_type = st.radio("Upload Type", ["Image", "PDF"], key="ocr_file_type")
        
        if file_type == "Image":
            image_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg", "gif", "bmp"], key="ocr_image_uploader")
            
            if image_file:
                st.image(image_file, caption="Uploaded Image", use_column_width=True)
                
                if st.button("Extract Text", key="ocr_extract_btn"):
                    image = Image.open(image_file)
                    result = processor.ocr_extractor(image, extraction_type)
                    
                    if "error" not in result:
                        st.success("Text extracted successfully!")
                        st.json(result)
                        
                        json_str, json_filename = processor.save_json(result)
                        st.download_button("Download JSON", json_str, json_filename, "application/json", key="ocr_download_json")
                    else:
                        st.error(f"Error: {result['error']}")
        
        else:
            pdf_file = st.file_uploader("Upload PDF", type=["pdf"], key="ocr_pdf_uploader")
            
            if pdf_file and st.button("Extract from PDF", key="ocr_pdf_extract_btn"):
                pdf_bytes = pdf_file.read()
                results = processor.ocr_extractor(pdf_bytes, extraction_type)
                
                st.success("PDF processed successfully!")
                st.json(results)
                
                json_str, json_filename = processor.save_json(results)
                st.download_button("Download JSON", json_str, json_filename, "application/json", key="ocr_pdf_download_json")
    
    with tab2:
        st.header("CAPTCHA Handler")
        st.markdown("Extract CAPTCHA content exactly as shown")
        
        captcha_type = st.selectbox("CAPTCHA Type", [
            "exact_extraction", "alphabetical", "numerical", 
            "arithmetic_expression", "mixed_captcha"
        ])
        
        file_type = st.radio("Upload Type", ["Image", "PDF"], key="captcha_file_type")
        
        if file_type == "Image":
            image_file = st.file_uploader("Upload CAPTCHA Image", type=["png", "jpg", "jpeg", "gif", "bmp"], key="captcha_image_uploader")
            
            if image_file:
                st.image(image_file, caption="CAPTCHA Image", use_column_width=True)
                
                if st.button("Process CAPTCHA", key="captcha_process_btn"):
                    image = Image.open(image_file)
                    result = processor.captcha_handler(image, captcha_type)
                    
                    if "error" not in result:
                        st.success("CAPTCHA processed successfully!")
                        st.json(result)
                        
                        json_str, json_filename = processor.save_json(result)
                        st.download_button("Download JSON", json_str, json_filename, "application/json", key="captcha_download_json")
                    else:
                        st.error(f"Error: {result['error']}")
        
        else:
            pdf_file = st.file_uploader("Upload PDF", type=["pdf"], key="captcha_pdf_uploader")
            
            if pdf_file and st.button("Process PDF CAPTCHAs", key="captcha_pdf_process_btn"):
                pdf_bytes = pdf_file.read()
                results = processor.captcha_handler(pdf_bytes, captcha_type)
                
                st.success("PDF CAPTCHAs processed!")
                st.json(results)
                
                json_str, json_filename = processor.save_json(results)
                st.download_button("Download JSON", json_str, json_filename, "application/json", key="captcha_pdf_download_json")
    
    with tab3:
        st.header("Handwritten Text Extractor")
        st.markdown("Extract handwritten text exactly as written")
        
        file_type = st.radio("Upload Type", ["Image", "PDF"], key="handwritten_file_type")
        
        if file_type == "Image":
            image_file = st.file_uploader("Upload Handwritten Image", type=["png", "jpg", "jpeg", "gif", "bmp"], key="handwritten_image_uploader")
            
            if image_file:
                st.image(image_file, caption="Handwritten Image", use_column_width=True)
                
                if st.button("Extract Handwritten Text", key="handwritten_extract_btn"):
                    image = Image.open(image_file)
                    result = processor.handwritten_extractor(image)
                    
                    if "error" not in result:
                        st.success("Handwritten text extracted!")
                        st.json(result)
                        
                        json_str, json_filename = processor.save_json(result)
                        st.download_button("Download JSON", json_str, json_filename, "application/json", key="handwritten_download_json")
                        
                        excel_data, excel_filename = processor.json_to_excel(result)
                        st.download_button("Download Excel", excel_data, excel_filename, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", key="handwritten_download_excel")
                    else:
                        st.error(f"Error: {result['error']}")
        
        else:
            pdf_file = st.file_uploader("Upload PDF", type=["pdf"], key="handwritten_pdf_uploader")
            
            if pdf_file and st.button("Extract from PDF", key="handwritten_pdf_extract_btn"):
                pdf_bytes = pdf_file.read()
                result = processor.handwritten_extractor(pdf_bytes)
                
                if "error" not in result:
                    st.success("PDF handwritten text extracted!")
                    st.json(result)
                    
                    json_str, json_filename = processor.save_json(result)
                    st.download_button("Download JSON", json_str, json_filename, "application/json", key="handwritten_pdf_download_json")
                    
                    excel_data, excel_filename = processor.json_to_excel(result)
                    st.download_button("Download Excel", excel_data, excel_filename, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", key="handwritten_pdf_download_excel")
                else:
                    st.error(f"Error: {result['error']}")
    
    with tab4:
        st.header("Information Extractor")
        st.markdown("Extract comprehensive information from images or PDFs")
        
        extraction_mode = st.selectbox("Extraction Mode", [
            "comprehensive", "text_only", "structured_data", "visual_elements"
        ])
        
        file_type = st.radio("Upload Type", ["Image", "PDF"], key="info_file_type")
        
        if file_type == "Image":
            image_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg", "gif", "bmp"], key="info_image_uploader")
            
            if image_file:
                st.image(image_file, caption="Image for Information Extraction", use_column_width=True)
                
                if st.button("Extract Information", key="info_extract_btn"):
                    image = Image.open(image_file)
                    result = processor.information_extractor(image, extraction_mode)
                    
                    if "error" not in result:
                        st.success("Information extracted successfully!")
                        st.json(result)
                        
                        json_str, json_filename = processor.save_json(result)
                        st.download_button("Download JSON", json_str, json_filename, "application/json", key="info_download_json")
                    else:
                        st.error(f"Error: {result['error']}")
        
        else:
            pdf_file = st.file_uploader("Upload PDF", type=["pdf"], key="info_pdf_uploader")
            
            if pdf_file and st.button("Extract from PDF", key="info_pdf_extract_btn"):
                pdf_bytes = pdf_file.read()
                result = processor.information_extractor(pdf_bytes, extraction_mode)
                
                if "error" not in result:
                    st.success("PDF information extracted!")
                    st.json(result)
                    
                    json_str, json_filename = processor.save_json(result)
                    st.download_button("Download JSON", json_str, json_filename, "application/json", key="info_pdf_download_json")
                else:
                    st.error(f"Error: {result['error']}")
    
    with tab5:
        st.header("Text to Voice Converter")
        st.markdown("Convert extracted text to speech")
        
      
        
        text_input = st.text_area("Enter Text to Convert", height=100)
        language = st.selectbox("Language", [
            "en", "es", "fr", "de", "it", "pt", "ru", "ja", "ko", "zh",
            "ar", "hi", "bn", "ur", "ta", "te", "ml", "kn", "gu", "pa"
        ])
        
        if text_input and st.button("Convert to Voice"):
            result = processor.captcha_to_voice(text_input, language)
            
            if "error" not in result:
                st.success("Voice generated successfully!")
                st.json(result)
                
                json_str, json_filename = processor.save_json(result)
                st.download_button("Download JSON", json_str, json_filename, "application/json")
            else:
                st.error(f"Error: {result['error']}")

if __name__ == "__main__":
    main()