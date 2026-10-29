**🎮 Tic-Tac-Toe: Human vs AI**

A classic Tic-Tac-Toe game built with Python, NumPy, and Streamlit, featuring an interactive web interface and an AI opponent powered by the Minimax algorithm.

Play against the computer, choose your difficulty level, and track your match results through a clean, modern interface.

✨ Features
Interactive web UI built with Streamlit
Human vs AI gameplay — play as ✕ against the computer's ○
Three difficulty levels
Easy: AI chooses a random available cell
Medium: AI looks for immediate wins and blocks immediate threats, but may make random moves
Impossible: AI uses Minimax to choose an optimal move
Scoreboard to track human wins, AI wins, and draws during the session
New Round button to start another match
Reset Scores button to clear the scoreboard
Game status and match feed to show the current state
Responsive dark-themed interface
🧰 Tech Stack
Python — game logic
NumPy — board representation and calculations
Streamlit — web UI and interactive controls
Minimax algorithm — AI decision-making
CSS — custom interface styling
This project uses a search-based game-playing algorithm. It does not use a trained machine-learning model or a large language model.

🧠 How the AI Works
The board is represented as a 3×3 NumPy array:

Value	Meaning
0	Empty cell
1	Human player (✕)
-1	AI player (○)
