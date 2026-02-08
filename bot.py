import os
import time
import random
from flask import Flask
from threading import Thread
import telebot

# --- GIỮ CHO BOT SỐNG 24/7 ---
app = Flask('')
@app.route('/')
def home(): return "Bot War Vô Tận đang chạy..."

def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start()

# --- CẤU HÌNH BOT ---
TOKEN = '8230881435:AAHJ86xrpzGZ0NQMIKPY_ymeZ61uYwrPY7c' # Token của bạn
bot = telebot.TeleBot(TOKEN)

# Biến để kiểm soát việc dừng bot
is_warring = {}

DANH_SACH_CHUI = [
    "Thằng nhóc ác này, tuổi gì mà đòi war?",
    "Gõ phím nhanh lên xem nào, chậm thế!",
    "Câm nín luôn rồi à? Sao không sủa tiếp đi?",
    "Nhìn mày gõ phím mà tao thấy tội nghiệp luôn á.",
    "Sủa mạnh lên, âm lượng hơi bé đấy em ơi!",
    "Đang gõ mà bị gãy tay à sao thấy im re thế?",
    "Trình độ này mà cũng đòi làm hacker à?",
    "Về nhà học lại cách gõ phím đi nhé em trai."
]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Bot War Vô Tận sẵn sàng! \n- Gõ /war để bắt đầu \n- Gõ /stop để dừng lại.")

@bot.message_handler(commands=['stop'])
def stop_war(message):
    is_warring[message.chat.id] = False
    bot.reply_to(message, "Đã đình chiến! Bot nghỉ ngơi đây. 🏳️")

@bot.message_handler(commands=['war'])
def start_war(message):
    chat_id = message.chat.id
    if is_warring.get(chat_id):
        bot.reply_to(message, "Bot đang chiến rồi, không cần bấm nữa đâu!")
        return

    is_warring[chat_id] = True
    bot.reply_to(message, "Chế độ đồ sát vô tận ĐÃ BẬT! 🔥🔥🔥")
    
    while is_warring.get(chat_id):
        try:
            cau_chui = random.choice(DANH_SACH_CHUI)
            bot.send_message(chat_id, cau_chui)
            # Nghỉ 1.5 giây để tránh bị Telegram chặn (Flood Wait)
            time.sleep(0) 
        except Exception as e:
            print(f"Lỗi: {e}")
            time.sleep(0) # Nếu lỗi thì nghỉ 5s rồi thử lại
