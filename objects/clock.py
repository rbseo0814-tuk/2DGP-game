import game_framework

SHIFT_SECONDS = 180.0       # 실제 180초 = 근무 120분 (1.5초 = 1분)
SHIFT_MINUTES = 120
START_HOUR = 2              # 02:00 시작


class Clock:
    def __init__(self):
        self.elapsed = 0.0      # 근무 시작 후 지난 실제 시간(초)

    def update(self):
        self.elapsed = min(SHIFT_SECONDS, self.elapsed + game_framework.frame_time)

    def draw(self):
        pass                    # 표시는 HUD가 담당

    def minutes(self):          # 근무 시작 후 지난 분
        return int(self.elapsed / SHIFT_SECONDS * SHIFT_MINUTES)

    def time_text(self):        # '02:00' ~ '04:00'
        m = self.minutes()
        return f'{START_HOUR + m // 60:02d}:{m % 60:02d}'

    def is_over(self):
        return self.elapsed >= SHIFT_SECONDS
