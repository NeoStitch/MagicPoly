import random
import sys
import time

# --- CONFIGURACIÓN GLOBAL ---
statnames = ["Brains", "Feet", "Arms", "Wand", "Beard"]

EXAM_MILESTONES = [(14, 3), (28, 4), (42, 6), (56, 7), (70, 10)]

ARTIFACTS_DATA = [
    [0, 3, "Libro Antiguo"],
    [2, 4, "Píldora Misteriosa"],
    [1, 0, "Zapatos Inteligentes"],
    [1, 2, "Barra Proteica Mágica"],
    [2, 3, "Guantes Parlantes"],
]

BOARD_CONFIG = {
    "C": [1, 4, 8, 11, 15, 18, 22, 25, 29, 32, 36, 39, 43, 46, 50, 53, 57, 60, 64, 67, 69],
    "A": [5, 10, 16, 20, 26, 31, 37, 41, 47, 52, 58, 62, 68],
    "S": [2, 6, 12, 17, 23, 27, 33, 38, 44, 48, 54, 59, 65],
    "R": [3, 9, 13, 19, 24, 30, 34, 40, 45, 51, 55, 61, 66],
    "M": [7, 21, 35, 49, 63],
    "E": [14, 28, 42, 56, 70],
}


def setup():
    """Generates initial random values between 1 and 5 for all five player stats."""
    ranges = [(1, 5), (1, 2), (1, 3), (1, 3), (1, 5)]
    return [random.randint(low, high) for low, high in ranges]


# Initialize global character stats
stats = setup()


def sPrint(sText):
    texto = str(sText)
    for letra in texto:
        sys.stdout.write(letra)
        sys.stdout.flush()
        time.sleep(0.015)
    print()


def Luckboost():
    return round((stats[4] * (random.random() + 1)) / 4)


def diceRoll():
    """Utility helper to roll a 6-sided die and add Beard (Luck) modifier."""
    sPrint("-->> Press enter to roll the dice_ ")
    input()
    n = random.randint(1, 6)
    sPrint(f"The dice roll was {n}")

    out = n + Luckboost()
    sPrint(f"You'll advance {out} spaces ")
    return out


def end():
    """Displays the victory message upon reaching the final tile."""
    sPrint("\n🎓 Congratulations! You graduated and beat MagicPolly!")


# --- GESTIÓN DEL TABLERO EN MATRIZ ---


def get_tile_type(pos):
    """Devuelve el identificador del tipo de casilla según su número."""
    for t_type, spaces in BOARD_CONFIG.items():
        if pos in spaces:
            return t_type
    return "."


def build_board_matrix(player_pos):
    """Crea una matriz de 7x10 e inserta al jugador en su posición actual."""
    rows, cols = 7, 10
    matrix = []
    for r in range(rows):
        row_list = []
        for c in range(cols):
            tile_num = r * cols + c + 1
            if tile_num == player_pos:
                row_list.append("[ 🧙 ]")
            else:
                t_type = get_tile_type(tile_num)
                row_list.append(f"[{t_type:^3}]")
        matrix.append(row_list)
    return matrix


def display_board(player_pos):
    """Imprime la matriz del tablero formateada en consola."""
    matrix = build_board_matrix(player_pos)
    print("\n" + "=" * 50)
    print(f" MAPA DEL TABLERO (Posición actual: {player_pos}/70)")
    print("=" * 50)
    for row in matrix:
        print(" ".join(row))
    print("=" * 50 + "\n")


# --- EVENTOS ---


def lecture():
    """Event: Boosts or reduces a single random stat."""
    sPrint("You fell in a lecture square")
    sPrint("You'll attend a lecture, press enter to see how you did ")
    input()
    n = random.choice([-1, 1])
    x = random.randint(0, 4)
    if n == 1:
        stats[x] += random.randint(1, 2)
        sPrint(f"Congrats! You took a class and your {statnames[x]} improved to {stats[x]}")
    else:
        stats[x] = max(0, stats[x] - 1)
        sPrint(f"Unfortunately, you fell asleep during the lecture. Your {statnames[x]} changed to {stats[x]}")


