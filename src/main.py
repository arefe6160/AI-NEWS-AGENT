import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from youtube import fetch_all_videos
from rss_fetcher import fetch_rss_articles
from email_agent import send_email
from database import init_db, is_seen, mark_seen
from summarizer import summarize

def run():
    init_db()

    # fetch from all sources
    print("Fetching YouTube videos...")
    videos = fetch_all_videos()
    print(f"  Found {len(videos)} YouTube videos.")

    print("Fetching RSS articles...")
    articles = fetch_rss_articles()
    print(f"  Found {len(articles)} RSS articles.")

    all_items = videos + articles

    # filter duplicates
    fresh = [item for item in all_items if not is_seen(item["video_id"])]
    print(f"{len(fresh)} new items total.")

    if not fresh:
        print("Nothing new today. No email sent.")
        return

    # summarize each item
    print("Summarizing with Groq...")
    for item in fresh:
        item["summary"] = summarize(item["title"], item["summary"])
        print(f"  Done: {item['title'][:50]}")

    send_email(fresh)

    for item in fresh:
        mark_seen(item["video_id"], item["title"])
    print("Done!")

if __name__ == "__main__":
    run()