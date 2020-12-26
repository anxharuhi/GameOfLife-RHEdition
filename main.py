import random
#from rich.table import Table


def random_state(x: int, y: int):
    return [[random.randrange(0,2) for j in range(y)] for i in range(x)]


def print_board(gof_board: list):
    for row in gof_board:
        print(row)


def render(gof_board: list):
    conversion_dict = {0: ' ', 1: '#'}
    print('-'*len(gof_board) + "--")
    for i, row in enumerate(gof_board):
        column = '|'
        for space in row:
            column += conversion_dict[space]
        column += '|'
        print(column)
    print('-' * len(gof_board) + "--")



def main():
    gof_board = random_state(3, 3)
    # print_board(gof_board)
    render(gof_board)

if __name__ == '__main__':
    main()


