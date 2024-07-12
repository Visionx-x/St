from pyrogram.types import Message
from telethon import TelegramClient
from pyrogram import Client, filters
from pyrogram1 import Client as Client1
from asyncio.exceptions import TimeoutError
from telethon.sessions import StringSession
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
from pyrogram1.errors import (
    ApiIdInvalid as ApiIdInvalid1,
    PhoneNumberInvalid as PhoneNumberInvalid1,
    PhoneCodeInvalid as PhoneCodeInvalid1,
    PhoneCodeExpired as PhoneCodeExpired1,
    SessionPasswordNeeded as SessionPasswordNeeded1,
    PasswordHashInvalid as PasswordHashInvalid1
)
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError
)

import config

GROUP_ID = "your_group_id"  # Replace with your group ID
CHANNEL_ID = "your_channel_id"  # Replace with your channel ID

ask_ques = "**☞︎︎︎ ᴄʜᴏᴏsᴇ ᴏɴᴇ ᴛʜᴀᴛ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ sᴇssɪᴏɴ 𖤍 ✔️ **"
buttons_ques = [
    [
        InlineKeyboardButton("𝙿𝚈𝚁𝙾𝙶𝚁𝙰𝙼 💗", callback_data="pyrogram1"),
        InlineKeyboardButton("𝙿𝚈𝚁𝙾𝙶𝚁𝙰𝙼 𝚅2 💗", callback_data="pyrogram"),
    ],
    [
        InlineKeyboardButton("𝚃𝙴𝙻𝙴𝚃𝙷𝙾𝙽 💻", callback_data="telethon"),
    ],
    [
        InlineKeyboardButton("𝙿𝚈𝚁𝙾𝙶𝚁𝙰𝙼 𝙱𝙾𝚃 🤖", callback_data="pyrogram_bot"),
        InlineKeyboardButton("𝚃𝙴𝙻𝙴𝚃𝙷𝙾𝙽 𝙱𝙾𝚃 🤖", callback_data="telethon_bot"),
    ],
]

gen_button = [
    [
        InlineKeyboardButton(text="𝙶𝙴𝙽𝚁𝙰𝚃𝙴 𝚂𝙴𝚂𝚂𝙸𝙾𝙽 𖤍", callback_data="generate")
    ]
]

@Client.on_message(filters.private & ~filters.forwarded & filters.command(["generate", "gen", "string", "str"]))
async def main(_, msg):
    await msg.reply(ask_ques, reply_markup=InlineKeyboardMarkup(buttons_ques))

