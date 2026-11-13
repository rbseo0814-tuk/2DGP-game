from pico2d import*
import game_world
import game_framework

def init():
    pass

def finish():
    pass

def pause():
    pass

def resume():
    pass

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_Quit:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()

def update():
    pass

def render():
    pass

