# MagicPolly — Digital Board Game

A terminal-based RPG board game inspired by *The Game of Life*, set in a chaotic magic academy. Roll the dice across a 70-tile board, survive classroom accidents and classmates' pranks, manage your coins and magical artifacts, and pass five milestone exams to graduate.

---

## Prerequisites & Updating Python

This game uses structural pattern matching (`match / case`), which requires **Python 3.10 or higher** (running the latest stable release is recommended).

### 1. Check Your Current Python Version
Open your terminal or command prompt and run:
```bash
python --version
# or on macOS/Linux:
python3 --version


### 2. Update Python to the Latest Version

* **Windows:**
* **Option A (Terminal via Winget):**
```powershell
winget install Python.Python.3.13

```


* **Option B (Installer):** Download the latest installer from [python.org/downloads](https://www.python.org/downloads/). **Important:** Check the box **"Add python.exe to PATH"** before clicking *Install Now*.


* **macOS:**
* Using [Homebrew](https://brew.sh/):
```bash
brew update && brew install python

```


* Or download the official macOS installer from [python.org/downloads](https://www.python.org/downloads/).


* **Linux (Ubuntu / Debian):**
```bash
sudo apt update && sudo apt install python3 python3-pip python3-venv -y

```



---

## Installation & Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd <your-repository-folder>

```

### 2. (Optional) Create a Virtual Environment

```bash
python -m venv venv

# Activate on Windows:
venv\Scripts\activate

# Activate on macOS/Linux:
source venv/bin/activate

```

### 3. Install Required Libraries

Install all third-party dependencies (`pyfiglet`, `readchar`, `pygame`, and `rich`) using `pip`:

```bash
pip install pyfiglet readchar pygame rich

```

### 4. Audio Folder Structure (Optional)

The game runs even if audio files or speakers are unavailable; the github repository includes the audio files itself, make sure to keep it in the same folder. If you want or need you may use your own audios, place your audio files inside a `Sounds/` directory next to the main script:

```text
MagicPolly/
├── main.py
├── README.md
└── Sounds/
    ├── diceE.mp3
    ├── Victory!.wav
    ├── Magic Music - A Wizards Dream (Beautiful Violin).mp3
    ├── fail.wav
    ├── magical_4.ogg
    ├── magical_1.ogg
    └── coin.wav

```

### 5. Run the Game

```bash
python Magicpolly.py
for mac: python3 Magicpolly.py


```

---

## Game Overview

Inspired by classic roll-and-move board games like *The Game of Life*, **MagicPolly** simulates a wizard student's journey from freshman orientation (Tile 0) to graduation (Tile 70). Instead of pure luck, players must weigh risk versus reward in every classroom event, manage limited backpack space, spend earned coins wisely at the Magic Store, and react quickly during timed spellcasting challenges.

---

## Game Algorithm 

### 1. Character Stats & Initialization

When starting a new game, you choose your wizard's name, start with **5 Coins**, an empty **5-slot Backpack**, and randomly rolled initial attributes:

| Stat | Role in Gameplay |
| --- | --- |
| **Brains** | Primary stat tested in all Exams; used to spot illusions in Shenanigans and grants extra casting time in Lectures. |
| **Feet** | Used to dodge exploding cauldrons in Accidents; can be sacrificed (`-1`) to pull an all-nighter before Exams. |
| **Arms** | Used to break free from classmates' traps by brute force in Shenanigan events. |
| **Wand** | Determines your barrier casting time in Accidents and your practical demonstration performance in Exams. |
| **Beard** | Acts as your **Luck** stat, adding a random `Luckboost` bonus to dice movement, skill checks, and exam scores. |

### 2. Turn Structure & Movement

On each turn, the player can:

1. **Roll Dice & Advance:** Rolls a 6-sided die (`1–6`) plus your `Beard` luck bonus (and `+1` if carrying *Smart Shoes*). Movement automatically stops at any **Exam Milestone** tile you pass over.
2. **Use an Active Item:** Consume items like the *Magical protein bar* before rolling.
3. **Visit the Magic Store:** Spend coins on Mystery Boxes or specific artifacts.
4. **Access Menu:** Save progress, load a previous `.txt` save file, view rules, or exit.

### 3. Board Layout & Space Types

The board is rendered in the terminal as a **7x10 matrix (70 tiles)** using `rich` panels and color-coded markers:

| Tile | Type | Effect & Player Choices |
| --- | --- | --- |
| `[ C ]` | **Class (Lecture)** | Choose **Safe Notes** (`+1` random stat, `+1` coin) or **Risky Spell** (reflex minigame for `+3` Brains/Wand & `+4` coins, or `-2` stat on failure). |
| `[ A ]` | **Accident** | A cauldron is about to explode. Choose to **Dodge** (`Feet + Luck >= 5`), **Cast a Barrier** (reflex minigame scaled by `Wand`), or use *Talking gloves*. |
| `[ S ]` | **Shenanigans** | Classmates set a trap. Choose to **Spot the Illusion** (`Brains`) or **Break Free** (`Arms`) against difficulty `5`, or use *Talking gloves*. |
| `[ R ]` | **Artifact** | Open a hidden chest to obtain a random magical artifact (or swap one if your 5-slot backpack is full). |
| `[ M ]` | **MagicPolly** | Restorative fountain that grants **+1 to all five stats** and **+5 coins**. |
| `[ E ]` | **Exam** | Mandatory academic checkpoints at tiles **14, 28, 42, 56, and 70** (Difficulties: `3, 4, 6, 7, 10`). |

### 4. Artifacts & Magic Store

Players earn coins by succeeding in events (`+1` to `+4` coins), visiting fountains (`+5` coins), and passing exams (`+10` coins). At the **Magic Store**, you can buy a **Mystery Box (5 coins)** (75% chance of a random artifact, 25% empty) or pick an exact item for **15 coins**:

* **Ancient book `[Exam]`:** Consume before an exam for a `+3` bonus to all checks.
* **Misterious pill `[Dice]`:** Consume after rolling to re-roll the die.
* **Smart Shoes `[Passive]`:** Automatically adds `+1` space to every movement roll while in your backpack.
* **Magical protein bar `[Active]`:** Eat between turns for a permanent `+2` to either `Feet` or `Arms`.
* **Talking gloves `[Danger]`:** Consume during an Accident or Shenanigan to auto-win the encounter and gain `+1 Wand`.

### 5. Skill Checks & Reflex Minigames (QTE)

* **Stat Checks:** Compare `Stat + Luckboost` against a target difficulty (`5` for events, or `3` to `10` for Exams).
* **Reflex Spellcasting:** Certain risky actions and Exam practical tests trigger a real-time Quick Time Event where you must type a random sequence of keys (`W, A, S, D, E, Q`) before the timer runs out. Higher `Brains` or `Wand` stats extend your time limit.

---

## Win & Loss Conditions

* **Victory (Graduation):** Reach **Tile 70** and pass the Final Exam (Difficulty `10`) to graduate and trigger the victory screen.
* **Setbacks (Exam Failure):** Failing an exam sends you **5 tiles backward** on the board, though you learn from the experience (`+1 Brains` and `+1` to the secondary tested stat if below 6) so you can prepare and try again.

## To be included
* **Loss conditions** *
* **Selection of characters for the board** *
* **System of high perk high drawback ** *

```

```
