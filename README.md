
<div align="center">

# ScreenshotAPI

<p>
  A lightweight and powerful REST API for generating
  high-quality website screenshots using Python,
  FastAPI, Playwright and Chromium.
</p>

<p>
  <img src="https://img.shields.io/badge/Version-1.0.0-blue" alt="Version">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-REST_API-009688" alt="FastAPI">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
</p>

<p>
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#api-endpoints">API Endpoints</a> •
  <a href="#usage-examples">Examples</a> •
  <a href="#documentation">Documentation</a>
</p>

</div>

---

<h2 id="overview">Overview</h2>

ScreenshotAPI is an open-source REST API designed to
capture screenshots of public HTTPS websites.

It supports multiple image formats, custom resolutions,
full-page screenshots, mobile viewport emulation,
and direct image downloads.

The API is powered by FastAPI and uses Playwright
with Chromium for browser automation.

<h2 id="features">Features</h2>

- Capture screenshots of public HTTPS websites
- Generate PNG, JPEG and WebP images
- Full-page screenshot support
- Custom viewport width and height
- Mobile viewport emulation
- Adjustable image quality
- Configurable screenshot delay
- Direct screenshot downloads
- Automatic Swagger UI and ReDoc documentation
- Basic URL validation and IP filtering

<h2 id="requirements">Requirements</h2>

| Technology | Purpose |
|------------|---------|
| Python 3.10+ | Programming language |
| FastAPI | REST API framework |
| Uvicorn | ASGI server |
| Playwright | Browser automation |
| Chromium | Screenshot rendering |
| Pillow | WebP image conversion |

<h2 id="installation">Installation</h2>

<h3>1. Clone the Repository</h3>

```bash
git clone https://github.com/louizmac/ScreenshotAPI.git
cd ScreenshotAPI
```

<h3>2. Install Dependencies</h3>

```bash
pip install -r requirements.txt
```

<h3>3. Install Chromium</h3>

```bash
python -m playwright install chromium
```

<h3>4. Start the API</h3>

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

<h2 id="api-endpoints">API Endpoints</h2>

<h3>GET /</h3>

Returns general API information.

Example response:

```json
{
  "name": "ScreenshotAPI",
  "version": "1.0.0",
  "status": "online",
  "documentation": "/docs",
  "endpoint": "/api/v1/screenshot",
  "supported_formats": [
    "png",
    "jpeg",
    "webp"
  ]
}
```

<h3>GET /api/v1/screenshot</h3>

Generates a website screenshot and returns it
as a downloadable image.

<h3>Query Parameters</h3>

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| url | string | Required | Target HTTPS URL |
| width | integer | 1280 | Viewport width (320–3840) |
| height | integer | 720 | Viewport height (240–2160) |
| full_page | boolean | false | Capture entire page |
| mobile | boolean | false | Enable mobile emulation |
| format | string | png | png, jpeg or webp |
| quality | integer | 85 | JPEG/WebP quality (1–100) |
| delay | integer | 1000 | Screenshot delay in ms (0–5000) |

<h2 id="usage-examples">Usage Examples</h2>

<h3>Basic Screenshot</h3>

```http
GET /api/v1/screenshot?url=https://example.com
```

<h3>Full HD Screenshot</h3>

```http
GET /api/v1/screenshot?url=https://example.com&width=1920&height=1080
```

<h3>Full-Page Screenshot</h3>

```http
GET /api/v1/screenshot?url=https://example.com&full_page=true
```

<h3>Mobile Screenshot</h3>

```http
GET /api/v1/screenshot?url=https://example.com&mobile=true&width=390&height=844
```

<h3>WebP Screenshot</h3>

```http
GET /api/v1/screenshot?url=https://example.com&format=webp&quality=85
```

<h3>Python Example</h3>

```python
import requests

endpoint = "http://127.0.0.1:8000/api/v1/screenshot"

params = {
    "url": "https://example.com",
    "width": 1920,
    "height": 1080,
    "format": "png"
}

response = requests.get(
    endpoint,
    params=params,
    timeout=60
)

response.raise_for_status()

with open("screenshot.png", "wb") as file:
    file.write(response.content)

print("Screenshot saved successfully.")
```

<h2 id="image-formats">Supported Image Formats</h2>

| Format | MIME Type | Quality Control |
|--------|-----------|-----------------|
| PNG | image/png | No |
| JPEG | image/jpeg | Yes |
| WebP | image/webp | Yes |

<h2 id="documentation">Documentation</h2>

ScreenshotAPI provides automatically generated
interactive API documentation.

<h3>Swagger UI</h3>

```text
http://127.0.0.1:8000/docs
```

<h3>ReDoc</h3>

```text
http://127.0.0.1:8000/redoc
```

<h2 id="security">Security</h2>

ScreenshotAPI includes basic URL validation:

- HTTPS-only URLs
- Port 443 restriction
- URL credential rejection
- Private and reserved IP filtering
- Browser request interception
- Disabled service workers
- Navigation and screenshot timeouts

<strong>Security Notice:</strong>

The current implementation is intended for local
development and trusted environments.

DNS validation alone does not fully prevent SSRF,
DNS rebinding, or access to internal network resources.

Public deployments require additional security
measures, including network isolation, rate limiting,
and resource restrictions.

<h2 id="hosting">Hosting</h2>

ScreenshotAPI requires a server capable of running
Chromium through Playwright.

Some free hosting providers may restrict Chromium
execution, memory usage, or external network access.

Verify browser support before deploying.

<h2 id="project-structure">Project Structure</h2>

```text
ScreenshotAPI/
├── main.py
├── requirements.txt
├── README.md
└── LICENSE
```

<h2 id="license">License</h2>

This project is licensed under the MIT License.

See the LICENSE file for details.

<h2 id="author">Author</h2>

Developed by
<a href="https://github.com/louizmac">louizmac</a>.

<p>
  Explore more projects at
  <a href="https://trymyapis.rf.gd">TryMyAPIs</a>.
</p>

---

<div align="center">

  <p>
    Made with Python, FastAPI and Playwright.
  </p>

  <p>
    ScreenshotAPI v1.0.0
  </p>

</div>
