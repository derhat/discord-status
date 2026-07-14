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
    {"text": "LIVE_CLOCK", "emoji_name": "loading_icon", "emoji_id": "1289683858337562625"}
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
        activities = [
            {
                "type": 4,
                "name": "Custom Status",
                "state": text,
                "emoji": {"name": emoji_name, "id": emoji_id}
            },
            {
                "type": 1,
                "name": "VEX",
                "url": "https://www.twitch.tv/discord",
                "application_id": "1526689014810148875",
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
            print(f"[+] Status updated: {text}", flush=True)
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
    client = StatusBot(chunk_guilds_at_startup=False)
    client.run(TOKEN)
