import random
import sys
import time
import pyfiglet as fi
import readchar as read
import os
from pygame import mixer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()
try:
    mixer.init()
    AUDIO_ENABLED = True
except Exception:
    AUDIO_ENABLED = False
    print("[yellow]Audio initialization failed. Sound effects will be disabled.[/yellow]")

# --- Global configuration ---
statnames = ["Brains", "Feet", "Arms", "Wand", "Beard"]

Sound_Effects = {
    "dice": "Sounds/diceE.mp3",
    "Victory": "Sounds/Victory!.wav",
    "Music": "Sounds/Magic Music - A Wizards Dream (Beautiful Violin).mp3",
    "fail": "Sounds/fail.wav",
    "Success":"Sounds/magical_4.ogg",
    "MagicPolly": "Sounds/magical_1.ogg",
    "Coin": "Sounds/coin.wav",
}
SOUNDS = {}
if AUDIO_ENABLED:
    for name, path in Sound_Effects.items():
        if os.path.exists(path):
            snd = mixer.Sound(path)
            snd.set_volume(0.5)  # Volumen entre 0.0 y 1.0
            SOUNDS[name] = snd
        else: 
            print(f"[yellow]Sound file '{path}' not found. '{name}' sound will be disabled.[/yellow]")

def Playsound(name):
    if AUDIO_ENABLED and name in SOUNDS:
        SOUNDS[name].play()
if AUDIO_ENABLED and "Music" in Sound_Effects and os.path.exists(Sound_Effects["Music"]):
    mixer.music.load(Sound_Effects["Music"])
    mixer.music.set_volume(0.25) 
    mixer.music.play(-1)
    
EXAM_MILESTONES = [(14, 3), (28, 4), (42, 6), (56, 7), (70, 10)]

ARTIFACTS_INFO = {
    "Ancient book": "[Exam] Consume before an exam for +3 bonus.",
    "Misterious pill": "[Dice] Consume after rolling to re-roll the die.",
    "Smart Shoes": "[Passive] Automatically adds +1 movement to every roll.",
    "Magical protein bar": "[Active] Eat before your turn for +2 Arms or +2 Feet.",
    "Talking gloves": "[Danger] Consume in an Accident/Shenanigan to auto-win (+1 Wand).",
}

MAX_INVENTORY = 5

BOARD_CONFIG = {
    "C": [1, 4, 8, 11, 15, 18, 22, 25, 29, 32, 36, 39, 43, 46, 50, 53, 57, 60, 64, 67, 69],
    "A": [5, 10, 16, 20, 26, 31, 37, 41, 47, 52, 58, 62, 68],
    "S": [2, 6, 12, 17, 23, 27, 33, 38, 44, 48, 54, 59, 65],
    "R": [3, 9, 13, 19, 24, 30, 34, 40, 45, 51, 55, 61, 66],
    "M": [7, 21, 35, 49, 63],
    "E": [14, 28, 42, 56, 70],
}

TILE_COLORS = {
    "C": "[cyan][ C ][/cyan]",
    "A": "[bold red][ A ][/bold red]",
    "S": "[magenta][ S ][/magenta]",
    "R": "[green][ R ][/green]",
    "M": "[bold gold1][ M ][/bold gold1]",
    "E": "[bold yellow][ E ][/bold yellow]",
}


def sPrint(sText, delay=0.015):
    formatted_text = console.render_str(str(sText))
    for char in formatted_text:
        console.print(char, end="", highlight=False)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def setup():
    """Generates initial random values for all five player stats."""
    ranges = [(1, 5), (1, 2), (1, 3), (1, 3), (1, 5)]
    return [random.randint(low, high) for low, high in ranges]


def Luckboost(stats):
    return round((stats[4] * (random.random() + 1)) / 4)


