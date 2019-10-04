from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module.util import PriorityQueue
from pacman_module.util import manhattanDistance


def h(state):
    min_dist = 100000
    current_food = state.getFood().asList()
    if len(current_food) == 0:
        return 0
    current_position = state.getPacmanPosition()
    # for food_position in current_food:
    #     min_dist = min(min_dist, manhattanDistance(current_position, food_position))
    # return min_dist

    result = 0
    for food_position in current_food:
        result = result + manhattanDistance(current_position, food_position) ^ 2
    return result / len(current_food)


def g(state, path):
    return len(path) / 2 + 50 * state.getNumFood()


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
            self.moves = self.astar(state)

        try:
            return self.moves.pop(0)

        except IndexError:
            return Directions.STOP

    def astar(self, state):
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
