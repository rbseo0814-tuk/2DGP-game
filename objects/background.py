from pico2d import load_image
from config import SCREEN_W, SCREEN_H

class Background:
    def __init__(self):
        self.sky = load_image('resource/image/bg_sky.png')
        self.fence = load_image('resource/image/bg_fence.png')
        self.post = load_image('resource/image/bg_post.png')

    def update(self):
        pass

    def draw(self):
        cx, cy = SCREEN_W // 2, SCREEN_H // 2
        self.sky.draw(cx, cy)
        self.fence.draw(cx, cy)
        self.post.draw(cx, cy)