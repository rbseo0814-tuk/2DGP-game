from pico2d import draw_rectangle, get_time
import game_framework
import game_world
from config import SCREEN_W
from objects.state_machine import StateMachine, hit, challenge, time_out
from objects.effects import SpeechBubble

ENEMY_SPEED = 40            # px/s (적군은 날짜별 값을 받음)
PATROL_SPEED = 50
OFFICER_SPEED = 60
VISITOR_W, VISITOR_H = 60, 160     # 임시 사각형 크기 (스프라이트로 교체 예정)
DOWN_DURATION = 1.0         # 쓰러진 뒤 사라질 때까지(초)
CHALLENGE_STOP = 1.0        # 수하 받고 멈춰 있는 시간(초)
REVEAL_TIME = 0.5           # 정체 공개 후 서 있는 시간(초)

KIND_COLOR = {              # 정체 공개 후 임시 색 (스프라이트로 교체 예정)
    'enemy': (170, 50, 50),
    'patrol': (60, 140, 60),
    'officer': (60, 90, 180),
}
KIND_REPLY = {              # 수하에 대한 응답
    'enemy': '…',
    'patrol': '담배! (답어)',
    'officer': '근무 중 이상 무',
}


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


class Challenged:
    def __init__(self, visitor):
        self.visitor = visitor

    def enter(self, e):
        self.start_time = get_time()

    def exit(self, e):
        pass

    def do(self):                   # 멈춰 있음
        if get_time() - self.start_time >= CHALLENGE_STOP:
            self.visitor.state_machine.handle_state_event(('TIME_OUT', 0))

    def draw(self):                 # 아직 정체 공개 전: 회색 실루엣
        v = self.visitor
        draw_rectangle(v.x - VISITOR_W / 2, v.y - VISITOR_H / 2,
                       v.x + VISITOR_W / 2, v.y + VISITOR_H / 2, 128, 128, 128, 255, True)


class Revealed:
    def __init__(self, visitor):
        self.visitor = visitor

    def enter(self, e):
        v = self.visitor
        game_world.add_object(SpeechBubble(KIND_REPLY[v.kind], v.x, v.y + VISITOR_H / 2 + 10), 3)
        self.start_time = get_time()

    def exit(self, e):
        pass

    def do(self):                   # 서서 응답
        if get_time() - self.start_time >= REVEAL_TIME:
            self.visitor.state_machine.handle_state_event(('TIME_OUT', 0))

    def draw(self):                 # 정체 공개: 종류별 색
        v = self.visitor
        r, g, b = KIND_COLOR[v.kind]
        draw_rectangle(v.x - VISITOR_W / 2, v.y - VISITOR_H / 2,
                       v.x + VISITOR_W / 2, v.y + VISITOR_H / 2, r, g, b, 255, True)


class Down:
    def __init__(self, visitor):
        self.visitor = visitor

    def enter(self, e):
        self.start_time = get_time()

    def exit(self, e):
        pass

    def do(self):
        if get_time() - self.start_time >= DOWN_DURATION:
            game_world.remove_object(self.visitor)

    def draw(self):
        v = self.visitor
        bottom = v.y - VISITOR_H / 2            # 바닥에 눕힌 사각형
        draw_rectangle(v.x - VISITOR_H / 2, bottom,
                       v.x + VISITOR_H / 2, bottom + VISITOR_W, 80, 80, 80, 255, True)


class Visitor:
    def __init__(self, darkness, kind, enemy_speed=ENEMY_SPEED):
        self.darkness = darkness
        self.kind = kind            # 'enemy' / 'patrol' / 'officer'
        if kind == 'enemy':
            self.speed = enemy_speed
        elif kind == 'patrol':
            self.speed = PATROL_SPEED
        else:
            self.speed = OFFICER_SPEED
        self.challenged = False     # 수하를 받았는지 (순찰조 미수하 감점에 사용)
        self.x, self.y = SCREEN_W + 30, 200     # 화면 오른쪽 밖에서 시작, 근무자와 같은 바닥

        self.APPROACH = Approach(self)
        self.CHALLENGED = Challenged(self)
        self.REVEALED = Revealed(self)
        self.DOWN = Down(self)
        self.state_machine = StateMachine(
            self.APPROACH,
            {
                self.APPROACH: {hit: self.DOWN, challenge: self.CHALLENGED},
                self.CHALLENGED: {hit: self.DOWN, time_out: self.REVEALED},
                self.REVEALED: {hit: self.DOWN},
                self.DOWN: {},
            }
        )

    def hit(self):
        self.state_machine.handle_state_event(('HIT', 0))

    def is_target(self):            # 사격 대상이 될 수 있는 상태인지 (DOWN·LEAVE 제외)
        return self.state_machine.cur_state != self.DOWN

    def challenge(self):
        self.challenged = True
        self.state_machine.handle_state_event(('CHALLENGE', 0))

    def is_approaching(self):       # 수하 대상이 될 수 있는 상태인지 (아직 수하 전)
        return self.state_machine.cur_state == self.APPROACH

    def update(self):
        self.state_machine.update()

    def draw(self):
        if not self.darkness.is_visible(self.x):    # 어둠 속이면 그리지 않음
            return
        self.state_machine.draw()
