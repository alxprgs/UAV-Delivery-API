from starlette.responses import FileResponse

from server import app

@app.get("/robots.txt", include_in_schema=False)
async def sitemap() -> FileResponse:
    return FileResponse("server/robots.txt")