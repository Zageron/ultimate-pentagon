# Ultimate Octagon

## Game Design

### MVP 1

- Window
  - Aspect ratio of 4:3 or 1:1, not widescreen.
- (Feature) Music
  - Seamless Loop
  - Plays Endlessly
  - Single song, single level.
- (State) Main Menu
  - Start Game Button
  - Level Music
  - Highest score text (in seconds)
- (Feature) Game Start
  - Level begins at the point where the level music was playing on the main menu.
- (State) Game
  - Player moves the character with LEFT and RIGHT arrows.
  - Character moves in a circle around a center piece.
  - Obstacles are circle or pentagon segments.
  - Character dies instantly the moment it hits an obstacle.
  - Game ends on character death, no respawning.

### MVP 2

- (State) Main Menu
  - Hi-Score Button
- (State) Hi-Score List
  - Shows your personal best scores. (in seconds)
- (State) Game
  - Obstacles are generated from the music

## Developing

- Open a Command line, and navigate to repository.
- From the root directory, type:

    > ```zsh
    > poetry shell
    > code .
    > ```

- Visual Studio Code should open.
- Close the command line.
- In VSC, open the embedded CLI with `Ctrl +` `
- Type

    > ```zsh
    > poetry install
    > ```.

- <kbd>F5</kbd> in `src/pentagon/__main__.py` to debug.

## Package for Distribution

Run the following command!

> ```zsh
> nuitka -o package/UltimatePentagon.exe --output-dir=package --remove-output src/pentagon/__main__.py
> ```
