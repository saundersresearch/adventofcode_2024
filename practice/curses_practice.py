# Create a simple curses animation of growing from the corner of the screen
# Separate the animation from the logic
import curses
from curses import wrapper

# Initialize the screen
stdscr = curses.initscr()

# Turn off echo of keys
curses.noecho()

# Immediate reaction to key presses
curses.cbreak()

# Enable keypad mode
stdscr.keypad(True)

# Allow default colors
curses.start_color()
curses.use_default_colors()

# Turn off curser visibility
curses.curs_set(0)

def main(stdscr):
    # Clear screen
    stdscr.clear()

    for i in range(0, 10):
        v = i - 10
        stdscr.addstr(i, 0, f'10 divided by {v} is {10/v}')

        # Get size of screen and print that too
        y, x = stdscr.getmaxyx()
        stdscr.addstr(y-1, 0, f"Screen size is {y} rows and {x} columns.")

        # Print a red box
        curses.init_pair(1, curses.COLOR_RED, -1) # -1 is default background color
        stdscr.addstr(y-2, 0, "X" * x, curses.color_pair(1))

        stdscr.refresh()

        # Wait a second
        curses.napms(500)

    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_MAGENTA)
    stdscr.addstr(10, 0, "DONE! Press any key to continue", curses.color_pair(2))

    # Put a block of OOO in the middle of the screen (3x3)
    for i in range(1, 4):
        for j in range(1, 4):
            stdscr.addstr(y//2 + i, x//2 + j, "O")
    
    # Wait for key press
    stdscr.getkey()

    # End curses
    curses.endwin()
    
wrapper(main)