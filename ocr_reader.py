import easyocr
import numpy as np
import cv2
from PIL import Image

# Initialiser le modèle EasyOCR (langue = anglais + chiffres)
reader = easyocr.Reader(['en'], gpu=False)

def parse_image_with_ocr(image_file):
    """
    Lit une image (photo de la roulette) et extrait le texte avec EasyOCR.
    """
    try:
        # Charger l'image en format PIL
        image = Image.open(image_file).convert("RGB")

        # Convertir en tableau numpy
        img_array = np.array(image)

        # Convertir en BGR pour OpenCV
        img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

        # OCR avec EasyOCR
        results = reader.readtext(img_bgr)

        # Extraire juste le texte reconnu
        extracted_texts = [res[1] for res in results]

        return " ".join(extracted_texts)

    except Exception as e:
        return f"Erreur OCR : {e}"
