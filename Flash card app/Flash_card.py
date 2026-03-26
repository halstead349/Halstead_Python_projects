from tkinter import *
import random
import pandas as pd
# structuring the base window.
BACKGROUND_COLOR = "#B1DDC6"
window = Tk()
window.title("Flash Card")
window.config(padx= 50, pady= 50,bg=BACKGROUND_COLOR)
data_dict = {}
# read the csv file and save as dictionary
try:
    data = pd.read_csv("data/words_to_learn.csv")
    
except FileNotFoundError:
    data = pd.read_csv("data/french_words.csv")
    data_dict = data.to_dict(orient="records")
    
else:
    data_dict = data.to_dict(orient="records")

display_ques_word = {}


def next_word():
    global display_ques_word, flip_time
    window.after_cancel(flip_time)
    display_ques_word = random.choice(data_dict)
    canva.itemconfig(card_title,text = "French")
    canva.itemconfig(card_word, text = display_ques_word["French"])
    canva.itemconfig(card_bg_img,image = card_front)
    flip_time = window.after(3000,func=flip_card)
    
    
def flip_card():
    canva.itemconfig(card_title,text = "English", fill = "black")
    canva.itemconfig(card_word, text = display_ques_word["English"],fill = "black")
    canva.itemconfig(card_bg_img,image = card_flippedimage)
    
def is_known(): # removes the known dict data and stores the new dictionary to the words_to_learn.csv file.
    data_dict.remove(display_ques_word)
    data = pd.DataFrame(data_dict)
    data.to_csv("data/words_to_learn.csv",index=False)
    next_word()
    

flip_time = window.after(3000,func=flip_card)
print(flip_time)
    

# inner structuring:
canva = Canvas(width=800,height=526)
card_front = PhotoImage(file="images/card_front.png")
card_flippedimage = PhotoImage(file="images/card_back.png")
card_bg_img = canva.create_image(400,263,image = card_front)
card_title = canva.create_text(400,150,text="",font=("Ariel",40,"italic"))
card_word = canva.create_text(400,263,text="",font=("Ariel",60,"italic"))
canva.config(bg=BACKGROUND_COLOR,highlightthickness=0)
canva.grid(row=0,column=0, columnspan=2)

cross_img = PhotoImage(file="images/wrong.png")
dont_know_img = Button(image=cross_img,highlightthickness=0, command=next_word)
dont_know_img.grid(row=1,column=0)
right_img = PhotoImage(file="images/right.png")
know_img = Button(image=right_img,highlightthickness=0, command= is_known)
know_img.grid(row=1,column=1)

next_word()

window.mainloop()

