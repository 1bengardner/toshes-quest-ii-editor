![Toshe's Quest II Editor](https://user-images.githubusercontent.com/6226898/119236959-4b285900-bb08-11eb-8445-8ece9be94cd6.png)

Character data editor for [Toshe's Quest II](https://github.com/1bengardner/toshes-quest-ii).

## ⚠ Warning

Using the editor may render your saved file incompatible with the game. If you manage to mess up your saved game, you'll have to un-mess it yourself. Keep a backup!

> I mainly used this as a tool to help test the game during development. It's not meant as a game enhancement tool, but you're free to use it that way!

## Requirements

The editor depends on many [game source](https://github.com/1bengardner/toshes-quest-ii/tree/master/source) files including its images and data.

- Modules must be in the same directory as `editor.py`
- The `images` directory must be in the same directory as `editor.py` (i.e. `.\images\` must contain the contents of `<game-source>\resources\assets\images\`)
- The `data` directory must be in the same directory as `editor.py` (same as above)

On Windows, you can use the included [mklinks.bat](mklinks.bat) to speed up linking the required files from your game source directory.

## Features

### Modify stats and items
![Main editor window](https://github.com/1bengardner/toshes-quest-ii-editor/assets/6226898/d498e469-3b3a-4568-8526-5c8279f28dc7)

### Change item graphics
![Armour Graphic Select window](https://github.com/1bengardner/toshes-quest-ii-editor/assets/6226898/a639afae-0c22-4e1a-8d11-8e1fa2b0595b)

### Browse, search, add and delete game progression data
![Flag editor window](https://github.com/1bengardner/toshes-quest-ii-editor/assets/6226898/10f05fe1-ec08-4581-b907-b0a8a19f5494)

## Known issues

- Currently the Editor only displays the first 9 items for characters with the Chasmic Rucksack
