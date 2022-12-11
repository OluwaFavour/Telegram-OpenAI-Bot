import os
import re

from pyrogram import Client, filters
from pyrogram.enums import ParseMode

from openai.error import InvalidRequestError

from utils import formatDescription
from openAI import generateImageUrls, generateVariationUrls


V_NEXT = False

@Client.on_message(filters.command("variation"))
async def variations_(bot, message):
    global V_NEXT
    V_NEXT = True
    reply  = "Send the base image and a caption in the format below.\n\n`<number of variations to create>%<size>\n\n> Note: The image needs to be a square PNG file that's less than 4MB in size.\n> You can only generate up to 10 images.\n> There are three acceptable options for the image size: 256x256, 512x512, and 1024x1024.`"
    await bot.send_message(message.chat.id, reply, parse_mode = ParseMode.MARKDOWN)


@Client.on_callback_query(filters.regex("Variation"))
async def variations(bot, callback):
    global V_NEXT
    V_NEXT = True
    message  = "Send the base image and a caption in the format below.\n\n`<number of variations to create>%<size>\n\n> Note: The image needs to be a square PNG file that's less than 4MB in size.\n> You can only generate up to 10 images.\n> There are three acceptable options for the image size: 256x256, 512x512, and 1024x1024.`"
    await bot.send_message(callback.message.chat.id, message, parse_mode = ParseMode.MARKDOWN)

@Client.on_message(filters.photo)
async def sendVariations(bot, message):
    global V_NEXT
    if V_NEXT:
        chat_id = message.chat.id
        pattern = re.compile(r"[0-9]+%[0-9]+x[0-9]+", flags=re.I|re.M)
        if pattern.match(message.caption):
            await bot.download_media(message.photo, "images/photo.png")
            request = await formatDescription(message.caption, True)
            try:
                await bot.send_message(chat_id, "Generating Variations 🧭")
                responses = await generateVariationUrls(
                    "images/photo.png",
                    request["n"],
                    request["size"]
                )
            except InvalidRequestError as e:
                await bot.send_message(chat_id, "⚠ You used the wrong syntax. Try again but make sure the caption of the image is in this format. '`<number of variations to create>%<size>`' and don't forget the rules\n\n> The image needs to be a square PNG file that's less than 4MB in size.\n> You can only generate up to 10 images.\n> There are three acceptable options for the image size: 256x256, 512x512, and 1024x1024.`\nYou're welcome by the way😉", parse_mode = ParseMode.MARKDOWN)
                print(e.error)
            else:
                for response in responses:
                    await bot.send_photo(chat_id, response['url'])
                os.remove("images/photo.png")
                await bot.send_message(chat_id, "Here are the images you asked for.")
                V_NEXT = False

