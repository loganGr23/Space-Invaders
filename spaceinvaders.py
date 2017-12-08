#Part 4: create an enemy/collision tracker
#Part 5: creating a missle
#Part 6: Create an ally
#Part 7: Game Status/Score
#Part 8: Multiple allys and enemys

import os
import random
import turtle

turtle.fd(0)
turtle.speed(0)
#Set screen size
turtle.setup (width=800, height=800, startx=0, starty=0)
turtle.bgcolor("black")
turtle.ht()
turtle.setundobuffer(1)
turtle.tracer(2)

class Sprite(turtle.Turtle):
   def __init__(self, spriteshape, color, startx, starty):
       turtle.Turtle.__init__(self, shape = spriteshape)
       self.speed(0)
       self.penup()
       self.color(color)
       self.fd(0)
       self.goto(startx,starty)
       self.speed = 1

   def move(self):
       self.fd(self.speed)

       #Boundary detection
       #check right side of border
       if self.xcor() > 290:
           self.setx(290)
           self.rt(60)
       #
       if self.xcor() < -290:
           self.setx(-290)
           self.rt(60)
       #
       if self.ycor() > 290:
           self.sety(290)
           self.rt(60)
       #
       if self.ycor() < -290:
           self.sety(-290)
           self.rt(60)

   def is_collision(self, other):
       if (self.xcor() >= (other.xcor() - 20)) and \
       (self.xcor() <= (other.xcor() + 20)) and \
       (self.ycor() >= (other.ycor() - 20)) and \
       (self.ycor() <= (other.ycor() + 20)):
           return True
       else:
           return False


class Player(Sprite):
   def __init__(self, spriteshape, color, startx, starty):
       Sprite.__init__(self, spriteshape, color, startx, starty)
       self.speed = 4
       self.lives = 3

   def turn_left(self):
       self.lt(45)

   def turn_right(self):
       self.rt(45)

   def accelerate(self):
       self.speed += 1

   def decelerate(self):
       self.speed -= 1

class Enemy(Sprite):
   def __init__(self, spriteshape, color, startx, starty):
       Sprite.__init__(self, spriteshape,color,startx,starty)
       self.speed = 6
       self.setheading(random.randint(0,360))

class Pickup(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 0
        self.setheading(random.randint(0,360))

class Ally(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 8
        self.setheading(random.randint(0,360))

    def move(self):
        self.fd(self.speed)

        # Boundary detection
        # check right side of border
        if self.xcor() > 290:
            self.setx(290)
            self.lt(60)
        #
        if self.xcor() < -290:
            self.setx(-290)
            self.lt(60)
            #
        if self.ycor() > 290:
            self.sety(290)
            self.lt(60)
        #
        if self.ycor() < -290:
            self.sety(-290)
            self.lt(60)

class Missile(Sprite):
   def __init__(self, spriteshape, color, startx, starty):
       Sprite.__init__(self,spriteshape, color, startx, starty)
       self.shapesize(stretch_wid=0.3, stretch_len=0.4, outline=None)
       self.speed = 20
       self.status = "ready"
       self.goto(-1000,1000)

   def fire(self):
       if self.status == "ready":
           self.goto(player.xcor(), player.ycor())
           self.setheading(player.heading())
           self.status = "firing"

   def move(self):
       if self.status == "ready":
           self.goto(-1000,1000)

       if self.status == "firing":
           self.fd(self.speed)

       #Border check
       #How can we add this to our Sprite?
       if self.xcor() < -290 or self.xcor() > 290 or \
               self.ycor() < -290 or self.ycor() > 290:
           self.goto(-1000,1000)
           self.status = "ready"


class Game():
   def __init__(self):
       self.level = 1
       self.score = 0
       self.state = True
       self.pen = turtle.Turtle()
       self.lives = 3

   def draw_border(self):
       #Draw border
       self.pen.speed(0)
       self.pen.color("white")
       self.pen.pensize(3)
       self.pen.penup()
       self.pen.goto(-300,300) #could make screen size a variable
       self.pen.pendown()
       for side in range(4):
           self.pen.fd(600) #move forward 600 pixels
           self.pen.rt(90) #turn right 90 degrees
       self.pen.penup() #lift pen so no more drawing
       self.pen.ht() #hide turtle
       self.pen.pendown()

   def show_status(self):
       self.pen.undo()
       msg = "Score: %s" %(self.score)
       self.pen.penup()
       self.pen.goto(-300,310)
       self.pen.write(msg, font=("Arial", 16, "normal"))

   def pause(self):
       if self.state == True:
           self.state =  False
       else:
           self.state = True



#Create game object
game = Game()

#Draw the game border
game.draw_border()

#Show game score
game.show_status()



#Create my sprites
player = Player("triangle", "white", 0,0)

pickup = Pickup("turtle", "green", 100,0)
enemies = []
for i in range(6):
    enemies.append(Enemy("circle", "red", -100,0))
#enemy = Enemy("circle", "red", -100,0)
missile = Missile("triangle", "yellow", 0,0)
allies = []
for x in range(1):
    allies.append(Ally("square", "blue", 0,0,))

#ally = Ally("square", "blue", 0,0)


#Keyboard bindings

turtle.listen()
turtle.onkey(player.turn_left, "a")
turtle.onkey(player.turn_right, "d")
turtle.onkey(player.accelerate, "w")
turtle.onkey(player.decelerate, "s")
turtle.onkey(missile.fire, "space")
turtle.onkey(game.pause, "p")

#Game Loop
while True:
    if game.state:
       player.move()
       missile.move()


       for enemy in enemies:
           enemy.move()

           #Check for a collision with the player
           if player.is_collision(enemy):
               x = random.randint(-250, 250)
               y = random.randint(-250, 250)
               enemy.goto(x, y)
               # Decrease the score
               game.score -= 50
               game.show_status()

           if player.is_collision(pickup):
               x = random.randint(-250, 250)
               y = random.randint(-250, 250)
               pickup.goto(x, y)
               allies.append(Ally("square", "orange", 0,0,))



           #Check fo a collision between the missile and the enemy
           if missile.is_collision(enemy):
               x = random.randint(-250, 250)
               y = random.randint(-250, 250)
               enemy.goto(x, y)
               #Increase the score
               game.score += 100
               game.show_status()

       for ally in allies:
           ally.move()

           if missile.is_collision(ally):
               x = random.randint(-250, 250)
               y = random.randint(-250, 250)
               ally.goto(x, y)
               missile.status = "ready"
               #Decrease the score
               game.score -= 50
               game.show_status()

           if player.is_collision(ally):
               # Decrease the score
               game.score -= 50
               game.show_status()

           if ally.is_collision(enemy):
               x = random.randint(-250, 250)
               y = random.randint(-250, 250)
               enemy.goto(x,y)
               #Increase the score
               game.score+=50
               game.show_status()

    else:
        pass