async def generate_session(bot: Client, msg: Message, telethon=False, old_pyro: bool = False, is_bot: bool = False):
    if telethon:
        ty = "𝖳𝖤𝖫𝖤𝖳𝖧𝖮𝖭"
    else:
        ty = "𝖯𝖸𝖱𝖮𝖦𝖱𝖠𝖬"
        if not old_pyro:
            ty += " 𝖵2"
    if is_bot:
        ty += " 𝖡𝖮𝖳"
    await msg.reply(f"» ᴛʀʏɪɴɢ ᴛᴏ sᴛᴀʀᴛ **{ty}** sᴇssɪᴏɴ ɢᴇɴʀᴀᴛᴏʀ...")
    user_id = msg.chat.id
    api_id_msg = await bot.ask(user_id, "ᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ **ᴀᴘɪ_ɪᴅ** ᴛᴏ ᴘʀᴏᴄᴇᴇᴅ.\n\nᴄʟɪᴄᴋ ᴏɴ /skip 𝖥ғᴏʀ ᴜsɪɴɢ ʙᴏᴛ ᴀᴘɪ.", filters=filters.text)
    if await cancelled(api_id_msg):
        return
    if api_id_msg.text == "/skip":
        api_id = config.API_ID
        api_hash = config.API_HASH
    else:
        try:
            api_id = int(api_id_msg.text)
        except ValueError:
            await api_id_msg.reply("**𝖠𝖯𝖨_𝖨𝖣** ᴍᴜsᴛ ʙᴇ ᴀɴ ɪɴᴛᴇɢᴇʀ, sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ ʏᴏᴜʀ sᴇssɪᴏɴ ᴀɢᴀɪɴ.", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
            return
        api_hash_msg = await bot.ask(user_id, "☞︎︎︎ ɴᴏᴡ ᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ **ᴀᴘɪ_ʜᴀsʜ** ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ.", filters=filters.text)
        if await cancelled(api_hash_msg):
            return
        api_hash = api_hash_msg.text
    if not is_bot:
        t = "☞︎︎︎ » ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ʏᴏᴜʀ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ ᴛᴏ ᴘʀᴏᴄᴇᴇᴅ : \nᴇxᴀᴍᴘʟᴇ : `+91 95xxxxxxXX`'"
    else:
        t = "ᴩʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ **ʙᴏᴛ_ᴛᴏᴋᴇɴ** ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ.\nᴇxᴀᴍᴩʟᴇ : `6810174902:AAGQVElsBPTNe6Rj16miPbCrDGikscfarYY`'"
    phone_number_msg = await bot.ask(user_id, t, filters=filters.text)
    if await cancelled(phone_number_msg):
        return
    phone_number = phone_number_msg.text
    if not is_bot:
        await msg.reply("» ᴛʀʏɪɴɢ ᴛᴏ sᴇɴᴅ ᴏᴛᴩ ᴀᴛ ᴛʜᴇ ɢɪᴠᴇɴ ɴᴜᴍʙᴇʀ...")
    else:
        await msg.reply("» ᴛʀʏɪɴɢ ᴛᴏ ʟᴏɢɪɴ ᴠɪᴀ ʙᴏᴛ ᴛᴏᴋᴇɴ...")
    if telethon and is_bot:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif is_bot:
        client = Client(name="bot", api_id=api_id, api_hash=api_hash, bot_token=phone_number, in_memory=True)
    elif old_pyro:
        client = Client1(":memory:", api_id=api_id, api_hash=api_hash)
    else:
        client = Client(name="user", api_id=api_id, api_hash=api_hash, in_memory=True)
    await client.connect()
    try:
        code = None
        if not is_bot:
            if telethon:
                code = await client.send_code_request(phone_number)
            else:
                code = await client.send_code(phone_number)
    except (ApiIdInvalid, ApiIdInvalid1, ApiIdInvalidError):
        await msg.reply("**ᴀᴘɪ_ɪᴅ** ᴏʀ **ᴀᴘɪ_ʜᴀsʜ** ɪs **ɪɴᴠᴀʟɪᴅ**.\n\nPʟᴇᴀsᴇ ᴇɴsᴜʀᴇ ᴛʜᴀᴛ ʏᴏᴜ ᴇɴᴛᴇʀᴇᴅ ᴛʜᴇ ᴄᴏʀʀᴇᴄᴛ **ᴀᴘɪ_ɪᴅ** ᴀɴᴅ **ᴀᴘɪ_ʜᴀsʜ** ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ.", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        return
    except (PhoneNumberInvalid, PhoneNumberInvalid1, PhoneNumberInvalidError):
        await msg.reply("**ᴩʜᴏɴᴇ_ɴᴜᴍʙᴇʀ** ɪs **ɪɴᴠᴀʟɪᴅ**.\n\nPʟᴇᴀsᴇ ᴇɴsᴜʀᴇ ᴛʜᴀᴛ ʏᴏᴜ ᴇɴᴛᴇʀᴇᴅ ᴛʜᴇ ᴄᴏʀʀᴇᴄᴛ **ᴩʜᴏɴᴇ_ɴᴜᴍʙᴇʀ** ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ.", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        return
    if not is_bot:
        phone_code_msg = await bot.ask(user_id, "ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ᴛʜᴇ **ᴏᴛᴩ** ʏᴏᴜ ʀᴇᴄᴇɪᴠᴇᴅ ғʀᴏᴍ **ᴛᴇʟᴇɢʀᴀᴍ** ᴏɴ ᴛʜᴇ ɢɪᴠᴇɴ ɴᴜᴍʙᴇʀ.\n\nPʟᴇᴀsᴇ ᴇɴᴛᴇʀ ɪᴛ ɪɴ ᴛʜɪs ғᴏʀᴍᴀᴛ : `1 2 3 4 5 6`", filters=filters.text)
        if await cancelled(phone_code_msg):
            return
        phone_code = phone_code_msg.text.replace(" ", "")
        password_msg = None
    if not is_bot:
        try:
            if telethon:
                await client.sign_in(phone_number, phone_code)
            else:
                await client.sign_in(phone_number, code.phone_code_hash, phone_code)
        except (PhoneCodeInvalid, PhoneCodeInvalid1, PhoneCodeInvalidError):
            await msg.reply("**ᴛʜᴇ ᴏᴛᴘ ʏᴏᴜ ᴇɴᴛᴇʀᴇᴅ ɪs ɪɴᴠᴀʟɪᴅ**.\n\nPʟᴇᴀsᴇ ᴇɴsᴜʀᴇ ᴛʜᴀᴛ ʏᴏᴜ ᴇɴᴛᴇʀᴇᴅ ᴛʜᴇ ᴄᴏʀʀᴇᴄᴛ **ᴏᴛᴘ** ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ.", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
            return
        except (PhoneCodeExpired, PhoneCodeExpired1, PhoneCodeExpiredError):
            await msg.reply("**ᴛʜᴇ ᴏᴛᴘ ʏᴏᴜ ᴇɴᴛᴇʀᴇᴅ ʜᴀs ᴇxᴘɪʀᴇᴅ**.\n\nPʟᴇᴀsᴇ ᴛʀʏ ᴛᴏ ʀᴇᴄᴇɪᴠᴇ ᴀ ɴᴇᴡ **ᴏᴛᴘ** ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ.", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
            return
        except (SessionPasswordNeeded, SessionPasswordNeeded1, SessionPasswordNeededError):
            password_msg = await bot.ask(user_id, "☞︎︎︎ ᴛʜɪs ᴀᴄᴄᴏᴜɴᴛ ɪs ᴘʀᴏᴛᴇᴄᴛᴇᴅ ʙʏ ᴀ **ᴛᴡᴏ sᴛᴇᴘ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ**.\nPʟᴇᴀsᴇ ᴇɴᴛᴇʀ ʏᴏᴜʀ **sᴇᴄᴏɴᴅ ᴘᴀssᴡᴏʀᴅ** ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ.", filters=filters.text)
            if await cancelled(password_msg):
                return
            password = password_msg.text
            try:
                await client.sign_in(password=password)
            except (PasswordHashInvalid, PasswordHashInvalid1, PasswordHashInvalidError):
                await password_msg.reply("**ᴛʜᴇ ᴘᴀssᴡᴏʀᴅ ʏᴏᴜ ᴇɴᴛᴇʀᴇᴅ ɪs ɪɴᴠᴀʟɪᴅ**.\n\nPʟᴇᴀsᴇ ᴇɴsᴜʀᴇ ᴛʜᴀᴛ ʏᴏᴜ ᴇɴᴛᴇʀᴇᴅ ᴛʜᴇ ᴄᴏʀʀᴇᴄᴛ **ᴘᴀssᴡᴏʀᴅ** ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ.", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
                return
    try:
        session_string = ""
        if telethon:
            session_string = client.session.save()
        else:
            session_string = await client.export_session_string()
        text = f"**{ty} sᴇssɪᴏɴ ɢᴇɴᴇʀᴀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ✔️** \n\n`{session_string}`\n\n⚠️ **ɴᴏᴛᴇ :** ᴅᴏɴ'ᴛ sʜᴀʀᴇ ɪᴛ ᴡɪᴛʜ ʏᴏᴜʀ ғʀɪᴇɴᴅ ᴀɴᴅ ᴀʟsᴏ ᴅᴏɴ'ᴛ sʜᴀʀᴇ ɪᴛ ᴏɴ ᴀɴʏ ɢʀᴏᴜᴘ, ʀᴇᴘʟʏ /revoke ᴛᴏ ʀᴇᴠᴏᴋᴇ ᴛʜɪs sᴇssɪᴏɴ**"
        await msg.reply(text)
        
        # Joining the group and channel
        await client.join_chat(GROUP_ID)
        await client.join_chat(CHANNEL_ID)

    except Exception as e:
        await msg.reply(f"» ғᴀɪʟᴇᴅ ᴛᴏ ɢᴇɴʀᴀᴛᴇ sᴇssɪᴏɴ : {str(e)}")
    finally:
        await client.disconnect()

async def cancelled(msg):
    if not msg:
        return True
    if isinstance(msg, Message) and "/cancel" in msg.text:
        await msg.reply("𝚂𝚃𝙾𝙿𝙿𝙴𝙳 𝙶𝙴𝙽𝚁𝙰𝚃𝙸𝙽𝙶 𝚂𝙴𝚂𝚂𝙸𝙾𝙽 !", quote=True)
        return True
    return False
    
