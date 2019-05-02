import random
import sys,os
import curses

UP = ord('w')
DOWN = ord('s')
LEFT = ord('a')
RIGHT = ord('d')
QUIT = ord('q')
block = '|||'

def get_next_move(snake, key):
    if key == UP:
        head = (snake[-1][0] - 1, snake[-1][1])
    elif key == DOWN:
        head = (snake[-1][0] + 1, snake[-1][1])
    elif key == LEFT:
        head = (snake[-1][0], snake[-1][1] - 1)
    elif key == RIGHT:
        head = (snake[-1][0], snake[-1][1] + 1)
    else: head = None
    return head
  

def draw_snake(stdscr):
    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    height, width = stdscr.getmaxyx()

    y_init = height // 2
    x_init = width // 4

    snake = [(y_init, x_init)]

    food = (int(height * random.random()), int(width * random.random()) )

    oldkey = LEFT
    key = oldkey

    while (key != QUIT):
        
        stdscr.clear()

        head = get_next_move(snake, key)

        # check if invalid input or it goes to itself
        if head is None and (len(snake) > 1 and head == snake[-2]):
            key = oldkey
            head = get_next_move(snake, key)


        # check if it goes out of bound
        if head[0] < 0 or head[0] > height - 1 or head[1] < 0 or head[1] > width - 1:
                break

        # else move forward
        oldkey = key
        if head == food:
            snake.append(head)
            food = (int(height * random.random()), int(width * random.random()) )

        else:
            snake.append(head)
            snake.pop(0)
            
        
        for b in snake:
            stdscr.addch(b[0], b[1], curses.ACS_PI)

        stdscr.addstr(food[0], food[1], block)


        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        key = stdscr.getch()

def main():
    curses.wrapper(draw_snake)

if __name__ == "__main__":
    main()
