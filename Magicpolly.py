import random

# Global stats 
# 0: Brains (Intelligence), 1: Feet (Speed/Agility), 2: Arms (Strength), 3: Wand (Magic), 4: Beard (Luck)
statnames = ["Brains", "Feet", "Arms", "Wand", "Beard"]


def setup():
    """Generates initial random values between 1 and 5 for all five player stats."""
    Brain = random.randint(1, 5)  # Intelligence (Index 0)
    Feet = random.randint(1, 5)  # Speed/Agility (Index 1)
    Arms = random.randint(1, 5)  # Strength (Index 2)
    Wand = random.randint(1, 5)  # Magic Ability (Index 3)
    Beard = random.randint(1, 5)  # Luck (Index 4)
    return Brain, Feet, Arms, Wand, Beard


# Initialize global character stats
stats = [int(x) for x in setup()]


def diceRoll(x):
    """Utility helper to roll a 6-sided die and add a modifier 'x' if wanted, in a future this may be the beard stat."""
    return random.randint(1, 6) + x


def mod_Stat(Stat, mod):
    """Directly modifies a specific stat by adding 'mod' (positive or negative)."""
    stats[Stat] = stats[Stat] + mod


def end():
    """Displays the victory message upon reaching the final tile."""
    print("Congratulations you gained MagicPolly")


# EVENTS


def lecture():
    """Event: Boosts a single random stat by +1 or +2."""
    x = random.randint(0, 4)
    stats[x] = stats[x] + random.randint(1, 2)
    print(
        f"Congrats you took a class and your {statnames[x]} improved to {stats[x]}"
    )


def accident():
    """Event: Randomly modifies a single stat between -2 and +2."""
    x = random.randint(0, 4)
    stats[x] = stats[x] + random.randint(-2, 2)
    print(
        f"Oh no! You failed a class and your {statnames[x]} was modified to {stats[x]}"
    )


def Shenaningan():
    """Event: Reduces a single random stat by -1 or -2."""
    x = random.randint(0, 4)
    stats[x] = stats[x] - random.randint(1, 2)
    print(
        f"Whoops your classmates played you a trick and your {statnames[x]} was modified to {stats[x]}"
    )


def artifact():
    """Event: Alters a random stat using a formula scaled by the player's Beard (Luck) stat."""
    x = random.randint(0, 4)
    stats[x] = stats[x] + (round((stats[4] * random.randint(-4, 4)) / 3))
    print(
        f"Wow you found an artifact your {statnames[x]} was modified to {stats[x]}!"
    )


def Magicpolly():
    """Event: Reward event that increases ALL player stats by +1."""
    for i in range(len(stats)):
        stats[i] += 1
    print(
        "Wow you arrived at the magicpolly, all of your stats are increased by 1!"
    )


# --- CHECKPOINTS & MECHANICS ---


def Exam(x):
    """Performs an exam skillcheck (Difficulty Levels: 1=7, 2=10, 3=12).

    Tests a random stat boosted by Beard (Luck). Returns 1 on pass, 0 on
    fail.
    """
    if x == 1:
        skillcheck = 7
    elif x == 2:
        skillcheck = 10
    elif x == 3:
        skillcheck = 12

    # Stat check calculation: Target Stat + Beard Luck modifier
    if stats[random.randint(0, 4)] + round(
        stats[4] * (random.random() + 1)
    ) >= skillcheck:
        print("you passed your exam")
        return 1
    else:
        print("you failed your exam")
        return 0


def Position(current):
    """Advances player position by dice roll, soft-capping progress at major milestone exames tiles (10, 15, 20)."""
    if current < 10:
        new = current + random.randint(1, 6)
        if new >= 10:
            new = 10  # Cap at lower exam milestone
    elif current < 15:
        new = current + random.randint(1, 6)
        if new >= 15:
            new = 15  # Cap at middle exam milestone
    elif current < 20:
        new = current + random.randint(1, 6)
        if new >= 20:
            new = 20  # Cap at final exam milestone

    return new


def box(current):
    """Evaluates the player's new position.

    Triggers a random event on standard tiles, or triggers an Exam on
    milestones (10, 15, 20). Failing an exam pushes the player back 5 spaces.
    """
    current = Position(current)

    # Standard Tiles: Random Event Roll
    if current != 10 and current != 15 and current != 20:
        n = random.randint(1, 5)
        if n == 1:
            lecture()
        elif n == 2:
            accident()
        elif n == 3:
            artifact()
        elif n == 4:
            Shenaningan()
        elif n == 5:
            Magicpolly()

    # Milestone Tiles: Exam Checks
    elif current == 10:
        if Exam(1) == 0:
            current = current - 5
    elif current == 15:
        if Exam(2) == 0:
            current = current - 5
    elif current == 20:
        if Exam(3) == 0:
            current = current - 5
    else:
        print("error")

    return current


def StatCheck(stat, V, skillcheck):
    """Helper function to test a specific stat against a difficulty threshold.

    Option V=1 applies Beard (Luck) scaling; V=0 compares raw stat.
    """
    if V == 1:
        if stats[stat] + round(
            stats[4] * (random.random() + 1)
        ) >= skillcheck:
            return 1
        else:
            return 0
    else:
        if stat >= skillcheck:
            return 1
        else:
            return 0


def void(CurrentP):
    """Manages the main game loop turn step.

    Checks if goal is reached or processes tile progression.
    """
    if CurrentP == 20:
        end()
        return 21  # Signals loop termination
    else:
        newPosition = box(CurrentP)
        return newPosition


def main_test():
    """Main testing routine to run a full simulated game session."""
    currentP = 0  # Starting position

    name = input("Insert user's name ")
    for stat, statname in zip(stats, statnames):
        print(f"Your {statname} value is {stat}")

    # Main gameplay loop
    while currentP != 21:
        currentP = void(currentP)


main_test()