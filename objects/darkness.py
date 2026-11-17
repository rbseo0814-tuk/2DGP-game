from pico2d import load_image
import game_framework
from config import SCREEN_W, SCREEN_H

DOZE_DARK_RATE = 0.10       # 초당 어둠 비율 변화량 (1.0 = 화면 전체)
AWAKE_DARK_RATE = -0.30


class Darkness:
    def __init__(self, guard):
        self.guard = guard
        self.ratio = 0.0        # 0.0 ~ 1.0, 오른쪽부터 덮인 비율
        self.image = load_image('resource/image/dark.png')

    def update(self):
        state = self.guard.state_machine.cur_state
        if state == self.guard.SLEEP:
            self.ratio = 1.0
        elif state == self.guard.DOZE:
            self.ratio = min(1.0, self.ratio + DOZE_DARK_RATE * game_framework.frame_time)
        else:                   # AWAKE, WAKE
            self.ratio = max(0.0, self.ratio + AWAKE_DARK_RATE * game_framework.frame_time)

    def draw(self):
        w = SCREEN_W * self.ratio
        if w <= 0:
            return
        self.image.opacify(1.0)
        self.image.draw(SCREEN_W - w / 2, SCREEN_H / 2, w, SCREEN_H)   # 오른쪽 끝 기준
