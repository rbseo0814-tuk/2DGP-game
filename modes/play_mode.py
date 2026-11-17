from pico2d import*
import game_world
import game_framework
from objects.background import Background
from objects.guard import Guard

guard = None
font = None     # 임시: 한글 폰트 확인용 (HUD 만들 때 교체)

def init():
    global guard, font
    font = load_font('resource/font/Galmuri11.ttf', 24)

    background = Background()
    game_world.add_object(background, 0)

    guard = Guard()
    game_world.add_object(guard, 2)

def finish():
    global guard
    game_world.clear()
    guard = None

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
    font.draw(20, 690, '집중력 / 교대까지 48분', (255, 255, 255))   # 임시
    update_canvas()