def spell_minigame(length=5, base_time=1.3, stat_bonus=0):
    """Reflex minigame: type the random key sequence before the timer expires."""
    keys_pool = ["W", "A", "S", "D", "E", "Q"]
    sequence = "".join(random.choices(keys_pool, k=length))
    time_limit = round(base_time + (stat_bonus * 0.1), 2)

    sPrint(f"[bold yellow]Get ready! You have {time_limit}s to cast a {length}-key spell.[/bold yellow]")
    sPrint("[dim]Press any key when ready to reveal the incantation...[/dim]")
    read.readkey()

    console.print(f"\n[bold magenta]>>> QUICK! PRESS:  {' - '.join(sequence)} <<<[/bold magenta]")
    console.print("Input: ", end="")
    sys.stdout.flush()

    start = time.time()
    for expected in sequence:
        key = read.readkey().upper()
        elapsed = time.time() - start
        if key != expected:
            console.print(f"[bold red]{key} (Wrong key! Expected {expected})[/bold red]")
            return False
        if elapsed > time_limit:
            console.print(f"[bold red]{key} (Too slow! {elapsed:.2f}s / {time_limit}s)[/bold red]")
            return False
        console.print(f"[bold green]{key}[/bold green] ", end="")
        sys.stdout.flush()

    total_time = time.time() - start
    Playsound("Success")
    console.print(f"\n[bold green]Spell cast cleanly in {total_time:.2f}s![/bold green]")
    return True


def diceRoll(stats, inventory):
    """Rolls a 6-sided die, allows Misterious pill reroll, and applies Smart Shoes + Beard."""
    sPrint("\n [bold blue]-->> Press any key to roll the dice_ [/bold blue]")
    read.readkey()
    n = random.randint(1, 6)
    Playsound("dice")
    sPrint(f"The dice roll was [red]{n}[/red]")

    if "Misterious pill" in inventory:
        ans = input("Use [Misterious pill] to re-roll the die? (y/n): ").strip().lower()
        if ans == "y":
            inventory.remove("Misterious pill")
            n = random.randint(1, 6)
            sPrint(f"You swallowed the pill! Your new roll is [bold green]{n}[/bold green]")

    luck = Luckboost(stats)
    shoe_bonus = 1 if "Smart Shoes" in inventory else 0
    if shoe_bonus:
        sPrint("[cyan]Smart Shoes activated! (+1 extra space)[/cyan]")

    out = n + luck + shoe_bonus
    sPrint(f"Luck bonus: +{luck} | You'll advance [cyan]{out}[/cyan] spaces")
    return out


def end():
    """Displays the victory message upon reaching the final tile."""
    Playsound("Victory")
    banner = fi.figlet_format("Graduated!", font="slant")
    console.print(f"[bold gold1]{banner}[/bold gold1]")
    content = "\n [bold gold1]Congratulations! You graduated and beat MagicPolly![/bold gold1]"
    console.print(Panel(content, border_style="gold1", expand=False))


# --- INTERFAZ: TABLERO, STATS E INVENTARIO ---

def display_Stats(stats, statnames, inventory):
    table = Table(title="Current Stats & Backpack", style="white", header_style="bold cyan")
    table.add_column("Stat", justify="left")
    table.add_column("Value", justify="right", style="bold blue")
    for name, val in zip(statnames, stats):
        table.add_row(name, str(val))
    console.print(table)

    if inventory:
        inv_lines = [f"• [bold green]{item}[/bold green]: {ARTIFACTS_INFO[item]}" for item in inventory]
        inv_text = "\n".join(inv_lines)
    else:
        inv_text = "[dim]Your backpack is empty. Land on [ R ] tiles to find artifacts![/dim]"

    console.print(Panel(inv_text, title=f"Backpack ({len(inventory)}/{MAX_INVENTORY})", border_style="green", expand=False))


def get_tile_type(pos):
    for t_type, spaces in BOARD_CONFIG.items():
        if pos in spaces:
            return t_type
    return "."


def display_board(player_pos):
    rows, cols = 7, 10
    board_output = ""
    for r in range(rows):
        row_list = []
        for c in range(cols):
            tile_num = r * cols + c + 1
            if tile_num == player_pos:
                row_list.append("[[bold yellow]⊙_⊙[/bold yellow]]")
            else:
                t_type = get_tile_type(tile_num)
                row_list.append(TILE_COLORS.get(t_type, f"[{t_type:^3}]"))
        board_output += " ".join(row_list) + "\n"

    legend = "[cyan][C] Class[/cyan]  [red][A] Accident[/red]  [magenta][S] Shenanigan[/magenta]  [green][R] Artifact[/green]  [gold1][M] MagicPolly[/gold1]  [yellow][E] Exam[/yellow]"
    console.print(
        Panel(
            f"{board_output.strip()}\n\n{legend}",
            title=f" MagicPolly Board (Position: [bold yellow]{player_pos}/70[/bold yellow])",
            border_style="blue",
            expand=False,
        )
    )


