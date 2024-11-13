from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import pytesseract
from PIL import Image
import cv2 
import numpy as np

from io import BytesIO
import os
import time
import re
import requests

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:80",
    "http://localhost:5173",
    "http://127.0.0.1",
    "http://127.0.0.1:80",
    "http://127.0.0.1:5173",
]
valid_req_types = {"text", "url"}

# CORS middleware, should probably remove at some point...
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory to save uploaded images
UPLOAD_DIR = "uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# OCR set up
tesseract_path = "/usr/bin/tesseract"
def preprocess_image_for_ocr(image):
    """
    Preprocesses an image for OCR by converting to grayscale, denoising, thresholding,
    resizing, and enhancing edges.

    Parameters:
    - image (PIL.Image): Input image in RGB format.

    Returns:
    - preprocessed_img (PIL.Image): Processed image suitable for OCR.
    """
    # Convert PIL Image to OpenCV format (numpy array)
    open_cv_image = np.array(image)
    open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)

    # Convert to grayscale
    gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian Blur to remove noise
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)

    # Apply Otsu's thresholding
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Resize the image to increase OCR accuracy (e.g., 150%)
    scale_percent = 150  # Scaling factor
    width = int(thresh.shape[1] * scale_percent / 100)
    height = int(thresh.shape[0] * scale_percent / 100)
    resized = cv2.resize(thresh, (width, height), interpolation=cv2.INTER_LINEAR)

    # Convert back to PIL Image for compatibility with Tesseract or other OCR tools
    preprocessed_img = Image.fromarray(resized)

    return preprocessed_img

# Extract URLs
def extract_urls(text):
    """
    Extracts all URLs from the given text string.

    Parameters:
        text (str): The string containing URLs.

    Returns:
        list: A list of URLs found in the text.
    """
    # Define the regex pattern for URLs
    url_pattern = re.compile(
        r'(https?://\S+|www\.\S+)',
        re.IGNORECASE
    )
    
    # Find all URLs using the regex pattern
    urls = re.findall(url_pattern, text)
    
    return urls

# Validate URLs
def validate_urls(urls):
    """
    Checks each URL in the list to see if it returns an HTTP error.

    Parameters:
        urls (list): A list of URLs to check.

    Returns:
        list:  A list of valid URLs.
    """
    valid = []
    failed = []
    headers = {'User-Agent': 'Mozilla/5.0'}  # To mimic a real browser request

    for url in urls:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                valid.append(url)
            else:
                failed.append(url)
        except requests.exceptions.RequestException as e:
            failed.append(url)

    return valid

@app.post("/upload")
async def upload_image(file: UploadFile = File(...), type: str = Form(...)):
    # Check if the uploaded file is an image
    print('Received file:', file.filename)
    print('Job type:', type)
    process_start = time.time()
    if file.content_type.startswith('image/') and type in valid_req_types:
        try:
            image_data = await file.read()
            img = Image.open(BytesIO(image_data)).convert('RGB')

            img = preprocess_image_for_ocr(img)
            extracted_text = pytesseract.image_to_string(img)
            print("Processing time:", time.time() - process_start)

            if type == 'url':
                urls = extract_urls(extracted_text)
                valid_urls = validate_urls(urls)
                return JSONResponse(content={
                    "urls": valid_urls
                })
            elif type == 'text':
                return JSONResponse(content={
                    "text": extracted_text
                })
        except Exception as e:
            return JSONResponse(content={"error": str(e)}, status_code=500)
    else:
        raise HTTPException(status_code=400, detail="Invalid file or request type.")



@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}