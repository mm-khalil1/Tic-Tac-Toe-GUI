'''
Tic-Tac-Toe Almdrasa
This Python script implements a simple version of the classic Tic-Tac-Toe game.
It uses the Tkinter library for the graphical user interface.
The game allows a player to compete against a computer opponent.
The player plays as "X" and the computer plays as "O".
The game continues until one player wins or the game ends in a draw.
Players can restart the game at any time using the "Restart" button.

Author: Mahmoud Khalil
Date: 29-02-2024
'''


# Import the necessary modules
from tkinter import *
import random
import time

# Constants
EMPTY = ""
PLAYER_X = "X"
PC_O = "O"
font_size_small = 14
font_size_big = 20

# Global variables to track game state
player_score = 0
pc_score = 0
board = [EMPTY] * 9
game_over = False

# Function to restart the game
def restart():
    global board, game_over

    board = [EMPTY] * 9
    game_over = False
    # Clear the board GUI
    for i in range(9):
        cells[i // 3][i % 3].config(text=EMPTY, bg='SystemButtonFace')
    label_result.config(text="")

# Function to declare the winner and update scores
def declare_winner(winner):
    global game_over, pc_score, player_score

    if winner == PLAYER_X:
        player_score += 1
    elif winner == PC_O:
        pc_score += 1
    
    # Update scores on GUI
    label_score.config(text=f"You: {player_score}   Computer: {pc_score}")
    label_result.config(text=f"{winner} wins!")
    game_over = True

# Function to declare a draw
def declare_draw():
    global game_over
    
    # Highlight the cells to indicate a draw
    for i in range(9):
        cells[i // 3][i % 3].config(bg="red")
    label_result.config(text=f"Tie, No Winner!")
    game_over = True

# Function to check for a winner based on current board state
def check_winner(board):
    winning_conditions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    for condition in winning_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] != EMPTY:
            # Highlight winning cells
            for i in condition:
                cells[i // 3][i % 3].config(bg="cyan")
            return board[condition[0]]
    return None

# Function to check if the game ended in a draw
def is_draw(board):
    for cell in board:
        if cell == EMPTY:
            return False
    return True

# Function to update the GUI board
def update_board(row, col, mark):
    cells[row][col].config(text=mark)

# Function to handle player's move
def player_move(row, col, board):
    if board[row * 3 + col] == EMPTY:
        board[row * 3 + col] = PLAYER_X
        update_board(row, col, PLAYER_X)
        return True
    return False

# Function to simulate computer's move
def computer_move(board):
    empty_cells = [i for i, cell in enumerate(board) if cell == EMPTY]
    if empty_cells and not game_over:
        random_cell = random.choice(empty_cells)
        board[random_cell] = PC_O
        update_board(row=random_cell//3, col=random_cell%3, mark=PC_O)

# Function to check the board state after each move
def check_board():
    winner = check_winner(board)
    if not game_over and winner:
        declare_winner(winner)
    elif is_draw(board) and not winner:
        declare_draw()

# Function to handle cell click event
def cell_clicked(row, col):
    if not game_over and player_move(row, col, board):
        check_board()
        window.after(500, computer_move, board)     # Add a delay to simulate computer thinking time
        check_board()

# Create the Tkinter window
window = Tk()
window.title("Tic-Tac-Toe Almdrasa")

# Create labels and button for score, result, and restart
label_score = Label(window, text=f"You: {player_score}   Computer: {pc_score}", font=("Arial", font_size_small))
label_result = Label(window, text="", font=("Arial", font_size_big))
restart_button = Button(window, text="Restart", command=restart, font=("Arial", font_size_small))

# Position labels and buttons on the grid
label_score.grid(row=0, columnspan=3)
label_result.grid(row=1, columnspan=3)
restart_button.grid(row=2, columnspan=3)

# Create the grid for the game board
cells = []
for i in range(3):
    row = []
    for j in range(3):
        cell = Button(window, text="", 
                      width=10, height=3,
                      command=lambda row=i, column=j: cell_clicked(row, column),
                      state=DISABLED if game_over else NORMAL, 
                      font=("Arial", font_size_big)
        )
        cell.grid(row=i+3, column=j)
        row.append(cell)
    cells.append(row)

# Start the Tkinter event loop
window.mainloop()
