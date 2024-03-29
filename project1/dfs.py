"""
Author : one of the TAs, just after
submitting an important journal manuscript.
I am so tired that I might have screwed up the following DFS implementation.
My fellow TAs are expected to fix all the errors
while I'm taking a very long nap.
I trust them but you should also, student,
check the following code against a possible *unique* error.
"""

from pacman_module.game import Agent
from pacman_module.pacman import Directions


def key(state):
    """
    Returns a key that uniquely identifies a Pacman game state.
    Arguments:
    ----------
    - `state`: the current game state. See FAQ and class
               `pacman.GameState`.
    Return:
    -------
    - A hashable key object that uniquely identifies a Pacman game state.
    """
    return state.getPacmanPosition()


class PacmanAgent(Agent):
    """
    A Pacman agent based on Depth-First-Search.
    """

    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        super().__init__()
        self.args = args
        self.moves = []

    def get_action(self, state):
        """
        Given a pacman game state, returns a legal move.
        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.
        Return:
        -------
        - A legal move as defined in `game.Directions`.
        """

        if not self.moves:
            self.moves = dfs(state)

        try:
            return self.moves.pop(0)

        except IndexError:
            return Directions.STOP


def dfs(state):
    """
    Given a pacman game state,
    returns a list of legal moves to solve the search layout.
    Arguments:
    ----------
    - `state`: the current game state. See FAQ and class
               `pacman.GameState`.
    Return:
    -------
    - A list of legal moves as defined in `game.Directions`.
    """
    path = []
    fringe = [(state, path)]
    closed = set()
    prev_n_food = 0

    while True:
        if len(fringe) == 0:
            return []  # failure

        current, path = fringe.pop()

        if current.isWin():
            return path

        current_key = key(current)

        n_food = current.getNumFood()

        if n_food < prev_n_food:
            closed.clear()

        if current_key not in closed:
            closed.add(current_key)

            for next_state, action in current.generatePacmanSuccessors():
                fringe.append((next_state, path + [action]))

        prev_n_food = n_food
