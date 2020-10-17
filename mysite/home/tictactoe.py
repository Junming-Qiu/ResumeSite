import random


class TicTacToe:
    empty_board = [["-", "-", "-"],
                   ["-", "-", "-"],
                   ["-", "-", "-"]]

    first_turn = True

    def __init__(self, board, first_turn=True):
        self.empty_board = board
        self.first_turn = first_turn

    def print_board(self, board):
        print(f"\t1:\t2:\t3:")
        for row_ind, row in enumerate(board):
            print(f"{row_ind + 1}:", end="\t")
            for column in row:
                print(column, end="\t")
            print("\n")

    def check_complete(self, board):
        result = self.scan(board)
        for block in result:
            if block == ["X", "X", "X"]:
                return 2
            elif block == ["O", "O", "O"]:
                return 1

        tie = True
        for row in range(3):
            for column in range(3):
                if board[row][column] == "-":
                    tie = False

        if tie:
            return -1
        # Game continues
        return 0

    def algorithm(self, side, board):

        if self.first_turn:
            self.first_turn = False
            if board[1][1] == "-":
                return (1, 1), 0
            rand_location = random.randint(0, 2), random.randint(0, 2)
            while board[rand_location[0]][rand_location[1]] != "-":
                rand_location = random.randint(0, 2), random.randint(0, 2)
            return rand_location, 0

        status = self.scan(board)

        if side == "O":
            opponent = "X"
            win_num = 1
            lose_num = 2
        elif side == "X":
            opponent = "O"
            win_num = 2
            lose_num = 1

        horizontal = status[:3]
        vertical = status[3:6]
        diag_LR = status[6]
        diag_RL = status[7]

        for row_ind in range(3):
            for col_ind in range(3):
                if board[row_ind][col_ind] == "-":
                    board[row_ind][col_ind] = side
                    if self.check_complete(board) == (win_num or -1):
                        board[row_ind][col_ind] = "-"
                        return (row_ind, col_ind), win_num
                    board[row_ind][col_ind] = "-"

        for row_ind, row in enumerate(horizontal):
            if "-" in row:
                count = 0
                for elem in row:
                    if elem == opponent:
                        count += 1
                if count == 2:
                    col = row.index("-")
                    return (row_ind, col), 0
                count = 0

        for col_ind, col in enumerate(vertical):
            if "-" in col:
                count = 0
                for elem in col:
                    if elem == opponent:
                        count += 1
                if count == 2:
                    row = col.index("-")
                    return (row, col_ind), 0
                count = 0

        if "-" in diag_LR:
            count = 0
            for elem in diag_LR:
                if elem == opponent:
                    count += 1
            if count == 2:
                return (diag_LR.index("-"), diag_LR.index("-")), 0

        if "-" in diag_RL:
            count = 0
            for row in range(3):
                if diag_RL[row] == opponent:
                    count += 1
            if count == 2:
                return (diag_RL.index("-"), [2, 1, 0][diag_RL.index("-")]), 0

        tie_ind = []

        for row_ind in range(3):
            for col_ind in range(3):
                if board[row_ind][col_ind] == "-":
                    board[row_ind][col_ind] = side
                    if self.check_complete(board) == -1:
                        board[row_ind][col_ind] = "-"
                        return (row_ind, col_ind), 0
                    else:
                        result = self.algorithm(opponent, board)
                        if result[1] != win_num:
                            tie_ind.append([row_ind, col_ind])
                            board[row_ind][col_ind] = "-"
                        else:
                            board[row_ind][col_ind] = "-"
                            return (row_ind, col_ind), 0

        return tie_ind[random.randint(0, len(tie_ind) - 1)], 0

    def scan(self, board):
        status = []

        for row in board:
            status.append(row)

        temp = []

        for column in range(3):
            for row in board:
                temp.append(row[column])
            status.append(temp)
            temp = []

        for row, column in zip(board, [0, 1, 2]):
            temp.append(row[column])

        status.append(temp)
        temp = []

        for row, column in zip(board, [2, 1, 0]):
            temp.append(row[column])

        status.append(temp)

        return status

    def game(self, bot=1):
        row = 0
        column = 0
        curr_player = random.randint(1, 2)
        chars = ["O", "X"]

        while True:
            self.print_board(self.empty_board)
            print(f"Player {curr_player}'s turn ({chars[curr_player - 1]})")

            if curr_player != bot:
                while True:
                    row = input("What row?\n")
                    column = input("What column?\n")
                    try:
                        row = int(row)
                        column = int(column)

                        if 0 < row < 4 and 0 < column < 4:
                            break

                    except:
                        print("Please try again")
            else:
                row, column = self.algorithm(chars[curr_player - 1], self.empty_board)[0]
                row += 1
                column += 1

            if self.empty_board[row - 1][column - 1] == "-":
                self.empty_board[row - 1][column - 1] = chars[curr_player - 1]

                if self.check_complete(self.empty_board) == 1:
                    print("Player 1 wins!")
                    break
                elif self.check_complete(self.empty_board) == 2:
                    print("Player 2 wins!")
                    break
                elif self.check_complete(self.empty_board) == -1:
                    print("Tie!")
                    break

                if curr_player == 1:
                    curr_player = 2
                else:
                    curr_player = 1
            else:
                print("Space is not empty")

        self.print_board(self.empty_board)

if __name__ == "__main__":
    game = TicTacToe([["-", "-", "-"],
                   ["-", "-", "-"],
                   ["-", "-", "-"]])
    game.game()