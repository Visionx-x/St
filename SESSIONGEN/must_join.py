from config import MUST_JOIN

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden


@Client.on_message(filters.incoming & filters.private, group=-1)
async def must_join_channels(bot: Client, msg: Message):
    if not MUST_JOIN:
        return

    not_joined_channels = []
    for channel in MUST_JOIN:
        try:
            await bot.get_chat_member(channel, msg.from_user.id)
        except UserNotParticipant:
            if channel.isalpha():
                link = "https://t.me/" + channel
            else:
                chat_info = await bot.get_chat(channel)
                link = chat_info.invite_link
            not_joined_channels.append(link)
        except ChatAdminRequired:
            print(f"Please promote me as an admin in the {channel} chat")

    if not_joined_channels:
        buttons = [InlineKeyboardButton("Join", url=link) for link in not_joined_channels]
        try:
            await msg.reply_photo(
                photo="https://telegra.ph/file/20d1bcedcf901bed9bf65.jpg",
                caption="» First, you need to join our channels before you can start messaging again!",
                reply_markup=InlineKeyboardMarkup([buttons])
            )
            await msg.stop_propagation()
        except ChatWriteForbidden:
            pass
            
