import fitz  # PyMuPDF
import streamlit as st
import os

st.set_page_config(
    page_title="PDF → TXT Dönüştürücü",
    page_icon="📄",
    layout="centered"
)

st.title("📄 PDF → TXT Dönüştürücü")
st.write("PDF dosyanızdaki metni TXT dosyası olarak indirin.")

# PDF yükleme alanı
pdf_dosyasi = st.file_uploader("PDF dosyanızı seçin", type=["pdf"])

if pdf_dosyasi is not None:
    try:
        # PDF'i aç
        pdf = fitz.open(stream=pdf_dosyasi.read(), filetype="pdf")
        tum_metin = ""

        # Sayfa sayfa metni al
        for sayfa in pdf:
            tum_metin += sayfa.get_text() + "\n"

        pdf.close()

        # TXT dosya adı
        txt_adi = os.path.splitext(pdf_dosyasi.name)[0] + ".txt"

        # Dosyayı UTF-8 ile kaydet (isteğe bağlı, Pydroid veya PC için)
        with open(txt_adi, "w", encoding="utf-8") as f:
            f.write(tum_metin)

        st.success(f"PDF metni başarıyla '{txt_adi}' dosyasına kaydedildi.")

        # Download button: UTF-8 encode ile Türkçe karakter sorunu çözülür
        st.download_button(
            label="TXT İndir",
            data=tum_metin.encode('utf-8'),
            file_name=txt_adi,
            mime='text/plain'
        )

    except Exception as e:
        st.error(f"Hata oluştu: {e}")