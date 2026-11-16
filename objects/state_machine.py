from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_DOWN, SDLK_SPACE


# 키 입력 이벤트 판정: e = ('INPUT', sdl_event)
def down_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN

def down_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_DOWN

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE
