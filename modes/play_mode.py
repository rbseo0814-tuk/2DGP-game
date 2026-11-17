from pico2d import*
import game_world
import game_framework
from objects.background import Background
from objects.guard import Guard
from objects.hud import Hud
from objects.darkness import Darkness

guard = None
darkness = None


class DebugSilhouette:      # 임시: is_visible 확인용 (확인 후 제거)
    def __init__(self, x):
        self.x = x

    def update(self):
        pass

    def draw(self):
        if darkness.is_visible(self.x):
            draw_rectangle(self.x - 30, 120, self.x + 30, 280, 128, 128, 128, 255, True)

def init():
    global guard, darkness

    background = Background()
    game_world.add_object(background, 0)

    guard = Guard()
    game_world.add_object(guard, 2)

    darkness = Darkness(guard)
    game_world.add_object(darkness, 4)

    game_world.add_object(DebugSilhouette(1000), 1)   # 임시

    hud = Hud(guard, darkness)
    game_world.add_object(hud, 5)

def finish():
    global guard, darkness
    game_world.clear()
    guard = None
    darkness = None

def pause():
    pass

def resume():
    pass

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            guard.handle_event(event)

def update():
    game_world.update()

def render():
    clear_canvas()
    game_world.render()
    update_canvas()