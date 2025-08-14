import streamlit as st
import random

st.set_page_config(page_title="Sayı Tahmin Oyunu", page_icon="🎯", layout="centered")

st.title("🎯 Sayı Tahmin Oyunu")

# Rastgele sayı oluşturma (session_state ile her kullanıcıya özel)
if "rastgele_sayi" not in st.session_state:
    st.session_state.rastgele_sayi = random.randint(1, 100)
    st.session_state.deneme = 0
    st.session_state.mesaj = "1 ile 100 arasında bir sayı tuttum, tahmin et!"

# Kullanıcıdan tahmin al
tahmin = st.number_input("Tahmininizi girin:", min_value=1, max_value=100, step=1)
tahmin_buton = st.button("Tahmin Et")

# Tahmin kontrolü
if tahmin_buton:
    st.session_state.deneme += 1
    if tahmin < st.session_state.rastgele_sayi:
        st.session_state.mesaj = "📈 Daha büyük bir sayı deneyin."
    elif tahmin > st.session_state.rastgele_sayi:
        st.session_state.mesaj = "📉 Daha küçük bir sayı deneyin."
    else:
        st.session_state.mesaj = f"🎉 Tebrikler! {st.session_state.deneme} denemede doğru bildiniz!"
        st.session_state.rastgele_sayi = random.randint(1, 100)
        st.session_state.deneme = 0

# Mesajı göster
st.write(st.session_state.mesaj)

# Yeni oyun butonu
if st.button("Yeni Oyun"):
    st.session_state.rastgele_sayi = random.randint(1, 100)
    st.session_state.deneme = 0
    st.session_state.mesaj = "1 ile 100 arasında yeni bir sayı tuttum, tahmin et!"