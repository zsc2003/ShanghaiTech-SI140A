import random
import alpha_beta


def random_algo(board):
    return random.choice(list(board.get_legal_actions()))


def alpha_beta_algo(board, time_limit):
    return alpha_beta.search(board, time_limit)
