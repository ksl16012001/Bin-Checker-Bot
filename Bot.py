import requests
from pyrogram import Client, filters
from configs import config
from asyncio import sleep
import ntplib
import time

from pyrogram.types import (
    Message, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup
)

# Hàm đồng bộ thời gian
def sync_time():
    try:
        client = ntplib.NTPClient()
        response = client.request('pool.ntp.org')  # Sử dụng server NTP đáng tin cậy
        current_time = time.ctime(response.tx_time)
        print(f"Thời gian đã đồng bộ: {current_time}")
    except Exception as e:
        print(f"Lỗi khi đồng bộ thời gian: {e}")

Bot = Client(
    ":memory:",
    api_hash=config.API_HASH,
    api_id=config.API_ID,
    bot_token=config.BOT_TOKEN,
)

@Bot.on_message(filters.command("start"))
async def start(_, m: Message):
    messy = m.from_user.mention
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Channel", url="https://t.me/szteambots"),
                InlineKeyboardButton("Support", url="https://t.me/slbotzone"),
            ],
            [
                InlineKeyboardButton(
                    "Source code", url="https://github.com/ImDenuwan/Bin-Checker-Bot"
                )
            ],
        ]
    )
    await m.reply_text(
        f"Hi! {messy} \nTôi có thể kiểm tra bin hợp lệ hay không.\n\nĐể biết thêm chi tiết, dùng lệnh /help",
        reply_markup=keyboard,
    )

@Bot.on_message(filters.command("help"))
async def help(_, m: Message):
    await m.reply_text(
        "/start - **Kiểm tra bot còn hoạt động không**.\n/help - **Xem menu trợ giúp.**\n/bin [bin] - **Kiểm tra Bin hợp lệ hay không.**"
    )

@Bot.on_message(filters.command("bin"))
async def bin(_, m: Message):
    if len(m.command) < 2:
        msg = await m.reply_text("Vui lòng cung cấp một Bin!\nVí dụ:- `/bin 401658`")
        await sleep(15)
        await msg.delete()
    else:
        try:
            mafia = await m.reply_text("Đang xử lý...")
            inputm = m.text.split(None, 1)[1]
            bincode = 6
            ask = inputm[:bincode]
            req = requests.get(f"https://madbin.herokuapp.com/api/{ask}").json()
            res = req["result"]

            if res == False:
                return await mafia.edit("❌ #BIN_KHÔNG_HỢP_LỆ ❌\n\nVui lòng cung cấp bin hợp lệ.")
            da = req["data"]
            bi = da["bin"]
            ve = da["vendor"]
            ty = da["type"]
            le = da["level"]
            ban = da["bank"]
            co = da["country"]
            cc = da["countryInfo"]
            nm = cc["name"]
            em = cc["emoji"]
            cod = cc["code"]
            dial = cc["dialCode"]

            mfrom = m.from_user.mention
            caption = f"""
    ╔ Hợp lệ :- `{res} ✅`\n╚ Bin :- `{bi}`\n\n╔ Thương hiệu :- `{ve}`\n╠ Loại :- `{ty}`\n╚ Cấp độ :- `{le}`\n\n╔ Ngân hàng :- `{ban} ({co})`\n╠ Quốc gia :- `{nm} {em}`\n╠ Mã Alpha2 :- `{cod}`\n╚ Mã quay số :- `{dial}`\n\n**↠ Kiểm tra bởi :-** {mfrom}\n**↠ __Bot bởi :-** [Denuwan](https://github.com/ImDenuwan/Bin-Checker-Bot)__
    """
            await mafia.edit(caption, disable_web_page_preview=True)
            
        except Exception as e:
            await m.reply_text(f"**Lỗi xảy ra!**\n{e}\n\n**Báo lỗi này cho chủ bot.**")

# Gọi hàm đồng bộ thời gian trước khi chạy bot
print("Bot đang khởi động...")
sync_time()  # Đồng bộ thời gian
Bot.run()
