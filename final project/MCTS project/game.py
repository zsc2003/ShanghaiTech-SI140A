import math
import copy
import re
import json
import random

from pprint import pprint


class Board(object):
    """
    This class represents an instantaneous board
    state of a game in progress. Should be able
    to be copied to keep track of board histories.
    """

    def __init__(self):
        raise NotImplemented

    def get_legal_actions(self):
        """
        Return a set of legal actions that can be
        on this current board.
        """

        raise NotImplemented

    def is_legal_action(self, action):
        """
        Returns True if the action is allowed
        to be performed on this board. False otherwise.

        params:
        action - the action to check
        """

        legal_actions = self.get_legal_actions()
        legal_actions = set([hash(act) for act in legal_actions])
        if hash(action) in legal_actions:
            return True
        return False

    def is_terminal(self):
        """
        Returns True if the state of the board
        is that of a finished game, False otherwise.
        """

        raise NotImplemented

    def reward_vector(self):
        """
        Returns the reward values for this state for each player
        as a tuple, with first player reward in 0th position,
        second player reward in 1st position, and so on.
        """

        raise NotImplemented

    def current_player_id(self):
        """
        Returns an integer id representing which player is to play next.
        """

        raise NotImplemented

    def visualize(self):
        """
        Visualize the board in some way or another.
        """

        raise NotImplemented

    def __copy__(self):
        raise NotImplemented


class ConnectFourBoard(Board):
    """
    This class represents a Connect Four board.
    Locations are accessed via a 0-indexed coordinate system.
    Coordinate (x,y) means row y of column x.
    Bottom row is row 0.
    Being a two-player game, we have Red and Black
    moves, represented as R and B respectively.
    The symbol '-' means no piece is at that coordinate.
    """
    RED = 'R'
    BLACK = 'X'
    EMPTY = '-'
    NUM_COLS = 7
    NUM_ROWS = 6

    def __init__(self, state=None, turn=None):
        """
        params:
        state - the board state represented as nested lists
        turn - which color is to play next. either RED or BLACK
        """

        if state is None:
            self.state = [[ConnectFourBoard.EMPTY for j in range(ConnectFourBoard.NUM_ROWS)] for i in range(ConnectFourBoard.NUM_COLS)]
            self.turn = ConnectFourBoard.RED
        else:
            self.state = state
            self.turn = turn

        self.last_move = None
        
    def get_legal_actions(self):
        actions = set()
        
        for col in range(len(self.state)):
            column = self.state[col]
            for row in range(len(column)):
                if column[row] == ConnectFourBoard.EMPTY:
                    actions.add(ConnectFourAction(self.turn, col, row))
                    break

        return actions

    def is_terminal(self):
        # if no move has been played, return False
        if self.last_move is None:
            return False

        # if someone has already won, return True
        if self._terminal_by_win():
            return True

        # if every slot is filled, then we've reached a terminal state
        for col in range(ConnectFourBoard.NUM_COLS):
            for row in range(ConnectFourBoard.NUM_ROWS):
                if self.state[col][row] == ConnectFourBoard.EMPTY:
                    return False

        return True

    def _terminal_by_win(self):            
        col, row = self.last_move
        color = self.state[col][row]

        # vertical
        four_in_col = self._check_seq(color, self.state[col])
        if four_in_col:
            return True
        
        # horizontal
        min_col = max(0, col-3)
        max_col = min(ConnectFourBoard.NUM_COLS-1, col+3)
        four_in_row = self._check_seq(color, [self.state[i][row] for i in range(min_col, max_col+1)])
        if four_in_row:
            return True

        # up diagonal
        coor = self.last_move
        seq = []
        valid = True
        while valid:
            new_col = coor[0] - 1
            new_row = coor[1] - 1
            if new_col < 0 or new_row < 0:
                valid = False
            else:
                coor = (new_col, new_row)
                seq.append(self.state[coor[0]][coor[1]])
        seq.reverse()
        seq.append(color)
        coor = self.last_move
        valid = True
        while valid:
            new_col = coor[0] + 1
            new_row = coor[1] + 1
            if new_col >= ConnectFourBoard.NUM_COLS or new_row >= ConnectFourBoard.NUM_ROWS:
                valid = False
            else:
                coor = (new_col, new_row)
                seq.append(self.state[coor[0]][coor[1]])
        four_in_up_diag = self._check_seq(color, seq)
        if four_in_up_diag:
            return True

        # down diagonal
        coor = self.last_move
        seq = []
        valid = True
        while valid:
            new_col = coor[0] - 1
            new_row = coor[1] + 1
            if new_col < 0 or new_row >= ConnectFourBoard.NUM_ROWS:
                valid = False
            else:
                coor = (new_col, new_row)
                seq.append(self.state[coor[0]][coor[1]])
        seq.reverse()
        seq.append(color)
        coor = self.last_move
        valid = True
        while valid:
            new_col = coor[0] + 1
            new_row = coor[1] - 1
            if new_col >= ConnectFourBoard.NUM_COLS or new_row < 0:
                valid = False
            else:
                coor = (new_col, new_row)
                seq.append(self.state[coor[0]][coor[1]])
        four_in_down_diag = self._check_seq(color, seq)
        if four_in_down_diag:
            return True
        
        return False

    def _check_seq(self, color, seq):
        length = len(seq)

        for i in range(length-3):
            four = True
            for j in range(4):
                if seq[i+j] != color:
                    four = False
                    break
            if four:
                return True
        return False

    def reward_vector(self):
        if self._terminal_by_win():
            col, row = self.last_move
            color = self.state[col][row]
        
            if color == ConnectFourBoard.RED:
                return (1,-1)
            return (-1,1)

        return (0,0)

    def current_player_id(self):
        if self.turn == ConnectFourBoard.RED:
            return 0
        return 1

    def visualize(self):
        for row in range(ConnectFourBoard.NUM_ROWS):
            row = ConnectFourBoard.NUM_ROWS - row - 1
            line = [self.state[col][row] for col in range(ConnectFourBoard.NUM_COLS)]
            line = ' '.join(line)
            print('{} '.format(row) + line)
        print('  ' + ' '.join([str(col) for col in range(ConnectFourBoard.NUM_COLS)]))

    def __copy__(self):
        new_state = copy.deepcopy(self.state)
        
        return ConnectFourBoard(new_state, self.turn)


