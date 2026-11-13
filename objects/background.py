from pico2d import load_image

class Background:
    def __init__(self):
        self.sky = load_image('resource/image/bg_sky.png')
        self.fence = load_image('resource/image/bg_fence.png')
        self.post = load_image('resource/image/bg_post.png')