import streamlit as st
import random

# 1. Cấu hình giao diện trò chơi
st.set_page_config(page_title="Game Đoán Số", page_icon="🎮")
st.title("🎮 TRÒ CHƠI: ĐOÁN SỐ MAY MẮN")
st.write("Máy tính đã chọn bí mật một số từ **1 đến 100**. Bạn có đoán được không?")

# 2. Tạo bộ nhớ cho game (để không bị mất dữ liệu khi bấm nút)
if 'target_number' not in st.session_state:
    st.session_state.target_number = random.randint(1, 100)
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0

# 3. Ô nhập số của người chơi
user_guess = st.number_input("Hãy nhập số bạn đoán vào đây:", min_value=1, max_value=100, step=1)

# 4. Nút bấm kiểm tra kết quả
if st.button("Kiểm tra kết quả"):
    st.session_state.attempts += 1 # Cộng thêm 1 lần đoán
    
    if user_guess < st.session_state.target_number:
        st.warning("🧩 Số bạn đoán hơi NHỎ rồi! Hãy thử số lớn hơn.")
    elif user_guess > st.session_state.target_number:
        st.warning("🧩 Số bạn đoán hơi LỚN rồi! Hãy thử số nhỏ hơn.")
    else:
        st.success(f"🎉 CHÚC MỪNG! Bạn đã đoán đúng số {st.session_state.target_number} sau {st.session_state.attempts} lần thử!")

# 5. Nút bấm chơi lại từ đầu
if st.button("🔄 Chơi lượt mới"):
    st.session_state.target_number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.rerun() # Tải lại trang để reset game
