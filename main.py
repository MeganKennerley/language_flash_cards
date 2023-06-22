from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
language_dict = {}


try:
    csv_file = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("./data/french_words.csv")
    language_dict = original_data.to_dict(orient="records")
else:
    language_dict = csv_file.to_dict(orient="records")

current_card = {}


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(language_dict)
    canvas.itemconfig(card_title, text="French", fill="black")
    word = canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front)
    flip_timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back)


def is_known():
    language_dict.remove(current_card)
    data = pandas.DataFrame(language_dict)
    data.to_csv("data/words_to_learn.csv", index=False)

    next_card()


# Interface
window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)

canvas = Canvas(width=800, height=530, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="./images/card_front.png")
card_back = PhotoImage(file="./images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.grid(row=1, column=1, columnspan=2)

x_img = PhotoImage(file="./images/wrong.png")
x_button = Button(image=x_img, highlightthickness=0, command=next_card)
x_button.grid(row=2, column=1)

y_img = PhotoImage(file="./images/right.png")
y_button = Button(image=y_img, highlightthickness=0, command=is_known)
y_button.grid(row=2, column=2)


next_card()


window.mainloop()