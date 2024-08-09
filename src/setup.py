# setup.py
from PyInstaller.__main__ import run

opts = [
    '--onefile',  # Bundle everything into a single executable
    'flappy_bird.py'
]

run(opts)
