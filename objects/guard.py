from pico2d import load_image, get_time
import game_framework
from objects.state_machine import StateMachine, down_down, down_up, focus_zero, time_out, space_down, wake_up, f_down

FRAMES_PER_ACTION = 4       # 상태마다 프레임 4장
FRAMES_PER_SECOND = 4.0     # 1초에 넘길 프레임 수

FOCUS_MAX = 100
AWAKE_FOCUS_RATE = -4       # 초당 집중력 변화량
DOZE_FOCUS_RATE = 12
SLEEP_FOCUS_RATE = 20

DOZE_LIMIT = 5.0            # 이 시간(초) 넘게 졸면 SLEEP
WAKE_DURATION = 0.5         # 화들짝 연출 시간(초)
WAKE_TAP_COUNT = 8          # SLEEP에서 깨는 데 필요한 Space 연타 수

FIRE_COOLDOWN = 0.5         # 사격 간 최소 간격(초)


class Awake:
    def __init__(self, guard):
        self.guard = guard

    def enter(self, e):
        if f_down(e):               # 사격: 자기 전이로 다시 들어옴
            self.guard.fire()
        else:
            self.guard.frame = 0

    def exit(self, e):
        pass

    def do(self):
        self.guard.frame = (self.guard.frame + FRAMES_PER_SECOND * game_framework.frame_time) % FRAMES_PER_ACTION
        self.guard.focus = max(0, self.guard.focus + AWAKE_FOCUS_RATE * game_framework.frame_time)
        if self.guard.focus == 0:
            self.guard.state_machine.handle_state_event(('FOCUS_ZERO', 0))

    def draw(self):
        self.guard.image.clip_draw(int(self.guard.frame) * 96, 0, 96, 160, self.guard.x, self.guard.y)


class Doze:
    def __init__(self, guard):
        self.guard = guard

    def enter(self, e):
        self.guard.frame = 0
        self.start_time = get_time()

    def exit(self, e):
        pass

    def do(self):
        self.guard.frame = (self.guard.frame + FRAMES_PER_SECOND * game_framework.frame_time) % FRAMES_PER_ACTION
        self.guard.focus = min(FOCUS_MAX, self.guard.focus + DOZE_FOCUS_RATE * game_framework.frame_time)
        if get_time() - self.start_time >= DOZE_LIMIT:
            self.guard.state_machine.handle_state_event(('TIME_OUT', 0))

    def draw(self):
        self.guard.image.clip_draw(int(self.guard.frame) * 96, 160, 96, 160, self.guard.x, self.guard.y)


class Sleep:
    def __init__(self, guard):
        self.guard = guard

    def enter(self, e):
        if space_down(e):           # 연타: 자기 전이로 다시 들어옴
            self.tap_count += 1
        else:                       # 처음 잠듦
            self.tap_count = 0
            self.guard.frame = 0

    def exit(self, e):
        pass

    def do(self):
        self.guard.frame = (self.guard.frame + FRAMES_PER_SECOND * game_framework.frame_time) % FRAMES_PER_ACTION
        self.guard.focus = min(FOCUS_MAX, self.guard.focus + SLEEP_FOCUS_RATE * game_framework.frame_time)
        if self.tap_count >= WAKE_TAP_COUNT:
            self.guard.state_machine.handle_state_event(('WAKE_UP', 0))

    def draw(self):
        self.guard.image.clip_draw(int(self.guard.frame) * 96, 320, 96, 160, self.guard.x, self.guard.y)


class Wake:
    def __init__(self, guard):
        self.guard = guard

    def enter(self, e):
        self.guard.frame = 0
        self.start_time = get_time()

    def exit(self, e):
        pass

    def do(self):
        self.guard.frame = (self.guard.frame + FRAMES_PER_SECOND * game_framework.frame_time) % FRAMES_PER_ACTION
        if get_time() - self.start_time >= WAKE_DURATION:
            self.guard.state_machine.handle_state_event(('TIME_OUT', 0))

    def draw(self):
        self.guard.image.clip_draw(int(self.guard.frame) * 96, 480, 96, 160, self.guard.x, self.guard.y)


class Guard:
    def __init__(self):
        self.image = load_image('resource/image/guard_sheet.png')
        self.x, self.y = 300, 200   # 발 위치 y=120 + 프레임 높이의 절반 80
        self.frame = 0
        self.focus = FOCUS_MAX
        self.last_fire_time = -FIRE_COOLDOWN    # 첫 발은 바로 쏠 수 있게

        self.AWAKE = Awake(self)
        self.DOZE = Doze(self)
        self.SLEEP = Sleep(self)
        self.WAKE = Wake(self)
        self.state_machine = StateMachine(
            self.AWAKE,
            {
                self.AWAKE: {down_down: self.DOZE, focus_zero: self.SLEEP, f_down: self.AWAKE},
                self.DOZE: {down_up: self.AWAKE, time_out: self.SLEEP},
                self.SLEEP: {space_down: self.SLEEP, wake_up: self.WAKE},
                self.WAKE: {time_out: self.AWAKE},
            }
        )

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

    def fire(self):
        if get_time() - self.last_fire_time < FIRE_COOLDOWN:
            return
        self.last_fire_time = get_time()

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()
