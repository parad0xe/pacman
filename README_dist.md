_This project has been created as part of the 42 curriculum by nlallema, nahecre._

# Pacman

## Description

Pacman is a Python-based implementation of the classic Pac-Man arcade game. This project features dynamic maze generation, a ghost pathfinding system, and an integrated highscore board. Built using the `pyray` (raylib) library for rendering and a custom UI system, it brings the arcade experience to the desktop while keeping a strictly modular and object-oriented architecture.

## Table of contents

- [Instructions](#instructions)
  - [Execution](#execution)
- [Configuration](#configuration)
- [Highscore](#highscore)

## Instructions

This version is the standalone executable of the game. No installation or building is required.

### Execution

To run the game, extract the archive and execute the provided binary from your terminal:

**On Linux / macOS:**
```bash
./pac-man <config_file>
```

## Configuration

The game relies on a JSON configuration file (by default `config.json`), managed and strictly validated through Pydantic models to ensure stability. 

**Structure and Default Values:**
- `score_file` (string): Path to the JSON file storing highscores (default: `"scores.json"`).
- `life` (integer): Initial number of lives (default: `3`, min: 1, max: 10).
- `width` (integer): Width of the generated maze (default: `15`, min: 10, max: 20).
- `height` (integer): Height of the generated maze (default: `15`, min: 10, max: 20).
- `seed` (integer): Random seed for the first maze generation. Set to `-1` for a random seed (default: `-1`, min: -1).
- `time` (integer): Time limit in seconds for a level (default: `90`, min: 1, max: 3600).
- `pacgum_points` (integer): Points awarded per regular pacgum (default: `10`, min: 0, max: 2000).
- `super_pacgum_points` (integer): Points awarded per super pacgum (default: `50`, min: 0, max: 4000).
- `ghost_points` (integer): Points awarded for eating a ghost in SUPER state (default: `250`, min: 0, max: 8000).

If a key is missing or invalid, the game automatically falls back to these default values, ignores unknown keys, and logs a warning to the console.

## Highscore

The highscore system persists player scores in a JSON file specified in the configuration. 

**How it works:**
- Data serialization and deserialization is handled by Pydantic models (`Score` and `Highscores`), ensuring validation logic is separated from UI logic.
- At the end of a game, the `save_highscores` function sorts the scores in descending order and truncates the list to the top 10 entries before writing to the JSON file.
- The UI retrieves these scores via `load_highscores` and presents them in a stylized table using a custom flex-like layout system built on top of `pyray`. Ranks are color-coded to emphasize the top 3 players.

**Why this implementation:**
Using JSON paired with Pydantic ensures data integrity, easy serialization, and immunity to manual tampering (invalid entries are immediately rejected). Constraining the highscores to the top 10 entries saves file space and limits processing time, which fits the classic arcade paradigm perfectly.
