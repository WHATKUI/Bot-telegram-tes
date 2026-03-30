import telebot

# Ganti 'TOKEN_KAMU' dengan token dari BotFather
TOKEN = 'TOKEN_KAMU'
bot = telebot.TeleBot(TOKEN)

# Menangani perintah /start dan /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Halo! Saya adalah bot asisten grup kamu. Ada yang bisa saya bantu?")

# Menangani pesan saat ada anggota baru masuk (khusus Grup)
@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    for new_user in message.new_chat_members:
        bot.send_message(message.chat.id, f"Selamat datang {new_user.first_name} di grup kami! Jangan lupa baca aturan ya.")

# Menangani pesan teks biasa (contoh: auto-response)
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if "info" in message.text.lower():
        bot.reply_to(message, "Grup ini adalah wadah diskusi komunitas. Gunakan bahasa yang sopan ya!")

print("Bot sedang berjalan...")
bot.infinity_polling()
