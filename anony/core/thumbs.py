import os
import aiohttp
from PIL import Image, ImageDraw

from py_yt import VideosSearch


async def get_video_data(vidid: str):

    search = VideosSearch(vidid, limit=1)

    data = await search.next()

    if not data or not data.get("result"):
        return {}

    v = data["result"][0]

    return {
        "title": v.get("title"),
        "duration": v.get("duration"),
        "thumb": v["thumbnails"][0]["url"]
        if v.get("thumbnails")
        else "",
        "channel": v.get("channel", {}).get("name", ""),
    }


async def gen_thumb(vidid: str):

    os.makedirs("thumbs", exist_ok=True)

    info = await get_video_data(vidid)

    title = info.get("title", "Unknown")
    thumb_url = info.get("thumb")

    if not thumb_url:
        return None, info

    async with aiohttp.ClientSession() as s:
        async with s.get(thumb_url) as r:
            data = await r.read()

    base = "thumbs/base.jpg"

    with open(base, "wb") as f:
        f.write(data)

    img = Image.open(base).convert("RGB")
    img = img.resize((1280, 720))

    draw = ImageDraw.Draw(img)

    draw.text(
        (50, 600),
        title[:40],
        fill="white",
    )

    out = "thumbs/out.png"

    img.save(out)

    return out, info
