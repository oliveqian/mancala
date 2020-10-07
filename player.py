import copy
import random


class Player:
    Human = 0
    Random = 1
    Minimax = 2
    Minimax_ab = 3

    def __init__(self, player_num, player_type):
        self.num = player_num
        self.type = player_type
        self.opponent = 2 - player_num + 1
        self.inf = float('inf')

    def make_move(self, board):
        if self.type == self.Human:
            move = int(input("Enter your move(1-6):"))
            while not board.check_legal_moves(self, move):
                print("Move is not valid")
                move = int(input("Enter your move(1-6):"))
            return move

        if self.type == self.Random:
            print(board.move_list(self))
            move = random.choice(board.move_list(self))
            return int(move + 1)

        if self.type == self.Minimax:
            move = self.minmax_move(board)
            return move

        if self.type == self.Minimax_ab:
            return

    def evaluate(self, board):
        if self.num == 1:
            return board.get_score(self) + sum(board.p1_pit)
        else:
            return board.get_score(self) + sum(board.p2_pit)



    def maxvalue(self, board, turn, level):
        if board.end_of_game():
            return turn.score_eval(board)

        score = -self.inf
        for elem in board.move_list(self):
            opponent = Player(self.opponent, self.type)
            next_board = copy.deepcopy(board)
            next_board.jump(self, elem)
            value = opponent.minvalue(next_board, turn)
            if value > score:
                score = value
        return score


    def minvalue(self, board, turn, level):
        score = self.inf
        # terminal state
        if board.end_of_game():
            return turn.score_eval(board)

        for elem in board.move_list(self):
            opponent = Player(self.opponent, self.type)
            next_board = copy.deepcopy(board)
            next_board.jump(self, elem)
            value = opponent.maxvalue(next_board, turn)
            if value < score:
                score = value
        return score

    def score_eval(self, board):
        if self.num == 1:
            if sum(board.p1_pit) + board.p1store > 24:
                return 1
            elif sum(board.p1_pit) + board.p1store == 24:
                return 0
            else:
                return -1
        else:
            if sum(board.p2_pit) + board.p2store > 24:
                return 1
            elif sum(board.p1_pit) + board.p2store == 24:
                return 0
            else:
                return -1

    def minmax_move(self, board):
        move = -1
        turn = self
        score = -self.inf
        for elem in board.move_list(self):
            if board.end_of_game():
                return -1
            new_board = copy.deepcopy(board)
            new_board.jump(self, elem)
            opponent = Player(self.opponent, self.type)
            value = opponent.minvalue(new_board, turn)
            if value > score:
                score = value
                move = elem
        return move

    def minvalue_ab(self):
        return

    def maxvalue_ab(self):
        return

    def minmax_ab_move(self):
        return