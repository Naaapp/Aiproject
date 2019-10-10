from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module.util import PriorityQueue
from pacman_module.util import manhattanDistance


def h(state):
    min_dist = 100000
    food_list = state.getFood().asList()
    if len(food_list) == 0:
        return 0
    current_position = state.getPacmanPosition()
    for food_position in food_list:
        min_dist = min(min_dist, manhattanDistance(current_position, food_position))
    return min_dist


def g(backward_cost, num_food):
    return backward_cost + num_food


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
        super().__init__()
        self.args = args
        self.moves = []
        self.food_list = []
        self.init_food_list = []

    def key(self, state):
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
        return tuple(state.getPacmanPosition()) + tuple(
            [(1 if state.hasFood(
                food[0], food[1]) else 0) for food in self.init_food_list])

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
        self.init_food_list = state.getFood().asList()
        fringe = PriorityQueue()
        fringe.push((state, [], 0), 0)
        closed = set()

        while True:
            if fringe.isEmpty() == 1:
                return []  # failure

            priority, (current, path, backward_cost) = fringe.pop()

            if current.isWin():
                return path

            current_key = self.key(current)

            if current_key not in closed:
                closed.add(current_key)

                for next_state, action in current.generatePacmanSuccessors():
                    next_key = self.key(next_state)
                    if next_key not in closed:
                        next_path = path + [action]
                        next_backward_cost = g(backward_cost, next_state.getNumFood())
                        next_priority = h(next_state) + next_backward_cost
                        fringe.push((next_state, next_path, next_backward_cost), next_priority)
