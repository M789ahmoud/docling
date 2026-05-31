---
  title: Docling API
  emoji: 📄
  colorFrom: blue
  colorTo: indigo
  sdk: docker
  app_port: 7860
  pinned: false
  license: mit
  ---

  # Docling REST API

  Free, permanent document conversion API powered by [Docling](https://github.com/DS4SD/docling).

  ## Endpoints

  | Method | Path | Description |
  |--------|------|-------------|
  | GET | `/docs` | Swagger UI (try it live) |
  | GET | `/health` | Health check |
  | POST | `/convert` | Upload file → Markdown / text / JSON |
  | POST | `/convert-url` | Public URL → Markdown / text / JSON |

  ## Example

  ```bash
  curl -X POST "https://<your-space>.hf.space/convert" \\
    -F "file=@document.pdf" \\
    -F "format=markdown"
  ```

  ## Supported formats
  PDF (including scanned via OCR), DOCX, PPTX, XLSX, HTML, Images (PNG/JPG), and more.
  