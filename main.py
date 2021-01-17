from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
data_dict = {}
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    data_dict = original_data.to_dict(orient="records")
else:
    data_dict = data.to_dict(orient="records")

current_card = {}


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(data_dict)
    canvas.itemconfig(title, text="French", fill="black")
    canvas.itemconfig(word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_image)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(title, text="English", fill="green")
    canvas.itemconfig(word, text=current_card["English"], fill="green")
    canvas.itemconfig(card_background, image=card_background_image)


def is_known():
    data_dict.remove(current_card)
    # save the data back to the file
    data = pandas.DataFrame(data_dict)
    data.to_csv("data/words_to_learn.csv", index=False)
    print(len(data_dict))
    next_card()


window = Tk()
window.title("Flash")
window.config(bg="white")
flip_timer = window.after(3000, func=flip_card)
canvas = Canvas(width=895, height=548)
card_front_image = PhotoImage(file="images/card_front.png")
card_background_image = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(447.5, 274, image=card_front_image)
canvas.grid(row=0, column=0, columnspan=2)
title = canvas.create_text(447, 200, text="Title", font=("Ariel", 40, "italic"))
word = canvas.create_text(447, 300, text="Word", font=("Ariel", 60, "bold"))

# wrong button
cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, highlightcolor="white", command=next_card)
unknown_button.grid(row=1, column=0)

# right button
check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, highlightthickness=0, highlightcolor="white", command=is_known)
known_button.grid(row=1, column=1)

# call the function to create card
next_card()
window.mainloop()
