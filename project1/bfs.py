from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module.util import PriorityQueue
from pacman_module.util import manhattanDistance


def h(state):
    return 0


def g(state, path):
    return len(path) + 50 * state.getNumFood()


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
    A Pacman agent based on A* algorithm.
    """

    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
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
            self.moves = self.bfs(state)

        try:
            return self.moves.pop(0)

        except IndexError:
            return Directions.STOP

    def bfs(self, state):
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
        fringe = PriorityQueue()
        fringe.push((state, path), 0)
        closed = dict()

        while True:
            if fringe.isEmpty() == 1:
                return []  # failure

            priority, (current, path) = fringe.pop()

            if current.isWin():
                return path

            current_key = key(current)
            closed[current_key] = priority

            successors = current.generatePacmanSuccessors()
            for next_state, action in successors:

                next_path = path + [action]
                next_priority = h(next_state) + g(next_state, next_path)
                next_key = key(next_state)
                if next_key not in closed:
                    fringe.update((next_state, next_path), next_priority)
                elif next_priority < closed[next_key]:
                    closed.pop(next_key)
                    fringe.push((next_state, next_path), next_priority)
