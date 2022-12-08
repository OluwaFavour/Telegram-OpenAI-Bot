import os
import re
import asyncio

from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from openai.error import InvalidRequestError

from openAI import generateImageUrls

api_id = os.getenv("PYROGRAM_API_ID")
api_hash = os.getenv("PYROGRAM_API_HASH")
bot_token = os.getenv("PYROGRAM_API_TOKEN")

bot = Client(
    "image_king_bot",
    api_id=int(api_id), api_hash=str(api_hash),
    bot_token=str(bot_token)
)

NEXT = False

async def formatDescription(text):
    """
        Formats user input for image description,
        Returns a dictionary {"description": text, "n": number, "size": text}
    """
    response = {}
    splitted_text = text.split("%")
    response.update({"description" : splitted_text[0].strip()})
    response.update({"n" : int(splitted_text[1].strip())})
    response.update({"size" : splitted_text[2].strip().lower()})

    return response
    

@bot.on_message(filters.command("start"))
async def start(bot, message):
    chat_id = message.chat.id
    text_1 = "Excuse me, I'm Mark, and I can make whatever kind of picture you want. In addition, I can mask and add new variations to your photographs."
    await bot.send_message(chat_id, text_1)
    await asyncio.sleep(0.5)
    caption = "Let's get started. How can I help you?"
    text_buttons = [
            [InlineKeyboardButton("Generate New Image", callback_data = "Generate")],
            #[InlineKeyboardButton("Edit Image", callback_data = "Edit")],
            [InlineKeyboardButton("Create Variations", callback_data = "Variation")]
        ]
    text_markup = InlineKeyboardMarkup(text_buttons)
    await bot.send_message(
        chat_id,
        text = caption,
        reply_markup = text_markup
    )

async def generate(bot, callback):
    global NEXT
    NEXT = True
    message  = "Type in a description of the picture you want using the syntax below.\n\n`<description>%<number of images to generate>%<size>\n\n> Note: The description can be up to 1000 characters long._\n> You can only generate up to 10 images.\n> There are three acceptable options for the image size: 256x256, 512x512, and 1024x1024.`"
    try:
        await bot.send_message(callback.chat.id, message, parse_mode = ParseMode.MARKDOWN)
    except AttributeError:
        await bot.send_message(callback.message.chat.id, message, parse_mode = ParseMode.MARKDOWN)

bot.add_handler(MessageHandler(generate, filters.command("generate")))
bot.add_handler(CallbackQueryHandler(generate, filters.regex("Generate")))

@bot.on_message(filters.regex(r"[a-z,\"'.!& ]+%[0-9]+%[0-9]+x[0-9]+", flags=re.I|re.M))
async def sendImages(bot, message):
    global NEXT
    if NEXT:
        chat_id = message.chat.id
        request = await formatDescription(message.text)
        try:
            await bot.send_message(chat_id, "Getting images 🧭")
            responses = await generateImageUrls(
                request["description"],
                request["n"],
                request["size"]
            )
        except InvalidRequestError:
            await bot.send_message(chat_id, "⚠ You used the wrong syntax. Try again but make sure it's in this format. '`<description>%<number of images to generate>%<size>`' and don't forget the rules\n\n> The description can be up to 1000 characters long._\n> You can only generate up to 10 images.\n> There are three acceptable options for the image size: 256x256, 512x512, and 1024x1024.\nYou're welcome by the way😉", parse_mode = ParseMode.MARKDOWN)
        else:
            for response in responses:
                await bot.send_photo(chat_id, response['url'])
            await bot.send_message(chat_id, "Here are the images you asked for.")
            NEXT = False

print("Holla, I'm online")
bot.run()