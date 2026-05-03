
import os
from flask import Flask
import threading

# التوكن والـ ID الخاص بك (جاهزين للعمل)
API_TOKEN = '8532444113:AAHrWpDY4CuE_94s75FDSgLpVOiMsqjqUgg'
MY_CHAT_ID = '1035541584' 

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is Live and Running!"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! أنا بوت BingX المطور. أعمل الآن بنظام الحماية المستقر. 🚀")

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    # إرسال تنبيه لك بكل رسالة
    user_info = f"وصلت رسالة جديدة!\nمن: {message.from_user.first_name}\nالنص: {message.text}"
    bot.send_message(MY_CHAT_ID, user_info)
    # الرد على المستخدم
    bot.reply_to(message, "تم استلام رسالتك بنجاح سيتم الرد عليك قريباً.")

def run_bot():
    bot.polling(none_stop=True)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

