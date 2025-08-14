import streamlit as st
import yt_dlp
import os

# Streamlit arayüzü
st.title("YouTube Video İndirici")
st.write("YouTube videosunu indirmek için URL'yi girin")

# Kullanıcıdan YouTube URL'sini al
url = st.text_input("YouTube Video URL'si:", value="https://youtu.be/45xdicPCZ9k?si=Szr8y-P3AOhEbLtq")

if url:
    try:
        # yt-dlp ayarları
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',  # MP4 formatında en iyi kalite
            'outtmpl': 'downloads/%(title)s.%(ext)s',  # Dosya adı formatı
            'noplaylist': True,  # Playlist değil, tek video indir
        }

        # Video bilgilerini al ve indir
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            st.write("Video bilgileri alınıyor...")
            info = ydl.extract_info(url, download=False)  # Önce bilgileri al
            st.write(f"**Video Başlığı:** {info['title']}")
            st.write(f"**Kanal:** {info['uploader']}")
            st.write(f"**Süre:** {info['duration'] // 60} dakika {info['duration'] % 60} saniye")

            # Kalite seçeneklerini listele
            formats = [f for f in info['formats'] if f.get('ext') == 'mp4' and f.get('vcodec') and f.get('acodec')]
            quality_options = [f"{f.get('resolution', 'Bilinmiyor')} ({f.get('format_note', 'N/A')})" for f in formats]
            
            # Kalite seçimi
            selected_quality = st.selectbox("İndirme Kalitesini Seçin:", quality_options)
            
            if st.button("İndir"):
                # Seçilen kaliteye göre format ID'sini al
                selected_format = formats[quality_options.index(selected_quality)]
                ydl_opts['format'] = selected_format['format_id']
                
                st.write("İndirme başlatılıyor...")
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                    video_path = ydl.prepare_filename(info)
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