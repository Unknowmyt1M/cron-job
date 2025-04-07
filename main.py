import subprocess
import requests
from yt_dlp import YoutubeDL
from bs4 import BeautifulSoup

channel_url = "https://www.youtube.com/channel/UCoB4IaEnVASj_7hn7Lxs6jQ/videos"
last_video_url = None

def get_latest_video_url():
    response = requests.get(channel_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and '/watch?v=' in href:
            return 'https://www.youtube.com' + href
    return None

def download_video(url):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'outtmpl': 'latest_video.%(ext)s',
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def call_webhook(video_url):
    webhook_url = 'https://connect.pabbly.com/workflow/sendwebhookdata/abcxyz'  # Replace this!
    requests.post(webhook_url, data={"video_url": video_url})
    print("Webhook triggered!")

def main():
    global last_video_url
    latest_url = get_latest_video_url()
    if latest_url != last_video_url:
        print("New video found:", latest_url)
        download_video(latest_url)
        call_webhook(latest_url)
        last_video_url = latest_url
    else:
        print("No new video.")

if __name__ == "__main__":
    main()
