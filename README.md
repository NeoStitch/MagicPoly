# Digital Board Game

Digital board game based on text and images created with characters.

---

## Project Overview

Tentative idea: a board game similar to the game "Life," based on the concept of going through a magic school trying to survive classes and the shenanigans that your classmates do.

### Inspiration & Core Concept

The Game of Life is a classic roll-and-move board game where players simulate a full life journey from early adulthood to retirement by driving miniature car tokens across a track. Starting with a fundamental choice between entering the workforce directly or taking on debt for a college degree to unlock higher salaries, players spin a central 1–10 spinner to navigate their path. As they land on various spaces, players experience major life milestones—such as getting married, adding family pegs to their car, purchasing real estate, and handling unexpected financial setbacks or paydays. The game's economy requires balancing risk, insurance, and loans while reacting to random life events. Ultimately, once all players reach retirement, everyone liquidates their assets and settles remaining debts, and the player who finishes with the highest overall net worth wins.

---

##  Game Algorithm & Flow

### 1. Character Initialization

* Initially, you'll insert data for your character that'll be saved and modified throughout the game whenever a random event alters the statistics of your character and resources.
* Players create a custom character profile within a limit of points (stats, name, etc.); these will be saved and checked throughout the whole game.

### 2. Turn Movement

* A random amount of spaces the character will move, depending on a randomly generated number between 1 and 6.

### 3. Space Types & Event Pools

Spaces can be one of 6 types: Class, Accident, Shenanigans, Exam, Artifact, and MagicPoly.

| Space Type | Effect Description |
| --- | --- |
| **Class** | Class will increase a certain attribute. |
| **Accident** | Accident will test luck and stats. |
| **Shenanigans** | Shenanigans a negative effect. |
| **Exam** | Exams will serve as turning points in the story, like finishing a semester. |
| **Artifact** | Artifact a card that will be helpful. |
| **MagicPoly** | MagicPoly a positive effect with a huge downside. |

* Different categories of events will be organized into distinct event decks/pools. Events are randomized encounters; if the event is fulfilled, Resolves in success or failure.

### 4. Skill Check Engine

* When making a skill check, it'll be a comparison between the necessary skill and a limit decided by a randomly generated number between 1 and 6.

---

##  Win & Loss Conditions

* The game ends when the character graduates, or if they fail enough.