def use_item_action(stats, inventory):
    """Allows the player to consume active items before rolling the dice."""
    if not inventory:
        sPrint("[yellow]Your backpack is empty![/yellow]")
        return

    if "Magical protein bar" not in inventory:
        sPrint("[yellow]You have no active items to eat right now (your current items trigger automatically during rolls, dangers, or exams).[/yellow]")
        return

    sPrint("[green]You take out the Magical protein bar![/green]")
    choice = input("Choose which stat to boost by +2: <1> Feet  <2> Arms  <3> Cancel\n> ").strip()
    if choice == "1":
        inventory.remove("Magical protein bar")
        stats[1] += 2
        sPrint(f"[bold green]Delicious! Your Feet increased to {stats[1]}![/bold green]")
    elif choice == "2":
        inventory.remove("Magical protein bar")
        stats[2] += 2
        sPrint(f"[bold green]Power up! Your Arms increased to {stats[2]}![/bold green]")
    else:
        sPrint("Cancelled.")


# --- EVENTOS CON TOMA DE DECISIONES Y MINIJUEGO ---

def lecture(stats):
    """Event: Safe notes (+1) or risky spell minigame (+3 / -2)."""
    sPrint("[cyan]You fell in a Lecture square![/cyan]")
    sPrint("The professor is demonstrating a tricky incantation. How do you act?")
    while True:
        choice = input(
            "  <1> Option A (Safe): Take quiet notes (+1 guaranteed to a random stat)\n"
            "  <2> Option B (Risky): Cast the advanced spell (Reflex Minigame -> +3, else -2)\n> "
        ).strip()
        if choice in ("1", "2"):
            break
        sPrint("[red]Choose 1 or 2![/red]")

    x = random.randint(0, 4)
    if choice == "1":
        stats[x] += 1
        sPrint(f"[green]Steady progress! Taking notes improved your {statnames[x]} to {stats[x]}.[/green]")
    else:
        sPrint(f"[cyan]Brains bonus grants extra casting time (+{stats[0] * 0.35:.2f}s)![/cyan]")
        if spell_minigame(length=4, base_time=2.3, stat_bonus=stats[0]):
            target = random.choice([0, 3])  # Brains o Wand
            stats[target] += 3
            Playsound("Success")
            sPrint(f"[bold green]Brilliant! The professor is impressed: +3 {statnames[target]} (now {stats[target]})![/bold green]")
        else:
            stats[x] = max(0, stats[x] - 2)
            Playsound("fail")
            sPrint(f"[bold red]The spell fizzled! You lost -2 {statnames[x]} (now {stats[x]}).[/bold red]")


def accident(stats, inventory):
    """Event: Dodge with Feet check, cast a shield via reflex minigame, or use Talking gloves."""
    sPrint("[bold red]You fell in an Accident square! A potion cauldron is about to explode![/bold red]")

    if "Talking gloves" in inventory:
        ans = input("Use [Talking gloves] to safely contain the explosion? (y/n): ").strip().lower()
        if ans == "y":
            inventory.remove("Talking gloves")
            stats[3] += 1
            Playsound("Success")
            sPrint(f"[bold green]The gloves cast a shield! You avoided damage and your Wand rose to {stats[3]}![/bold green]")
            return

    while True:
        choice = input(
            "How do you react?\n"
            "  <1> Dodge and sprint away (Stat Check: Feet + Luck >= 5)\n"
            "  <2> Cast a containment barrier (Reflex Minigame scaled by Wand)\n> "
        ).strip()
        if choice in ("1", "2"):
            break
        sPrint("[red]Choose 1 or 2![/red]")

    if choice == "1":
        score = stats[1] + Luckboost(stats)
        sPrint(f"Check (Feet + Luck): [bold]{score}[/bold] vs 5")
        if score >= 5:
            gain = random.randint(1, 2)
            stats[1] += gain
            Playsound("Success")
            sPrint(f"[green]Close call! You dodged it and gained +{gain} Feet (now {stats[1]})![/green]")
        else:
            loss = random.randint(1, 2)
            stats[1] = max(0, stats[1] - loss)
            Playsound("fail")
            sPrint(f"[red]Boom! You tripped and lost -{loss} Feet (now {stats[1]}).[/red]")
    else:
        sPrint(f"[cyan]Wand bonus grants extra barrier time (+{stats[3] * 0.35:.2f}s)![/cyan]")
        if spell_minigame(length=5, base_time=2.5, stat_bonus=stats[3]):
            stats[3] += 2
            Playsound("Success")
            sPrint(f"[bold green]Barrier held! You absorbed the magic: +2 Wand (now {stats[3]})![/bold green]")
        else:
            loss = random.randint(1, 2)
            stats[3] = max(0, stats[3] - loss)
            Playsound("fail")
            sPrint(f"[bold red]Your barrier shattered! You lost -{loss} Wand (now {stats[3]}).[/bold red]")


