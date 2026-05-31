import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import os
import time

# =========================
# CONFIG
# =========================

BOT_TOKEN = "8869788533:AAFsBKHuV-tPlYO9CCPZh-yItEms55hm6Xs"
ADMIN_ID = 6859793726

bot = telebot.TeleBot(BOT_TOKEN)

USERS_FILE = "users.json"
LANG_FILE = "language.json"

# =========================
# FILE SYSTEM
# =========================

def load_users():
    if not os.path.exists(USERS_FILE):
        return []

    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_user(user_id):
    users = load_users()

    if user_id not in users:
        users.append(user_id)

        with open(USERS_FILE, "w") as f:
            json.dump(users, f)

def load_lang():
    if not os.path.exists(LANG_FILE):
        return {}

    with open(LANG_FILE, "r") as f:
        return json.load(f)

def save_lang(user_id, lang):
    data = load_lang()

    data[str(user_id)] = lang

    with open(LANG_FILE, "w") as f:
        json.dump(data, f)

# =========================
# START
# =========================

@bot.message_handler(commands=['start'])
def start(message):

    save_user(message.chat.id)

    text = """
🔥 *WELCOME TO ELITE CHAT ID BOT* 🔥

━━━━━━━━━━━━━━━━━━
⚡ Instant Telegram Chat ID
🌍 Hindi + English Mode
📋 One Tap Copy System
🚀 Ultra Fast Response
━━━━━━━━━━━━━━━━━━

👇 Click Below To Continue
"""

    markup = InlineKeyboardMarkup()

    a = InlineKeyboardButton(
        "🆔 Get Any Chat ID",
        callback_data="chatid"
    )

    b = InlineKeyboardButton(
        "🤖 More Useful Bots",
        url="https://t.me/EliteHubZone"
    )

    markup.add(a)
    markup.add(b)

    bot.send_message(
        message.chat.id,
        text,
        parse_mode="Markdown",
        reply_markup=markup
    )

# =========================
# CALLBACKS
# =========================

