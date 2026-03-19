import os
import asyncio
import aiohttp
from youtubesearchpython import VideosSearch


BASE_URL = "https://www.babyapi.pro"
API_KEY = "BABYXF0C2B2F1869BAEE698C65BF3C0BA57A16"


# =========================
# SEARCH
# =========================

async def search(query: str):

    vs = VideosSearch(query, limit=1)

    r = vs.result()["result"]

    if not r:
        raise Exception("No result")

    data = r[0]

    return {
        "title": data["title"],
        "url": data["link"],
        "duration": data.get("duration"),
        "thumb": data["thumbnails"][0]["url"],
    }


# =========================
# INTERNAL API DOWNLOAD
# =========================

async def _download_media(
    link: str,
    kind: str,
    exts: list[str],
    wait: int = 60,
):

    vid = link.split("v=")[-1].split("&")[0]

    os.makedirs("downloads", exist_ok=True)

    for ext in exts:

        path = f"downloads/{vid}.{ext}"

        if os.path.exists(path):
            return path

    async with aiohttp.ClientSession() as session:

        async with session.get(
            f"{BASE_URL}/api/{kind}?query={vid}&api={API_KEY}"
        ) as resp:

            res = await resp.json()

        stream = res.get("stream")
        media_type = res.get("type")

        if not stream:
            raise Exception(f"{kind} stream not found")

        # live stream
        if media_type == "live":
            return stream

        # wait until ready

        for _ in range(wait):

            async with session.get(stream) as r:

                if r.status == 200:
                    return stream

                if r.status in (423, 404, 410):
                    await asyncio.sleep(2)
                    continue

                if r.status in (401, 403, 429):
                    txt = await r.text()
                    raise Exception(
                        f"{kind} blocked {r.status}: {txt[:100]}"
                    )

                raise Exception(f"{kind} failed ({r.status})")

        raise Exception(f"{kind} timeout")


# =========================
# SONG
# =========================

async def download_song(link: str):

    return await _download_media(
        link,
        "song",
        ["mp3", "m4a", "webm"],
        wait=60,
    )


# =========================
# VIDEO
# =========================

async def download_video(link: str):

    return await _download_media(
        link,
        "video",
        ["mp4", "webm", "mkv"],
        wait=90,
    )
