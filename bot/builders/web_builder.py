"""Web project file builder."""

from pathlib import Path

from bot.utils.file_writer import write_file


def create_web_files(project_path: Path) -> None:
    """Create web controllers, routes, templates, and static assets."""

    write_file(
        project_path / "routes" / "web.py",
        '''"""Web routes."""

from fastapi import APIRouter

from app.Http.Controllers.Web.home_controller import router as home_router


router = APIRouter()
router.include_router(home_router)
''',
        overwrite=True,
    )
    write_file(
        project_path
        / "app"
        / "Http"
        / "Controllers"
        / "Web"
        / "home_controller.py",
        '''"""Home web controller."""

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter(tags=["web"])
templates = Jinja2Templates(directory="resources/views")


@router.get("/")
def home(request: Request):
    """Render the home page."""

    return templates.TemplateResponse(
        request,
        "home.html",
        {"title": "Home"},
    )


@router.get("/about")
def about(request: Request):
    """Render the about page."""

    return templates.TemplateResponse(
        request,
        "about.html",
        {"title": "About"},
    )
''',
        overwrite=True,
    )
    write_file(
        project_path / "resources" / "views" / "layouts" / "app.html",
        '''<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ title }}</title>
    <link rel="stylesheet" href="/static/css/app.css">
</head>
<body>
    <header class="site-header">
        <nav>
            <a href="/">Home</a>
            <a href="/about">About</a>
            <a href="/docs">API Docs</a>
        </nav>
    </header>
    <main class="page">
        {% block content %}{% endblock %}
    </main>
    <script src="/static/js/app.js"></script>
</body>
</html>
''',
        overwrite=True,
    )
    write_file(
        project_path / "resources" / "views" / "home.html",
        '''{% extends "layouts/app.html" %}

{% block content %}
<section class="hero">
    <h1>FastAPI</h1>
    <p>Your generated web starter is running.</p>
</section>
{% endblock %}
''',
        overwrite=True,
    )
    write_file(
        project_path / "resources" / "views" / "about.html",
        '''{% extends "layouts/app.html" %}

{% block content %}
<section class="content">
    <h1>About</h1>
    <p>This page is rendered with FastAPI, Jinja2, and a Laravel-inspired layout.</p>
</section>
{% endblock %}
''',
        overwrite=True,
    )
    write_file(
        project_path / "public" / "css" / "app.css",
        '''body {
    margin: 0;
    font-family: Arial, sans-serif;
    color: #17202a;
    background: #f6f8fb;
}

.site-header {
    background: #17202a;
    padding: 16px 24px;
}

.site-header a {
    color: #ffffff;
    margin-right: 18px;
    text-decoration: none;
}

.page {
    max-width: 960px;
    margin: 48px auto;
    padding: 0 24px;
}

.hero,
.content {
    background: #ffffff;
    border: 1px solid #dce3ea;
    border-radius: 8px;
    padding: 32px;
}
''',
        overwrite=True,
    )
    write_file(
        project_path / "public" / "js" / "app.js",
        '''console.log("Generated FastAPI web app loaded.");
''',
        overwrite=True,
    )
