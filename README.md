# OCR A-Level Dungeon Crawler (Python + Pygame)

This project is a small, teaching-focused game that helps OCR Computer Science A-Level students practise:

- object-oriented programming (OOP)
- decomposition and abstraction
- game loops and event-driven programming
- testing and extending a pre-existing codebase

Use it as a **starter project** to build your own game idea.

---

## What this game currently does

- Moves a player with **WASD / arrow keys**
- Spawns simple enemies that chase the player
- Lets the player cast a spell with **Space** (uses mana)
- Tracks player health and mana on screen

---

## Quick start

1. Make sure you have **Python 3.11+** installed.
2. Install dependencies:

```bash
pip install pygame==2.6.1
```

3. Run the game:

```bash
python /home/runner/work/ocr-dungeon/ocr-dungeon/main.py
```

---

## File guide (where to look first)

- `/home/runner/work/ocr-dungeon/ocr-dungeon/main.py`  
  Entry point. Creates `Game` and runs it.

- `/home/runner/work/ocr-dungeon/ocr-dungeon/game.py`  
  Main game manager and game loop (`_handle_events`, `_update`, `_draw`).

- `/home/runner/work/ocr-dungeon/ocr-dungeon/entity.py`  
  Abstract base class showing shared behaviour for all game objects.

- `/home/runner/work/ocr-dungeon/ocr-dungeon/player.py`  
  Player logic, keyboard input, mana, spell casting.

- `/home/runner/work/ocr-dungeon/ocr-dungeon/enemy.py`  
  Enemy chase behaviour.

- `/home/runner/work/ocr-dungeon/ocr-dungeon/settings.py`  
  All key constants in one place (screen size, speeds, health, spell values).

- `/home/runner/work/ocr-dungeon/ocr-dungeon/sprite_sheet_demo.py`  
  Optional animation demo using a sprite sheet.

---

## OCR A-Level links to theory

This code is useful for exam/coursework discussion:

- **Abstraction:** `Game.run()` hides complexity from `main.py`.
- **Encapsulation:** health in `Entity` is managed by methods, not direct external edits.
- **Inheritance:** `Player` and `Enemy` both inherit from `Entity`.
- **Polymorphism:** each class implements/uses `update(...)` differently.
- **Decomposition:** game tasks are split into clear methods and modules.

Try explaining each of these with references to the code in your own words.

---

## Suggested student extension path

Build your own version in small, testable steps:

1. **Change settings only**  
   Edit values in `settings.py` (speed, health, mana, spell range) and observe impact.

2. **Add one new mechanic**  
   Examples: score, enemy damage cooldown, health pickups, win condition.

3. **Improve enemy logic**  
   Add multiple enemy types (fast/weak, slow/strong, ranged).

4. **Improve feedback**  
   Add better UI text, damage flashes, or sound effects.

5. **Add art assets**  
   Use `sprite_sheet_demo.py` ideas to replace colour blocks with sprites.

6. **Evaluate and refine**  
   Playtest, identify bugs, then refactor duplicated code.

---

## Example mini-project ideas

- “Zombie survival” (time-based score + increasing enemy waves)
- “Wizard arena” (mana management + different spells)
- “Stealth dungeon” (line-of-sight enemies)
- “Treasure escape” (collect items before exiting)

Each idea can reuse the same core structure and classes.

---

## Tips for coursework write-up

- Keep a development log of each feature you add.
- Justify design choices (why classes/methods are split this way).
- Show iterative testing (what you tested, expected result, actual result).
- Include short evaluations after each milestone.

---

## Common next improvements for this codebase

- Add collision with walls/tiles
- Add game states (menu, playing, game over, restart)
- Add proper asset loading from `/assets`
- Add unit tests for pure logic methods

---

## Controls

- Move: **WASD** or **Arrow keys**
- Cast spell: **Space**
- Quit: close the game window
