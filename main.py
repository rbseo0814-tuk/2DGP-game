from pico2d import open_canvas, close_canvas
import game_framework
from config import SCREEN_W, SCREEN_H

import modes.play_mode as start_mode

open_canvas(SCREEN_W, SCREEN_H)
game_framework.run(start_mode)
close_canvas()