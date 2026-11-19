from pico2d import load_font, draw_rectangle
from config import SCREEN_W
from objects.guard import FOCUS_MAX, WAKE_TAP_COUNT

BAR_X, BAR_Y = 20, 650      # 집중력 바 왼쪽 아래
BAR_W, BAR_H = 300, 20


class Hud:
    def __init__(self, guard, darkness, clock):
        self.guard = guard
        self.darkness = darkness
        self.clock = clock
        self.font = load_font('resource/font/Galmuri11.ttf', 24)

    def update(self):
        pass

    def draw(self):
        self.font.draw(BAR_X, BAR_Y + BAR_H + 20, '집중력', (255, 255, 255))

        fill_w = BAR_W * self.guard.focus / FOCUS_MAX
        if fill_w > 0:
            draw_rectangle(BAR_X, BAR_Y, BAR_X + fill_w, BAR_Y + BAR_H, 255, 210, 0, 255, True)
        draw_rectangle(BAR_X, BAR_Y, BAR_X + BAR_W, BAR_Y + BAR_H, 255, 255, 255)

        self.font.draw(SCREEN_W - 100, BAR_Y + BAR_H + 20, self.clock.time_text(), (255, 255, 255))

        # 디버그: 현재 상태 (최종 제출 전 제거)
        state = self.guard.state_machine.cur_state
        text = type(state).__name__.upper()
        if state == self.guard.SLEEP:
            text += f' {state.tap_count}/{WAKE_TAP_COUNT}'
        self.font.draw(BAR_X + BAR_W + 20, BAR_Y + BAR_H // 2, text, (255, 255, 255))
        self.font.draw(BAR_X, BAR_Y - 20, f'어둠 {int(self.darkness.ratio * 100)}%', (255, 255, 255))
