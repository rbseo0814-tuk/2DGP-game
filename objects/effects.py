from pico2d import draw_rectangle, get_time, load_font
import game_world

FLASH_DURATION = 0.1        # 총구 화염 표시 시간(초)
FLASH_W, FLASH_H = 20, 12   # 임시 사각형 크기 (이미지로 교체 예정)

BUBBLE_DURATION = 1.0       # 말풍선 표시 시간(초)
BUBBLE_FONT_SIZE = 20
BUBBLE_PAD = 8              # 글자와 테두리 사이 여백(px)


class MuzzleFlash:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.start_time = get_time()

    def update(self):
        if get_time() - self.start_time >= FLASH_DURATION:
            game_world.remove_object(self)

    def draw(self):
        draw_rectangle(self.x - FLASH_W / 2, self.y - FLASH_H / 2,
                       self.x + FLASH_W / 2, self.y + FLASH_H / 2, 255, 220, 60, 255, True)


class SpeechBubble:
    font = None                 # 모든 말풍선이 같이 쓰는 폰트 (처음 한 번만 로드)

    def __init__(self, text, x, y):
        if SpeechBubble.font is None:
            SpeechBubble.font = load_font('resource/font/Galmuri11.ttf', BUBBLE_FONT_SIZE)
        self.text = text
        self.x, self.y = x, y   # 말풍선 아래쪽 가운데
        self.start_time = get_time()

    def update(self):
        if get_time() - self.start_time >= BUBBLE_DURATION:
            game_world.remove_object(self)

    def draw(self):
        w = len(self.text) * BUBBLE_FONT_SIZE + BUBBLE_PAD * 2     # 글자 너비는 어림값
        h = BUBBLE_FONT_SIZE + BUBBLE_PAD * 2
        left, bottom = self.x - w / 2, self.y
        draw_rectangle(left, bottom, left + w, bottom + h, 255, 255, 255, 255, True)
        draw_rectangle(left, bottom, left + w, bottom + h, 0, 0, 0)
        self.font.draw(left + BUBBLE_PAD, bottom + h / 2, self.text, (0, 0, 0))
