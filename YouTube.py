import streamlit as st
from pytube import YouTube
import os

# Streamlit arayüzü
st.title("YouTube Video İndirici")
st.write("YouTube videosunu indirmek için URL'yi girin")

# Kullanıcıdan YouTube URL'sini al
url = st.text_input("YouTube Video URL'si:")

if url:
    try:
        # YouTube nesnesi oluştur
        yt = YouTube(url)
        st.write(f"**Video Başlığı:** {yt.title}")
        st.write(f"**Kanal:** {yt.author}")
        st.write(f"**Süre:** {yt.length // 60} dakika {yt.length % 60} saniye")

        # Video kalite seçeneklerini listele
        streams = yt.streams.filter(progressive=True, file_extension="mp4").order_by('resolution')
        quality_options = [f"{stream.resolution} ({stream.mime_type})" for stream in streams]
        
        # Kalite seçimi
        selected_quality = st.selectbox("İndirme Kalitesini Seçin:", quality_options)
        
        # İndir butonu
        if st.button("İndir"):
            # Seçilen kaliteye göre stream'i al
            stream = streams[quality_options.index(selected_quality)]
            st.write("İndirme başlatılıyor...")
            
            # Videoyu indir
            video_path = stream.download(output_path="downloads/")
            st.success(f"Video indirildi: {video_path}")
            
            # İndirilen dosyayı kullanıcıya sun
            with open(video_path, "rb") as file:
                st.download_button(
                    label="İndirilen Videoyu Kaydet",
                    data=file,
                    file_name=os.path.basename(video_path),
                    mime="video/mp4"
                )
            
    except Exception as e:
        st.error(f"Hata oluştu: {str(e)}")

# İndirme klasörünü oluştur
if not os.path.exists("downloads"):
    os.makedirs("downloads")