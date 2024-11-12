from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import os

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:80",
    "http://localhost:5173",
    "http://127.0.0.1",
    "http://127.0.0.1:80",
    "http://127.0.0.1:5173",
    # Add more if necessary
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specified origins
    allow_credentials=True,
    allow_methods=["*"],    # Allows all HTTP methods
    allow_headers=["*"],    # Allows all headers
)

# Create a directory to store uploaded images
UPLOAD_DIR = "uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    # Check if the uploaded file is an image
    print('Received file:', file.filename)
    if file.content_type.startswith('image/'):

        file_location = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())

        return {"info": f"file '{file.filename}' saved at '{file_location}'"}

    else:
        raise HTTPException(status_code=400, detail="Invalid file type. Only images are allowed.")
    

@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}