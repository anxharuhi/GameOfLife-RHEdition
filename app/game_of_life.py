import copy
import random
import curses
import _curses


class Screen:

    def __init__(self):
        # noinspection PyUnresolvedReferences
        self.screen: _curses.window = curses.initscr()
        self.windows = {}

    def add_window(self, window_id: str, x_size: int, y_size: int, x_pos: int = None, y_pos: int = None):
        raise NotImplementedError()

    def remove_window(self, window_id: str):
        raise NotImplementedError()

    def update_window(self, window_id: str):
        raise NotImplementedError()

    def redraw_window(self, window_id: str):
        raise NotImplementedError()


class GameOfLife:

    def __init__(self, screen: Screen = None, x_size: int = None, y_size: int = None, file: str = None):
        # if screen is not None:  # TODO: Change negation once screen is implemented
        #     raise RuntimeError('No screen provided')
        if x_size is not None and y_size is not None and file is None:
            self.gof_board = self.random_state(x_size, y_size)
            self.x_size = x_size
            self.y_size = y_size
        elif x_size is None and y_size is None and file is not None:
            with open(file, 'r') as board:
                self.gof_board = [list(map(int, list(row))) for row in board.read().split()]
            self.x_size = len(self.gof_board[0])
            self.y_size = len(self.gof_board)
        else:
            raise RuntimeError('Please provide either a size or a premade petri dish')
        # noinspection PyUnresolvedReferences
        # self.screen: screen = screen
        # self.screen.add_window(self.x_size + 2, self.y_size + 2, 0, 0)
        self.screen: _curses.window = curses.initscr()
        y_size, x_size = self.screen.getmaxyx()
        # noinspection PyUnresolvedReferences
        self.window: _curses.window = curses.newwin(self.y_size + 2, self.x_size + 2, 0, 0)  # curses doesn't like
        # writes to the lower right hand corner of a window, so 2 offset: one for the border, 1 to avoid the corner

    # noinspection PyMethodMayBeStatic
    def random_state(self, x: int, y: int):
        return [[random.randrange(0, 2) for _ in range(y)] for _ in range(x)]

    def load_from_file(self, file: str):
        raise NotImplementedError

    def render(self):
        conversion_dict = {0: ' ', 1: '#'}
        print('+' + '-' * len(self.gof_board) + '+')
        for i, row in enumerate(self.gof_board):
            column = '|'
            for space in row:
                column += conversion_dict[space]
            column += '|'
            print(column)
        print('+' + '-' * len(self.gof_board) + "+")

    def render_curses(self):
        conversion_dict = {0: ' ', 1: curses.ACS_CKBOARD}  # noinspection PyUnresolvedReferences
        self.window.clear()
        self.window.box()
        curses.curs_set(0)
        for i, row in enumerate(self.gof_board):
            for j, space in enumerate(row):
                try:
                    self.window.addch(i + 1, j + 1, conversion_dict[space])  # offset position by one to clear the border
                except _curses.error:
                    print('i, j, value: ', i, j, space)
                    print('Board size:', self.x_size, self.y_size)
                    raise
        self.window.refresh()

    def next_board_state(self):
        updated_board = copy.deepcopy(self.gof_board)
        for i, row in enumerate(self.gof_board):
            for j, point in enumerate(row):
                alive = 0
                for k in range(i - 1, i + 2):
                    for m in range(j - 1, j + 2):
                        if k < 0 or m < 0:
                            pass
                        elif k >= len(self.gof_board) or m >= len(self.gof_board[0]):
                            pass
                        else:
                            alive += self.gof_board[k][m]
                if self.gof_board[i][j] == 0:
                    if alive == 3:
                        updated_board[i][j] = 1
                    else:
                        pass
                else:
                    alive -= 1  # Remove the center square
                    if alive <= 1 or alive > 3:
                        updated_board[i][j] = 0
                    else:
                        updated_board[i][j] = 1
        self.gof_board = updated_board


def main():
    board_size_x, board_size_y = 6, 6
    # gof_board = GameOfLife(x_size=board_size_x, y_size=board_size_y)
    gof_board = GameOfLife(file='patterns/ggg.txt')
    for i in range(1*1):
        gof_board.render_curses()
        gof_board.next_board_state()
        curses.napms(16)


if __name__ == '__main__':
    main()
