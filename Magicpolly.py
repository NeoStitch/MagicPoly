import random
import time
import sys

# Global stats 
# 0: Brains (Intelligence), 1: Feet (Speed/Agility), 2: Arms (Strength), 3: Wand (Magic), 4: Beard (Luck)
statnames = [
 "Brains", #0
 "Feet",   #1
 "Arms",   #2
 "Wand",   #3
 "Beard"   #4
 ]
class_spaces = [1, 4, 8, 11, 15, 18, 22, 25, 29, 32, 36, 39, 43, 46, 50, 53, 57, 60, 64, 67, 69]
accident_spaces = [5, 10, 16, 20, 26, 31, 37, 41, 47, 52, 58, 62, 68]
shenanigans_spaces = [2, 6, 12, 17, 23, 27, 33, 38, 44, 48, 54, 59, 65]
artifact_spaces = [3, 9, 13, 19, 24, 30, 34, 40, 45, 51, 55, 61, 66]
magicpoly_spaces = [7, 21, 35, 49, 63]
exam_spaces = [14, 28, 42, 56, 70]




def setup():
    """Generates initial random values between 1 and 5 for all five player stats."""
    Brain = random.randint(1, 5)  # Intelligence (Index 0)
    Feet = random.randint(1, 2)  # Speed/Agility (Index 1)
    Arms = random.randint(1, 3)  # Strength (Index 2)
    Wand = random.randint(1, 3)  # Magic Ability (Index 3)
    Beard = random.randint(1, 5)  # Luck (Index 4)
    return Brain, Feet, Arms, Wand, Beard


# Initialize global character stats
stats = [int(x) for x in setup()]


def diceRoll():
    """Utility helper to roll a 6-sided die and add a modifier 'x' if wanted, in a future this may be the beard stat."""
    sPrint("-->>Press enter to roll the dice_ ")
    input ()
    n = random.randint(1, 6) 
    sPrint(f"The dice roll was {n}")
    
    out = n + Luckboost()
    sPrint(f"You'll advance {out} spaces ")
    return out


def mod_Stat(Stat, mod):
    """Directly modifies a specific stat by adding 'mod' (positive or negative)."""
    stats[Stat] = stats[Stat] + mod


def end():
    """Displays the victory message upon reaching the final tile."""
    sPrint("Congratulations you graduated and beated MagicPolly!")


# EVENTS

def sPrint(sText):
    texto = str(sText)
    for letra in texto:
        sys.stdout.write(letra)
        sys.stdout.flush()  # Muestra la letra inmediatamente en la pantalla
        time.sleep(0.02)
    print()


def lecture():
    """Event: Boosts a single random stat by +1 or +2."""
    sPrint("You fell in a lecture square ")

    sPrint("You'll atend a lecture, press enter to see how you did ")
    input()
    n = random.choice([-1,1])
    x = random.randint(0, 4)
    if n == 1:
        stats[x] = stats[x] + random.randint(1, 2)
        sPrint(
            f"Congrats you took a class and your {statnames[x]} improved to {stats[x]}"
        )
    else:
        stats[x] = stats[x] - 1
        sPrint(
            f"Unfortunately, you fell asleep during the lecture and you were reprehended, your {statnames[x]} changed to {stats[x]}"
        )


def accident():
    """Event: Randomly modifies a single stat between -2 and +2."""
    sPrint("You fell in an accident square ")
    while True:
        try:
            print("Oh no! accident occured during a class. Quick choose a number between 1 to 5 to try to solve it ")
            r = int(input())
            if r > 5 or r < 1:
                print("Answer must be number between 1 to 5! ")
                continue
            break

        except ValueError:
            sPrint("Must be an int number")
    if r == random.randint(1,5):

        x = random.randint(0, 4)
        stats[x] = stats[x] + random.randint(0, 3)
        sPrint(
            f" your {statnames[x]} was modified to {stats[x]}!"
        )
    else:
        x = random.randint(0, 4)
        stats[x] = stats[x] + random.randint(-3, 0)
        sPrint(
            f" your {statnames[x]} was modified to {stats[x]}!"
        )


def Shenaningan():
    """Event: Reduces a single random stat by -1 or -2."""
    sPrint("You fell in an shenanigan square ")
    x = random.randint(0, 4)
    stats[x] = stats[x] - random.randint(1, 2)
    sPrint(
        f"Whoops your classmates played you a trick and your {statnames[x]} was modified to {stats[x]}"
    )


def artifact():
    """Event: Alters a random stat using a formula scaled by the player's Beard (Luck) stat."""
    sPrint("You stumbled an ancient hidden chest! press enter to continue... ")
    input()
    r = random.randint(1,5)
    if r == 1:
        x = 0
        y = 3
        art = "Ancient book" 
    elif r==2:
        x = 2
        y = 4
        art = "Misterious pill"
    elif r ==3:
        x = 1
        y = 0
        art = "Smart shoes"
    elif r == 4:
        x = 1
        y = 2
        art = "Magical protein bar"
    else:
        x=2
        y=3
        art = "Talking gloves"
   


    stats[x] = stats[x] + (round((stats[4] * random.randint(0, 4)) / 3))
    stats[y] = stats[y] + (round((stats[4] * random.randint(0, 4)) / 3))

    sPrint(
        f"Wow you found an {art} your {statnames[x]} and {statnames[y]} were modified to {stats[x]} and {stats[y]}!"
    )


