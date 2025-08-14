import streamlit as st
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import asyncio
import nest_asyncio

nest_asyncio.apply()

TOKEN = "8350284060:AAELTkDNIEt_oWP-ZXYDRlo_eBSofz2cziA"

async def start(update, context):
    print("Start komutu geldi")
    await update.message.reply_text("Merhaba! Bu bot Streamlit içinden çalışıyor 🚀")

async def echo(update, context):
    print("Mesaj geldi:", update.message.text)
    await update.message.reply_text(f"Aldım: {update.message.text}")

async def run_bot():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    await app.run_polling(stop_signals=None)

st.title("📩 Telegram Bot Kontrol Paneli")
if st.button("Botu Başlat"):
    st.write("Bot çalışmaya başladı... Telegram'dan deneyebilirsin.")
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())
