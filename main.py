import io
import ipaddress
import socket
from urllib.parse import urlparse

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import Response
from playwright.async_api import (
    async_playwright,
    TimeoutError as PlaywrightTimeout,
    Error as PlaywrightError,
)
from PIL import Image

app = FastAPI(
    title="ScreenshotAPI",
    description="Generate screenshots of public websites.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

def validate_url(url: str):
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname
        port = parsed.port
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid URL."
        )

    if parsed.scheme != "https" or not hostname:
        raise HTTPException(
            status_code=400,
            detail="Only valid HTTPS URLs are supported."
        )

    if parsed.username or parsed.password:
        raise HTTPException(
            status_code=400,
            detail="URL credentials are not allowed."
        )

    if port not in (None, 443):
        raise HTTPException(
            status_code=400,
            detail="Only HTTPS port 443 is allowed."
        )

    try:
        addresses = socket.getaddrinfo(
            hostname,
            443,
            type=socket.SOCK_STREAM
        )
    except socket.gaierror:
        raise HTTPException(
            status_code=400,
            detail="Could not resolve hostname."
        )

    if not addresses:
        raise HTTPException(
            status_code=400,
            detail="Hostname has no IP addresses."
        )

    for address in addresses:
        ip = ipaddress.ip_address(address[4][0])

        if not ip.is_global:
            raise HTTPException(
                status_code=403,
                detail="Private or reserved IP addresses are blocked."
            )

@app.get("/")
async def home():
    return {
        "name": "ScreenshotAPI",
        "version": "1.0.0",
        "status": "online",
        "documentation": "/docs",
        "endpoint": "/api/v1/screenshot",
        "supported_formats": ["png", "jpeg", "webp"],
        "features": [
            "Public HTTPS websites",
            "Custom resolution",
            "Full page screenshots",
            "Mobile screenshots",
            "Direct image download"
        ]
    }

@app.get("/api/v1/screenshot")
async def screenshot(
    url: str = Query(
        ...,
        description="Public HTTPS website URL"
    ),
    width: int = Query(
        1280,
        ge=320,
        le=3840
    ),
    height: int = Query(
        720,
        ge=240,
        le=2160
    ),
    full_page: bool = Query(False),
    mobile: bool = Query(False),
    format: str = Query(
        "png",
        pattern="^(png|jpeg|webp)$"
    ),
    quality: int = Query(
        85,
        ge=1,
        le=100,
    ),
    delay: int = Query(
        1000,
        ge=0,
        le=5000
    ),
):
    validate_url(url)

    try:
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(
                headless=True
            )

            try:
                context = await browser.new_context(
                    viewport={
                        "width": width,
                        "height": height
                    },
                    device_scale_factor=1,
                    is_mobile=mobile,
                    has_touch=mobile,
                    service_workers="block",
                    accept_downloads=False
                )

                page = await context.new_page()

                async def validate_request(route):
                    request_url = route.request.url

                    try:
                        validate_url(request_url)
                    except HTTPException:
                        await route.abort()
                        return

                    await route.continue_()

                await context.route(
                    "**/*",
                    validate_request
                )

                await page.goto(
                    url,
                    wait_until="domcontentloaded",
                    timeout=20000
                )

                if delay:
                    await page.wait_for_timeout(delay)

                screenshot_format = (
                    "png" if format == "webp" else format
                )

                options = {
                    "type": screenshot_format,
                    "full_page": full_page,
                    "animations": "disabled",
                    "timeout": 15000
                }

                if screenshot_format == "jpeg":
                    options["quality"] = quality

                image_data = await page.screenshot(
                    **options
                )

                if format == "webp":
                    image = Image.open(
                        io.BytesIO(image_data)
                    )

                    output = io.BytesIO()

                    image.save(
                        output,
                        format="WEBP",
                        quality=quality
                    )

                    image_data = output.getvalue()

                await context.close()

            finally:
                await browser.close()

        media_types = {
            "png": "image/png",
            "jpeg": "image/jpeg",
            "webp": "image/webp"
        }

        return Response(
            content=image_data,
            media_type=media_types[format],
            headers={
                "Content-Disposition":
                f'attachment; filename="screenshot.{format}"',
                "Cache-Control": "no-store",
                "X-Content-Type-Options": "nosniff"
            }
        )

    except PlaywrightTimeout:
        raise HTTPException(
            status_code=504,
            detail="Website or screenshot timed out."
        )

    except PlaywrightError:
        raise HTTPException(
            status_code=502,
            detail="Browser could not capture the website."
        )

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Screenshot generation failed."
        )