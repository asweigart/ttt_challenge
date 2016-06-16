# Tic Tac Toe coding challenge
# Al Sweigart

'''
NOTE: Specs for this program are at https://docs.google.com/document/d/1vaCKjzBmlyihqLKGh3IDLgmTgLCLXnRr7gOHxgfKqPc/edit#

The TTT board is represented as a string of 9 characters: x, o, and (space) for each
of the 9 spaces on the board (starting top left, and going across):

x|o|
-+-+-
o| |
-+-+-
 |x|
would be encoded with the string "xo o   x "
'''

import unittest

# constants for mapping board spaces to string indexes
# Note: These are module level because they're used by the Board and TTTAI classes. Don't move them into the Board class.
TOP_LEFT = 0
TOP_MIDDLE = 1
TOP_RIGHT = 2
MIDDLE_LEFT = 3
MIDDLE_MIDDLE = 4
MIDDLE_RIGHT = 5
BOTTOM_LEFT = 6
BOTTOM_MIDDLE = 7
BOTTOM_RIGHT = 8

MOVES = [TOP_LEFT, TOP_MIDDLE, TOP_RIGHT, MIDDLE_LEFT, MIDDLE_MIDDLE, MIDDLE_RIGHT, BOTTOM_LEFT, BOTTOM_MIDDLE, BOTTOM_RIGHT]
CORNER_MOVES = [TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT]
EDGE_MOVES = [TOP_MIDDLE, MIDDLE_LEFT, MIDDLE_RIGHT, BOTTOM_MIDDLE]

MIN_TTT_INDEX = 0
MAX_TTT_INDEX = 8

X = 'x'
O = 'o'
SPACE = ' '


class TestBoard(unittest.TestCase):
    def test_basics(self):
        b = Board()
        self.assertTrue(b.is_empty())
        self.assertTrue(b.is_valid())

        b.make_move(X, TOP_LEFT)
        self.assertEqual(str(b), 'x        ')
        self.assertTrue(b.is_valid())

        b.make_move(O, TOP_MIDDLE)
        self.assertEqual(str(b), 'xo       ')
        self.assertTrue(b.is_valid())
        self.assertTrue(b, Board('xo       '))

        self.assertRaises(ValueError, b.make_move, 'bad player arg', TOP_LEFT)
        self.assertRaises(ValueError, b.make_move, X, 9999)
        self.assertRaises(ValueError, b.make_move, X, 'bad position arg')

    def test_valid_boards(self):
        self.assertRaises(ValueError, Board, 'xoxoxo')

        self.assertRaises(ValueError, Board, 'invalid marks xoxoxo')


        b = Board('xxxxxxxxx')
        self.assertFalse(b.is_valid())

        b = Board('xoxoxoxox')
        self.assertTrue(b.is_valid())

    def test_is_winner(self):
        self.assertTrue(Board('xxx      ').is_winner(X))
        self.assertTrue(Board('   xxx   ').is_winner(X))
        self.assertTrue(Board('      xxx').is_winner(X))
        self.assertTrue(Board('x  x  x  ').is_winner(X))
        self.assertTrue(Board(' x  x  x ').is_winner(X))
        self.assertTrue(Board('  x  x  x').is_winner(X))
        self.assertTrue(Board('x   x   x').is_winner(X))
        self.assertTrue(Board('  x x x  ').is_winner(X))

    def test_swap_marks(self):
        b1 = Board('xxoooxxox')
        b2 = Board('xxoooxxox')
        b2.swap_marks()
        self.assertEquals(str(b2), 'ooxxxooxo')
        b2.swap_marks()
        self.assertEquals(b1, b2)


class TestAI(unittest.TestCase):
    def test_blocks_correctly(self):
        ai = TTTAI(X)
        b = Board('oo x     ')
        self.assertTrue(ai.next_move(b) == TOP_RIGHT)

        ai = TTTAI(O)
        b = Board('xx o     ')
        self.assertTrue(ai.next_move(b) == TOP_RIGHT)

    def test_takes_winning_move(self):
        ai = TTTAI(X)
        b = Board('xx oo    ')
        self.assertTrue(ai.next_move(b) == TOP_RIGHT)

        ai = TTTAI(O)
        b = Board('oo xx    ')
        self.assertTrue(ai.next_move(b) == TOP_RIGHT)

    def test_basic(self):
        # just testing that no exceptions are raised
        ai = TTTAI(O)
        b = Board('xox oox  ')
        b.make_move(O, ai.next_move(b))

        b = Board('x        ')
        b.make_move(O, ai.next_move(b))

        b = Board('x   o    ')
        b.make_move(O, ai.next_move(b))

    def test_game(self):
        # have the ai play against itself
        b = Board()
        ai = TTTAI(O)
        for i in range(9):
            b.make_move(O, ai.next_move(b))
            b.swap_marks()
        self.assertTrue(b.is_full)



