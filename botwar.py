import telebot
import time
import random
import os
from threading import Thread
from flask import Flask

# --- CẤU HÌNH CƠ BẢN ---
TOKEN = '8230881435:AAHJ86xrpzGZ0NQMIKPY_ymeZ61uYwrPY7c'
ADMIN_ID = 5457141246
bot = telebot.TeleBot(TOKEN)

# --- DỮ LIỆU ---
authorized_users = [ADMIN_ID]
user_tasks = {} # Lưu task: {user_id: ["task1", "task2"]}
is_running = {} # Trạng thái treo: {chat_id: True/False}

# Danh sách từ ngữ (Cụ tự sửa/thêm vào đây)
NGON_NHAY = ["Nhây tí cho vui nào!", "Sao im re thế?", "Gõ phím tiếp đi em!", "Trình độ này chưa đủ đâu."]
NGON_WAR = ["Đồ nhóc con!", "Tuổi gì mà đòi chiến?", "Về nhà học thêm đi!", "Sủa mạnh lên xem nào!"]
NGON_SPAM = ["Đang spam nhé...", "Spam liên tục...", "Đứng máy chưa em?"]

# --- GIỮ BOT SỐNG 24/7 ---
app = Flask('')
@app.route('/')
def home(): return "Bot đang Online!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# --- HÀM KIỂM TRA QUYỀN ---
def is_authorized(user_id):
    return user_id in authorized_users

# --- CÁC LỆNH QUẢN LÝ ---
@bot.message_handler(commands=['start', 'menu', 'help'])
def send_menu(message):
    help_text = """
🔥 MENU BOT WAR PRO 🔥
/taska - Xem danh sách người có task
/addtask <id> - Thêm quyền dùng bot (Admin)
/deltask <id> - Xóa quyền dùng bot (Admin)
/meta - Hỏi Meta AI
/nhay - Nhây khịa đối phương
/war - War tổng lực
/spam <câu> - Spam 1 câu duy nhất
/treo <loại> <vohan> [@tag] - Treo tự động
/stop - Dừng mọi hoạt động
    """
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['addtask'])
def add_task_user(message):
    if message.from_user.id != ADMIN_ID: return
    try:
        new_id = int(message.text.split()[1])
        authorized_users.append(new_id)
        bot.reply_to(message, f"✅ Đã thêm ID {new_id} vào danh sách sử dụng.")
    except: bot.reply_to(message, "Sử dụng: /addtask <ID_USER>")

@bot.message_handler(commands=['taska'])
def show_tasks(message):
    res = "👥 Người dùng có quyền: " + ", ".join(map(str, authorized_users))
    bot.reply_to(message, res)

# --- CHỨC NĂNG CHIẾN ĐẤU ---
def attack_loop(chat_id, word_list, tag="", speed=1.2):
    is_running[chat_id] = True
    while is_running.get(chat_id):
        try:
            msg = f"{random.choice(word_list)} {tag}"
            bot.send_message(chat_id, msg)
            time.sleep(speed)
        except: break

@bot.message_handler(commands=['war'])
def war_cmd(message):
    if not is_authorized(message.from_user.id): return
    # Cú pháp: /war @user 0.5
    args = message.text.split()
    tag = args[1] if len(args) > 1 else ""
    speed = float(args[2]) if len(args) > 2 else 1.0
    bot.reply_to(message, f"🚀 Bắt đầu War vào {tag} với tốc độ {speed}s!")
    attack_loop(message.chat.id, NGON_WAR, tag, speed)

@bot.message_handler(commands=['treo'])
def treo_cmd(message):
    if not is_authorized(message.from_user.id): return
    args = message.text.split()
    if len(args) < 3: return
    
    mode = args[1] # nhay, war, spam
    tag = args[3] if len(args) > 3 else ""
    
    if mode == 'nhay': words = NGON_NHAY
    elif mode == 'war': words = NGON_WAR
    else: words = NGON_SPAM
    
    bot.reply_to(message, f"⏳ Đang treo chế độ {mode} {tag}...")
    attack_loop(message.chat.id, words, tag, 1.5)

@bot.message_handler(commands=['spam'])
def spam_cmd(message):
    if not is_authorized(message.from_user.id): return
    text_to_spam = message.text.replace('/spam', '').strip()
    if not text_to_spam: return
    is_running[message.chat.id] = True
    while is_running.get(message.chat.id):
        bot.send_message(message.chat.id, text_to_spam)
        time.sleep(0)

@bot.message_handler(commands=['stop'])
def stop_all(message):
    is_running[message.chat.id] = False
    bot.reply_to(message, "🛑 Đã dừng chửi nhau!")

@bot.message_handler(commands=['meta'])
def meta_ai(message):
    bot.reply_to(message, "🤖 Meta AI đang bận chửi lộn, vui lòng thử lại sau!")

# --- CHẠY BOT ---
if __name__ == "__main__":
    keep_alive()
    print("bot đang chạy by - cracker!")
    bot.infinity_polling()
