from pico2d import load_image
import game_framework
from objects.state_machine import StateMachine, down_down, down_up

FRAMES_PER_ACTION = 4       # 상태마다 프레임 4장
FRAMES_PER_SECOND = 4.0     # 1초에 넘길 프레임 수

FOCUS_MAX = 100
AWAKE_FOCUS_RATE = -4       # 초당 집중력 변화량
DOZE_FOCUS_RATE = 12
SLEEP_FOCUS_RATE = 20


class Awake:
    def __init__(self, guard):
        self.guard = guard

    def enter(self, e):
        self.guard.frame = 0

    def exit(self, e):
        pass

    def do(self):
        self.guard.frame = (self.guard.frame + FRAMES_PER_SECOND * game_framework.frame_time) % FRAMES_PER_ACTION
        self.guard.focus = max(0, self.guard.focus + AWAKE_FOCUS_RATE * game_framework.frame_time)

    def draw(self):
        self.guard.image.clip_draw(int(self.guard.frame) * 96, 0, 96, 160, self.guard.x, self.guard.y)


class Doze:
    def __init__(self, guard):
        self.guard = guard

    def enter(self, e):
        self.guard.frame = 0

    def exit(self, e):
        pass

    def do(self):
        self.guard.frame = (self.guard.frame + FRAMES_PER_SECOND * game_framework.frame_time) % FRAMES_PER_ACTION
        self.guard.focus = min(FOCUS_MAX, self.guard.focus + DOZE_FOCUS_RATE * game_framework.frame_time)

    def draw(self):
        self.guard.image.clip_draw(int(self.guard.frame) * 96, 160, 96, 160, self.guard.x, self.guard.y)


class Sleep:
    def __init__(self, guard):
        self.guard = guard

    def enter(self, e):
        self.guard.frame = 0

    def exit(self, e):
        pass

    def do(self):
        self.guard.frame = (self.guard.frame + FRAMES_PER_SECOND * game_framework.frame_time) % FRAMES_PER_ACTION
        self.guard.focus = min(FOCUS_MAX, self.guard.focus + SLEEP_FOCUS_RATE * game_framework.frame_time)

    def draw(self):
        self.guard.image.clip_draw(int(self.guard.frame) * 96, 320, 96, 160, self.guard.x, self.guard.y)


class Guard:
    def __init__(self):
        self.image = load_image('resource/image/guard_sheet.png')
        self.x, self.y = 300, 200   # 발 위치 y=120 + 프레임 높이의 절반 80
        self.frame = 0
        self.focus = FOCUS_MAX

        self.AWAKE = Awake(self)
        self.DOZE = Doze(self)
        self.SLEEP = Sleep(self)
        self.state_machine = StateMachine(
            self.AWAKE,
            {
                self.AWAKE: {down_down: self.DOZE},
                self.DOZE: {down_up: self.AWAKE},
                self.SLEEP: {},
            }
        )

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()
