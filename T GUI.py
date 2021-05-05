from tkinter import *
root = Tk()


def f_playerScore():
    pass
def f_nextPiece():
    pass

f_playerScore()
f_nextPiece()

t_frame = Frame(root, height=200, width=400, bg="aquamarine")
d_frame = Frame(root, height=200, width=500, bg="turquoise2")
s_frame = Frame(root, height=100, width=400, bg="turquoise2")
n_frame = Frame(root, height=100, width=500, bg="turquoise2")

# Title
title = Label(root, font=("ENGRAVERS MT", 25),fg="magenta3",bg="aquamarine", text="Titanic Tetris")


# Desc.
desc = Label(root, font=("Arial", 15),bg="turquoise2", text="""Use Joy Stick to move the pieces.
Press button to rotate a piece.
GUI provides information on your
score and what the subsequent piece will be.""")

# Score
# Function to insert an ever changeing Score
score = Label(root, font=("Arial", 20),bg="turquoise2", text="Score: {}".format("8888888"))

# Next Piece
# Function to insert an ever changing Piece
nextPiece = Label(root, font=("Arial", 20),bg="turquoise2", text="Next Piece: {}".format("L-Piece"))

#
t_frame.grid(row=0, column=0)
d_frame.grid(row=0, column=1)
s_frame.grid(row=1, column=0)
n_frame.grid(row=1, column=1)
#
title.grid(row=0, column=0)
desc.grid(row=0, column=1)
score.grid(row=1, column=0)
nextPiece.grid(row=1, column=1)



root.mainloop()
