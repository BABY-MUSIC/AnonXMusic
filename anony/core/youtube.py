import yt_dlp


def search(query):

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "format": "bestaudio",
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        info = ydl.extract_info(
            f"ytsearch:{query}",
            download=False,
        )["entries"][0]

    return {
        "title": info["title"],
        "url": info["webpage_url"],
        "stream": info["url"],
        "duration": info.get("duration", 0),
        "thumb": info.get("thumbnail"),
    }
