import time

running = False
stack = []
frame_time = 0.0


def change_mode(mode):
    pass


def push_mode(mode):
    pass


def pop_mode():
    pass


def quit():
    global running
    running = False


def run(start_mode):
    global running, stack, frame_time
    running = True
    stack = [start_mode]

    try:
        start_mode.init()

        frame_time = 0.0
        current_time = time.time()

        while running:
            stack[-1].handle_events()
            stack[-1].update() 
            stack[-1].render()
            frame_time = time.time() - current_time
            current_time += frame_time

    finally:
        while stack:
            stack.pop().finish()
        running = False

    