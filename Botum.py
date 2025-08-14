import streamlit as st
from telegram.ext import Application, CommandHandler
import asyncio
import nest_asyncio

nest_asyncio.apply()  # Streamlit'in kendi event loop'u ile uyum sağlamak için

TOKEN = "8350284060:AAELTkDNIEt_oWP-ZXYDRlo_eBSofz2cziA"

async def start(update, context):
    await update.message.reply_text("Merhaba! Bu bot Streamlit içinden çalışıyor 🚀")

async def run_bot():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    await app.run_polling(stop_signals=None)

st.title("📩 Telegram Bot Kontrol Paneli")
st.write("Bu bot Streamlit ile başlatıldı. /start yazınca yanıt verecek.")

if st.button("Botu Başlat"):
    st.write("Bot çalışmaya başladı... Telegram'dan deneyebilirsin.")
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())
