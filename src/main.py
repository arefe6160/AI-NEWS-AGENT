import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from youtube import fetch_all_videos
from email_agent import send_email

def run():
    print("Fetching videos from last 24 hours...")
    videos = fetch_all_videos()
    print(f"Found {len(videos)} new videos.")

    if not videos:
        print("Nothing new today. No email sent.")
        return

    send_email(videos)

if __name__ == "__main__":
    run()