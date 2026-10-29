
import numpy as np

# 0 = empty, 1 = X (human), -1 = O (AI)
board = np.zeros((3, 3), dtype=int)

def print_board(b):
    symbol = {0: " ", 1: "X", -1: "O"}
    for r in range(3):
        row = " | ".join(symbol[val] for val in b[r])
        print(" " + row)
        if r < 2:
            print("---+---+---")
    print()

def check_winner(b):
    # Rows & Columns
    if 3 in np.sum(b, axis=1) or 3 in np.sum(b, axis=0):
        return 1
    if -3 in np.sum(b, axis=1) or -3 in np.sum(b, axis=0):
        return -1

    # Diagonals
    if np.trace(b) == 3 or np.trace(np.fliplr(b)) == 3:
        return 1
    if np.trace(b) == -3 or np.trace(np.fliplr(b)) == -3:
        return -1

    # Draw
    if 0 not in b:
        return 0

    return None


def minimax(b, is_maximizing):
    winner = check_winner(b)
    if winner is not None:
        return winner

    if is_maximizing:  # AI turn (O = -1)
        best_score = -100
        for r in range(3):
            for c in range(3):
                if b[r][c] == 0:
                    b[r][c] = -1
                    score = minimax(b, False)
                    b[r][c] = 0
                    best_score = max(best_score, score)
        return best_score
    else:  # Human turn (X = 1)
        best_score = 100
        for r in range(3):
            for c in range(3):
                if b[r][c] == 0:
                    b[r][c] = 1
                    score = minimax(b, True)
                    b[r][c] = 0
                    best_score = min(best_score, score)
        return best_score


def best_move(b):
    best_score = -100
    move = (0, 0)

    for r in range(3):
        for c in range(3):
            if b[r][c] == 0:
                b[r][c] = -1
                score = minimax(b, False)
                b[r][c] = 0
                if score > best_score:
                    best_score = score
                    move = (r, c)
    return move


print("Tic Tac Toe — You (X) vs AI (O)")
print("Enter positions: row and col (0-2)\n")

while True:
    print_board(board)

    # Human move
    try:
        r = int(input("Your row (0-2): "))
        c = int(input("Your col (0-2): "))
    except:
        print("Invalid input")
        continue

    if r not in range(3) or c not in range(3) or board[r][c] != 0:
        print("Invalid move")
        continue

    board[r][c] = 1

    winner = check_winner(board)
    if winner is not None:
        break

    # AI move
    ai_r, ai_c = best_move(board)
    board[ai_r][ai_c] = -1
    print(f"AI played: {ai_r}, {ai_c}")

    winner = check_winner(board)
    if winner is not None:
        break

print_board(board)

if winner == 1:
    print("You win! 🎉")
elif winner == -1:
    print("AI wins 🤖")
else:
    print("Draw 😐")
