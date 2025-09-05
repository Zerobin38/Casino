# ocr_reader.py
import requests, io
from PIL import Image
import re

# Put your API key here if you have one (optional).
# You can sign up at https://ocr.space/ for a free API key with rate limits.
OCR_SPACE_API_KEY = ""  # optional: put key string here

def _call_ocr_space(image_bytes):
    url = "https://api.ocr.space/parse/image"
    payload = {
        "isOverlayRequired": False,
        "language": "eng",
        "OCREngine": 2,
    }
    files = {"file": ("image.jpg", image_bytes)}
    headers = {}
    if OCR_SPACE_API_KEY:
        payload["apikey"] = OCR_SPACE_API_KEY
    r = requests.post(url, data=payload, files=files, timeout=30)
    r.raise_for_status()
    return r.json()

def parse_image_with_ocr(streamlit_image):
    # streamlit_image is an UploadedFile or Image object; get bytes
    if hasattr(streamlit_image, "getvalue"):
        img_bytes = streamlit_image.getvalue()
    else:
        # fallback: streamlit camera_input gives object with .read()
        img_bytes = streamlit_image.read()
    resp = _call_ocr_space(img_bytes)
    parsed = []
    try:
        text = ""
        if resp.get("ParsedResults"):
            for pr in resp["ParsedResults"]:
                text += pr.get("ParsedText","") + "\\n"
        # look for numbers 0-36 in the OCR text
        nums = re.findall(r"\\b([0-3]?\\d)\\b", text)
        # filter 0-36
        for s in nums:
            v = int(s)
            if 0 <= v <= 36:
                parsed.append(v)
    except Exception:
        parsed = []
    # return numbers with most-recent-first assumption (OCR often writes newest first if photo shows that)
    return parsed
