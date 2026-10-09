
import random
import time
import sys

# Global stats index mapping
# 0: Brains (Intelligence), 1: Feet (Speed/Agility), 2: Arms (Strength), 3: Wand (Magic), 4: Beard (Luck)
statnames = [
    "Brains",  # 0
    "Feet",    # 1
    "Arms",    # 2
    "Wand",    # 3
    "Beard"    # 4
]

class_spaces = [1, 4, 8, 11, 15, 18, 22, 25, 29, 32, 36, 39, 43, 46, 50, 53, 57, 60, 64, 67, 69]
accident_spaces = [5, 10, 16, 20, 26, 31, 37, 41, 47, 52, 58, 62, 68]
shenanigans_spaces = [2, 6, 12, 17, 23, 27, 33, 38, 44, 48, 54, 59, 65]
artifact_spaces = [3, 9, 13, 19, 24, 30, 34, 40, 45, 51, 55, 61, 66]
magicpoly_spaces = [7, 21, 35, 49, 63]
exam_spaces = [14, 28, 42, 56, 70]


def setup():
    """Generates initial random values between 1 and 5 for all five player stats.

    Detailed Algorithm:
        1. Generates pseudo-random integers within specific bounds for each stat:
           - Brains: [1, 5]
           - Feet: [1, 2]
           - Arms: [1, 3]
           - Wand: [1, 3]
           - Beard: [1, 5]
        2. Packs and returns the generated values as a 5-element list.

    Inputs:
        None

    Outputs:
        list[int, int, int, int, int]: Initial values for (Brain, Feet, Arms, Wand, Beard).
    """
    Brain = random.randint(1, 5)  # Intelligence (Index 0)
    Feet = random.randint(1, 2)   # Speed/Agility (Index 1)
    Arms = random.randint(1, 3)   # Strength (Index 2)
    Wand = random.randint(1, 3)   # Magic Ability (Index 3)
    Beard = random.randint(1, 5)  # Luck (Index 4)
    return Brain, Feet, Arms, Wand, Beard


# Initialize global character stats
stats = [int(x) for x in setup()]


def diceRoll():
    """Rolls a 6-sided die and adds a luck-based bonus to determine player movement.

    Detailed Algorithm:
        1. Prompts user to press Enter to initiate roll.
        2. Generates a random integer n in range [1, 6].
        3. Calls Luckboost() to compute additional movement spaces based on the Beard stat.
        4. Calculates total advancement: out = n + Luckboost().
        5. Prints intermediate dice roll and final total spaces.

    Inputs:
        None (Reads user Enter key input from standard input).

    Outputs:
        int: Total number of spaces the player will advance.
    """
    sPrint("-->>Press enter to roll the dice_ ")
    input()
    n = random.randint(1, 6) 
    sPrint(f"The dice roll was {n}")
    
    out = n + Luckboost()
    sPrint(f"You'll advance {out} spaces ")
    return out


def mod_Stat(Stat, mod):
    """Directly modifies a specific stat by adding 'mod' (positive or negative).

    Detailed Algorithm:
        1. Accesses the global `stats` list at position `Stat`.
        2. Adds the modifier `mod` directly to the existing stat value.

    Inputs:
        Stat (int): Target stat index (0 to 4).
        mod (int): Numerical modifier to add to the stat.

    Outputs:
        None (Modifies the global `stats` list in-place).
    """
    stats[Stat] = stats[Stat] + mod


def end():
    """Displays the victory message upon reaching the final tile.

    Detailed Algorithm:
        1. Calls `sPrint()` to print the victory string character by character.

    Inputs:
        None

    Outputs:
        None
    """
    sPrint("Congratulations you graduated and beated MagicPolly!")


# EVENTS

def sPrint(sText):
    """Prints text slowly letter-by-letter to simulate typewriter output.

    Detailed Algorithm:
        1. Converts input `sText` into string format.
        2. Iterates over each character in the string.
        3. Writes character to standard output buffer (`sys.stdout.write`) and flushes immediately.
        4. Delays execution for 0.02 seconds via `time.sleep()`.
        5. Prints a newline at completion.

    Inputs:
        sText (Any): Object or message to be animated and printed.

    Outputs:
        None
    """
    texto = str(sText)
    for letra in texto:
        sys.stdout.write(letra)
        sys.stdout.flush()  # Muestra la letra inmediatamente en la pantalla
        time.sleep(0.02)
    print()


