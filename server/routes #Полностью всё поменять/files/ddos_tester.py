from fastapi.responses import PlainTextResponse

from server import app
from server.core.config import settings

@app.get("/loaderio-b3c4d227f1716194b9b4abf76e3d79bc/", include_in_schema=False)
async def loaderio():
    if settings.DEV:
        return PlainTextResponse(content="loaderio-b3c4d227f1716194b9b4abf76e3d79bc")
    return None