@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    # =========================
    # LANGUAGE SELECT
    # =========================

    if call.data == "chatid":

        markup = InlineKeyboardMarkup()

        h = InlineKeyboardButton(
            "🇮🇳 Hindi",
            callback_data="hindi"
        )

        e = InlineKeyboardButton(
            "🇺🇸 English",
            callback_data="english"
        )

        back = InlineKeyboardButton(
            "🔙 Back",
            callback_data="back"
        )

        markup.add(h, e)
        markup.add(back)

        bot.edit_message_text(
            """
🌍 Choose Your Language

अपनी भाषा चुनें 👇
""",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    # =========================
    # HINDI
    # =========================

    elif call.data == "hindi":

        save_lang(call.message.chat.id, "hindi")

        markup = InlineKeyboardMarkup()

        back = InlineKeyboardButton(
            "🔙 Back",
            callback_data="back"
        )

        markup.add(back)

        bot.edit_message_text(
            """
🔥 💬 मुझे कोई भी मैसेज भेजो 😛
कुछ भी लिख सकते हो ✍️🔥
👉 Example: “हैलो भाई 😂”
🤖 मैं तुम्हारा Chat ID बता दूंगा 👀⚡
""",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    # =========================
    # ENGLISH
    # =========================

    elif call.data == "english":

        save_lang(call.message.chat.id, "english")

        markup = InlineKeyboardMarkup()

        back = InlineKeyboardButton(
            "🔙 Back",
            callback_data="back"
        )

        markup.add(back)

        bot.edit_message_text(
            """
🔥 Send Me Any Message

📩 Whatever You Send
I Will Instantly Give Your Telegram Chat ID 😈

⚡ Fast System
📋 Copy Friendly
🚀 Ultra Secure
""",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    # =========================
    # BACK
    # =========================

    elif call.data == "back":

        markup = InlineKeyboardMarkup()

        a = InlineKeyboardButton(
            "🆔 Get Any Chat ID",
            callback_data="chatid"
        )

        b = InlineKeyboardButton(
            "🤖 More Useful Bots",
            url="https://t.me/EliteHubZone"
        )

        markup.add(a)
        markup.add(b)

        bot.edit_message_text(
            """
🔥 *WELCOME TO ELITE CHAT ID BOT* 🔥

━━━━━━━━━━━━━━━━━━
⚡ Instant Telegram Chat ID
🌍 Hindi + English Mode
📋 One Tap Copy System
🚀 Ultra Fast Response
━━━━━━━━━━━━━━━━━━

👇 Click Below To Continue
""",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=markup
        )

# =========================
# MAIN MESSAGE SYSTEM
# =========================

@bot.message_handler(func=lambda message: True)
def main(message):

    save_user(message.chat.id)

    # =========================
    # BROADCAST
    # =========================

    if (
        message.chat.id == ADMIN_ID
        and message.text
        and message.text.startswith("/send")
    ):

        msg = message.text.replace("/send", "").strip()

        users = load_users()

        total = 0

        for user in users:

            try:
                bot.send_message(
                    user,
                    f"📢 ADMIN MESSAGE\n\n{msg}"
                )

                total += 1

            except:
                pass

        bot.reply_to(
            message,
            f"✅ Sent To {total} Users"
        )

        return

    # =========================
    # LANGUAGE CHECK
    # =========================

    langs = load_lang()

    user_lang = langs.get(str(message.chat.id), "english")

    # =========================
    # PROCESSING BAR
    # =========================

    processing = bot.send_message(
        message.chat.id,
        "🔍 Processing Request..."
    )

    for i in range(1, 11):

        filled = "█" * i
        empty = "░" * (10 - i)

        bot.edit_message_text(
            f"""
⚡ Processing Your Request...

[{filled}{empty}] {i*10}%
""",
            message.chat.id,
            processing.message_id
        )

        time.sleep(1)

    # =========================
    # EXTRA EFFECT MESSAGES
    # =========================

    if user_lang == "english":

        msgs = [
            "🔎 We are detecting your account...",
            "📡 Connecting to Telegram servers...",
            "🔐 Encrypting secure response...",
            "⚡ Finalizing your Chat ID..."
        ]

    else:

        msgs = [
            "🔎 आपका अकाउंट डिटेक्ट किया जा रहा है...",
            "📡 Telegram सर्वर से कनेक्ट हो रहा है...",
            "🔐 Secure Response तैयार किया जा रहा है...",
            "⚡ आपका Chat ID तैयार हो रहा है..."
        ]

    for x in msgs:

        bot.send_message(
            message.chat.id,
            x
        )

        time.sleep(2)

    # =========================
    # CHAT ID RESULT
    # =========================

    chat_id = message.chat.id

    if user_lang == "english":

        final = f"""
✅ 𝗬𝗢𝗨𝗥 𝗧𝗘𝗟𝗘𝗚𝗥𝗔𝗠 𝗖𝗛𝗔𝗧 𝗜𝗗 😈

━━━━━━━━━━━━━━━━━━
🆔 CHAT ID :

`{chat_id}`

━━━━━━━━━━━━━━━━━━
⚡ Tap To Copy
🚀 Generated Successfully
🔐 Keep It Secure
━━━━━━━━━━━━━━━━━━
"""

        copy_text = "📋 Copy Chat ID"

    else:

        final = f"""
✅ 𝗔𝗣𝗞𝗔 𝗧𝗘𝗟𝗘𝗚𝗥𝗔𝗠 𝗖𝗛𝗔𝗧 𝗜𝗗 😈

━━━━━━━━━━━━━━━━━━
🆔 CHAT ID :

`{chat_id}`

━━━━━━━━━━━━━━━━━━
⚡ ऊपर Tap करके Copy करें
🚀 Successfully Generate हो गया
🔐 इसे सुरक्षित रखें
━━━━━━━━━━━━━━━━━━
"""

        copy_text = "📋 Chat ID Copy करें"

    markup = InlineKeyboardMarkup()

    copy = InlineKeyboardButton(
        copy_text,
        switch_inline_query=str(chat_id)
    )

    bots = InlineKeyboardButton(
        "🤖 More Bots Here",
        url="https://t.me/EliteHubZone"
    )

    back = InlineKeyboardButton(
        "🔙 Back",
        callback_data="back"
    )

    markup.add(copy)
    markup.add(bots)
    markup.add(back)

    bot.send_message(
        message.chat.id,
        final,
        parse_mode="Markdown",
        reply_markup=markup
    )

# =========================
# PHOTO BROADCAST
# =========================

@bot.message_handler(content_types=['photo'])
def photo_handler(message):

    if message.chat.id != ADMIN_ID:
        return

    users = load_users()

    caption = message.caption if message.caption else ""

    for user in users:

        try:

            bot.send_photo(
                user,
                message.photo[-1].file_id,
                caption=caption
            )

        except:
            pass

# =========================
# AUDIO BROADCAST
# =========================

@bot.message_handler(content_types=['audio'])
def audio_handler(message):

    if message.chat.id != ADMIN_ID:
        return

    users = load_users()

    for user in users:

        try:

            bot.send_audio(
                user,
                message.audio.file_id
            )

        except:
            pass

# =========================
# RUN
# =========================

print("🔥 BOT RUNNING 🔥")

bot.infinity_polling()