def Shenaningan(stats, inventory):
    """Event: Counter classmates' pranks using Arms, Brains, or Talking gloves."""
    sPrint("[magenta]You fell in a Shenanigan square! Classmates set a magical trap for you![/magenta]")

    if "Talking gloves" in inventory:
        ans = input("Use [Talking gloves] to outsmart the pranksters? (y/n): ").strip().lower()
        if ans == "y":
            inventory.remove("Talking gloves")
            stats[3] += 1
            sPrint(f"[bold green]The gloves warned you in time! Your Wand rose to {stats[3]}![/bold green]")
            return

    while True:
        choice = input(
            "How do you counter the prank? (Difficulty: 5)\n"
            "  <1> Spot the illusion before stepping in (Uses Brains)\n"
            "  <2> Break free by brute force (Uses Arms)\n> "
        ).strip()
        if choice in ("1", "2"):
            break
        sPrint("[red]Choose 1 or 2![/red]")

    stat_idx = 0 if choice == "1" else 2
    score = stats[stat_idx] + Luckboost(stats)
    sPrint(f"Check ({statnames[stat_idx]} + Luck): [bold]{score}[/bold] vs 5")

    if score >= 5:
        stats[stat_idx] += 1
        Playsound("Success")
        sPrint(f"[green]You turned the tables on them! +1 {statnames[stat_idx]} (now {stats[stat_idx]}).[/green]")
    else:
        loss = random.randint(1, 2)
        x = random.randint(0, 4)
        stats[x] = max(0, stats[x] - loss)
        Playsound("fail")
        sPrint(f"[red]Pranked! You lost -{loss} {statnames[x]} (now {stats[x]}).[/red]")


def artifact(stats, inventory):
    """Event: Find an artifact and store it in the player's inventory."""
    Playsound("Coin")
    sPrint("[green]You stumbled upon an ancient hidden chest! Press any key to open it...[/green]")
    read.readkey()
    found_item = random.choice(list(ARTIFACTS_INFO.keys()))
    sPrint(f"You found: [bold gold1]{found_item}[/bold gold1] — {ARTIFACTS_INFO[found_item]}")

    if len(inventory) < MAX_INVENTORY:
        inventory.append(found_item)
        sPrint(f"[green]{found_item} was added to your backpack![/green]")
    else:
        sPrint(f"[yellow]Your backpack is full ({MAX_INVENTORY}/{MAX_INVENTORY})![/yellow]")
        ans = input(f"Do you want to swap an item for {found_item}? (y/n): ").strip().lower()
        if ans == "y":
            for idx, item in enumerate(inventory, start=1):
                print(f"  <{idx}> Drop {item}")
            try:
                drop_idx = int(input("Choose item number to replace: ")) - 1
                if 0 <= drop_idx < len(inventory):
                    dropped = inventory.pop(drop_idx)
                    inventory.append(found_item)
                    sPrint(f"Dropped {dropped} and equipped [green]{found_item}[/green].")
            except ValueError:
                sPrint("Invalid input. You left the chest behind.")


def Magicpolly(stats):
    """Event: Increases ALL player stats by +1."""
    Playsound("MagicPolly")
    for i in range(len(stats)):
        stats[i] += 1
    sPrint("[bold gold1]Wow! You arrived at MagicPolly fountain! All of your stats increased by +1![/bold gold1]")


