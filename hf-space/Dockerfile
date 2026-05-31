FROM python:3.11-slim

  WORKDIR /app

  RUN apt-get update && apt-get install -y --no-install-recommends \
      poppler-utils \
      tesseract-ocr \
      libgl1 \
      libglib2.0-0 \
      && rm -rf /var/lib/apt/lists/*

  COPY hf-space/requirements.txt .
  RUN pip install --no-cache-dir -r requirements.txt

  # Pre-download models at build time so cold starts are instant
  RUN python -c "from docling.document_converter import DocumentConverter; DocumentConverter()"

  COPY hf-space/app.py .

  EXPOSE 7860

  CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
  