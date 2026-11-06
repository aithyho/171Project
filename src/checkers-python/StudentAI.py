from random import randint
from BoardClasses import Move
from BoardClasses import Board
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
class StudentAI():

    # PART 1: Initialize the AI and the checkers board
    def __init__(self, col, row, p):
        self.col = col
        self.row = row
        self.p = p

        # Create and initialize the checkers board
        self.board = Board(col, row, p)
        self.board.initialize_game()

        # Keep track of our color and the opponent's color
        # Player 1 is the opponent of Player 2, and vice versa
        self.color = 2
        self.opponent = {1: 2, 2: 1}


    # PART 2: Choose the best move
    # This function is called whenever it is our 'StudentAI' turn
    def get_move(self, move):

        # STEP 1: Update our board with the opponent's last move
        if len(move) != 0:
            self.board.make_move(
                move,
                self.opponent[self.color]
            )
        else:
            # An empty move means our StudentAI plays first
            self.color = 1

        # STEP 2: Get all legal moves for our StudentAI
        moves = self.board.get_all_possible_moves(self.color)

        # Track the best move and its score
        best_move = None
        best_score = float('-inf')

        # STEP 3: Examine every possible move
        for group in moves:
            for candidate in group:

                # Start each candidate with a score of zero
                score = 0

                # Get the first two positions of this move
                start = candidate.seq[0]
                end = candidate.seq[1]

                # Calculate how many rows the checker travels
                row_difference = abs(end[0] - start[0])

                # STEP 4: Reward capturing opponent pieces
                # A jump travels two rows diagonally
                if row_difference == 2:

                    # Number of captures equals number of jumps
                    captures = len(candidate.seq) - 1

                    # Reward 10 points per captured piece
                    score = 10 * captures

                # STEP 5: Temporarily simulate our candidate move
                self.board.make_move(candidate, self.color)

                # Find all legal responses available to the opponent
                opponent_moves = self.board.get_all_possible_moves(
                    self.opponent[self.color]
                )

                # STEP 6: Determine the greatest number of pieces
                # the opponent could capture in one response
                max_opponent_captures = 0

                for opponent_group in opponent_moves:
                    for opponent_move in opponent_group:

                        # Get the first two positions
                        opponent_start = opponent_move.seq[0]
                        opponent_end = opponent_move.seq[1]

                        # Calculate the opponent's row difference
                        opponent_row_difference = abs(
                            opponent_end[0] - opponent_start[0]
                        )

                        # Determine how many pieces are captured
                        if opponent_row_difference == 2:
                            opponent_captures = len(opponent_move.seq) - 1
                        else:
                            opponent_captures = 0

                        # Remember the largest possible capture
                        if opponent_captures > max_opponent_captures:
                            max_opponent_captures = opponent_captures

                # STEP 7: Restore the original board
                # This lets us evaluate the next candidate fairly
                self.board.undo()

                # STEP 8: Penalize dangerous moves
                # Subtract 15 points for every piece the opponent
                # could capture in their strongest immediate response
                score = score - 15 * max_opponent_captures

                # STEP 9: Remember the highest-scoring candidate
                if score > best_score:
                    best_score = score
                    best_move = candidate

        # STEP 10: Select the highest-scoring move
        move = best_move

        # ADDED (STEP 11): Apply our chosen move to our own internal board.
        self.board.make_move(move, self.color)

        # ADDED (STEP 12): Return the chosen move to the game runner.
        # Previously get_move() returned None, which would crash the game.
        return move