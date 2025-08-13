import fitz  # PyMuPDF
import streamlit as st
import os

st.title("PDF → TXT Dönüştürücü")

pdf_dosyasi = st.file_uploader("PDF dosyanızı seçin", type=["pdf"])

if pdf_dosyasi is not None:
    pdf = fitz.open(stream=pdf_dosyasi.read(), filetype="pdf")
    tum_metin = ""

    for sayfa in pdf:
        tum_metin += sayfa.get_text() + "\n"

    pdf.close()

    txt_adi = os.path.splitext(pdf_dosyasi.name)[0] + ".txt"
    with open(txt_adi, "w", encoding="utf-8") as f:
        f.write(tum_metin)

    st.success(f"PDF metni '{txt_adi}' dosyasına kaydedildi.")
    st.download_button(label="TXT İndir", data=tum_metin, file_name=txt_adi)