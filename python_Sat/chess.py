import tkinter as tk

SQ = 640 // 8

board = [
    ["r","n","b","q","k","b","n","r"],
    ["p","p","p","p","p","p","p","p"],
    ["","","","","","","",""],
    ["","","","","","","",""],
    ["","","","","","","",""],
    ["","","","","","","",""],
    ["P","P","P","P","P","P","P","P"],
    ["R","N","B","Q","K","B","N","R"],
]

root = tk.Tk()
root.title("Chess Game")

canvas = tk.Canvas(root, width=640, height=640)
canvas.pack()

def draw():
    canvas.delete("all")

    for row in range(8):
        for col in range(8):
                if (row+col) % 2 == 0:
                    color = "#71C964"
                else:
                     color = "#b8874a"
                canvas.create_rectangle(
                    col * SQ, row * SQ,
                    (col + 1) * SQ, (row + 1) * SQ,
                    fill=color,
                    outline=color
                )

                piece = board[row][col]
                if piece:
                     canvas.create_text(
                          col * SQ + SQ // 2,
                          row * SQ + SQ // 2,
                          text = piece,
                          font=("Arial", 36, "bold")
                     )

draw()
root.mainloop()
                
            