import streamlit as st
import chess
import chess.svg
import random

# Cấu hình giao diện ứng dụng
st.set_page_config(page_title="Cờ Vua AI", page_icon="🤖", layout="centered")
st.title("👑 GAME CỜ VUA: ĐẤU VỚI MÁY (AI)")

# Khởi tạo hoặc khôi phục trạng thái Game ẩn
if "board_fen" not in st.session_state:
    board = chess.Board()
    st.session_state.board_fen = board.fen()

# Tạo lại đối tượng bàn cờ từ bộ nhớ FEN
current_board = chess.Board(st.session_state.board_fen)

# Thanh điều khiển bên cạnh (Sidebar)
st.sidebar.header("🛠️ CÀI ĐẶT TRẬN ĐẤU")
play_mode = st.sidebar.selectbox("Chế độ chơi:", ["Đấu với Máy (AI)", "2 Người chơi"])

difficulty = "Dễ"
if play_mode == "Đấu với Máy (AI)":
    difficulty = st.sidebar.select_slider("Mức độ khó của Máy:", options=["Dễ", "Trung bình", "Khó"])

if st.sidebar.button("🔄 Làm mới ván cờ"):
    new_board = chess.Board()
    st.session_state.board_fen = new_board.fen()
    st.rerun()

# --- HÀM TÌM NƯỚC ĐI CHO MÁY ---
def get_ai_move(board, level):
    legal_moves = list(board.legal_moves)
    if not legal_moves:
        return None
    if level == "Dễ":
        return random.choice(legal_moves)
        
    # Tính điểm bàn cờ cơ bản cho mức Trung bình / Khó
    def eval_board(b):
        vals = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3, chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0}
        score = 0
        for sq in chess.SQUARES:
            p = b.piece_at(sq)
            if p:
                val = vals.get(p.piece_type, 0)
                score += val if p.color == chess.WHITE else -val
        return score

    if level == "Trung bình":
        best_move = random.choice(legal_moves)
        best_score = float('inf')
        for m in legal_moves:
            board.push(m)
            s = eval_board(board)
            board.pop()
            if s < best_score:
                best_score = s
                best_move = m
        return best_move
        
    if level == "Khó":
        best_move = random.choice(legal_moves)
        best_score = float('inf')
        for m in legal_moves:
            board.push(m)
            if board.is_checkmate():
                board.pop()
                return m
            opp_moves = list(board.legal_moves)
            max_opp = float('-inf')
            for om in opp_moves:
                board.push(om)
                s = eval_board(board)
                board.pop()
                if s > max_opp: max_opp = s
            board.pop()
            if max_opp < best_score:
                best_score = max_opp
                best_move = m
        return best_move

# --- GIAO DIỆN CHÍNH ---
# Vẽ bàn cờ dạng ảnh SVG để tránh lỗi hiển thị tương tác
board_svg = chess.svg.board(board=current_board, size=400)
st.image(board_svg, use_container_width=False)

# Hiển thị các nước đi hợp lệ dưới dạng danh sách chọn cho dễ bấm
legal_moves_list = [m.uci() for m in current_board.legal_moves]

if not current_board.is_game_over():
    st.write("👉 **Lượt của bạn (Quân Trắng):**")
    
    # Cho người dùng chọn nước đi bằng danh sách thả xuống
    chosen_move_str = st.selectbox("Chọn nước đi của bạn (Ví dụ: e2e4):", ["-- Chọn nước đi --"] + legal_moves_list)
    
    if st.button("Đi quân ➡️"):
        if chosen_move_str != "-- Chọn nước đi --":
            player_move = chess.Move.from_uci(chosen_move_str)
            current_board.push(player_move)
            
            # Nếu là chế độ đấu với Máy, để Máy đi luôn ngay sau đó
            if play_mode == "Đấu với Máy (AI)" and not current_board.is_game_over():
                ai_move = get_ai_move(current_board, difficulty)
                if ai_move:
                    current_board.push(ai_move)
            
            # Lưu lại trạng thái mới vào bộ nhớ ứng dụng
            st.session_state.board_fen = current_board.fen()
            st.rerun()
else:
    st.markdown("---")
    st.subheader("🏁 KẾT QUẢ TRẬN ĐẤU")
    if current_board.is_checkmate():
        st.error("💀 CHIẾU TƯỚNG! Trận đấu kết thúc.")
    else:
        st.info("🤝 Trận đấu kết thúc với kết quả Hòa!")
 
   
       

    