def lecture():
    """Event: Boosts a single random stat by +1/+2 or penalizes it by -1.

    Detailed Algorithm:
        1. Prompts player for Enter key input.
        2. Randomly selects outcome direction n from {-1, 1}.
        3. Selects a random stat index x from [0, 4].
        4. If n == 1 (Success): Adds random boost [1, 2] to stats[x].
        5. If n == -1 (Failure): Subtracts 1 from stats[x].
        6. Prints outcome message with updated stat value.

    Inputs:
        None (Reads Enter input from keyboard).

    Outputs:
        None (Modifies global `stats` list).
    """
    sPrint("You fell in a lecture square ")

    sPrint("You'll atend a lecture, press enter to see how you did ")
    input()
    n = random.choice([-1, 1])
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
    """Event: Solves an accident by guessing a number, resulting in positive or negative stat adjustments.

    Detailed Algorithm:
        1. Prompts user to input an integer between 1 and 5.
        2. Validates input using a try-except block; loops until valid integer in range [1, 5] is entered.
        3. Generates a random target number in range [1, 5].
        4. Selects a random stat index x in range [0, 4].
        5. If guess matches target: Adds random boost [0, 3] to stats[x].
        6. If guess mismatches target: Adds random negative modifier [-3, 0] to stats[x].
        7. Prints outcome with updated stat value.

    Inputs:
        None (Reads user integer guess from keyboard).

    Outputs:
        None (Modifies global `stats` list).
    """
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
    if r == random.randint(1, 5):

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
    """Event: Reduces a single random stat by -1 or -2.

    Detailed Algorithm:
        1. Selects a random stat index x in range [0, 4].
        2. Decrements stats[x] by a random integer in range [1, 2].
        3. Prints message notifying player of penalized stat and new value.

    Inputs:
        None

    Outputs:
        None (Modifies global `stats` list).
    """
    sPrint("You fell in an shenanigan square ")
    x = random.randint(0, 4)
    stats[x] = stats[x] - random.randint(1, 2)
    sPrint(
        f"Whoops your classmates played you a trick and your {statnames[x]} was modified to {stats[x]}"
    )


def artifact():
    """Event: Alters two stats based on an artifact type scaled by player's Beard (Luck) stat.

    Detailed Algorithm:
        1. Prompts user for Enter input.
        2. Roll random artifact index r in range [1, 5].
        3. Maps r to artifact name and two target stat indices (x, y):
           - 1: "Ancient book" -> Brains (0) & Wand (3)
           - 2: "Misterious pill" -> Arms (2) & Beard (4)
           - 3: "Smart shoes" -> Feet (1) & Brains (0)
           - 4: "Magical protein bar" -> Feet (1) & Arms (2)
           - 5: "Talking gloves" -> Arms (2) & Wand (3)
        4. Computes modifier scaled by Beard stat (index 4):
           stat_boost = round((Beard_stat * randint(0, 4)) / 3)
        5. Adds computed modifier to stats[x] and stats[y].
        6. Prints found artifact name and updated stat values.

    Inputs:
        None (Reads Enter key press).

    Outputs:
        None (Modifies global `stats` list).
    """
    sPrint("You stumbled an ancient hidden chest! press enter to continue... ")
    input()
    r = random.randint(1, 5)
    if r == 1:
        x = 0
        y = 3
        art = "Ancient book" 
    elif r == 2:
        x = 2
        y = 4
        art = "Misterious pill"
    elif r == 3:
        x = 1
        y = 0
        art = "Smart shoes"
    elif r == 4:
        x = 1
        y = 2
        art = "Magical protein bar"
    else:
        x = 2
        y = 3
        art = "Talking gloves"

    stats[x] = stats[x] + (round((stats[4] * random.randint(0, 4)) / 3))
    stats[y] = stats[y] + (round((stats[4] * random.randint(0, 4)) / 3))

    sPrint(
        f"Wow you found an {art} your {statnames[x]} and {statnames[y]} were modified to {stats[x]} and {stats[y]}!"
    )


def Magicpolly():
    """Event: Reward event that increases ALL player stats by +1.

    Detailed Algorithm:
        1. Loops through every stat index i in range [0, len(stats)-1].
        2. Increments stats[i] by 1.
        3. Prints notification message.

    Inputs:
        None

    Outputs:
        None (Modifies global `stats` list).
    """
    for i in range(len(stats)):
        stats[i] += 1
    sPrint(
        "Wow you arrived at the magicpolly, all of your stats are increased by 1!"
    )


# --- CHECKPOINTS & MECHANICS ---


