from turtle import Turtle,Screen
import time
from Snake import Snake
from food import Food
from scoreboard import Score
# screen setup
screen = Screen()
screen.setup(width= 600,height=600)
screen.title("Snake Game")
screen.bgcolor("black")
screen.tracer(0)

snake = Snake()
food = Food()
score = Score()
screen.listen()
screen.onkey(snake.up,"Up")
screen.onkey(snake.down,"Down")
screen.onkey(snake.left,"Left")
screen.onkey(snake.right,"Right")

   
game_is_on = True
while game_is_on:
    screen.update()
    time.sleep(0.1)
    snake.move()
    
    if snake.head.distance(food) < 15: # Detecting collision with food .
        score.inc_score()
        food.refresh()
        snake.extend_snake()
    
    # Detecting collision against wall.
    if snake.head.xcor() > 280 or snake.head.xcor() < -280 or snake.head.ycor() > 280 or snake.head.ycor() < -280: 
        game_is_on = False
        score.gameover()
        
    # detecting collision against Snacks body or tail.
    
    for segment in snake.segments[1:]:  # list sliced of segments
        if snake.head.distance(segment) < 10 :
            game_is_on = False
            score.gameover()
            
            


screen.exitonclick()