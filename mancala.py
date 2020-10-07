import itertools
import random
import copy
from enum import Enum

inf = float("inf")

class Board:

    def __init__(self):
        self.p1_pit = [4,4,4,4,4,4]
        self.p2_pit = [4,4,4,4,4,4]
        self.p1store = 0
        self.p2store = 0

    def display(self):
        # display all relevant info
        disp = "%2d -" % self.p1store + "||".join(["%2d"%num for num in self.p1_pit]) + "\n"
        disp += '---------------------------------------------' + '\n'
        disp += '    ' + "||".join(["%2d"%num for num in self.p2_pit]) + " -%2d" % self.p2store
        return disp


    def check_legal_moves(self, player, move):
        # check if the move is legal or not
        if player.num == 1:
            pit = self.p1_pit
        elif player.num == 2:
            pit = self.p2_pit
        if pit[move-1] != 0 and move <= len(pit) and move >= 1:
            return True
        else:
            return False

    def move_list(self, player):
        # returns all feasible returns for a player
        if player.num == 1:
            pit = self.p1_pit
        else:
            pit = self.p2_pit
        move_list = []
        for i in range(len(pit)):
            if pit[i] != 0:
                move_list += [i]
        return move_list

    # returns whether a player has earned another move, makes the move
    def jump(self, player, move):

        if self.end_of_game():
            self.clean_board()
            return False
        else:
            if player.num == 2:
                pos = 1
                pit = self.p2_pit
                oppo_pit = self.p1_pit[::-1]
                # check 0
                check_zero = any(elem == 0 for elem in pit)
                # flatten all lists so that values can be incremented
                temp_list = []
                temp_list += pit + [self.p2store] + oppo_pit
                temp_list[move-1] = 0
                for i in range(1, pit[move-1]+1):
                    pos = int((move-1+i)%(len(temp_list)))
                    temp_list[pos] += 1
                # capture
                if check_zero:
                    zero_pos = [i for i, val in enumerate(pit) if val == 0]
                    # capture occurs
                    if pos in zero_pos:
                        if temp_list[len(temp_list)-1-pos] == 0:
                            pass
                        else:
                            temp_list[len(self.p2_pit)] += temp_list[len(temp_list)-1-pos] + 1
                            temp_list[len(temp_list)-1-pos] = 0
                            temp_list[pos] = 0
                # see if this player gets another chance
                if pos == len(self.p2_pit) and temp_list[len(temp_list) - 1 - pos] != 0:
                    play_again = True
                else:
                    play_again = False
                self.p2_pit = temp_list[0:len(self.p2_pit)]
                self.p2store = temp_list[len(self.p2_pit)]
                self.p1_pit = temp_list[len(self.p2_pit)+1:]
                self.p1_pit = self.p1_pit[::-1]
                return play_again

            else:
                pos = 1
                pit = self.p1_pit
                pit = pit[::-1]
                oppo_pit = self.p2_pit
                # check zero
                check_zero = any(elem == 0 for elem in pit)
                # flatten all lists so that values can be incremented
                temp_list = []
                temp_list += pit + [self.p1store] + oppo_pit
                temp_list[6 - move] = 0
                for i in range(1, pit[6-move]+1):
                    pos = int((6-move+i)%(len(temp_list)))
                    temp_list[pos] += 1
                    # capture
                if check_zero:
                    zero_pos = [i for i, val in enumerate(pit) if val == 0]
                    if pos in zero_pos:
                        if temp_list[len(temp_list) - 1 - pos] == 0:
                            pass
                        else:
                            temp_list[len(pit)] += temp_list[len(temp_list)-1 - pos] + 1
                            temp_list[len(temp_list) - 1 - pos] = 0
                            temp_list[pos] = 0
                # see if this player gets another chance
                if pos == len(self.p1_pit) and temp_list[len(temp_list) - 1 - pos] != 0:
                    play_again = True
                else:
                    play_again = False
                self.p1_pit = temp_list[0:len(self.p1_pit)]
                self.p1_pit = self.p1_pit[::-1]
                self.p1store = temp_list[len(self.p1_pit)]
                self.p2_pit = temp_list[len(self.p1_pit)+1:]
                return play_again

    def clean_board(self):
        self.p1store += sum(self.p1_pit)
        self.p2store += sum(self.p2_pit)
        self.p2_pit = [0*i for i in range(len(self.p1_pit))]
        self.p1_pit = [0*i for i in range(len(self.p2_pit))]

    def end_of_game(self):
        sum_1 = 0
        for i in self.p1_pit:
            sum_1 += i
            if sum_1 == 0:
                over1 = True
            else:
                over1 = False
        sum_2 = 0
        for i in self.p2_pit:
            sum_2 += i
            if sum_2 == 0:
                over2 = True
            else:
                over2 = False
        over = over1 or over2
        return over

    def get_score(self, player):
        if player.num == 1:
            return self.p1store
        else:
            return self.p2store

    def host_game(self, player1, player2):
        current_player = player1
        next_player = player2

        while not self.end_of_game():
            chance = True
            while chance:
                print('current player:', current_player.num)
                print(self.display())
                move = current_player.make_move(self)
                chance = self.jump(current_player, move)
                print(self.display())
                if self.end_of_game():
                    break
            current_player, next_player = next_player, current_player

        winner = self.judge(current_player, next_player)
        print('winner is:', winner)
        sum1 = sum(self.p1_pit)
        sum2 = sum(self.p2_pit)
        self.p1store += sum1
        self.p2store += sum2
        self.zero_up()
        print(self.display())

    def zero_up(self):
        self.p1_pit = [0 * i for i in range(len(self.p1_pit))]
        self.p2_pit = [0 * i for i in range(len(self.p2_pit))]

    def judge(self, player1, player2):
        if player1.num == 1:
            score = self.p1store + sum(self.p1_pit)
            if score > 24:
                return player1.num
            elif score < 24:
                return player2.num
            else:
                return 0
        else:
            score = self.p2store + sum(self.p2_pit)
            if score > 24:
                return player2.num
            elif score < 24:
                return player1.num
            else:
                return 0

