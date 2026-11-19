from pico2d import*
import game_world
import game_framework
from objects.background import Background
from objects.guard import Guard
from objects.hud import Hud
from objects.darkness import Darkness
from objects.clock import Clock

guard = None
darkness = None
clock = None

def init():
    global guard, darkness, clock

    background = Background()
    game_world.add_object(background, 0)

    guard = Guard()
    game_world.add_object(guard, 2)

    darkness = Darkness(guard)
    game_world.add_object(darkness, 4)

    clock = Clock()
    game_world.add_object(clock, 5)

    hud = Hud(guard, darkness, clock)
    game_world.add_object(hud, 5)

def finish():
    global guard, darkness, clock
    game_world.clear()
    guard = None
    darkness = None
    clock = None

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