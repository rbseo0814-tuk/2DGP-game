from pico2d import*
import game_world
import game_framework

def init():
    pass

def finish():
    game_world.clear()

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

def update():
    game_world.update()

def render():
    clear_canvas()
    game_world.render()
    update_canvas()