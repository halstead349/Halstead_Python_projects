from tkinter import *
from quiz_brain import QuizBrain
THEME_COLOR = "#375362"

class QuizUi:
    def __init__(self,quizBrain : QuizBrain):
        self.quiz = quizBrain
        
        self.window = Tk()
        self.window.title("Quiz app")
        self.window.config(padx=20,pady=20,bg=THEME_COLOR)
        
        self.score_label = Label(text="Score : 0", fg="white", bg= THEME_COLOR)
        self.score_label.grid(column=1,row=0)
        
        self.canva = Canvas(width=300, height= 250, bg= THEME_COLOR)
        self.question_text = self.canva.create_text(150,125,text="Questions",font=("Ariel",20,"italic"),fill= "black",width=280)
        self.canva.grid(row=1,column=0,columnspan=2,padx=50)
        
        true_img = PhotoImage(file="images/true.png")
        self.true_button = Button(image=true_img,highlightthickness=0,command=self.tick_pressed)
        self.true_button.grid(row=2,column=0)
        
        wrong_img = PhotoImage(file="images/false.png")
        self.wrong_button = Button(image=wrong_img,highlightthickness=0,command=self.x_pressed)
        self.wrong_button.grid(row=2,column=1)
        
        self.get_string()
        self.window.mainloop()
        
    def get_string(self):
        self.canva.config(bg="white")
        q_text = self.quiz.next_question()
        self.canva.itemconfig(self.question_text,text= q_text)
        
    def tick_pressed(self):
        is_right_tuple = self.quiz.check_answer("True")
        self.next_step(is_right_tuple)
        
        
    def x_pressed(self):
        is_right_tuple = self.quiz.check_answer("False")
        self.next_step(is_right_tuple)
    
    def next_step(self,is_right_tuple : tuple):
        
        if is_right_tuple[0]:
            self.canva.config(bg="green")
            score = is_right_tuple[1]
            self.score_label.config(text = f"Score : {score}")
            
        else:
            self.canva.config(bg="red")
            
        self.window.after(2000,self.get_string)
        


