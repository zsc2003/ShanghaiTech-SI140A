import copy
import game
import time
from pprint import pprint

INFINITY = 9001 * 9001

def search(board, time_budget):
    # Initial queue of actions to investigate
    # (board, move to take if you want to see this board)
    # Really bad because making it better will need recursion and a heuristic
    deadline = time.time() + time_budget

    chosen_action = None
    player_color = board.turn

    for depth in range(2,24,2):
        _, new_chosen_action = alpha_beta(player_color, board, depth, -INFINITY, INFINITY, True, deadline)
        if not chosen_action or (new_chosen_action and time.time() <= deadline):
            chosen_action = new_chosen_action
    return chosen_action

def get_run_len(state, start_col, start_row, d_col, d_row):
    run_len = 0
    col = start_col + d_col
    row = start_row + d_row
    run_color = None
    while col >= 0 and row >= 0 and col < len(state) and row < len(state[col]):
        if state[col][row] == game.ConnectFourBoard.EMPTY:
            break
        if not run_color:
            run_color = state[col][row]
        if run_color != state[col][row]:
            break
        run_len += 1
        col += d_col
        row += d_row
    return (run_len, run_color)

def get_score(player_color, run_len, run_color, supported):
    # Are we happy to see this run?
    player_mod = 1
    if player_color != run_color:
        player_mod = -1
    # Prefer longer runs
    len_mods = [0, 1, 16, 160]
    # Saturate at 3 because 3 is already good enough to win on the next turn
    if run_len > 3:
        run_len = 3

    # Being support means we (or them) can place immediately
    supported_mod = 1
    if supported:
        supported_mod = 9

    return player_mod * len_mods[run_len] * supported_mod

def heuristic(player_color, board, debug=False):
    score = 0

    if board.is_terminal():
        if board.turn == player_color:
            return -9001
        else:
            return 9001

    debug_state = copy.deepcopy(board.state)

    for col in range(len(board.state)):
        for row in range(len(board.state[col])):
            blank = board.state[col][row]
            if blank != game.ConnectFourBoard.EMPTY:
                continue
            down_len, down_color = get_run_len(board.state, col, row, 0, -1)
            left_len, left_color = get_run_len(board.state, col, row, -1, 0)
            right_len, right_color = get_run_len(board.state, col, row, 1, 0)
            down_left_len, down_left_color = get_run_len(board.state, col, row, -1, -1)
            down_right_len, down_right_color = get_run_len(board.state, col, row, 1, -1)
            up_left_len, up_left_color = get_run_len(board.state, col, row, -1, 1)
            up_right_len, up_right_color = get_run_len(board.state, col, row, 1, 1)


            supported = row == 0 or down_len > 0

            cell_score = get_score(player_color, down_len, down_color, supported)
            # Note that this does not ignore situations where the board looks
            # like RR-BB where even though we have a free move we could never
            # win from it

            # If we get a split like RR-R weight it as high as RRR-
            if left_color == right_color:
                cell_score += get_score(player_color, left_len + right_len, left_color, supported)
            else:
                cell_score += get_score(player_color, left_len, left_color, supported)
                cell_score += get_score(player_color, right_len, right_color, supported)

            if down_left_color == up_right_color:
                cell_score += get_score(player_color, down_left_len + up_right_len, down_left_color, supported)
            else:
                cell_score += get_score(player_color, down_left_len, down_left_color, supported)
                cell_score += get_score(player_color, up_right_len, up_right_color, supported)

            if down_right_color == up_left_color:
                cell_score += get_score(player_color, down_right_len + up_left_len, down_right_color, supported)
            else:
                cell_score += get_score(player_color, down_right_len, down_right_color, supported)
                cell_score += get_score(player_color, up_left_len, up_left_color, supported)
            debug_state[col][row] = cell_score
            score += cell_score

    if debug:
        pprint(debug_state)

    return score

# Time to steal from wikipedia
# From https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
def alpha_beta(player_color, board, depth, alpha, beta, is_player, deadline):
    actions = board.get_legal_actions()

    if depth == 0 or len(actions) == 0 or time.time() > deadline:
        return (heuristic(player_color, board), None)

    if is_player:
        best_result = (-INFINITY, None)
        for action in actions:
            new_board = action.apply(board)
            new_value, _ = alpha_beta(player_color, new_board, depth - 1, alpha, beta, False, deadline)

            if new_value > best_result[0]:
                best_result = (new_value, action)
            alpha = max(alpha, new_value)
            # if beta <= alpha:
            #     break
        return best_result
    else:
        worst_result = (INFINITY, None)
        for action in actions:
            new_board = action.apply(board)
            new_value, _ = alpha_beta(player_color, new_board, depth - 1, alpha, beta, True, deadline)

            if new_value < worst_result[0]:
                worst_result = (new_value, action)
            beta = min(beta, new_value)
            # if beta <= alpha:
            #     break
        return worst_result
