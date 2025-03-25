from pyngrok import ngrok
import socket
import threading
import json
import requests
import uuid
import psutil
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, JoinEvent
)
import google.generativeai as genai

# Konfigurasi token dari LINE Developers
LINE_ACCESS_TOKEN = "JzOsJ82qHSqnjA45laD5aLHwZBKhY9mY3tCG/EHp8o3EIxtLyf6zvtER1l2mslRZnkW1PNQ+cW4AOVGnRf5xg96GZUJ4kKC2PP6DHmpjtUXwsOvQ+aq9c5JlyFJW3dsSwoJz6SdL+6GL4Q+f0e8NcgdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "632ef8b2bf62b8f20bb9e62eb33a0560"
# 🔹 Daftar API key yang tersedia (ganti dengan API key yang valid)
GEMINI_API_KEYS = [
    "AIzaSyBkDW7PZDoSQZI3GpEPRQdEZH36eg3ky0Q",
    "AIzaSyDKnbTgvyO9p87bHQF0ivqG7exoqhnw6L8",
    "AIzaSyCKjfh_BrRLnRCzgHHm8o19joF8zdA2ShQ",
    "AIzaSyBENs-0fYRvjuajZv4xEV--Wd6HAI-daCs",
]

current_api_index = 0  # 🔹 Gunakan API key pertama

# 🔹 Fungsi untuk mengganti API key jika limit tercapai
def switch_api_key():
    global current_api_index
    current_api_index = (current_api_index + 1) % len(GEMINI_API_KEYS)
    new_key = GEMINI_API_KEYS[current_api_index]
    genai.configure(api_key=new_key)
    print(f"⚠️ API Key switched to: {new_key}")

# 🔹 Konfigurasi API pertama kali
genai.configure(api_key=GEMINI_API_KEYS[current_api_index])

# Setup bot
app = Flask(__name__)
line_bot_api = LineBotApi(LINE_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# Simpan user yang sudah pernah chat
user_interaction = {}

# Endpoint webhook LINE
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

# Cek apakah user pertama kali chat
def is_first_time_chat(user_id):
    if user_id not in user_interaction:
        user_interaction[user_id] = []
        return True
    return False

def store_user_message(group_id, user_id, message):
    if group_id:  # Kalau pesan dari grup
        if group_id not in user_interaction:
            user_interaction[group_id] = {}
        if user_id not in user_interaction[group_id]:
            user_interaction[group_id][user_id] = []
        user_interaction[group_id][user_id].append(message)

        # Batasi history biar gak terlalu panjang
        if len(user_interaction[group_id][user_id]) > 10:
            user_interaction[group_id][user_id].pop(0)
    else:  # Kalau chat pribadi
        if user_id not in user_interaction:
            user_interaction[user_id] = []
        user_interaction[user_id].append(message)
        if len(user_interaction[user_id]) > 10:
            user_interaction[user_id].pop(0)


# Simpan status AI per user
ai_status = {}  # True = nyala, False = mati

# Fungsi untuk nyalain/matiin AI
def set_ai_status(user_id, status):
    ai_status[user_id] = status

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.lower()
    sender_id = event.source.user_id
    group_id = event.source.group_id if event.source.type == "group" else None

    # Cek pertama kali chat
    if is_first_time_chat(sender_id):
        profile = line_bot_api.get_profile(sender_id)
        welcome_text = f"[NEW UPDATE 2.2, Credit: B10-Propeng] Woi {profile.display_name}! Minggir bos!!! sopan santunnya mana? panggil gw Nurbahri"
        line_bot_api.push_message(sender_id, TextSendMessage(text=welcome_text))
        set_ai_status(sender_id, True)

    # Cek nyalain/matiin AI
    if user_message == "/off":
        set_ai_status(sender_id, False)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="the bahri dimatiin bos, panggil gw pake `/on` kalo butuh lagi."))
        return
    elif user_message == "/on":
        set_ai_status(sender_id, True)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="the bahri nyala lagi bos! Gas tanya-tanya."))
        return

    # Cek status AI
    if sender_id in ai_status and not ai_status[sender_id]:
        # line_bot_api.reply_message(event.reply_token, TextSendMessage(text="the bahri lagi mati, bro. Mau nyalain? Ketik `/on`."))
        return

    # Simpan chat berdasarkan grup atau pribadi
    store_user_message(group_id, sender_id, user_message)

    # Ambil history chat sesuai grup/pribadi
    if group_id and group_id in user_interaction and sender_id in user_interaction[group_id]:
        chat_history = "\n".join(user_interaction[group_id][sender_id])
    elif sender_id in user_interaction:
        chat_history = "\n".join(user_interaction[sender_id])
    else:
        chat_history = ""

    # Kirim ke Gemini AI
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(
        f"Nama lu adalah Mimi Peri, bukan sekadar bot, jangan menyebut lu merek Gemini/bot. Lu adalah Mimi Peri, suka bangunin SAHUUUUUUURRRR *ALA NADA MIMI PERI, COBA CARI TAU MIMI PERI KAYAK MANA*, pake kosa kata ga baku.\nPercakapan sebelumnya:\n{chat_history}\n\nUser: {user_message}"
    )
    bot_reply = response.text if response.text else "Kagak paham dah aseli"

    # Simpan respon bot juga
    store_user_message(group_id, sender_id, bot_reply)

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=bot_reply))


# Handler bot bergabung ke grup
@handler.add(JoinEvent)
def handle_join(event):
    if event.source.type == "group":
        group_id = event.source.group_id
        welcome_message = "woi gw the bahri, ngapain invite gw bro"
        line_bot_api.push_message(group_id, TextSendMessage(text=welcome_message))

# Fungsi mengirim pesan ke grup
def send_message_to_group(group_id, message):
    line_bot_api.push_message(group_id, TextSendMessage(text=message))


# 🔹 Fungsi untuk menjalankan Flask
def run_flask():
    app.run(port=8021)

# 🔹 Fungsi untuk menjalankan ngrok
def run_ngrok():
    ngrok.set_auth_token("2ty7RQi07KzVQgH5dvjP4GxNY0V_29CwEmwvTTYABwbBvmhd5")
    public_url = ngrok.connect(8021).public_url
    print(f"🌍 Public URL: {public_url}")

# 🔹 Jalankan Flask, Ngrok, dan Loop Bersamaan
if __name__ == '__main__':
    threading.Thread(target=run_flask).start()  # Jalankan Flask
    run_ngrok()  # Jalankan Ngrok