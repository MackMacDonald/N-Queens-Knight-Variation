import tkinter
from PIL import ImageTk, Image

def draw_solution(optimal_solution):
    root = tkinter.Tk()

    chess_board = tkinter.Canvas(root,width=800,height=800)
    size = 800 // len(optimal_solution)

    queen_image = Image.open("queen.png")
    queen_image = queen_image.resize((size, size))
    queen_image = ImageTk.PhotoImage(queen_image)

    for row in range(len(optimal_solution)):
        for col in range(len(optimal_solution)):
            if row % 2 == 0:
                if col % 2 == 0:
                    color = "#6D2100"
                else:
                    color = "#FFE59B"
            else:
                if col % 2 == 0:
                    color = "#FFE59B"
                else:
                    color = "#6D2100"
            chess_board.create_rectangle(row * size,col * size,row * size + size,col * size + size,fill=color,)

            if optimal_solution[row] == col:
                chess_board.create_image(row * size, col * size, image=queen_image, anchor="nw")

    chess_board.pack()
    root.mainloop()