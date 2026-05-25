import resend
import os
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")

def build_html(videos: list[dict]) -> str:
    items = ""
    for v in videos:
        items += f"""
        <div style="margin-bottom:24px;padding-bottom:24px;border-bottom:1px solid #eee;">
          <p style="margin:0 0 4px;font-size:12px;color:#888;">{v['channel']} &middot; {v['published'][:10]}</p>
          <h2 style="margin:0 0 8px;font-size:16px;">
            <a href="{v['url']}" style="color:#1a1a1a;text-decoration:none;">{v['title']}</a>
          </h2>
          <p style="margin:0;font-size:14px;color:#555;">{v['summary'][:300]}...</p>
        </div>"""

    return f"""
    <html><body style="font-family:sans-serif;max-width:600px;margin:auto;padding:24px;">
      <h1 style="font-size:22px;border-bottom:2px solid #eee;padding-bottom:12px;">
        Your Daily AI News Digest
      </h1>
      {items}
      <p style="font-size:12px;color:#aaa;margin-top:32px;">
        Sent automatically by your news agent.
      </p>
    </body></html>"""

def send_email(videos: list[dict]):
    params = {
        "from": "News Agent <onboarding@resend.dev>",
        "to": [os.getenv("TO_EMAIL")],
        "subject": "Your Daily AI News Digest",
        "html": build_html(videos),
    }
    response = resend.Emails.send(params)
    print(f"Email sent! ID: {response['id']}")