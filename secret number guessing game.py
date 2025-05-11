import random

secret=random.randrange(1, 101)

guess=0
tries=0
while guess !=secret:
    guess=int(input("Make a guess:"))
    tries=tries+1

    if guess > secret:
        print("Too High!")
    elif guess < secret:
        print("Too Low!")
    else:
        print("You got it!")
print("Nuber of tries:", tries)
