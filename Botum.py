import streamlit as st
from telegram.ext import Application, CommandHandler
import asyncio

# Bot tokenını buraya yaz
TOKEN = "8350284060:AAELTkDNIEt_oWP-ZXYDRlo_eBSofz2cziA"

# Bot komutları
async def start(update, context):
    await update.message.reply_text("Merhaba! Bu bot Streamlit içinden çalışıyor 🚀")

# Botu başlatan fonksiyon
async def run_bot():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    await app.run_polling()

# Streamlit arayüzü
st.title("📩 Telegram Bot Kontrol Paneli")
st.write("Bu bot Streamlit ile başlatıldı. /start yazınca yanıt verecek.")

# Botu çalıştırma butonu
if st.button("Botu Başlat"):
    st.write("Bot çalışmaya başladı... Telegram'dan deneyebilirsin.")
    asyncio.run(run_bot())