def Magicpolly():
    """Event: Reward event that increases ALL player stats by +1."""
    for i in range(len(stats)):
        stats[i] += 1
    sPrint(
        "Wow you arrived at the magicpolly, all of your stats are increased by 1!"
    )


# --- CHECKPOINTS & MECHANICS ---


def Exam(x):
    """Performs an exam skillcheck (Difficulty Levels: 1=7, 2=10, 3=12).
    
    Tests a random stat boosted by Beard (Luck). Returns 1 on pass, 0 on
    fail.
    """
    sPrint("You fell in an exam square ")

    n = random.randint(0, 4)
    if x == 1:
        skillcheck = 3
    elif x == 2:
        skillcheck = 4
    elif x == 3:
        skillcheck = 6
    elif x == 4:
        skillcheck = 7
    elif x == 5:
        skillcheck = 10
    elif x == 6:
        skillcheck = 12

    # Stat check calculation: Target Stat + Beard Luck modifier
    if stats[n] + Luckboost() >= skillcheck and stats[0] + Luckboost() >= skillcheck:
        sPrint("you passed your exam")
        return 1
    else:
        sPrint("you failed your exam")
        return 0


def Position(current):
    """Advances player position by dice roll, soft-capping progress at major milestone exames tiles (10, 15, 20)."""
    if current < 14:
        new = current + diceRoll()  
        if new >= 14:
            new = 14  # Cap at lower exam milestone
    elif current < 28:
        new = current + diceRoll()
        if new >= 28:
            new = 28  # Cap at middle exam milestone
    elif current < 42:
        new = current + diceRoll()
        if new >= 42:
            new = 42  # Cap at final exam milestone
    elif current < 56:
        new = current + diceRoll()
        if new >= 56:
            new = 56  # Cap at middle exam milestone
    elif current < 70:
        new = current + diceRoll()
        if new >= 70:
            new = 70  # Cap at final exam milestone


    return new


def box(current):
    """Evaluates the player's new position.

    Triggers a random event on standard tiles, or triggers an Exam on
    milestones (10, 15, 20). Failing an exam pushes the player back 5 spaces.
    """
    current = Position(current)
    sPrint(f"You are now in the {current} box ")


    # Standard Tiles: Random Event Roll
    if current not in exam_spaces:
    
        if current in class_spaces:
            lecture()
        elif current in accident_spaces:
            accident()
        elif current in artifact_spaces:
            artifact()
        elif current in shenanigans_spaces:
            Shenaningan()
        elif current in magicpoly_spaces:
            Magicpolly()
        else:
            sPrint("Error no casilla posible")

    # Milestone Tiles: Exam Checks
    elif current == 14:
        if Exam(1) == 0:
            current = current - 5
            stats[0] = stats[0] + random.randint(0,1)
            sPrint(f"Your brain stat changed to {stats[0]} after doing the exam ")
    elif current == 28:
        if Exam(2) == 0:
            current = current - 5
            stats[0] = stats[0] + random.randint(0,1)
            sPrint(f"Your brain stat changed to {stats[0]} after doing the exam ")
    elif current == 42:
        if Exam(3) == 0:
            current = current - 5
            stats[0] = stats[0] + random.randint(0,1)
            sPrint(f"Your brain stat changed to {stats[0]} after doing the exam ")
    elif current == 56:
        if Exam(4) == 0:
            current = current - 5
            stats[0] = stats[0] + random.randint(0,1)
            sPrint(f"Your brain stat changed to {stats[0]} after doing the exam ")
    elif current == 70:
        if Exam(5) == 0:
            current = current - 5
            stats[0] = stats[0] + random.randint(0,1)
            sPrint(f"Your brain stat changed to {stats[0]} after doing the exam ")

    else:
        sPrint("error")
    return current


def Luckboost():


    return round((stats[4] * (random.random() + 1))/4)
       
            


"""def void(CurrentP):
    Manages the main game loop turn step.

    Checks if goal is reached or processes tile progression.
    
    if CurrentP == 20:
        end()
        return 21  # Signals loop termination
    else:
        newPosition = box(CurrentP)
        return newPosition"""


def Turn(Pos,name):
    sPrint(f">>>>>Start of your turn {name}")
    
     

    if Pos >= 70:
        end()
        return 70  # Signals loop termination
    else:
        newPosition = box(Pos)
        return newPosition
    






def main():
    currentP = 0  # Starting position
    name = input("Insert user's name ")


    for stat, statname in zip(stats, statnames):
        sPrint(f"Your {statname} value is {stat}")

    # Main gameplay loop
    while currentP != 70:
        currentP = Turn(currentP,name)



main()