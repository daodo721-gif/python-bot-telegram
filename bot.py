import os
import time
import random # Thêm thư viện để chọn ngẫu nhiên
from flask import Flask
from threading import Thread
import telebot

# --- PHẦN GIỮ CHO BOT SỐNG ---
app = Flask('')
@app.route('/')
def home(): return "Bot War đang online!"

def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start()

# --- PHẦN CODE BOT CHIẾN ---
TOKEN = '8230881435:AAHJ86xrpzGZ0NQMIKPY_ymeZ61uYwrPY7c' # Thay Token của bạn vào đây
bot = telebot.TeleBot(TOKEN)

# Danh sách các câu chửi/war mẫu (Bạn có thể thêm bớt tùy ý)
DANH_SACH_CHUI = [
    "Thằng nhóc ác này, tuổi gì mà đòi war?",
    "Gõ phím nhanh lên xem nào, chậm thế!",
    "Trình độ này mà cũng đòi làm hacker à?",
    "Về nhà học lại cách gõ phím đi nhé em trai.",
    "Câm nín luôn rồi à? Sao không sủa tiếp đi?",
    "Đang gõ mà bị gãy tay à sao thấy im re thế?",
    "Nhìn mày gõ phím mà tao thấy tội nghiệp luôn á.",
    "Sủa mạnh lên, âm lượng hơi bé đấy em ơi!"
]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Bot War đã sẵn sàng! Gõ /war để bắt đầu xả đạn.")

@bot.message_handler(commands=['war'])
def start_war(message):
    bot.reply_to(message, "Đang tiến hành xả đạn vào mục tiêu... 🔥")
    
    # Bot sẽ gửi 30 câu ngẫu nhiên từ danh sách trên
    for i in range(30):
        # Chọn ngẫu nhiên 1 câu trong danh sách
        cau_chui = random.choice(DANH_SACH_CHUI)
        bot.send_message(message.chat.id, cau_chui)
        
        # Nghỉ 1.2 giây để tránh bị Telegram khóa (Ban)
        time.sleep(1.2)

if __name__ == "__main__":
    keep_alive()
    print("Bot War Ready!")
    bot.infinity_polling()
