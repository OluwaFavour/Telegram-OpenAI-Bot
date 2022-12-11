import re

from pyrogram import Client, filters
from pyrogram.enums import ParseMode

from openai.error import InvalidRequestError

from utils import formatDescription
from openAI import generateImageUrls


NEXT = False

@Client.on_message(filters.command("generate"))
async def generate_(bot, message):
    global NEXT
    NEXT = True
    reply  = "Type in a description of the picture you want using the syntax below.\n\n`<description>%<number of images to generate>%<size>\n\n> Note: The description can be up to 1000 characters long.\n> You can only generate up to 10 images.\n> There are three acceptable options for the image size: 256x256, 512x512, and 1024x1024.`"
    await bot.send_message(message.chat.id, reply, parse_mode = ParseMode.MARKDOWN)

@Client.on_callback_query(filters.regex("Generate"))
async def generate(bot, callback):
    global NEXT
    NEXT = True
    message  = "Type in a description of the picture you want using the syntax below.\n\n`<description>%<number of images to generate>%<size>\n\n> Note: The description can be up to 1000 characters long._\n> You can only generate up to 10 images.\n> There are three acceptable options for the image size: 256x256, 512x512, and 1024x1024.`"
    await bot.send_message(callback.message.chat.id, message, parse_mode = ParseMode.MARKDOWN)


@Client.on_message(filters.regex(r"[a-z,\"'.!& ]+%[0-9]+%[0-9]+x[0-9]+", flags=re.I|re.M))
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