# --- CHECKPOINTS & MECÁNICAS ---

def Exam(difficulty, stats, inventory):
    """Exam checkpoint with items, all-nighter prep, and a practical spellcasting test."""
    n = random.randint(1, 4)
    sPrint(f"\n[bold yellow]>>> EXAM CHECKPOINT (Difficulty: {difficulty}) <<<[/bold yellow]")
    sPrint(f"Subjects tested today: [bold cyan]Brains[/bold cyan] and [bold cyan]{statnames[n]}[/bold cyan]")

    exam_bonus = 0

    if "Ancient book" in inventory:
        ans = input("Consume [Ancient book] for +3 to both exam checks? (y/n): ").strip().lower()
        if ans == "y":
            inventory.remove("Ancient book")
            exam_bonus += 3
            sPrint("[green]You studied the Ancient book! (+3 Exam Bonus)[/green]")

    if stats[1] > 0:
        cram = input("Pull an all-nighter? (-1 permanent Feet for +2 Exam Bonus) (y/n): ").strip().lower()
        if cram == "y":
            stats[1] -= 1
            exam_bonus += 2
            sPrint(f"[yellow]You drank 4 espressos! Feet dropped to {stats[1]}, +2 Exam Bonus.[/yellow]")

    # Prueba práctica con el minijuego de reflejos
    sPrint("\n[bold magenta]Part 1: Practical Wand Demonstration![/bold magenta]")
    if spell_minigame(length=5, base_time=2.6, stat_bonus=stats[3]):
        exam_bonus += 2
        sPrint("[bold green]Examiners loved your technique! (+2 Practical Bonus)[/bold green]")
    else:
        sPrint("[yellow]Sloppy wandwork — no practical bonus awarded.[/yellow]")

    brains_score = stats[0] + Luckboost(stats) + exam_bonus
    second_score = stats[n] + Luckboost(stats) + exam_bonus
    sPrint(f"\nFinal Results -> Brains: [bold]{brains_score}[/bold]/{difficulty} | {statnames[n]}: [bold]{second_score}[/bold]/{difficulty}")

    if brains_score >= difficulty and second_score >= difficulty:
        sPrint("[bold green]You passed your exam![/bold green]")
        Playsound("Success")
        return 1
    else:
        sPrint("[bold red]You failed your exam...[/bold red]")
        Playsound("fail")
        return 0


def Position(current, stats, inventory):
    target = current + diceRoll(stats, inventory)
    for milestone, _ in EXAM_MILESTONES:
        if current < milestone <= target:
            return milestone
    return min(target, 70)


def box(current, stats, inventory):
    current = Position(current, stats, inventory)
    display_board(current)

    exam_dict = dict(EXAM_MILESTONES)
    if current in exam_dict:
        if Exam(exam_dict[current], stats, inventory) == 0:
            current = max(0, current - 5)
            stats[0] += 1
            sPrint(f"You were sent back to tile {current}, but learned from your mistakes (+1 Brains -> {stats[0]}).")
        return current

    tile_type = get_tile_type(current)
    if tile_type == "C":
        lecture(stats)
    elif tile_type == "A":
        accident(stats, inventory)
    elif tile_type == "S":
        Shenaningan(stats, inventory)
    elif tile_type == "R":
        artifact(stats, inventory)
    elif tile_type == "M":
        Magicpolly(stats)

    return current


def Turn(Pos, name, stats, inventory):
    sPrint(f"\n>>>>> Start of your turn: {name}")
    return box(Pos, stats, inventory)


# --- GUARDADO, CARGA Y MENÚS ---

def save_game(filename, currentP, stats, name, inventory):
    if not filename:
        sPrint("[red]Invalid file name! Game was not saved.[/red]")
        return False
    try:
        with open(filename, 'w') as f:
            f.write(f"{currentP}\n")
            f.write(','.join(map(str, stats)) + '\n')
            f.write(f"{name}\n")
            f.write(','.join(inventory) + '\n')
        return True
    except OSError:
        sPrint("[red]Could not save file. Check the file name or permissions.[/red]")
        return False


