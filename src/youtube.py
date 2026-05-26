import feedparser
from datetime import datetime, timezone, timedelta

CHANNELS = [
    {"name": "Fireship",   "id": "UCsBjURrPoezykLs9EqgamOA"},
    {"name": "AI Explained", "id": "UCNJ1Ymd5yFuUPtn21xtRbbw"},
    {"name": "Andrej Karpathy",   "id": "UCXUPKJO5MZQN11PqgIvyuvQ"},
    {"name": "Two Minute Papers", "id": "UCbfYPyITQ-7l4upoX8nvctg"},
    
]

def fetch_all_videos(max_per_channel: int = 10) -> list[dict]:
    cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
    all_videos = []

    for channel in CHANNELS:
        url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel['id']}"
        feed = feedparser.parse(url)

        for entry in feed.entries[:max_per_channel]:
            published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)

            if published < cutoff:
                continue  # skip anything older than 24 hours

            all_videos.append({
                "channel": channel["name"],
                "title": entry.title,
                "url": entry.link,
                "published": published.strftime("%Y-%m-%d %H:%M UTC"),
                "summary": entry.get("summary", "")
            })

    return all_videos