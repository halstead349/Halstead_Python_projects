from turtle import Turtle

class Score(Turtle):
    
    def __init__(self):
        super().__init__()
        self.score = 0
        self.color("white")
        self.penup()
        self.goto(0,270)
        self.update_score()
        self.hideturtle()
    
    def update_score(self):
        self.write(f"SCORE : {self.score}",align="center",font=("Arial",20,"normal"))
        
    
    def inc_score(self):
        self.score+=1
        self.clear()
        self.update_score()
        
    def gameover(self):
        self.goto(0,0)
        self.write(f"GAME OVER",align="center",font=("Ariel",30,"normal"))
        
        