class Action(object):
    """
    This class represents a generic action that
    can be performed on a certain board.
    Needs to be hashable in order
    to distinguish from other possible
    actions for the same board.
    """

    def __init__(self):
        raise NotImplemented

    def apply(board):
        """
        Applies the action to the board and returns a new board
        that results from it.
        Throws an error if action cannot be applied.
        """

        raise NotImplemented
        
    def __hash__(self):
        raise NotImplemented


class ConnectFourAction(Action):
    """
    This board represents an action in Connect Four.
    The actions specifies the color of the piece
    and the coordinate of where to place it.
    """

    def __init__(self, color, col, row):
        """
        params:
        color - a string from ['R', 'B'] that represents the color of the piece
        col - integer for the column
        row - integer for the row
        """

        self.color = color
        self.col = col
        self.row = row

    def apply(self, board):
        if not board.is_legal_action(self):
            raise Exception('This action is not allowed! => {}'.format(self))
            
        new_board = copy.copy(board)
        new_board.state[self.col][self.row] = self.color

        if self.color == ConnectFourBoard.RED:
            new_board.turn = ConnectFourBoard.BLACK
        else:
            new_board.turn = ConnectFourBoard.RED

        new_board.last_move = (self.col, self.row)

        return new_board

    def __hash__(self):
        return hash((self.color, self.col, self.row))

    def __repr__(self):
        return 'ConnectFourAction(color={},col={},row={})'.format(self.color,self.col,self.row)


class Player(object):
    """
    This class represents a player.
    Subclasses can be human agents
    that takes input, or programs
    that run an algorithm.
    """

    def __init__(self, name):
        self.name = name

    def choose_action(self, board):
        """
        Returns an action that the player
        wishes to perform on the board.

        params:
        board -  the current board
        """

        raise NotImplemented

    def play_action(self, action, board):
        """
        Player performs an action
        on a given board.
        Returns the new board that results from it.

        params:
        action - the action that the player wishes to perform
        board - the current board
        """

        new_board = action.apply(board)

        return new_board


