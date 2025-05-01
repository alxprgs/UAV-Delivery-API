from server import app
from starlette.responses import FileResponse

@app.get("/robots.txt", include_in_schema=False)
async def sitemap() -> FileResponse:
    return FileResponse("server/robots.txt")