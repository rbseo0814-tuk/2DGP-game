from pico2d import load_font

TUTORIAL_X = 20             # 화면 왼쪽 아래 (어둠은 오른쪽부터 차오름)
TUTORIAL_TOP = 90           # 첫 줄 y, 아래로 LINE_GAP씩
LINE_GAP = 30
LINES = [
    '↓ 누르고 있기: 졸기 (집중력 회복, 대신 어둠이 다가옴)',
    'Space: 수하 · F: 사격 (적군만 쏠 것)',
    '잠들면 Space 연타로 기상',
]


class Tutorial:                 # 1일 차 조작 안내 (근무 내내 표시)
    def __init__(self):
        self.font = load_font('resource/font/Galmuri11.ttf', 20)

    def update(self):
        pass

    def draw(self):
        for i, line in enumerate(LINES):
            self.font.draw(TUTORIAL_X, TUTORIAL_TOP - i * LINE_GAP, line, (255, 255, 255))
