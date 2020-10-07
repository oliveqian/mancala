import itertools
import random


class Board:
    def __init__(self):
        self.p1_pit = [4,4,4,4,4,4]
        self.p2_pit = [4,4,4,4,4,4]
        self.p1store = 0
        self.p2store = 0

    def display(self):
        # display all relevant info
        disp = str(self.p1store)
        disp += ' - | '
        for i in self.p1_pit:
            disp += str(i) + '||  '
        disp += '\n'
        disp += '---------------------------------------------' + '\n' + '     '
        for i in self.p2_pit:
            disp += str(i) + '||  '
        disp += '| - ' + str(self.p2store)
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
                pit = self.p1_pit
                pit = pit[::-1]
                oppo_pit = self.p2_pit
                # check zero
                check_zero = any(elem == 0 for elem in pit)
                # flatten all lists so that values can be incremented
                temp_list = []
                temp_list += pit + [self.p1store] + oppo_pit
                temp_list[6 - move] = 0
                for i in range(1,pit[6-move]+1):
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




board = Board()
yq = Player(1,0)
yz = Player(2,1)

#board.host_game(yq,yz)

