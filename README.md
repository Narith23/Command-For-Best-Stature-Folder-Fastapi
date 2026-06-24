# FastAPI Laravel-Style Project Generator Bot

This generator creates FastAPI projects with a Laravel-inspired folder layout.

## Run the Generator

```powershell
python main.py
```

or:

```powershell
py -3.13 main.py
```

The bot asks for:

- Project name
- Project parent folder
- Project type:
  - API only
  - Web only
  - API + Web

The folder selector uses the standard-library `tkinter` dialog first. If the dialog is not available, the bot falls back to manual path input.

## Generated Project Modes

API only creates FastAPI API routes:

- `GET /`
- `GET /api/v1/health`
- `GET /api/v1/items`
- `GET /api/v1/items/{item_id}`
- `POST /api/v1/items`

Web only creates Jinja-backed web routes:

- `GET /`
- `GET /about`

API + Web creates both sets of routes.

## Run a Generated Project

```powershell
cd generated_project
py -3.13 -m venv .venv
.\\.venv\\Scripts\\activate
pip install -r requirements.txt
python main.py
```

Open:

- http://127.0.0.1:8000
- http://127.0.0.1:8000/about
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/api/v1/health
- http://127.0.0.1:8000/api/v1/items

## Generator Structure

```text
main.py
README.md
bot/
    __init__.py
    cli.py
    builders/
        __init__.py
        api_builder.py
        common_builder.py
        project_builder.py
        web_builder.py
    utils/
        __init__.py
        file_writer.py
        name_utils.py
        path_utils.py
```

## Generated Project Structure

Generated projects follow this Laravel-style naming pattern:

- `routes/api.py`
- `routes/web.py`
- `app/Http/Controllers/Api`
- `app/Http/Controllers/Web`
- `app/Http/Requests`
- `app/Http/Resources`
- `app/Models`
- `app/Services`
- `resources/views`
- `public/css`
- `public/js`
- `config/app.py`
- `bootstrap/app.py`
- `vendor/helpers/response.py`
- `vendor/helpers/datetime_helper.py`
- `vendor/helpers/string_helper.py`

## API Response Standard

Generated API and hybrid projects use generic response models from `vendor.helpers`.

For one object:

```python
response_model=ApiResponse[ItemResource]
```

For list data:

```python
response_model=ApiResponse[list[ItemResource]]
```

Example response:

```json
{
  "success": true,
  "message": "Items fetched successfully",
  "data": [
    {
      "id": 1,
      "name": "Sample Item",
      "description": "Laravel-style FastAPI item"
    }
  ],
  "timestamp": "2026-06-24T04:06:47.964Z",
  "errors": {}
}
```

For paginated list data:

```python
response_model=PaginatedApiResponse[ItemResource]
```

Example pagination response:

```json
{
  "success": true,
  "message": "Items fetched successfully",
  "data": [
    {
      "id": 1,
      "name": "Sample Item",
      "description": "Laravel-style FastAPI item"
    }
  ],
  "meta": {
    "page": 1,
    "per_page": 10,
    "total": 100,
    "total_pages": 10
  },
  "timestamp": "2026-06-24T04:06:47.964Z",
  "errors": {}
}
```
