import tkinter as tk
from tkinter import messagebox


#Solver

def solve(bo):
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if valid(bo, i, (row, col)):
            bo[row][col] = i

            if solve(bo):
                return True

            bo[row][col] = 0

    return False

def valid(bo, num, pos):
    # Row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False

    return True

def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)
    return None


#Tkinter part

root = tk.Tk()
root.title("Sudoku Solver")

entries = [[None for _ in range(9)] for _ in range(9)]

grid_frame = tk.Frame(root)
grid_frame.grid(row=0, column=0, columnspan=9, padx=7, pady=7)

def build_grid():
    for row in range(9):
        for col in range(9):

            top = 9 if row % 3 == 0 else 1
            left = 9 if col % 3 == 0 else 1
            bottom = 2 if row == 8 else 1
            right = 2 if col == 8 else 1

            e = tk.Entry(
                grid_frame,
                width=2,
                font=("Arial", 20),
                justify="center",
                relief="solid",
                bd=1,
                highlightthickness=0
            )

            e.grid(
                row=row,
                column=col,
                padx=(left, right),
                pady=(top, bottom)
            )

            entries[row][col] = e

def read_board():
    board = []
    for row in range(9):
        current_row = []
        for col in range(9):
            val = entries[row][col].get()
            if val == "":
                current_row.append(0)
            else:
                try:
                    num = int(val)
                    if 1 <= num <= 9:
                        current_row.append(num)
                    else:
                        raise ValueError
                except:
                    messagebox.showerror("Error", "Only digits 1-9 allowed")
                    return None
        board.append(current_row)
    return board

def fill_board(board):
    for row in range(9):
        for col in range(9):
            entries[row][col].delete(0, tk.END)
            if board[row][col] != 0:
                entries[row][col].insert(0, str(board[row][col]))

def solve_gui():
    board = read_board()
    if board is None:
        return

    if solve(board):
        fill_board(board)
    else:
        messagebox.showinfo("Sudoku Solver", "No solution exists.")

def clear_board():
    for row in range(9):
        for col in range(9):
            entries[row][col].delete(0, tk.END)

build_grid()

button_frame = tk.Frame(root)
button_frame.grid(row=1, column=0, columnspan=9, pady=10)

solve_button = tk.Button(button_frame, text="Solve", command=solve_gui, font=("Arial", 14))
solve_button.grid(row=0, column=0, padx=25)

clear_button = tk.Button(button_frame, text="Clear", command=clear_board, font=("Arial", 14))
clear_button.grid(row=0, column=1, padx=25)

root.mainloop()
