from pico2d import draw_rectangle
import game_framework
from config import SCREEN_W
from objects.state_machine import StateMachine

ENEMY_SPEED = 40            # px/s
VISITOR_W, VISITOR_H = 60, 160     # 임시 사각형 크기 (스프라이트로 교체 예정)


class Approach:
    def __init__(self, visitor):
        self.visitor = visitor

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        self.visitor.x -= self.visitor.speed * game_framework.frame_time

    def draw(self):
        v = self.visitor
        draw_rectangle(v.x - VISITOR_W / 2, v.y - VISITOR_H / 2,
                       v.x + VISITOR_W / 2, v.y + VISITOR_H / 2, 128, 128, 128, 255, True)


class Visitor:
    def __init__(self, darkness, speed=ENEMY_SPEED):
        self.darkness = darkness
        self.speed = speed
        self.x, self.y = SCREEN_W + 30, 200     # 화면 오른쪽 밖에서 시작, 근무자와 같은 바닥

        self.APPROACH = Approach(self)
        self.state_machine = StateMachine(
            self.APPROACH,
            {
                self.APPROACH: {},
            }
        )

    def update(self):
        self.state_machine.update()

    def draw(self):
        if not self.darkness.is_visible(self.x):    # 어둠 속이면 그리지 않음
            return
        self.state_machine.draw()
