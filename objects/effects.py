from pico2d import draw_rectangle, get_time
import game_world

FLASH_DURATION = 0.1        # 총구 화염 표시 시간(초)
FLASH_W, FLASH_H = 20, 12   # 임시 사각형 크기 (이미지로 교체 예정)


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