def Exam(x):
    """Performs an exam skillcheck test against required difficulty thresholds.

    Detailed Algorithm:
        1. Maps difficulty level parameter x to skillcheck threshold:
           - Level 1 -> Threshold 3
           - Level 2 -> Threshold 4
           - Level 3 -> Threshold 6
           - Level 4 -> Threshold 7
           - Level 5 -> Threshold 10
           - Level 6 -> Threshold 12
        2. Picks a random secondary stat index n in range [0, 4].
        3. Evaluates check condition: Both (stats[n] + Luckboost()) AND (Brain_stat + Luckboost())
           must be greater than or equal to `skillcheck`.
        4. If both pass: Prints success message and returns 1.
        5. Else: Prints failure message and returns 0.

    Inputs:
        x (int): Exam difficulty stage level (1 to 6).

    Outputs:
        int: 1 if exam passed, 0 if exam failed.
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
    """Advances player position by dice roll, soft-capping progress at major milestone exam tiles.

    Detailed Algorithm:
        1. Identifies player's current stage interval bracket (<14, <28, <42, <56, or <70).
        2. Computes prospective new position: new = current + diceRoll().
        3. If `new` exceeds or equals the upper exam milestone tile (14, 28, 42, 56, 70),
           caps `new` exactly at that milestone tile.
        4. Returns the capped `new` position.

    Inputs:
        current (int): Player's current tile position index.

    Outputs:
        int: Updated board position tile index.
    """
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
    """Evaluates tile effects or exam checkpoints for the player's updated position.

    Detailed Algorithm:
        1. Updates position by calling `Position(current)`.
        2. Checks if new position is standard tile vs exam milestone:
           a. Standard tile: Identifies matching category array (`class_spaces`, `accident_spaces`, 
              `artifact_spaces`, `shenanigans_spaces`, `magicpoly_spaces`) and executes event function.
           b. Exam tile (14, 28, 42, 56, 70): Executes corresponding Exam(level) skillcheck.
        3. If exam fails (returns 0):
           - Penalizes player by moving back 5 spaces (`current -= 5`).
           - Gives study consolidation bonus to Brain stat: `stats[0] += randint(0, 1)`.
        4. Returns final resolved board position.

    Inputs:
        current (int): Player's current position prior to dice roll.

    Outputs:
        int: Resolved player position after processing space events/penalties.
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
            stats[0] = stats[0] + random.randint(0, 1)
            sPrint(f"Your brain stat changed to {stats[0]} after doing the exam ")
    elif current == 28:
        if Exam(2) == 0:
            current = current - 5
            stats[0] = stats[0] + random.randint(0, 1)
            sPrint(f"Your brain stat changed to {stats[0]} after doing the exam ")
    elif current == 42:
        if Exam(3) == 0:
            current = current - 5
            stats[0] = stats[0] + random.randint(0, 1)
            sPrint(f"Your brain stat changed to {stats[0]} after doing the exam ")
    elif current == 56:
        if Exam(4) == 0:
            current = current - 5
            stats[0] = stats[0] + random.randint(0, 1)
            sPrint(f"Your brain stat changed to {stats[0]} after doing the exam ")
    elif current == 70:
        if Exam(5) == 0:
            current = current - 5
            stats[0] = stats[0] + random.randint(0, 1)
            sPrint(f"Your brain stat changed to {stats[0]} after doing the exam ")

    else:
        sPrint("error")
    return current


def Luckboost():
    """Calculates a numerical luck boost bonus based on player's Beard stat.

    Detailed Algorithm:
        1. Reads Beard stat value at stats[4].
        2. Generates random float scale multiplier in range [1.0, 2.0) via `random.random() + 1`.
        3. Computes formula: bonus = round((stats[4] * multiplier) / 4).
        4. Returns rounded integer bonus value.

    Inputs:
        None

    Outputs:
        int: Numerical luck bonus addition.
    """
    return round((stats[4] * (random.random() + 1)) / 4)


def Turn(Pos, name):
    """Executes a single turn cycle for the player.

    Detailed Algorithm:
        1. Prints player turn header message.
        2. Checks win condition (`Pos >= 70`).
        3. If win condition met: Calls `end()` and returns 70 to terminate loop.
        4. Otherwise: Calls `box(Pos)` to roll, move, and trigger tile effects, returning new position.

    Inputs:
        Pos (int): Player's starting position for the turn.
        name (str): Player's character name.

    Outputs:
        int: Player's new position after completing the turn (70 indicates game completion).
    """
    sPrint(f">>>>>Start of your turn {name}")

    if Pos >= 70:
        end()
        return 70  # Signals loop termination
    else:
        newPosition = box(Pos)
        return newPosition


def main():
    """Main game orchestration function.

    Detailed Algorithm:
        1. Initializes player position `currentP = 0`.
        2. Prompts user for player name input.
        3. Prints starting character stats using `sPrint()`.
        4. Enters main game loop (`while currentP != 70`).
        5. Invokes `Turn(currentP, name)` on each loop iteration until end tile (70) is reached.

    Inputs:
        None (Reads user input from stdin).

    Outputs:
        None
    """
    currentP = 0  # Starting position
    name = input("Insert user's name ")

    for stat, statname in zip(stats, statnames):
        sPrint(f"Your {statname} value is {stat}")

    # Main gameplay loop
    while currentP != 70:
        currentP = Turn(currentP, name)


main()

