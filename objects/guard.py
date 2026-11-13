from pico2d import load_image
import game_framework

FRAMES_PER_ACTION = 4       # 상태마다 프레임 4장
FRAMES_PER_SECOND = 4.0     # 1초에 넘길 프레임 수


class Guard:
    def __init__(self):
        self.image = load_image('resource/image/guard_sheet.png')
        self.x, self.y = 320, 168   # 발 위치 y=120 + 키의 절반 48
        self.frame = 0

    def update(self):
        self.frame = (self.frame + FRAMES_PER_SECOND * game_framework.frame_time) % FRAMES_PER_ACTION

    def draw(self):
        self.image.clip_draw(int(self.frame) * 64, 0, 64, 96, self.x, self.y)
