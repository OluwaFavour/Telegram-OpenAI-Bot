import asyncio

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_message(filters.command("start"))
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