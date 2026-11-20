import random
import game_framework
import game_world
from objects.visitor import Visitor

FIRST_SPAWN_DELAY = 3.0     # 시작 후 첫 등장까지(초)
SPAWN_STOP_TIME = 165.0     # 03:50 이후 새 접근자 없음


class Spawner:
    def __init__(self, stage, clock, darkness):
        self.stage = stage          # config.STAGES[day]
        self.clock = clock
        self.darkness = darkness
        self.timer = FIRST_SPAWN_DELAY

    def update(self):
        if self.clock.elapsed >= SPAWN_STOP_TIME:
            return

        self.timer -= game_framework.frame_time
        if self.timer > 0:
            return

        if len(game_world.world[1]) < self.stage['max_active']:    # 1번 레이어 = 접근자
            kind = random.choice(self.stage['kinds'])
            visitor = Visitor(self.darkness, kind, self.stage['enemy_speed'])
            game_world.add_object(visitor, 1)
            self.timer = self.stage['interval']
        # 자리가 없으면 timer가 0 이하인 채로 대기 → 자리가 나면 바로 등장

    def draw(self):
        pass
