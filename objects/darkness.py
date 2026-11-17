import game_framework

DOZE_DARK_RATE = 0.10       # 초당 어둠 비율 변화량 (1.0 = 화면 전체)
AWAKE_DARK_RATE = -0.30


class Darkness:
    def __init__(self, guard):
        self.guard = guard
        self.ratio = 0.0        # 0.0 ~ 1.0, 오른쪽부터 덮인 비율

    def update(self):
        state = self.guard.state_machine.cur_state
        if state == self.guard.SLEEP:
            self.ratio = 1.0
        elif state == self.guard.DOZE:
            self.ratio = min(1.0, self.ratio + DOZE_DARK_RATE * game_framework.frame_time)
        else:                   # AWAKE, WAKE
            self.ratio = max(0.0, self.ratio + AWAKE_DARK_RATE * game_framework.frame_time)

    def draw(self):
        pass
