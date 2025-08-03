import asyncio
import re
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# === KONFIGURASI ===
BOT_TOKEN = "8415211091:AAFzxOSn_JIyBXyBmDX4VNjseteoH2HePdI"
ADMIN_ID = 7974037486
ALLOWED_USERS = [7974037486, 6297978902]

# === DATA KUOTA ===
user_cp_quota = {}


# === UTILITAS ===
def extract_phone_number(text):
    text = text.replace(" ", "").replace("-", "")
    pattern = r'^(?:\+62|62|08)\d{7,15}$'
    match = re.search(pattern, text)
    if match:
        nomor = match.group()
        if nomor.startswith("+62"):
            nomor = "0" + nomor[3:]
        elif nomor.startswith("62"):
            nomor = "0" + nomor[2:]
        return nomor
    return None


def extract_nopol(text):
    clean = re.sub(r'[\s\-.]', '', text.upper())
    if re.match(r'^[A-Z]{1,2}\d{1,4}[A-Z]{1,3}$', clean):
        return clean
    return None


# === HANDLERS ===
async def handle_any_command(update: Update,
                             context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        await update.message.reply_text(
            "❌ Anda siapa? Bot ini bukan untuk anda!!!!")
        return

    username = update.effective_user.username or "Tanpa Username"
    text = update.message.text

    # Handle /cp
    if text.startswith("/cp"):
        parts = text.split(maxsplit=1)
        if len(parts) < 2:
            await update.message.reply_text(
                "⚠️ Format salah. Sertakan nomor setelah /cp\nContoh: /cp 0822xxxxxxx"
            )
            return
        nomor = extract_phone_number(parts[1])
        if not nomor:
            await update.message.reply_text(
                "❌ Nomor tidak valid. Gunakan format yang benar.")
            return
        if user_id not in user_cp_quota:
            user_cp_quota[user_id] = 0
        if user_cp_quota[user_id] >= 15:
            await update.message.reply_text(
                "❌ Kuota harian habis. Hubungi admin.")
            return
        user_cp_quota[user_id] += 1
        await update.message.reply_text("⏳ Mohon tunggu!!")
        message_to_admin = f"""📨 *Perintah dari User*

👤 *Username:* @{username}
🆔 *User ID:* `{user_id}`
💬 *Perintah:* /cp {nomor}

🛠️ Balas pakai:
/balas {user_id} <pesan>"""
        await context.bot.send_message(chat_id=ADMIN_ID,
                                       text=message_to_admin,
                                       parse_mode="Markdown")
        return

    # Handle /nik
    if text.startswith("/nik"):
        parts = text.split(maxsplit=1)
        if len(parts) < 2 or not re.fullmatch(r"\d{16}", parts[1]):
            await update.message.reply_text(
                "⚠️ Format salah. Sertakan 16 digit angka NIK.\nContoh: /nik 3276021234567890"
            )
            return
        nik = parts[1]
        await update.message.reply_text("⏳ Mohon tunggu!!")
        message_to_admin = f"""📨 *Perintah dari User*

👤 *Username:* @{username}
🆔 *User ID:* `{user_id}`
💬 *Perintah:* /nik {nik}

🛠️ Balas pakai:
/balas {user_id} <pesan>"""
        await context.bot.send_message(chat_id=ADMIN_ID,
                                       text=message_to_admin,
                                       parse_mode="Markdown")
        return

    # Handle /kk
    if text.startswith("/kk"):
        parts = text.split(maxsplit=1)
        if len(parts) < 2 or not re.fullmatch(r"\d{16}", parts[1]):
            await update.message.reply_text(
                "⚠️ Format salah. Sertakan 16 digit angka KK.\nContoh: /kk 3201234567890123"
            )
            return
        kk = parts[1]
        await update.message.reply_text("⏳ Mohon tunggu!!")
        message_to_admin = f"""📨 *Perintah dari User*

👤 *Username:* @{username}
🆔 *User ID:* `{user_id}`
💬 *Perintah:* /kk {kk}

🛠️ Balas pakai:
/balas {user_id} <pesan>"""
        await context.bot.send_message(chat_id=ADMIN_ID,
                                       text=message_to_admin,
                                       parse_mode="Markdown")
        return

    # Handle /reg
    if text.startswith("/reg"):
        parts = text.split(maxsplit=1)
        if len(parts) < 2:
            await update.message.reply_text(
                "⚠️ Format salah. Sertakan nomor HP atau NIK setelah /reg.\nContoh: /reg 082212345678 atau /reg 3276021234567890"
            )
            return
        value = parts[1].strip()
        nomor = extract_phone_number(value)
        if not nomor and not re.fullmatch(r"\d{16}", value):
            await update.message.reply_text(
                "❌ Format salah. Harus nomor HP valid atau NIK 16 digit.")
            return
        await update.message.reply_text("⏳ Mohon tunggu!!")
        message_to_admin = f"""📨 *Perintah dari User*

👤 *Username:* @{username}
🆔 *User ID:* `{user_id}`
💬 *Perintah:* /reg {value}

🛠️ Balas pakai:
/balas {user_id} <pesan>"""
        await context.bot.send_message(chat_id=ADMIN_ID,
                                       text=message_to_admin,
                                       parse_mode="Markdown")
        return

    # Handle /nopol
    if text.startswith("/nopol"):
        parts = text.split(maxsplit=1)
        if len(parts) < 2:
            await update.message.reply_text(
                "⚠️ Sertakan plat nomor.\n Contoh: /nopol B1234BZY")
            return
        nopol = extract_nopol(parts[1])
        if not nopol:
            await update.message.reply_text(
                "❌ Format nopol tidak valid. Contoh: /nopol B1234BZY")
            return
        await update.message.reply_text("⏳ Mohon tunggu!!")
        message_to_admin = f"""📨 *Perintah dari User*

👤 *Username:* @{username}
🆔 *User ID:* `{user_id}`
💬 *Perintah:* /nopol {nopol}

🛠️ Balas pakai:
/balas {user_id} <pesan>"""
        await context.bot.send_message(chat_id=ADMIN_ID,
                                       text=message_to_admin,
                                       parse_mode="Markdown")
        return

    # Handle /nama
    if text.startswith("/nama"):
        parts = text.split(maxsplit=1)
        if len(parts) < 2:
            await update.message.reply_text(
                "⚠️ Sertakan nama setelah /nama.\nContoh: /nama Rina Amelia")
            return
        nama = parts[1].strip()
        if len(nama) < 3:
            await update.message.reply_text("❌ Nama terlalu pendek.")
            return
        if not re.fullmatch(r"[A-Za-z\s\-]+", nama):
            await update.message.reply_text(
                "❌ Nama hanya boleh huruf, spasi, atau strip.")
            return
        await update.message.reply_text("⏳ Mohon tunggu!!")
        message_to_admin = f"""📨 *Perintah dari User*

👤 *Username:* @{username}
🆔 *User ID:* `{user_id}`
💬 *Perintah:* /nama {nama}

🛠️ Balas pakai:
/balas {user_id} <pesan>"""
        await context.bot.send_message(chat_id=ADMIN_ID,
                                       text=message_to_admin,
                                       parse_mode="Markdown")
        return

    # Default
    await update.message.reply_text("⏳ Mohon tunggu!!")
    message_to_admin = f"""📨 *Perintah dari User*

👤 *Username:* @{username}
🆔 *User ID:* `{user_id}`
💬 *Perintah:* {text}

🛠️ Balas pakai:
/balas {user_id} <pesan>"""
    await context.bot.send_message(chat_id=ADMIN_ID,
                                   text=message_to_admin,
                                   parse_mode="Markdown")


# === HANDLER LAIN ===
async def handle_invalid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        await update.message.reply_text(
            "❌ Anda siapa? Bot ini bukan untuk anda!!!!")
        return
    await update.message.reply_text("❌ Perintah tidak valid. Ketik /help.")


async def handle_admin_reply(update: Update,
                             context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    try:
        args = update.message.text.split(' ', 2)
        target_id = int(args[1])
        reply_text = args[2]
        await context.bot.send_message(chat_id=target_id,
                                       text=f"\n\n{reply_text}")
        await update.message.reply_text("✅ Pesan berhasil dikirim ke user.")
    except:
        await update.message.reply_text(
            "⚠️ Format salah. Gunakan:\n/balas <user_id> <pesan>")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        await update.message.reply_text(
            "❌ Anda siapa? Bot ini bukan untuk anda!!!!")
        return
    await update.message.reply_text(
        "Halo! Selamat datang dan selamat bertugas, keselamatan yang utama!!")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        await update.message.reply_text(
            "❌ Anda siapa? Bot ini bukan untuk anda!!!!")
        return
    help_text = ("📘 *Cara Penggunaan:*\n\n"
                 "`/cp 082212345678`\n"
                 "`/nik 3276021234567890`\n"
                 "`/kk 3201234567890123`\n"
                 "`/reg no hp atau nik`\n"
                 "`/nopol b1234bzy`\n"
                 "`/nama Rina Amelia`")
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def quota_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        await update.message.reply_text(
            "❌ Anda siapa? Bot ini bukan untuk anda!!!!")
        return
    used = user_cp_quota.get(user_id, 0)
    await update.message.reply_text(
        f"📊 Sisa kuota /cp hari ini: {15 - used} dari 15. Reset tiap jam 2 pagi."
    )


async def reset_quota_daily(context: ContextTypes.DEFAULT_TYPE):
    global user_cp_quota
    user_cp_quota = {}
    print("🔁 Kuota CP direset.")


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    now = datetime.now()
    reset_time = datetime.combine(now.date(),
                                  datetime.min.time()) + timedelta(hours=2)
    if now > reset_time:
        reset_time += timedelta(days=1)
    delay = (reset_time - now).total_seconds()

    app.job_queue.run_once(reset_quota_daily, when=delay)
    app.job_queue.run_repeating(reset_quota_daily, interval=86400, first=delay)

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("quota", quota_command))
    app.add_handler(CommandHandler("balas", handle_admin_reply))
    app.add_handler(MessageHandler(filters.COMMAND, handle_any_command))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_invalid))

    print("🤖 Bot aktif! Menunggu pesan...")
    app.run_polling()


if __name__ == "__main__":
    main()
