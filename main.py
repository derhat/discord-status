import discord
import asyncio
import datetime
import requests
import os
import sys
import http.server
import socketserver
from threading import Thread

# ══════════════════════════════════════════
#           ⚙️ CONFIGURATION
# ══════════════════════════════════════════
TOKEN      = os.getenv("DISCORD_TOKEN")
WATCH_LINK = "https://guns.lol/1s1dk"
INTERVAL   = 10

# ══════════════════════════════════════════
#           📝 ROTATING STATUSES
# ══════════════════════════════════════════
STATUSES = [
    {"text": "Money can buy many things. Even power.", "emoji_name": "7_star", "emoji_id": "1424510375390478407"},
    {"text": "𝘓𝘦𝘨𝘦𝘯𝘥", "emoji_name": "7_crown", "emoji_id": "1432835236932358298"},
    {"text": "Victory smiles upon those who take bold risks; only those with courage to act can hope to change the world.", "emoji_name": "satanic~1", "emoji_id": "1423198805788200981"},
    {"text": "LIVE_CLOCK", "emoji_name": "loading_icon", "emoji_id": "1289683858337562625"},
    {"text": "/HvH", "emoji_name": "custom", "emoji_id": "1158064269267574824"},
    {"text": "Ideas have the power to outlive us; while men may pass, their thoughts and beliefs will endure for generations.", "emoji_name": "custom", "emoji_id": "896093827666948198"},
    {"text": "Milliers d'euros, plus de peine de cœur. Cœur à zéro, j't'oublie sans rancœur", "emoji_name": "custom", "emoji_id": "1424513479813107762"}
]

# ══════════════════════════════════════════
#           🌐 WEB SERVER
# ══════════════════════════════════════════
def run_server():
    try:
        port = int(os.environ.get('PORT') or os.environ.get('SERVER_PORT') or 8080)
        Handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("0.0.0.0", port), Handler) as httpd:
            print(f"Web server started on port {port}", flush=True)
            httpd.serve_forever()
    except Exception:
        pass

# ══════════════════════════════════════════
#           🤖 BOT
# ══════════════════════════════════════════
class StatusBot(discord.Client):

    async def on_ready(self):
        print(f"Logged in as {self.user}", flush=True)
        print("Bot is ready", flush=True)
        asyncio.create_task(self.rotate_status())

    async def set_streaming_and_status(self, text, emoji_name, emoji_id):
        import time
        now_ms = int(time.time() * 1000)
        
        activities = [
            {
                "type": 4,
                "name": "Custom Status",
                "state": text,
                "emoji": {"name": emoji_name, "id": emoji_id}
            },
            {
                "type": 1,
                "name": "Streaming",
                "details": text,
                "url": "https://www.twitch.tv/discord",
                "application_id": "1526689014810148875",
                "assets": {
                    "large_image": "mp:emojis/1423198805788200981.gif"
                },
                "buttons": ["/nosuce"],
                "metadata": {"button_urls": [WATCH_LINK]}
            },
            {
                "type": 2,
                "name": "Spotify",
                "details": text,
                "application_id": "1125656070484934676",
                "assets": {
                    "large_image": "mp:emojis/1418648754545758248.webp"
                },
                "timestamps": {
                    "start": now_ms - (404 * 3600 * 1000),
                    "end": now_ms
                },
                "buttons": ["Listen Along", "Play on Spotify"],
                "metadata": {"button_urls": ["https://open.spotify.com/", "https://open.spotify.com/"]}
            },
            {
                "type": 0,
                "name": "PlayStation",
                "details": text,
                "application_id": "1125658851849556048",
                "assets": {
                    "large_image": "mp:emojis/1416587771321126942.webp"
                },
                "timestamps": {
                    "start": now_ms - (13 * 60 * 1000 + 37 * 1000)
                },
                "buttons": ["Watch"],
                "metadata": {"button_urls": [WATCH_LINK]}
            }
        ]
        try:
            await self.ws.send_as_json({
                "op": 3,
                "d": {
                    "status": "online",
                    "since": 0,
                    "afk": False,
                    "activities": activities
                }
            })
            print(f"[+] Status updated: {text[:20]}...", flush=True)
        except Exception as e:
            print(f"[!] Error: {e}", flush=True)

    async def rotate_status(self):
        i = 0
        while True:
            s = STATUSES[i]
            text = datetime.datetime.now().strftime("%d/%m/%Y %H:%M") if s["text"] == "LIVE_CLOCK" else s["text"]
            await self.set_streaming_and_status(text, s["emoji_name"], s["emoji_id"])
            await asyncio.sleep(INTERVAL)
            i = (i + 1) % len(STATUSES)

# ══════════════════════════════════════════
#           🚀 START
# ══════════════════════════════════════════
if __name__ == "__main__":
    Thread(target=run_server, daemon=True).start()
    print("Starting bot...", flush=True)
    
    import time
    while True:
        try:
            client = StatusBot(chunk_guilds_at_startup=False)
            client.run(TOKEN)
        except Exception as e:
            print(f"Bot crashed: {e}", flush=True)
        
        print("Bot disconnected! Restarting in 5 seconds...", flush=True)
        time.sleep(5)
