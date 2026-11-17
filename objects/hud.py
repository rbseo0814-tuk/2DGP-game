from pico2d import load_font, draw_rectangle
from objects.guard import FOCUS_MAX

BAR_X, BAR_Y = 20, 650      # 집중력 바 왼쪽 아래
BAR_W, BAR_H = 300, 20


class Hud:
    def __init__(self, guard):
        self.guard = guard
        self.font = load_font('resource/font/Galmuri11.ttf', 24)

    def update(self):
        pass

    def draw(self):
        self.font.draw(BAR_X, BAR_Y + BAR_H + 20, '집중력', (255, 255, 255))

        fill_w = BAR_W * self.guard.focus / FOCUS_MAX
        if fill_w > 0:
            draw_rectangle(BAR_X, BAR_Y, BAR_X + fill_w, BAR_Y + BAR_H, 255, 210, 0, 255, True)
        draw_rectangle(BAR_X, BAR_Y, BAR_X + BAR_W, BAR_Y + BAR_H, 255, 255, 255)
