# Ultimate Octagon

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
