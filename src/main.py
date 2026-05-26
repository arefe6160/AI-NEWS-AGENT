import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from youtube import fetch_all_videos
from email_agent import send_email
from database import init_db, is_seen, mark_seen

def run():
    init_db()

    print("Fetching videos from last 24 hours...")
    videos = fetch_all_videos()
    print(f"Found {len(videos)} new videos.")

    # filter out already-seen videos
    fresh = [v for v in videos if not is_seen(v["video_id"])]
    print(f"{len(fresh)} videos not seen before.")

    if not fresh:
        print("Nothing new today. No email sent.")
        return

    send_email(fresh)

    # mark them all as seen after sending
    for v in fresh:
        mark_seen(v["video_id"], v["title"])
    print("Marked all as seen.")

if __name__ == "__main__":
    run()