class Board:
    def __init__(self, board=None):
        if board is None:
            self._board = [' '] * 9
        else:
            self._board = list(board) # list of 9 characters. private internal use only

        if len(self._board) != 9:
            self._board = [' '] * 9
            raise ValueError('len of board argument must be 9, one char for each space')


    def is_full(self):
        '''Return False if there are no free spaces on the board.'''
        return SPACE not in self._board

    def is_empty(self):
        '''Return True if this is a blank board with only free spaces.'''
        return self._board == [' '] * 9

    def space_is_free(self, space):
        return self._board[space] == SPACE

    def is_winner(self, mark):
        b = self._board # shortcut name
        return ((b[TOP_LEFT] == mark and b[TOP_MIDDLE] == mark and b[TOP_RIGHT] == mark) or      # across top
            (b[MIDDLE_LEFT] == mark and b[MIDDLE_MIDDLE] == mark and b[MIDDLE_RIGHT] == mark) or # across middle
            (b[BOTTOM_LEFT] == mark and b[BOTTOM_MIDDLE] == mark and b[BOTTOM_RIGHT] == mark) or # across bottom
            (b[TOP_LEFT] == mark and b[MIDDLE_LEFT] == mark and b[BOTTOM_LEFT] == mark) or  # down left
            (b[TOP_MIDDLE] == mark and b[MIDDLE_MIDDLE] == mark and b[BOTTOM_MIDDLE] == mark) or # down middle
            (b[TOP_RIGHT] == mark and b[MIDDLE_RIGHT] == mark and b[BOTTOM_RIGHT] == mark) or    # down right
            (b[TOP_LEFT] == mark and b[MIDDLE_MIDDLE] == mark and b[BOTTOM_RIGHT] == mark) or  # diagonal
            (b[TOP_RIGHT] == mark and b[MIDDLE_MIDDLE] == mark and b[BOTTOM_LEFT] == mark))  # diagonal

    def xcount(self):
        return self._board.count(X)

    def ocount(self):
        return self._board.count(O)

    def swap_marks(self):
        '''Replaces X's with O's and O's with X's.'''
        for space in MOVES:
            if self._board[space] == X:
                self._board[space] = O
            elif self._board[space] == O:
                self._board[space] = X


    def is_valid(self):
        '''Return True if this is a board that could come from valid gameplay.'''

        # check for valid characters
        for c in self._board:
            if c != X and c != O and c != SPACE:
                return False

        # compare number of X's and O's for fair number of moves made by each player
        if self.xcount() > self.ocount() + 1 or self.xcount() < self.ocount() - 1:
            return False

        return True

    def make_move(self, player, space):
        if player != X and player != O:
            raise ValueError("player argument must be 'x' or 'o'")
        try:
            if int(space) < MIN_TTT_INDEX or int(space) > MAX_TTT_INDEX:
                raise ValueError("invalid space argument")
        except ValueError:
            raise ValueError("space argument must be int")

        self._board[space] = player

    def __str__(self):
        return ''.join(self._board)

    def __eq__(self, other):
        return self._board == other._board

class TTTAI:
    '''A stateless Tic Tac Toe AI. Subclasses may override the AI's strategies.

    This class plays a "perfect" strategy as detailed at https://www.quora.com/Is-there-a-way-to-never-lose-at-Tic-Tac-Toe

    This class is stateless: it does not remember previous games.'''

    def __init__(self, mark=O):
        self.mark = mark
        if mark == X:
            self.opponent_mark = O
        elif mark == O:
            self.opponent_mark = X
        else:
            raise ValueError('mark arg must be X or O constant')

    def is_valid_game_in_progress(self, board):
        '''Returns True if this board represents a validly-played game that is not yet finished,
        and where the computer can make a move.'''
        if not board.is_valid():
            return False

        if board.is_full():
            return False # board must be in progress

        if board.is_winner(X) or board.is_winner(O):
            return False # board must be playable

        if self.mark == X:
            if board.xcount() > board.ocount():
                return False # it isn't the ai's turn
        elif self.mark == O:
            if board.ocount() > board.xcount():
                return False # it isn't the ai's turn

        return True

    def next_move(self, board):
        '''Returns space to move on, given the Board object.

        Assumes a valid board is passed in.'''

        if not self.is_valid_game_in_progress(board):
            raise ValueError('board arg is not valid')

        # make winning move, if there is one
        for move in MOVES:
            b = Board(str(board)) # duplicate board to simulate on
            if not b.space_is_free(move):
                continue
            b.make_move(self.mark, move)
            if b.is_winner(self.mark):
                return move


        # block other player's winning move, if there is one
        for move in MOVES:
            b = Board(str(board)) # duplicate board to simulate on
            if not b.space_is_free(move):
                continue
            b.make_move(self.opponent_mark, move)
            if b.is_winner(self.opponent_mark):
                return move

        # moves for beginning game:

        if board.is_empty():
            # make first move on corner
            return TOP_LEFT

        b = Board() # board to simulate on
        b.make_move(self.opponent_mark, MIDDLE_MIDDLE)
        if board == b:
            # if player started in center, move on corner
            return TOP_LEFT

        for move in CORNER_MOVES:
            b = Board() # board to simulate on
            b.make_move(self.opponent_mark, move)
            if board == b:
                # if player started in center, move on corner
                return MIDDLE_MIDDLE

        # moves for middle and end game:

        # move on center, if free
        if board.space_is_free(MIDDLE_MIDDLE):
            return MIDDLE_MIDDLE

        # move on edge, if free
        for move in EDGE_MOVES:
            if board.space_is_free(move):
                return move

        # move on corner, if free
        for move in CORNER_MOVES:
            if board.space_is_free(move):
                return move




if __name__ == '__main__':
    unittest.main()
