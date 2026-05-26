import feedparser
from datetime import datetime, timezone, timedelta

RSS_FEEDS = [
    {"name": "Anthropic Blog",  "url": "https://www.anthropic.com/rss.xml"},
    {"name": "OpenAI Blog",     "url": "https://openai.com/blog/rss.xml"},
    {"name": "Google DeepMind", "url": "https://deepmind.google/blog/rss.xml"},
    {"name": "Wired AI",        "url": "https://www.wired.com/feed/tag/ai/latest/rss"},
    {"name": "MIT Tech Review", "url": "https://www.technologyreview.com/feed/"},
]

def fetch_rss_articles(max_per_feed: int = 3) -> list[dict]:
    cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
    all_articles = []

    for feed in RSS_FEEDS:
        parsed = feedparser.parse(feed["url"])

        for entry in parsed.entries[:max_per_feed]:
            # parse the published date
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
            else:
                # if no date, include it anyway to be safe
                published = datetime.now(timezone.utc)

            if published < cutoff:
                continue

            all_articles.append({
                "video_id": entry.get("id", entry.link),  # reuse same field for deduplication
                "channel": feed["name"],
                "title": entry.title,
                "url": entry.link,
                "published": published.strftime("%Y-%m-%d %H:%M UTC"),
                "summary": entry.get("summary", entry.get("description", ""))[:1000]
            })

    return all_articles