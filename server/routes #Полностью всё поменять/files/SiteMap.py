from xml.etree.ElementTree import Element, SubElement, tostring

from starlette.responses import Response

from server import app, redis_client

BASE_URL = "https://api.asfes.ru"

@app.get("/sitemap.xml", include_in_schema=False)
async def sitemap():
    cache_key = "sitemap.xml"
    cached = await redis_client.get(cache_key)
    if cached:
        return Response(content=cached, media_type="application/xml")

    urlset = Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    for route in app.routes:
        if getattr(route, "include_in_schema", True):
            methods = getattr(route, "methods", set())
            if "GET" in methods and isinstance(route.path, str):
                if "{" in route.path:
                    continue
                url = SubElement(urlset, "url")
                SubElement(url, "loc").text = f"{BASE_URL}{route.path}"
                SubElement(url, "changefreq").text = "hourly"
                if "login" in route.path:
                    priority = "1.0"
                elif "registration" in route.path:
                    priority = "0.9"
                else:
                    priority = "0.7"
                SubElement(url, "priority").text = priority

    xml_bytes = tostring(urlset, encoding="utf-8", method="xml")
    await redis_client.set(cache_key, xml_bytes, ex=3600)
    return Response(content=xml_bytes, media_type="application/xml")
