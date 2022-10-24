title Building Just a normal endless runner game
pip install pygame
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed --icon "graphics/icon.ico" --splash "splash.png" --add-data "audio;audio/" --add-data "font;font/" --add-data "graphics;graphics/" --hidden-import "pyi_splash"  "game.py"