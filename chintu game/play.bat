@echo off
echo launching chintu's game ....
python -m pip install --upgrade pip
pip install -r requirements.txt
python animation.py
python game.py
python game_items.py
