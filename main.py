from fastapi import Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from app import app
from services.factory import Shortener, CustomShortener
from settings.config import get_settings, Settings

templates = Jinja2Templates(directory="templates")
SHORTENER: Shortener = CustomShortener


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("index.html", context)


@app.post("/encode-url", response_class=HTMLResponse)
def encode_url(request: Request, url: str = Form(...)):
    base_url = request.base_url
    url = SHORTENER(url=url, base_url=base_url).shorten()
    return f' <div class="code highcontrast-dark" id="short_url_display" hx-swap="outerHTML">' \
           f' <a href="{url}" target=”_blank”>{url}</a></div>'


@app.get("/v1/{slug}")
def redirect_url(slug: str):
    url = SHORTENER(slug=slug).enlarge()
    return RedirectResponse(url)


@app.get("/health")
def health_check(settings: Settings = Depends(get_settings)):
    try:
        app.state.redis.set(str(settings.redis_url), settings.up)
        value = app.state.redis.get(str(settings.redis_url))
    except Exception as e:
        print(f"Error on redis check, {e}")
        value = settings.down
    return {str(settings.redis_url): value}
