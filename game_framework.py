import time

running = False
stack = []


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
    global running, stack
    running = True
    stack = [start_mode]
    start_mode.init()

    while running:
        stack[-1].handle_events()
        stack[-1].update() 
        stack[-1].render()
