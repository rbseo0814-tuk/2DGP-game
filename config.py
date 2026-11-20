SCREEN_W, SCREEN_H = 1280, 720

POST_X = 360                # 위병소 도착선: 적군이 이 x 이하로 오면 패배

# 날짜별 난이도: 등장 종류, 등장 간격(초), 적군 속도(px/s), 동시 접근 수, 집중력 감소 배율
STAGES = {
    1: dict(kinds=['enemy'],                      interval=15, enemy_speed=40, max_active=1, focus_mul=1.0, tutorial=True),
    2: dict(kinds=['enemy', 'patrol'],            interval=13, enemy_speed=40, max_active=1, focus_mul=1.0),
    3: dict(kinds=['enemy', 'patrol', 'officer'], interval=12, enemy_speed=45, max_active=1, focus_mul=1.0),
    4: dict(kinds=['enemy', 'patrol', 'officer'], interval=10, enemy_speed=50, max_active=2, focus_mul=1.0),
    5: dict(kinds=['enemy', 'patrol', 'officer'], interval=8,  enemy_speed=55, max_active=2, focus_mul=1.3),
}