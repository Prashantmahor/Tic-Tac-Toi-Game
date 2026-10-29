
import random
import numpy as np
import streamlit as st

st.set_page_config(page_title="Tic-Tac-Toe | AI Arena", page_icon="⭕", layout="wide")

# ---------- Styling ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
.stApp {
  background: radial-gradient(ellipse at 10% 0%, rgba(45,212,191,.12), transparent 35%),
              radial-gradient(ellipse at 90% 10%, rgba(139,92,246,.13), transparent 32%), #0b1020;
  color:#eef4ff; font-family:'Manrope',sans-serif;
}
.block-container {max-width:1100px; padding-top:2rem; padding-bottom:3rem;}
.hero {padding:26px 30px; border:1px solid #29344d; border-radius:22px;
       background:linear-gradient(135deg,rgba(18,26,46,.97),rgba(20,27,48,.8)); margin-bottom:22px;}
.eyebrow {color:#5eead4; font:500 11px 'DM Mono',monospace; letter-spacing:.18em;}
.hero-title {font-size:clamp(28px,4vw,42px);font-weight:800;letter-spacing:-.04em;margin:8px 0;color:#eef4ff;}
.sub {color:#94a3b8;font-size:14px;}
.stat {padding:15px;border:1px solid #29344d;border-radius:15px;background:rgba(255,255,255,.025);}
.stat-label {color:#94a3b8;font:500 10px 'DM Mono',monospace;letter-spacing:.12em;text-transform:uppercase;}
.stat-value {font-size:27px;font-weight:800;color:#eef4ff;}
.status {padding:14px 16px;border:1px solid rgba(94,234,212,.3);border-radius:14px;background:rgba(94,234,212,.07);margin:18px 0;}
.status-title {color:#5eead4;font-weight:800;font-size:16px;}
.status-sub {color:#94a3b8;font-size:12px;margin-top:3px;}
.section-label {color:#94a3b8;font:500 11px 'DM Mono',monospace;letter-spacing:.14em;margin:0 0 12px;}
div[data-testid="stButton"] button {transition:all .15s ease;}
div[data-testid="stButton"] button[kind="secondary"] {
  min-height:95px;border-radius:16px;border:1px solid #293651;
  background:linear-gradient(145deg,#151f35,#10182a);color:#eef4ff;
  font-size:34px;font-weight:800;box-shadow:0 5px 0 #070c17;
}
div[data-testid="stButton"] button[kind="secondary"]:hover {border-color:#5eead4;color:#5eead4;transform:translateY(-2px);}
div[data-testid="stButton"] button:disabled {opacity:1!important;cursor:default!important;}
div[data-testid="stButton"] button[kind="primary"] {border:0;border-radius:12px;background:linear-gradient(90deg,#5eead4,#a7f3d0);color:#07121c;font-weight:800;}
footer {visibility:hidden;}
@media(max-width:700px) {
 .block-container{padding:1rem .65rem 2rem;}
 div[data-testid="stButton"] button[kind="secondary"]{min-height:65px;font-size:28px;}
 .hero{padding:20px;}
}
</style>
""", unsafe_allow_html=True)

EMPTY, HUMAN, AI = 0, 1, -1
SYMBOLS = {EMPTY: "·", HUMAN: "✕", AI: "○"}

# ---------- Game logic ----------
def check_winner(board):
    for row in board:
        total = int(np.sum(row))
        if total == 3:
            return HUMAN
        if total == -3:
            return AI
    for c in range(3):
        total = int(np.sum(board[:, c]))
        if total == 3:
            return HUMAN
        if total == -3:
            return AI
    d1 = int(np.trace(board))
    d2 = int(np.trace(np.fliplr(board)))
    if d1 == 3 or d2 == 3:
        return HUMAN
    if d1 == -3 or d2 == -3:
        return AI
    if not np.any(board == EMPTY):
        return 0
    return None

def minimax(board, is_maximizing, depth=0):
    result = check_winner(board)
    if result is not None:
        if result == AI:
            return 10 - depth
        if result == HUMAN:
            return depth - 10
        return 0

    if is_maximizing:
        best = -100
        for r in range(3):
            for c in range(3):
                if board[r, c] == EMPTY:
                    board[r, c] = AI
                    score = minimax(board, False, depth + 1)
                    board[r, c] = EMPTY
                    best = max(best, score)
        return best

    best = 100
    for r in range(3):
        for c in range(3):
            if board[r, c] == EMPTY:
                board[r, c] = HUMAN
                score = minimax(board, True, depth + 1)
                board[r, c] = EMPTY
                best = min(best, score)
    return best

def winning_move(board, player):
    for r in range(3):
        for c in range(3):
            if board[r, c] == EMPTY:
                board[r, c] = player
                wins = check_winner(board) == player
                board[r, c] = EMPTY
                if wins:
                    return (r, c)
    return None

def best_move(board):
    best_score = -100
    moves = []
    for r in range(3):
        for c in range(3):
            if board[r, c] == EMPTY:
                board[r, c] = AI
                score = minimax(board, False)
                board[r, c] = EMPTY
                if score > best_score:
                    best_score, moves = score, [(r, c)]
                elif score == best_score:
                    moves.append((r, c))
    return random.choice(moves) if moves else None

def choose_ai_move(board, difficulty):
    available = [(r, c) for r in range(3) for c in range(3) if board[r, c] == EMPTY]
    if not available:
        return None
    if difficulty == "Easy":
        return random.choice(available)
    if difficulty == "Medium":
        move = winning_move(board, AI)
        if move:
            return move
        move = winning_move(board, HUMAN)
        if move:
            return move
        if random.random() < 0.55:
            return random.choice(available)
    return best_move(board)

def reset_board():
    st.session_state.board = np.zeros((3, 3), dtype=int)
    st.session_state.winner = None
    st.session_state.message = "Your move — choose a square."
    st.session_state.last_move = None

def end_game(result):
    st.session_state.winner = result
    if result == HUMAN:
        st.session_state.scores["human"] += 1
        st.session_state.message = "Victory! You outplayed the machine."
    elif result == AI:
        st.session_state.scores["ai"] += 1
        st.session_state.message = "AI wins this round. Try again!"
    else:
        st.session_state.scores["draw"] += 1
        st.session_state.message = "Draw! Both sides defended well."

def handle_move(r, c):
    board = st.session_state.board
    if st.session_state.winner is not None or board[r, c] != EMPTY:
        return

    board[r, c] = HUMAN
    st.session_state.last_move = (r, c)
    result = check_winner(board)
    if result is not None:
        end_game(result)
        return

    move = choose_ai_move(board, st.session_state.difficulty)
    if move is not None:
        ar, ac = move
        board[ar, ac] = AI
        st.session_state.last_move = (ar, ac)

    result = check_winner(board)
    if result is not None:
        end_game(result)
    else:
        st.session_state.message = "Your move — the arena is yours."

# ---------- State initialization ----------
if "board" not in st.session_state:
    st.session_state.board = np.zeros((3, 3), dtype=int)
if "winner" not in st.session_state:
    st.session_state.winner = None
if "message" not in st.session_state:
    st.session_state.message = "Your move — choose a square."
if "last_move" not in st.session_state:
    st.session_state.last_move = None
if "scores" not in st.session_state:
    st.session_state.scores = {"human": 0, "ai": 0, "draw": 0}
if "difficulty" not in st.session_state:
    st.session_state.difficulty = "Impossible"

# ---------- UI ----------
st.markdown("""
<div class="hero">
  <div class="eyebrow">NEURAL ARCADE / GAME 001</div>
  <div class="hero-title">Noughts <span style="color:#5eead4">&</span> Crosses</div>
  <div class="sub">Human intuition versus machine strategy. One board. Nine squares. Make every move count.</div>
  <div style="margin-top:15px"><span class="eyebrow">● AI ARENA ONLINE &nbsp; / &nbsp; MINIMAX ENGINE</span></div>
</div>
""", unsafe_allow_html=True)

s1, s2, s3, s4 = st.columns([1, 1, 1, 1.5])
with s1:
    st.markdown(f'<div class="stat"><div class="stat-label">You · X</div><div class="stat-value">{st.session_state.scores["human"]}</div></div>', unsafe_allow_html=True)
with s2:
    st.markdown(f'<div class="stat"><div class="stat-label">AI · O</div><div class="stat-value">{st.session_state.scores["ai"]}</div></div>', unsafe_allow_html=True)
with s3:
    st.markdown(f'<div class="stat"><div class="stat-label">Draws</div><div class="stat-value">{st.session_state.scores["draw"]}</div></div>', unsafe_allow_html=True)
with s4:
    chosen = st.selectbox("AI difficulty", ["Easy", "Medium", "Impossible"],
                          index=["Easy", "Medium", "Impossible"].index(st.session_state.difficulty))
    st.session_state.difficulty = chosen

left, right = st.columns([1.25, 0.85], gap="large")
with left:
    if st.session_state.winner is None:
        title = "YOUR TURN"
        subtitle = f"You play ✕ · Difficulty: {st.session_state.difficulty}"
    elif st.session_state.winner == HUMAN:
        title, subtitle = "VICTORY CONFIRMED", "You claimed this round. Nicely played."
    elif st.session_state.winner == AI:
        title, subtitle = "AI TAKES THE ROUND", "The machine found its line. Run it back."
    else:
        title, subtitle = "MATCH DRAWN", "A perfectly defended board from both sides."

    st.markdown(f'<div class="status"><div class="status-title">{title}</div><div class="status-sub">{subtitle}</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">THE BATTLEFIELD</div>', unsafe_allow_html=True)

    for r in range(3):
        cols = st.columns(3, gap="small")
        for c in range(3):
            value = int(st.session_state.board[r, c])
            label = SYMBOLS[value]
            disabled = value != EMPTY or st.session_state.winner is not None
            with cols[c]:
                if st.button(label, key=f"cell_{r}_{c}", use_container_width=True,
                             disabled=disabled, type="secondary"):
                    handle_move(r, c)
                    st.rerun()

    st.caption("Choose an empty square to play. You are ✕; the AI is ○.")
    b1, b2 = st.columns(2)
    with b1:
        if st.button("↻  New round", type="primary", use_container_width=True):
            reset_board()
            st.rerun()
    with b2:
        if st.button("⟲  Reset scores", use_container_width=True):
            st.session_state.scores = {"human": 0, "ai": 0, "draw": 0}
            reset_board()
            st.rerun()

with right:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">MISSION BRIEF</div>', unsafe_allow_html=True)
    st.markdown("### Outsmart the algorithm")
    st.write("Get three of your marks in a row, column, or diagonal to win.")
    st.markdown("---")
    st.markdown('<div class="section-label">DIFFICULTY PROTOCOL</div>', unsafe_allow_html=True)
    st.markdown("**Easy** — Random moves.")
    st.markdown("**Medium** — Tries to win or block, with some randomness.")
    st.markdown("**Impossible** — Minimax search; optimal play cannot be beaten.")
    st.markdown("---")
    st.markdown('<div class="section-label">MATCH FEED</div>', unsafe_allow_html=True)
    st.write(st.session_state.message)
    if st.session_state.last_move:
        rr, cc = st.session_state.last_move
        st.caption(f"Last move: row {rr + 1}, column {cc + 1}")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='text-align:center;color:#64748b;font-size:11px;margin-top:28px'>PYTHON · NUMPY · STREAMLIT · MINIMAX SEARCH</div>", unsafe_allow_html=True)
