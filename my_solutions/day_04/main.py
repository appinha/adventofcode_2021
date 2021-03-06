from puzzle_solver import PuzzleSolver, run_puzzle_solver
from helpers import Grid
from pprint import pprint
import numpy as np


delimiter = "\n\n"


class DayPuzzleSolver(PuzzleSolver):
    def __init__(self, input_file, delimiter):
        PuzzleSolver.__init__(self, input_file, delimiter)

    def get_input(self, raw_input):
        self.numbers = list(map(int, raw_input[0].split(',')))
        self.boards = [Grid.get_from_string(board, int) for board in raw_input[1:]]

    def _mark_number_on_board(self, number, board, marked_board):
        index = np.where(board == number)
        marked_board[index] = number
        board[board == number] = -1

    def _board_has_full_array(self, board):
        full_rows = np.all(board >= 0, axis=Grid.row_axis)
        full_columns = np.all(board >= 0, axis=Grid.col_axis)
        return any(full_rows) or any(full_columns)

    def _play_bingo(self, numbers, boards, get_all=False):
        marked_boards = [Grid.create_filled_with(boards[0].shape, -1) for _ in range(len(boards))]
        winning_board_indexes = []
        all_winning = []
        for number in numbers:

            for i, board in enumerate(boards):
                if i in winning_board_indexes:
                    continue
                self._mark_number_on_board(number, board, marked_boards[i])

            for i, marked_board in enumerate(marked_boards):
                if i in winning_board_indexes:
                    continue
                if self._board_has_full_array(marked_board):
                    if get_all:
                        winning_board_indexes.append(i)
                        all_winning.append((number, boards[i]))
                    else:
                        return number, boards[i]

        return all_winning

    def _sum_unmarked_numbers(self, board):
        board[board == -1] = 0
        return Grid.sum(board)

    def solve_part_1(self):
        winning_number, unmarked_winning_board = self._play_bingo(self.numbers, self.boards)
        return winning_number * self._sum_unmarked_numbers(unmarked_winning_board)

    def solve_part_2(self):
        all_winning = self._play_bingo(self.numbers, self.boards, get_all=True)
        winning_number, unmarked_winning_board = all_winning[-1]
        return winning_number * self._sum_unmarked_numbers(unmarked_winning_board)


if __name__ == '__main__':
    run_puzzle_solver(DayPuzzleSolver, delimiter)