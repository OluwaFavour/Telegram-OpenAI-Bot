import os
import uvloop

from pyrogram import Client, filters

api_id = os.getenv("PYROGRAM_API_ID")
api_hash = os.getenv("PYROGRAM_API_HASH")
bot_token = os.getenv("PYROGRAM_API_TOKEN")

plugins = dict(
    root="plugins",
    include=[
        "handlers.start",
        "handlers.generateButton",
        "handlers.variationsButton",
    ]
)

print("Holla! I'm online")
uvloop.install()

Client(
    "image_king_bot",
    api_id=int(api_id), api_hash=str(api_hash),
    bot_token=str(bot_token),
    plugins=plugins
).run()