def accident():
    """Event: Randomly modifies a single stat."""
    sPrint("You fell in an accident square")
    while True:
        try:
            r = int(input("Oh no! An accident occurred during class. Choose a number between 1 and 5 to try to solve it: "))
            if 1 <= r <= 5:
                break
            print("Answer must be a number between 1 and 5!")
        except ValueError:
            sPrint("Must be an integer number")

    x = random.randint(0, 4)
    if r == random.randint(1, 5):
        stats[x] += random.randint(0, 3)
        sPrint(f"Great job! Your {statnames[x]} was modified to {stats[x]}!")
    else:
        stats[x] = max(0, stats[x] - random.randint(0, 3))
        sPrint(f"Unlucky... Your {statnames[x]} was modified to {stats[x]}!")


def Shenaningan():
    """Event: Reduces a single random stat."""
    sPrint("You fell in a shenanigan square")
    x = random.randint(0, 4)
    stats[x] = max(0, stats[x] - random.randint(1, 2))
    sPrint(f"Whoops! Your classmates played a trick on you and your {statnames[x]} was modified to {stats[x]}")


def artifact():
    """Event: Alters two random stats scaling with Beard (Luck). CORREGIDO DUPLICADO."""
    sPrint("You stumbled upon an ancient hidden chest! Press enter to continue...")
    input()
    x, y, art = random.choice(ARTIFACTS_DATA)

    stats[x] += round((stats[4] * random.randint(0, 4)) / 3)
    stats[y] += round((stats[4] * random.randint(0, 4)) / 3)

    sPrint(f"Wow! You found a {art}! Your {statnames[x]} and {statnames[y]} were modified to {stats[x]} and {stats[y]}!")


def Magicpolly():
    """Event: Increases ALL player stats by +1."""
    for i in range(len(stats)):
        stats[i] += 1
    sPrint("Wow! You arrived at Magicpolly! All of your stats increased by 1!")


# --- CHECKPOINTS & MECÁNICAS ---


def Exam(difficulty):
    """Realiza la prueba de examen según la dificultad recibida."""
    sPrint(f"You fell in an exam square (Difficulty: {difficulty})")
    n = random.randint(0, 4)
    if stats[n] + Luckboost() >= difficulty and stats[0] + Luckboost() >= difficulty:
        sPrint("You passed your exam!")
        return 1
    else:
        sPrint("You failed your exam...")
        return 0


def Position(current):
    """Avanza la posición limitando el avance en las casillas de examen mediante EXAM_MILESTONES."""
    target = current + diceRoll()
    for milestone, _ in EXAM_MILESTONES:
        if current < milestone <= target:
            return milestone
    return min(target, 70)


def box(current):
    """Evalúa la casilla actual usando el mapa de BOARD_CONFIG y EXAM_MILESTONES."""
    current = Position(current)
    display_board(current)

    exam_dict = dict(EXAM_MILESTONES)
    if current in exam_dict:
        if Exam(exam_dict[current]) == 0:
            current = max(0, current - 5)
            stats[0] += random.randint(0, 1)
            sPrint(f"Your brain stat changed to {stats[0]} after failing the exam.")
        return current

    tile_type = get_tile_type(current)
    if tile_type == "C":
        lecture()
    elif tile_type == "A":
        accident()
    elif tile_type == "S":
        Shenaningan()
    elif tile_type == "R":
        artifact()
    elif tile_type == "M":
        Magicpolly()

    return current


def Turn(Pos, name):
    sPrint(f"\n>>>>> Start of your turn: {name}")
    return box(Pos)


def main():
    currentP = 0
    name = input("Insert user's name: ").strip() or "Mago"

    print("\n--- INITIAL PLAYER STATS ---")
    for stat, statname in zip(stats, statnames):
        sPrint(f" • Your {statname} value is {stat}")
    print("----------------------------\n")

    while currentP < 70:
        currentP = Turn(currentP, name)

    end()


if __name__ == "__main__":
    main()
