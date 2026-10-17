import streamlit as st
import chess
import chess.svg

# 1. Cấu hình giao diện
st.set_page_config(page_title="Game Cờ Vua Ổn Định", page_icon="👑", layout="centered")
st.title("👑 GAME CỜ VUA: CHƠI BẰNG ĐIỀU KHIỂN TỌA ĐỘ")

# Khởi tạo bộ nhớ bàn cờ (sử dụng chuỗi FEN để lưu trạng thái)
if "board_fen" not in st.session_state:
    st.session_state.board_fen = chess.Board().fen()
if "selected_square" not in st.session_state:
    st.session_state.selected_square = None

# Tải lại bàn cờ hiện tại từ bộ nhớ
board = chess.Board(st.session_state.board_fen)

# Cấu hình thanh Sidebar đấu với Máy
st.sidebar.header("🛠️ CÀI ĐẶT")
play_mode = st.sidebar.selectbox("Chế độ:", ["Đấu với Máy (AI)", "2 Người chơi"])

if st.sidebar.button("🔄 Xếp lại bàn cờ"):
    st.session_state.board_fen = chess.Board().fen()
    st.session_state.selected_square = None
    st.rerun()

# --- BỘ NÃO MÁY TÍNH (AI) ---
def make_ai_move(current_board):
    import random
    legal_moves = list(current_board.legal_moves)
    if legal_moves:
        # Máy quét tìm nước ăn quân tốt nhất ngay lập tức
        best_move = random.choice(legal_moves)
        max_score = -1
        for move in legal_moves:
            if current_board.is_capture(move):
                current_board.push(move)
                if current_board.is_checkmate():
                    current_board.pop()
                    return move
                current_board.pop()
                best_move = move
        return best_move
    return None

# --- HIỂN THỊ HÌNH ẢNH BÀN CỜ ---
# Vẽ bàn cờ dạng ảnh sắc nét (Tự động tô màu ô đang chọn)
fill_dict = {}
if st.session_state.selected_square:
    sq_index = chess.parse_square(st.session_state.selected_square)
    fill_dict[sq_index] = "#ccffcc" # Tô màu xanh ô đang chọn

board_svg = chess.svg.board(board=board, size=420, fill=fill_dict)
st.image(board_svg, use_container_width=False)

# --- BỘ ĐIỀU KHIỂN TƯƠNG TÁC ---
if not board.is_game_over():
    st.write(f"👉 Lượt đi: **{'Quân Trắng (Bạn)' if board.turn == chess.WHITE else 'Quân Đen'}**")
    
    # BƯỚC A: CHỌN QUÂN CỜ
    all_squares = [chess.square_name(s) for s in chess.SQUARES]
    # Lọc danh sách các ô có quân cờ của mình để người chơi chọn
    my_pieces_squares = [sq for sq in all_squares if board.piece_at(chess.parse_square(sq)) and board.piece_at(chess.parse_square(sq)).color == board.turn]
    
    col1, col2 = st.columns(2)
    
    with col1:
        src_sq = st.selectbox("1. Chọn quân cờ muốn đi:", ["-- Chọn ô --"] + sorted(my_pieces_squares))
        if src_sq != "-- Chọn ô --" and src_sq != st.session_state.selected_square:
            st.session_state.selected_square = src_sq
            st.rerun()

    # BƯỚC B: CHỌN ĐÍNH ĐẾN VÀ ĐI QUÂN
    with col2:
        if st.session_state.selected_square:
            active_sq = chess.parse_square(st.session_state.selected_square)
            # Lọc các nước đi hợp lệ từ ô đã chọn
            possible_destinations = [chess.square_name(m.to_square) for m in board.legal_moves if m.from_square == active_sq]
            
            dest_sq = st.selectbox("2. Chọn ô muốn đi tới:", ["-- Chọn đích --"] + sorted(possible_destinations))
            
            if st.button("Đi quân ➡️"):
                if dest_sq != "-- Chọn đích --":
                    move_str = f"{st.session_state.selected_square}{dest_sq}"
                    move = chess.Move.from_uci(move_str)
                    
                    # Đi quân Trắng
                    board.push(move)
                    
                    # Nếu bật chế độ đấu với Máy, để máy đi luôn quân Đen
                    if play_mode == "Đấu với Máy (AI)" and not board.is_game_over():
                        ai_move = make_ai_move(board)
                        if ai_move:
                            board.push(ai_move)
                    
                    # Lưu trạng thái và đặt lại lựa chọn
                    st.session_state.board_fen = board.fen()
                    st.session_state.selected_square = None
                    st.rerun()
        else:
            st.info("Hãy chọn quân cờ trước!")
else:
    st.subheader("🏁 TRẬN ĐẤU KẾT THÚC!")
    if board.is_checkmate():
        st.error("💀 Chiếu tướng kết thúc!")
    else:
        st.info("🤝 Trận đấu Hòa cờ!")
