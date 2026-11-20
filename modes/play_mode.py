from pico2d import*
import game_world
import game_framework
from objects.background import Background
from objects.guard import Guard
from objects.hud import Hud
from objects.darkness import Darkness
from objects.clock import Clock
from objects.spawner import Spawner
from config import STAGES, POST_X
import modes.result_mode as result_mode

day = 3     # 임시: 3주차는 접근자 3종 확인용, 4주차 날짜 진행 때 1로
guard = None
darkness = None
clock = None
defeat_reason = None    # 판정 시점(update)까지 미뤄 둔 패배 원인 (예: 오인 사격)

def init():
    global guard, darkness, clock, defeat_reason
    defeat_reason = None

    background = Background()
    game_world.add_object(background, 0)

    guard = Guard()
    game_world.add_object(guard, 2)

    darkness = Darkness(guard)
    game_world.add_object(darkness, 4)

    clock = Clock()
    game_world.add_object(clock, 5)

    spawner = Spawner(STAGES[day], clock, darkness)
    game_world.add_object(spawner, 5)

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

def shoot():
    # 보이는 접근자 중 가장 가까운(x가 가장 작은) 1명을 맞힘. 맞힌 접근자를 돌려줌, 없으면 None
    global defeat_reason
    targets = [v for v in game_world.world[1] if v.is_target() and darkness.is_visible(v.x)]
    if not targets:
        return None
    target = min(targets, key=lambda v: v.x)
    target.hit()
    if target.kind != 'enemy':
        defeat_reason = '패배: 오인 사격'    # 바로 끝내지 않고 update에서 판정
    return target

def challenge():
    # 아직 수하 받지 않은 보이는 접근자 중 가장 가까운 1명에게 수하. 대상이 없으면 None
    targets = [v for v in game_world.world[1] if v.is_approaching() and darkness.is_visible(v.x)]
    if not targets:
        return None
    target = min(targets, key=lambda v: v.x)
    target.challenge()
    return target

def end_shift(text):
    result_mode.result = text
    result_mode.score = guard.score
    game_framework.change_mode(result_mode)

def update():
    game_world.update()

    # 승패 판정: 한 곳에 모아서, 패배를 먼저
    if defeat_reason:
        end_shift(defeat_reason)
        return
    for v in game_world.world[1]:
        if v.is_target() and v.x <= POST_X:
            if v.kind == 'enemy':
                end_shift('패배: 적군 도착')
                return
            if v.is_approaching():          # 아군이 수하 없이 도착
                if v.kind == 'patrol':
                    guard.score -= 50       # 순찰조 미수하 감점
                v.arrive()                  # 복귀(LEAVE)
    if clock.is_over():
        end_shift('근무 완료')

def render():
    clear_canvas()
    game_world.render()
    update_canvas()