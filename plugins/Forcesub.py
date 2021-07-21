import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant
from database.database import *
from config import *

@Client.on_message(filters.private & filters.incoming)
async def forcesub(c, m):
    owner = await c.get_users(int(OWNER_ID))
    if UPDATE_CHANNEL:
        try:
            user = await c.get_chat_member(UPDATE_CHANNEL, m.from_user.id)
            if user.status == "kicked":
               await m.reply_text("**Yᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ ɪɴ Oᴜʀ ᴄʜᴀɴɴᴇʟ Cᴏɴᴛᴀᴄᴛ Aᴅᴍɪɴ 😜**", quote=True)
               return
        except UserNotParticipant:
            buttons = [[InlineKeyboardButton(text='Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ 🔖', url=f"https://t.me/{UPDATE_CHANNEL}")]]
            if m.text:
                if (len(m.text.split(' ')) > 1) & ('start' in m.text):
                    chat_id, msg_id = m.text.split(' ')[1].split('_')
                    buttons.append([InlineKeyboardButton('🔄 Rᴇғʀᴇsʜ', callback_data=f'refresh+{chat_id}+{msg_id}')])
            await m.reply_text(
                f"Hey {m.from_user.mention(style='md')} ʏᴏᴜ ɴᴇᴇᴅ ᴊᴏɪɴ Mʏ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ ɪɴ ᴏʀᴅᴇʀ ᴛᴏ ᴜsᴇ ᴍᴇ 😉\n\n"
                "__Pʀᴇss ᴛʜᴇ Fᴏʟʟᴏᴡɪɴɢ Bᴜᴛᴛᴏɴ ᴛᴏ ᴊᴏɪɴ Nᴏᴡ 👇__",
                reply_markup=InlineKeyboardMarkup(buttons),
                quote=True
            )
            return
        except Exception as e:
            print(e)
            await m.reply_text(f"Sᴏᴍᴇᴛʜɪɴɢ Wʀᴏɴɢ. Pʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ ᴏʀ ᴄᴏɴᴛᴀᴄᴛ {owner.mention(style='md')}", quote=True)
            return
    await m.continue_propagation()


@Client.on_callback_query(filters.regex('^refresh'))
async def refresh_cb(c, m):
    owner = await c.get_users(int(OWNER_ID))
    if UPDATE_CHANNEL:
        try:
            user = await c.get_chat_member(UPDATE_CHANNEL, m.from_user.id)
            if user.status == "kicked":
               try:
                   await m.message.edit("**Yᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ ɪɴ Oᴜʀ ᴄʜᴀɴɴᴇʟ Cᴏɴᴛᴀᴄᴛ Aᴅᴍɪɴ 😜**")
               except:
                   pass
               return
        except UserNotParticipant:
            await m.answer('Yᴏᴜ ᴀʀᴇ ɴᴏᴛ ʏᴇᴛ ᴊᴏɪɴᴇᴅ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ. \nFɪʀsᴛ ᴊᴏɪɴ ᴀɴᴅ ᴛʜᴇɴ ᴘʀᴇss ʀᴇғʀᴇsʜ ʙᴜᴛᴛᴏɴ 🤤', show_alert=True)
            return
        except Exception as e:
            print(e)
            await m.message.edit(f"Sᴏᴍᴇᴛʜɪɴɢ Wʀᴏɴɢ. Pʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ ᴏʀ ᴄᴏɴᴛᴀᴄᴛ{owner.mention(style='md')}")
            return

    cmd, chat_id, msg_id = m.data.split("+")
    msg = await c.get_messages(int(chat_id), int(msg_id)) if not DB_CHANNEL_ID else await c.get_messages(int(DB_CHANNEL_ID), int(msg_id))
    if msg.empty:
        return await m.reply_text(f"🥴 Sᴏʀʀʏ ʙʀᴏ ʏᴏᴜʀ ғɪʟᴇ ᴡᴀs ᴍɪssɪɴɢ\n\nPʟᴇᴀsᴇ ᴄᴏɴᴛᴀᴄᴛ ᴍʏ ᴏᴡɴᴇʀ 👉 {owner.mention(style='md')}")

    caption = msg.caption.markdown
    as_uploadername = (await get_data(str(chat_id))).up_name
    if as_uploadername:
        if chat_id.startswith('-100'): #if file from channel
            channel = await c.get_chat(int(chat_id))
            caption += "\n\n\n**--Uᴘʟᴏᴀᴅᴇʀ Dᴇᴛᴀɪʟs:--**\n\n"
            caption += f"**📢 Cʜᴀɴɴᴇʟ Nᴀᴍᴇ:** __{channel.title}__\n\n"
            caption += f"**🗣 Usᴇʀ Nᴀᴍᴇ:** @{channel.username}\n\n" if channel.username else ""
            caption += f"**👤 Cʜᴀɴɴᴇʟ Iᴅ:** __{channel.id}__\n\n"
        
        else: #if file not from channel
            user = await c.get_users(int(chat_id))
            caption += "\n\n\n**--Uᴘʟᴏᴀᴅᴇʀ Dᴇᴛᴀɪʟs:--**\n\n"
            caption += f"**🍁 Nᴀᴍᴇ:** [{user.from_user.first_name}](tg://user?id={user.from_user.id})\n\n"
            caption += f"**🖋 Usᴇʀ Nᴀᴍᴇ:** @{user.username}\n\n" if user.username else ""



    await msg.copy(m.from_user.id, caption=caption)
    await m.message.delete()
