from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_DOWN, SDLK_SPACE


# 키 입력 이벤트 판정: e = ('INPUT', sdl_event)
def down_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN

def down_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_DOWN

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


# 내부 이벤트 판정: 상태가 직접 만들어 넘기는 이벤트
def time_out(e):
    return e[0] == 'TIME_OUT'

def focus_zero(e):
    return e[0] == 'FOCUS_ZERO'


class StateMachine:
    def __init__(self, start_state, rules):
        self.cur_state = start_state
        self.rules = rules              # {상태: {판정함수: 다음상태}}
        self.cur_state.enter(('START', 0))

    def update(self):
        self.cur_state.do()

    def draw(self):
        self.cur_state.draw()

    def handle_state_event(self, state_event):
        for check_event, next_state in self.rules[self.cur_state].items():
            if check_event(state_event):
                self.cur_state.exit(state_event)
                self.cur_state = next_state
                self.cur_state.enter(state_event)
                return
