from youtube import fetch_all_videos
from email_agent import send_email

def run():
    print("Fetching videos...")
    videos = fetch_all_videos(max_per_channel=3)
    print(f"Found {len(videos)} videos.")

    send_email(videos)

if __name__ == "__main__":
    run()