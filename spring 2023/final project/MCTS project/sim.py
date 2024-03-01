import game
import algo
import time

from IPython.display import display, display_html, display_markdown, IFrame

from pprint import pprint

def simulate_game(uct):
    make_game_vis()

    time_limit_1 = 0.4
    time_limit_2 = 0.4

    board = game.ConnectFourBoard()
    player_1 = game.ComputerPlayer('mcts', uct, time_limit_1)
    player_2 = game.ComputerPlayer('alpha-beta', algo.alpha_beta_algo, time_limit_2)
    sim = game.Simulation(board, player_1, player_2)
    sim.run(json_visualize=True)
    time.sleep(0.3)
    print("Player", sim.board.current_player_id()," won")
    return sim.board.current_player_id()

def make_game_vis():
    frame = IFrame('vis/index.html', 490, 216)
    display(frame)

def run_final_test(uct):
    losses = 0
    for i in range(10):
        loser = simulate_game(uct)
        if loser == 0:
            losses += 1
            if losses > 1:
                lose()
                return
    win()

def win():
    display_html("""<div class="alert alert-success">
    <strong>You win!!</strong>
    </div>

<p>Stonn sits back in shock, displaying far more emotion than any Vulcan should.</p>

<p>"Cadet, it looks like your thousands of years in the mud while we Vulcans
explored the cosmos were not in vain. Congratulations."</p>

<p>The class breaks into applause! Whoops and cheers ring through the air as
Captain James T. Kirk walks into the classroom to personally award you with
the Kobayashi Maru Award For Excellence In Tactics.</p>

<p>The unwelcome interruption of your blaring alarm clock brings you back to
reality, where in the year 2200 Earth's Daylight Savings Time was finally
abolished by the United Federation of Planets.</p>""", raw=True)

def lose():
    display_html("""<div class="alert alert-failure">
    <strong>You can only lose once :(</strong>
    </div>""", raw=True)
