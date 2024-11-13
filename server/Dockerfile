FROM python:3.10

WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Update package lists and install tesseract-ocr
RUN apt-get update && apt-get install -y tesseract-ocr
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# Copy the rest of your app's source code
COPY . .

# Expose port 8000
EXPOSE 8000

# Start the FastAPI app using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