class PlayerType(Enum):
    Human = 0
    Random = 1
    Minimax = 2
    Minimax_ab = 3

class Player:
    __slots__ = ("num", "type", "opponent","level")

    def __init__(self, player_num: int, player_type: PlayerType, level: int):
        self.num = player_num
        self.type = player_type
        self.opponent = 3 - player_num
        self.level = level


    def make_move(self, board):
        if self.type == PlayerType.Human:
            move = int(input("Enter your move(1-6):"))
            assert move > 0 and move < 7
            while not board.check_legal_moves(self, move):
                print("Move is not valid")
                move = int(input("Enter your move(1-6):"))
            return move

        if self.type == PlayerType.Random:
            print(board.move_list(self))
            move = random.choice(board.move_list(self))
            return int(move + 1)

        if self.type == PlayerType.Minimax:
            move = self.minmax_move(board, self.level)
            return int(move)

        if self.type == PlayerType.Minimax_ab:
            return

    def evaluate(self, board):
        if self.num == 1:
            return board.get_score(self) + sum(board.p1_pit)
        else:
            return board.get_score(self) + sum(board.p2_pit)



    def maxvalue(self, board, turn, level = 0):
        if board.end_of_game():
            return turn.score_eval(board)

        score = -inf
        for elem in board.move_list(self):
            if level == 0:
                return turn.score_eval(board)
            opponent = Player(self.opponent, self.type, self.level - 1)
            next_board = copy.deepcopy(board)
            next_board.jump(self, elem + 1)
            value = opponent.minvalue(next_board, turn, level - 1)
            if value > score:
                score = value
        return score

    def minvalue(self, board, turn, level = 0):
        score = inf
        # terminal state
        if board.end_of_game():
            return turn.score_eval(board)
        if level == 0:
            return (self.score_eval(board))
        for elem in board.move_list(self):
            opponent = Player(self.opponent, self.type, self.level - 1)
            next_board = copy.deepcopy(board)
            next_board.jump(self, elem+1)
            value = opponent.maxvalue(next_board, turn, level - 1)
            if value < score:
                score = value
        return score

    def score_eval(self, board):

        if self.num == 1:
            return (sum(board.p1_pit) + board.p1store) - (sum(board.p2_pit) + board.p2store)
        else:
            return (sum(board.p2_pit) + board.p1store) - (sum(board.p1_pit) + board.p1store)

    def minmax_move(self, board, level):
        move = -1
        turn = self
        score = -inf
        if board.end_of_game():
            return -1
        for elem in board.move_list(self):
            if level == 0:
                return self.score_eval(board)
            new_board = copy.deepcopy(board)
            new_board.jump(self, elem + 1)
            opponent = Player(self.opponent, self.type, self.level)
            value = opponent.minvalue(new_board, turn, level - 1)
            if value > score:
                score = value
                move = elem +1
        return move

    def minvalue_ab(self):

        return

    def maxvalue_ab(self):
        return

    def minmax_ab_move(self):
        return

board = Board()
yq = Player(1, PlayerType.Human,0)
yz = Player(2, PlayerType.Minimax,5)
board.host_game(yq, yz)