def load_game(filename):
    if not filename or not os.path.exists(filename):
        sPrint("[red]Save file does not exist! Starting a new game instead.[/red]")
        name = input("Insert user's name: ").strip() or "Mago"
        return 0, setup(), name, []

    try:
        with open(filename, 'r') as f:
            currentP = int(f.readline().strip())
            stats = list(map(int, f.readline().strip().split(',')))
            name = f.readline().strip() or "Mago"
            inv_line = f.readline().strip()
            inventory = [item for item in inv_line.split(',') if item in ARTIFACTS_INFO] if inv_line else []

        if len(stats) != 5 or not (0 <= currentP <= 70):
            raise ValueError("Invalid save structure")
        return currentP, stats, name, inventory
    except (ValueError, IndexError, OSError):
        sPrint("[red]Corrupted save file! Starting a new game instead.[/red]")
        name = input("Insert user's name: ").strip() or "Mago"
        return 0, setup(), name, []


def menu(currentP, stats, name, inventory):
    a = input(
        "\nPress <1> to continue playing"
        "\nPress <2> to load a previous save"
        "\nPress <3> to save the current game"
        "\nPress <4> for rules"
        "\nPress <5> to exit the game\n> "
    ).strip()

    match a:
        case "1":
            return currentP, stats, name, inventory
        case "2":
            file = input("Enter the save file name: ").strip()
            currentP, stats, name, inventory = load_game(file)
            display_board(currentP)
            display_Stats(stats, statnames, inventory)
            return currentP, stats, name, inventory
        case "3":
            file = input("Enter the file name to save the game: ").strip()
            if save_game(file, currentP, stats, name, inventory):
                sPrint(f"[green]Game saved to {file}[/green]")
            return currentP, stats, name, inventory
        case "4":
            rules_text = (
                "• Roll the dice to advance across 70 tiles.\n"
                "• Choose safe or risky actions in Lectures, Accidents, and Shenanigans.\n"
                "• Cast spells fast in reflex minigames to earn bonus points.\n"
                "• Collect Artifacts on [R] tiles to use passively or during tough checks.\n"
                "• Pass all 5 Exams (tiles 14, 28, 42, 56, 70) to graduate!"
            )
            console.print(Panel(rules_text, title="MagicPolly Rules", border_style="yellow", expand=False))
            return currentP, stats, name, inventory
        case "5":
            sPrint("[bold red]Exiting the game...[/bold red]")
            sPrint("Goodbye!")
            sys.exit()
        case _:
            sPrint("[red]Invalid option! Please choose a valid option.[/red]")
            return currentP, stats, name, inventory


def main():
    while True:
        a = input(
            "\nPress <1> for new game"
            "\nPress <2> for loading a save file"
            "\nPress <3> for instructions"
            "\nPress <4> to close the game\n> "
        ).strip()

        match a:
            case "1":
                sPrint("[green]Starting a new game...[/green]")
                currentP = 0
                name = input("Insert user's name: ").strip() or "Mago"
                stats = setup()
                inventory = []
                break
            case "2":
                file = input("Enter the save file name: ").strip()
                currentP, stats, name, inventory = load_game(file)
                break
            case "3":
                sPrint("[yellow]Roll the dice, choose how to handle events, cast spells in reflex challenges, and pass the exams at tiles 14, 28, 42, 56, and 70![/yellow]")
            case "4":
                sPrint("[bold red]Exiting the game...[/bold red]")
                sPrint("Goodbye!")
                sys.exit()
            case _:
                sPrint("[red]Invalid option! Please choose a valid option.[/red]")

    title_banner = fi.figlet_format("MAGIC POLLY", font="slant")
    console.print(f"[bold cyan]{title_banner}[/bold cyan]")

    display_board(currentP)
    display_Stats(stats, statnames, inventory)

    while currentP < 70:
        choice = input(
            "\nPress <1> to roll dice & start turn"
            "\nPress <2> to use an item from backpack"
            "\nPress <3> to access the menu\n> "
        ).strip()

        match choice:
            case "1":
                currentP = Turn(currentP, name, stats, inventory)
                display_Stats(stats, statnames, inventory)
            case "2":
                use_item_action(stats, inventory)
                display_Stats(stats, statnames, inventory)
            case "3":
                currentP, stats, name, inventory = menu(currentP, stats, name, inventory)
            case _:
                sPrint("[red]Invalid option! Please choose a valid option.[/red]")

    end()


if __name__ == "__main__":
    main()