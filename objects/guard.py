from pico2d import load_image


class Guard:
    def __init__(self):
        self.image = load_image('resource/image/guard_sheet.png')
        self.x, self.y = 320, 168   # 발 위치 y=120 + 키의 절반 48
        self.frame = 0
