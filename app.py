import streamlit as st
import chess
import random
from streamlit_chess import chess_board

# 1. Cấu hình giao diện ứng dụng
st.set_page_config(page_title="Cờ Vua AI Click Chuột", page_icon="🤖", layout="centered")
st.title("👑 GAME CỜ VUA: ĐIỀU KHIỂN BẰNG CHUỘT")
st.write("👉 **Hướng dẫn:** Dùng chuột click vào quân cờ của bạn (Trắng) rồi click vào ô muốn đi đến!")

# 2. Khởi tạo bộ nhớ lưu trữ trạng thái ván cờ
if "board" not in st.session_state:
    st.session_state.board = chess.Board()

# 3. Thanh điều khiển ở cột bên cạnh (Sidebar)
st.sidebar.header("🛠️ CÀI ĐẶT TRẬN ĐẤU")
play_mode = st.sidebar.selectbox("Chế độ chơi:", ["Đấu với Máy (AI)", "2 Người chơi (PvP)"])

difficulty = "Dễ"
if play_mode == "Đấu với Máy (AI)":
    difficulty = st.sidebar.select_slider("Mức độ khó của Máy:", options=["Dễ", "Trung bình", "Khó"])

if st.sidebar.button("🔄 Làm mới ván cờ"):
    st.session_state.board = chess.Board()
    st.rerun()

# --- BỘ NÃO AI TÌM NƯỚC ĐI ---
def evaluate_board(board):
    piece_values = {
        chess.PAWN: 10, chess.KNIGHT: 30, chess.BISHOP: 30, 
        chess.ROOK: 50, chess.QUEEN: 90, chess.KING: 900
    }
    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            val = piece_values[piece.piece_type]
            score += val if piece.color == chess.WHITE else -val
    return score

def get_ai_move(board, level):
    legal_moves = list(board.legal_moves)
    if not legal_moves:
        return None
    if level == "Dễ":
        return random.choice(legal_moves)
    
    best_move = random.choice(legal_moves)
    if level == "Trung bình":
        best_score = float('inf')
        for move in legal_moves:
            board.push(move)
            score = evaluate_board(board)
            board.pop()
            if score < best_score:
                best_score = score
                best_move = move
        return best_move
        
    if level == "Khó":
        best_score = float('inf')
        for move in legal_moves:
            board.push(move)
            if board.is_checkmate():
                board.pop()
                return move
            opp_moves = list(board.legal_moves)
            max_opp = float('-inf')
            for opp_move in opp_moves:
                board.push(opp_move)
                s = evaluate_board(board)
                board.pop()
                if s > max_opp: max_opp = s
            board.pop()
            if max_opp < best_score:
                best_score = max_opp
                best_move = move
        return best_move

# 4. HIỂN THỊ BÀN CỜ TƯƠNG TÁC CHUỘT
# Hàm này tự vẽ bàn cờ và trả về nước đi dạng chữ khi người dùng click chuột xong
move = chess_board(st.session_state.board.fen(), key="chess_mouse_game")

# 5. XỬ LÝ NƯỚC ĐI TỪ CHUỘT
if move and not st.session_state.board.is_game_over():
    try:
        chess_move = chess.Move.from_uci(move)
        # Nếu nước đi bằng chuột hợp lệ theo luật cờ vua
        if chess_move in st.session_state.board.legal_moves:
            st.session_state.board.push(chess_move)
            
            # Nếu đang bật chế độ đấu với máy, cho máy đi luôn
            if play_mode == "Đấu với Máy (AI)" and not st.session_state.board.is_game_over():
                with st.spinner("🤖 Máy đang tính toán..."):
                    ai_move = get_ai_move(st.session_state.board, difficulty)
                    if ai_move:
                        st.session_state.board.push(ai_move)
            
            st.rerun()
    except Exception:
        pass

# 6. THÔNG BÁO KẾT THÚC VÁN
if st.session_state.board.is_game_over():
    st.markdown("---")
    st.subheader("🏁 KẾT QUẢ TRẬN ĐẤU")
    if st.session_state.board.is_checkmate():
        if st.session_state.board.turn == chess.WHITE:
            st.error("💀 Máy đã chiến thắng! Bạn đã bị chiếu hết.")
        else:
            st.success("🎉 Xuất sắc! Bạn đã chiếu hết Máy!")
    else:
        st.info("🤝 Trận đấu kết thúc với kết quả Hòa!")
