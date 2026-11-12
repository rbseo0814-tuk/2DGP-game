# 0 배경 / 1 접근자 / 2 근무자 / 3 이펙트 / 4 어둠 / 5 HUD
world = [[] for _ in range(6)]

def add_object(o, depth):
    world[depth].append(o)

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            return

def update():
    for layer in world:
        for o in layer[:]:
            o.update()

def render():
    for layer in world:
        for o in layer:
            o.draw()

def clear():
    for layer in world:
        layer.clear()