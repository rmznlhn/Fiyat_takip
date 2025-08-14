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
            'outtmpl': 'downloads/%(title)s.%(ext)s',  # Dosya adı formatı
            'noplaylist': True,  # Playlist değil, tek video indir
            'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None,  # Çerez dosyası (varsa)
        }

        # Video bilgilerini al
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            st.write("Video bilgileri alınıyor...")
            info = ydl.extract_info(url, download=False)
            st.write(f"**Video Başlığı:** {info['title']}")
            st.write(f"**Kanal:** {info['uploader']}")
            st.write(f"**Süre:** {info['duration'] // 60} dakika {info['duration'] % 60} saniye")

            # MP4 formatlarını filtrele (hem video hem ses içeren)
            formats = [f for f in info['formats'] if f.get('ext') == 'mp4' and f.get('vcodec') and f.get('acodec')]
            if not formats:
                st.error("Uygun MP4 formatı bulunamadı. Lütfen başka bir video deneyin.")
                st.stop()

            # Kalite seçeneklerini oluştur
            quality_options = [f"{f.get('resolution', 'Bilinmiyor')} ({f.get('format_note', 'N/A')}) - ID: {f['format_id']}" for f in formats]
            quality_dict = {f"{f.get('resolution', 'Bilinmiyor')} ({f.get('format_note', 'N/A')}) - ID: {f['format_id']}": f['format_id'] for f in formats}

            # Kalite seçimi
            selected_quality = st.selectbox("İndirme Kalitesini Seçin:", quality_options)

            if st.button("İndir"):
                # Seçilen format ID'sini al
                selected_format_id = quality_dict[selected_quality]
                ydl_opts['format'] = selected_format_id  # Kullanıcının seçtiği formatı kullan

                st.write("İndirme başlatılıyor...")
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                    video_path = f"downloads/{info['title']}.mp4"  # Dosya adı
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
                        st.error("İndirilen dosya bulunamadı. Lütfen tekrar deneyin.")
    except Exception as e:
        st.error(f"Hata oluştu: {str(e)}")

# İndirme klasörünü oluştur
if not os.path.exists("downloads"):
    os.makedirs("downloads")