class ConnectFourHumanPlayer(Player):
    """
    Human player that plays Connect Four.
    """

    INPUT_RE = re.compile(r'\s*(\d+)\s+(\d+)\s*')

    def choose_action(self, board):
        action = None
        
        while action is None:
            inp = raw_input("Enter column and row as two whitespace separated integers: ")
            m = ConnectFourHumanPlayer.INPUT_RE.match(inp)

            if m:
                col = int(m.group(1))
                row = int(m.group(2))
            else:
                print ('Incorrect format. Syntax: [COLUMN NUMBER] [ROW NUMBER]')
                continue

            if col >= 0 and col < ConnectFourBoard.NUM_COLS and row >= 0 and row < ConnectFourBoard.NUM_ROWS:
                action = ConnectFourAction(board.turn, col, row)
            else:
                print ('Coordinate out of range: 0 <= COLUMN NUMBER <= {}, 0 <= ROW NUMBER <= {}'.format(ConnectFourBoard.NUM_COLS-1, ConnectFourBoard.NUM_ROWS-1))

            if not board.is_legal_action(action):
                print ('{} is not a legal action on this board.'.format(action))
                action = None

        return action


class ComputerPlayer(Player):
    """
    A generic computer player that takes an algorithm
    as a strategy. If the algorithm is time-limited,
    as time limit can be supplied.
    """

    def __init__(self, name, algo, time_limit=None):
        Player.__init__(self, name)
        self.algo = algo
        self.time_limit = time_limit

    def choose_action(self, board):
        if self.time_limit:
            return self.algo(board, self.time_limit)
        return self.algo(board)


class Node(object):
    """
    A class that represents nodes in the MCTS tree.
    """

    def __init__(self, board, action=None, parent=None):
        """
        Create new node.

        params:
        board - Board object that this node represents.
        action - Incoming action that created this node. None for root.
        parent - Parent node. None for root.
        """

        self.board = board
        self.action = action
        self.parent = parent
        self.children = [] # children nodes
        self.num_visits = 0 # number of times node has been visited
        self.q = 0.0 # simulation reward
        
    def get_action(self):
        """
        Return associated incoming action.
        """
        
        return self.action

    def get_board(self):
        """
        Returns associated board state.
        """

        return self.board
        
    def get_parent(self):
        """
        Return parent node.
        """

        return self.parent

    def get_children(self):
        """
        Return children nodes.
        """
        
        return self.children

    def add_child(self, child):
        """
        Adds a new child node to the nodes visited children.
        """

        self.children.append(child)

    def get_num_visits(self):
        """
        Return number of time this node has been visited.
        """

        return self.num_visits

    def get_player_id(self):
        return self.board.current_player_id()

    def q_value(self):
        """
        Return the simulation Q value reward.
        """

        return self.q

    def visit(self):
        """
        Increment visit counter.
        """

        self.num_visits += 1

    def is_fully_expanded(self):
        """
        Returns True if the node has
        all possible children in self.children,
        False otherwise.
        """
        
        possible_actions = set([hash(action) for action in self.board.get_legal_actions()])
        taken_actions = set([hash(child.action) for child in self.children])
        untaken_actions = possible_actions ^ taken_actions
        
        return len(untaken_actions) == 0

    def value(self, c):
        """
        Return the UCT heuristic value of the node.

        params:
        c - exploration value. Larger values encourage exploration of tree.
        """

        exploitation_value = self.q / self.num_visits
        exploration_value = c * math.sqrt(2 * math.log(self.parent.num_visits) / self.num_visits)
        
        return exploitation_value + exploration_value


class Simulation(object):
    """
    This class represents and simulates a game
    between two players.
    """

    def __init__(self, board, *players):
        self.init_board = board
        self.board = board
        self.players = players
        self.history = []

    def run(self, visualize=False, json_visualize=False):
        self.game_id = str(random.randint(0,3133337))

        while not self.board.is_terminal():
            if visualize:
                self.board.visualize()
            if json_visualize:
                self.write_visualization_json()
            player_id = self.board.current_player_id()
            player = self.players[player_id]
            action = player.choose_action(self.board)
            self.board = player.play_action(action, self.board)
            self.history.append((player_id, action))

        if json_visualize:
            self.write_visualization_json()

    def write_visualization_json(self):
        json_str = json.dumps({
            "board": self.board.state,
            "finished": self.board.is_terminal(),
            "player": self.board.current_player_id(),
            "gameId": self.game_id
        })
        out_file = open("vis/game-state.json", "w")
        out_file.write(json_str)
        out_file.close()
