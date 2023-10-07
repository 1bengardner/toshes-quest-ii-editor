![Toshe's Quest II Editor](https://user-images.githubusercontent.com/6226898/119236959-4b285900-bb08-11eb-8445-8ece9be94cd6.png)

Character data editor for [Toshe's Quest II](https://github.com/1bengardner/toshes-quest-ii).

## ⚠ Warning

Using the editor may render your saved file incompatible with the game. If you manage to mess up your saved game, you'll have to un-mess it yourself. Keep a backup!

## Requirements

The editor depends on many [game source](https://github.com/1bengardner/toshes-quest-ii/tree/master/source) files including its images and data.

- Modules must be in the same directory as `editor.py`
- The `images` directory must be in the same directory as `editor.py` (i.e. `.\images\` must contain the contents of `<game-source>\resources\assets\images\`)
- The `data` directory must be in the same directory as `editor.py` (same as above)

On Windows, you can use the included [mklinks.bat](mklinks.bat) to speed up linking the required files from your game source directory.

## Features

### Modify stats and items
![Main editor window](https://user-images.githubusercontent.com/6226898/119273813-a3c82680-bbda-11eb-9552-acb5c72ecddc.png)

### Change item graphics
![Armour Graphic Select window](https://user-images.githubusercontent.com/6226898/119273858-df62f080-bbda-11eb-889f-945ba84a1312.png)

### Browse, search, add and delete game progression data
![Flag editor window](https://user-images.githubusercontent.com/6226898/119273897-06212700-bbdb-11eb-91d8-fb22ede64d6d.png)

## Known issues

- Currently the Editor only displays the first 9 items for characters with the Chasmic Rucksack