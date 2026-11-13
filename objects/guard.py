from pico2d import load_image
import game_framework

FRAMES_PER_ACTION = 4       # 상태마다 프레임 4장
FRAMES_PER_SECOND = 4.0     # 1초에 넘길 프레임 수


class Guard:
    def __init__(self):
        self.image = load_image('resource/image/guard_sheet.png')
        self.x, self.y = 300, 200   # 발 위치 y=120 + 프레임 높이의 절반 80
        self.frame = 0

    def update(self):
        self.frame = (self.frame + FRAMES_PER_SECOND * game_framework.frame_time) % FRAMES_PER_ACTION

    def draw(self):
        self.image.clip_draw(int(self.frame) * 96, 0, 96, 160, self.x, self.y)
