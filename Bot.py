import telebot
from telebot import types # Untuk membuat tombol/keyboard
import yt_dlp
import os
import uuid

TOKEN = '6440891289:AAFPyx0EDNbLxTMYFkAajc0C5dge3D97T8I'
bot = telebot.TeleBot(TOKEN)

# --- FUNGSI UTAMA MENU ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('📥 Download Video')
    btn2 = types.KeyboardButton('🎵 Download MP3')
    btn3 = types.KeyboardButton('ℹ️ Info Bot')
    markup.add(btn1, btn2, btn3)
    return markup

# --- HANDLER /START ---
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        f"Halo {message.from_user.first_name}! 👋\n\n"
        "Selamat datang di Downloader Bot.\n"
        "Silakan pilih menu di bawah atau langsung kirim link video."
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu())

# --- HANDLER TOMBOL MENU BAWAH ---
@bot.message_handler(func=lambda message: True)
def handle_menu(message):
    if message.text == '📥 Download Video':
        bot.reply_to(message, "Silakan kirimkan link TikTok/IG/YouTube yang ingin kamu download.")
    elif message.text == '🎵 Download MP3':
        bot.reply_to(message, "Kirimkan linknya, saya akan ambil audionya saja untukmu.")
    elif message.text == 'ℹ️ Info Bot':
        bot.reply_to(message, "Bot ini dibuat untuk mendownload konten media dari media sosial.\n\nSupport: YT, IG, TikTok, FB.")
    
    # Jika pesan berupa link (Deteksi otomatis)
    elif message.text.startswith('http'):
        ask_format(message)

# --- MENU INLINE (TOMBOL DI BAWAH PESAN) ---
def ask_format(message):
    url = message.text
    markup = types.InlineKeyboardMarkup()
    # Kita simpan URL di callback_data (Hati-hati: limit callback_data 64 karakter)
    # Untuk link panjang, sebaiknya simpan di database/variabel sementara
    btn_vid = types.InlineKeyboardButton("🎬 Video (MP4)", callback_data=f"vid|{url[:50]}")
    btn_aud = types.InlineKeyboardButton("🎧 Audio (MP3)", callback_data=f"aud|{url[:50]}")
    markup.add(btn_vid, btn_aud)
    
    bot.send_message(message.chat.id, "Pilih format yang diinginkan:", reply_markup=markup)

# --- HANDLER TOMBOL INLINE ---
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    action, short_url = call.data.split("|")
    # Karena tadi link dipotong, kita ambil link asli dari pesan sebelumnya
    original_url = call.message.reply_to_message.text if call.message.reply_to_message else short_url
    
    bot.edit_message_text("Sedang diproses... Mohon tunggu ⏳", call.message.chat.id, call.message.message_id)
    
    file_id = str(uuid.uuid4())
    
    if action == "vid":
        ext = "mp4"
        ydl_opts = {'format': 'best', 'outtmpl': f'{file_id}.%(ext)s'}
    else:
        ext = "mp3"
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{file_id}.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(original_url, download=True)
            filename = ydl.prepare_filename(info)
            # Jika MP3, nama filenya mungkin berubah jadi .mp3 setelah diproses
            if action == "aud": filename = filename.rsplit('.', 1)[0] + ".mp3"

        with open(filename, 'rb') as f:
            if action == "vid":
                bot.send_video(call.message.chat.id, f, caption="Ini videonya! ✅")
            else:
                bot.send_audio(call.message.chat.id, f, caption="Ini audionya! 🎧")
        
        os.remove(filename)
        bot.delete_message(call.message.chat.id, call.message.message_id)

    except Exception as e:
        bot.send_message(call.message.chat.id, f"Terjadi kesalahan: {str(e)[:100]}")

bot.infinity_polling()
    
