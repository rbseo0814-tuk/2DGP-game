from pico2d import *
import game_framework
import modes.play_mode as play_mode
from config import SCREEN_W, SCREEN_H

LAST_DAY = 5    # 마지막 근무 날짜 (클리어하면 1일 차로)

result = ''     # play_mode가 넘겨주는 결과 문구 (예: '근무 완료', '패배: 적군 도착')
score = 0
cleared = False # 클리어했는지 → 다음 날 / 패배 → 같은 날
day = 1         # 방금 끝난 근무 날짜
font = None


def init():
    global font
    font = load_font('resource/font/Galmuri11.ttf', 32)

def finish():
    global font
    font = None

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
        elif event.type == SDL_KEYDOWN:
            if cleared:
                play_mode.day = day + 1 if day < LAST_DAY else 1    # 다음 날 (5일 차 다음은 1일 차)
            else:
                play_mode.day = day                                 # 같은 날 다시
            game_framework.change_mode(play_mode)

def update():
    pass

def render():
    clear_canvas()
    draw_rectangle(0, 0, SCREEN_W, SCREEN_H, 0, 0, 0, 255, True)     # 검은 배경
    cx, cy = SCREEN_W // 2, SCREEN_H // 2
    font.draw(cx - 150, cy + 60, result, (255, 255, 255))
    font.draw(cx - 150, cy, f'점수 {score}', (255, 255, 255))
    font.draw(cx - 150, cy - 80, '아무 키나 누르면 다시 근무 · ESC 종료', (180, 180, 180))
    update_canvas()
