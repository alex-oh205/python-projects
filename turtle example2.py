import random
import turtle
fred=turtle.Pen()

fred.shape("turtle")
fred.width(3)
fred.speed(0)

colorlist=["red", "green", "blue", "orange", "yellow"]

def square(size):
    for i in range(8):
        fred.forward(size)
        fred.left(225)

for i in range(200):
    x=random.randrange(-300, 300)
    y=random.randrange(-300, 300)
    fred.up()
    fred.goto(x, y)
    fred.down()
    col=random.choice(colorlist)
    fred.color(col)
    square(random.randrange(10, 300))
