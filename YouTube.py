import streamlit as st
import yt_dlp
import os

st.title("YouTube Video İndirici")
st.write("YouTube videosunu indirmek için URL'yi girin")

url = st.text_input("YouTube Video URL'si:", value="https://youtu.be/45xdicPCZ9k?si=Szr8y-P3AOhEbLtq")

if url:
    try:
        ydl_opts = {
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'noplaylist': True,
            'format': 'best[ext=mp4]',  # En iyi MP4 formatı
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',  # User-Agent
        }

        if os.path.exists('cookies.txt'):
            try:
                with open('cookies.txt', 'r') as f:
                    if '# Netscape HTTP Cookie File' in f.read():
                        ydl_opts['cookiefile'] = 'cookies.txt'
                        st.info("cookies.txt dosyası kullanılıyor.")
                    else:
                        st.warning("cookies.txt Netscape formatında değil.")
            except:
                st.warning("cookies.txt okunamadı. Çerezler kullanılmayacak.")
        else:
            st.info("cookies.txt bulunamadı. Çerez olmadan devam ediliyor.")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            st.write("Video bilgileri alınıyor...")
            info = ydl.extract_info(url, download=False)
            st.write(f"**Video Başlığı:** {info['title']}")
            st.write(f"**Kanal:** {info['uploader']}")
            st.write(f"**Süre:** {info['duration'] // 60} dakika {info['duration'] % 60} saniye")

            if st.button("İndir"):
                st.write("İndirme başlatılıyor...")
                ydl.download([url])
                video_path = f"downloads/{info['title']}.mp4"
                if os.path.exists(video_path):
                    st.success(f"Video indirildi: {video_path}")
                    with open(video_path, "rb") as file:
                        st.download_button(
                            label="İndirilen Videoyu Kaydet",
                            data=file,
                            file_name=os.path.basename(video_path),
                            mime="video/mp4"
                        )
                else:
                    st.error("İndirilen dosya bulunamadı.")
    except Exception as e:
        st.error(f"Hata oluştu: {str(e)}")

if not os.path.exists("downloads"):
    os.makedirs("downloads")
