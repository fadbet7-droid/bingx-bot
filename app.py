import telebot
from telebot import types

TOKEN = '8532444113:AAF8YmyQGBy87kN49p4ryD8wgNAv42Sl0yQ'
ADMIN_ID = 6085684684
bot = telebot.TeleBot(TOKEN)
user_status = {}

def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add("لديك قسيمة بينغ اكس", "سحب الارباح", "حملة باينانس")
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "أهلاً وسهلاً بك، اختر من القائمة أدناه:", reply_markup=main_menu())

@bot.message_handler(func=lambda message: message.chat.id != ADMIN_ID)
def handle_users(message):
    cid = message.chat.id
    if message.text == "لديك قسيمة بينغ اكس":
        user_status[cid] = 'bingx'
        bot.send_message(cid, "يرجى إرسال صور القسيمة والمتداولين.")
    elif message.text == "سحب الارباح":
        user_status[cid] = 'withdraw'
        bot.send_message(cid, "يرجى إرسال آي دي الحساب على بينغ اكس.")
    elif message.text == "حملة باينانس":
        user_status[cid] = 'binance'
        bot.send_message(cid, "يرجى كتابة الاستفسارات الخاصة بك.")
    else:
        status = user_status.get(cid)
        info = f"👤 من: @{message.from_user.username} | ID: {cid}\n"
        if status == 'bingx':
            bot.forward_message(ADMIN_ID, cid, message.message_id)
            bot.send_message(ADMIN_ID, info + "الطلب: قسيمة")
            bot.send_message(cid, "سيتم الرد عليك بأقرب وقت ممكن.")
        elif status == 'withdraw':
            bot.send_message(ADMIN_ID, info + f"الطلب: سحب\nالبيانات: {message.text}")
            bot.send_message(cid, "يرجى الانتظار سيتم وصلك مع المتداول لسحب ارباحك.")
        elif status == 'binance':
            bot.send_message(ADMIN_ID, info + f"الطلب: استفسار\nالبيانات: {message.text}")
            bot.send_message(cid, "سيتم الرد عليك قريباً.")

@bot.message_handler(func=lambda message: message.chat.id == ADMIN_ID and message.reply_to_message)
def reply_to_user(message):
    try:
        text = message.reply_to_message.text or message.reply_to_message.caption
        target_id = [int(s) for s in text.split() if s.isdigit()][0]
        bot.send_message(target_id, f"رد من الإدارة:\n\n{message.text}")
        bot.send_message(ADMIN_ID, "✅ تم إرسال ردك.")
    except:
        bot.send_message(ADMIN_ID, "❌ اعمل رد (Reply) على رسالة فيها ID المستخدم.")

bot.infinity_polling()
