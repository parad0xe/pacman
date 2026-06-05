_This project has been created as part of the 42 curriculum by nlallema, nahecre._

# Pacman

## Description

Pacman is a Python-based implementation of the classic Pac-Man arcade game. This project features dynamic maze generation, a ghost pathfinding system, and an integrated highscore board. Built using the `pyray` (raylib) library for rendering and a custom UI system, it brings the arcade experience to the desktop while keeping a strictly modular and object-oriented architecture.

## Table of contents

- [Instructions](#instructions)
  - [Installation](#installation)
  - [Execution](#execution)
  - [Build](#build)
- [Configuration](#configuration)
- [Highscore](#highscore)
- [Maze Generation](#maze-generation)
- [Implementation](#implementation)
- [General Software Architecture](#general-software-architecture)
- [Project Management](#project-management)
- [Resources](#resources)

## Instructions

### Installation

The project uses `uv` for dependency management. To install the required packages (including `pyray`, `pydantic`, and the provided `mazegenerator`), run:

```bash
make
```

Or you can use `uv` directly to sync dependencies:

```bash
uv sync
```

### Execution

To run the game, use the following command at the root of the repository:

```bash
make run [ARGS="config_file"]
```

Alternatively, you can run it directly using uv:

```bash
uv run python pac-man.py <config_file>
```

### Build

To create a standalone executable of the game using `pyinstaller`, run:

```bash
make build
```

This will create an executable and bundle it alongside its required assets, configuration file, and documentation into a `pac-man.zip` archive located in the `dist/` directory.

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

## Maze generation

The maze generation utilizes the provided `A-Maze-ing` package (imported as `mazegenerator`). 

At the start of a new stage, the `Game` controller instantiates `MazeGenerator` with the configured `width` and `height`. 
For the first level, it uses the `seed` from the configuration (unless set to `-1`, which generates a random seed). For subsequent levels, a new random seed is generated. 
Calling the `mazegenerator.generate(seed)` method executes the generation algorithm, and the resulting 2D array (`maze`) is passed directly to the `Stage` class. The stage then interprets the grid, placing the player at the center, ghosts in the four corners, and super pacgums in the four corners.

## Implementation

The project is built entirely in Python, utilizing `pyray` (Raylib) for fast, hardware-accelerated 2D rendering at a smooth 120 FPS. 
A major technical highlight is the use of a fixed timestep update loop within the `Game.update` method. The loop breaks down delta time (dt) into smaller sub-steps to ensure entities (like the player) never skip over cell boundaries during movement, thus eliminating collision tunneling.
State management is decoupled from the rendering loop. Logical entities (`Player`, `Ghost`, `Stage`, `Game`) only manage internal states, making the game loop predictable and easy to manage. Additionally, a custom mini UI framework was developed, implementing UI views and flex-box layouts (`VBox`, `HBox`) directly over Raylib's primitive drawing functions.

## General software architecture

The architecture relies on decoupling logic, state, and rendering, following a clear Model-View-Controller (MVC) pattern.

- **src/game/** (The Core Engine): 
  - `Game`: The top-level controller, orchestrating stages, cheat codes, and overall transitions (game over, victory).
  - `Stage`: Represents a single level instance, owning the maze board, pacgums, player, and ghosts.
  - `Player` / `Ghost`: Entity models maintaining movement logic, states (NORMAL, SUPER), and sub-step physics.
  - `PathFinder`: Handles shortest-path evaluations for ghost AI targeting.
- **src/ui/** (The Custom mini UI Framework):
  - `ViewManager`: Handles scene routing and transitions (Menu -> Game -> Highscores).
  - **views/** (`MenuView`, `PacmanView`, `HighscoreView`): Specific screen layouts.
  - **core/ & elements/** (`HBox`, `VBox`, `Button`, `Text`): Building blocks of the UI.
- **src/models/** (Data & Configuration):
  - `Config`: Validates and parses `config.json`.
  - `Score` / `Highscores`: Validates `scores.json`.
- **src/application.py**: The main application lifecycle manager, initializing the Raylib window, the global context, and the 120 FPS game loop.
- **src/context.py & src/event.py**: Implements a global event dispatcher (`AppEvent`, `GameEvent`) to facilitate loosely coupled communication across the app (e.g., a button click triggering a view switch).

## Project management

Project planning and task decomposition were organized using Trello. The workload was divided so that one person focused on implementing the custom UI system, while the other was dedicated to creating the core game engine.

## Resources

- **Raylib python (pyray)**: [https://electronstudio.github.io/raylib-python-cffi/pyray.html](https://electronstudio.github.io/raylib-python-cffi/pyray.html)
- **Pydantic documentation**: [https://docs.pydantic.dev/](https://docs.pydantic.dev/)
- **PyInstaller documentation**: [https://pyinstaller.org/en/v6.13.0/usage.html](https://pyinstaller.org/en/v6.13.0/usage.html)

### AI Usage

AI was utilized during this project for:
- helping to resolve rendering issues.
- generating the documentation.
- drafting and structuring this README.
