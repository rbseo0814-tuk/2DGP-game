from pico2d import load_image
import game_framework
from objects.state_machine import StateMachine

FRAMES_PER_ACTION = 4       # 상태마다 프레임 4장
FRAMES_PER_SECOND = 4.0     # 1초에 넘길 프레임 수


class Awake:
    def __init__(self, guard):
        self.guard = guard

    def enter(self, e):
        self.guard.frame = 0

    def exit(self, e):
        pass

    def do(self):
        self.guard.frame = (self.guard.frame + FRAMES_PER_SECOND * game_framework.frame_time) % FRAMES_PER_ACTION

    def draw(self):
        self.guard.image.clip_draw(int(self.guard.frame) * 96, 0, 96, 160, self.guard.x, self.guard.y)


class Guard:
    def __init__(self):
        self.image = load_image('resource/image/guard_sheet.png')
        self.x, self.y = 300, 200   # 발 위치 y=120 + 프레임 높이의 절반 80
        self.frame = 0

        self.AWAKE = Awake(self)
        self.state_machine = StateMachine(
            self.AWAKE,
            {
                self.AWAKE: {},
            }
        )

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()
