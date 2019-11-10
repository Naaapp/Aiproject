from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module.util import manhattanDistance
import math


class PacmanAgent(Agent):
    """
    A Pacman agent based on Minimax.
    """

    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        super().__init__()
        self.args = args
        self.init_food_list = []
        self.moves = []

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
            state.getGhostPosition(1))

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
            self.moves = self.minimax(state)

        try:
            return self.moves.pop(0)

        except IndexError:
            return Directions.STOP

    def minimax(self, state):
        """
        Given a pacman game state,
        returns a list of legal moves to solve the search layout using
        the minimax algorithm
        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.
        Return:
        -------
        - A list of legal moves as defined in `game.Directions`.
        """

        self.init_food_list = state.getFood().asList()
        closed = set()

        # first step necessary to have different path depending
        # on the type of ghost. We go to the position the most distant of the
        # ghost . The reaction of the ghost will be different
        # depending of it type (smarty and dumby / greedy)
        if state.getGhostDirection(1) == 'Stop':
            successors = state.generatePacmanSuccessors()
            max_dist = -math.inf
            chosen_action = 'Stop'
            for next_state, action in successors:
                dist = manhattanDistance(
                    state.getGhostPosition(1), state.getPacmanPosition())
                if max_dist < dist:
                    max_dist = dist
                    chosen_action = action
            return [chosen_action]

        final_score, final_path = self.minimax_rec(state, 0, 0, closed)

        return final_path

    def minimax_rec(self, current, player, depth, closed):
        """
        Recursive function which implements the minimax algorithm
        Arguments:
        ----------
        - 'current' :       the current game state.
        - 'player'  :       boolean value, 0 if pacman turn, 1 if ghost turn
        - 'depth'   :       current depth of the tree
        - 'closed'  :       set of states already visited in the tree branch

        Return:
        -------
        - 'result'  :   resulting score
        - 'path'    :   resulting path
        """
        current_key = self.key(current)
        # If already visited, stop the recursion and return
        # the worst score possible
        if current_key in closed:
            return -math.inf, []
        closed.add(current_key)

        # Loose case
        if current.isLose():
            return current.getScore(), []

        # Win case
        if current.isWin():
            return current.getScore(), []

        # Recursive case
        chosen_next_path = []

        # It is the turn of ghost, generate it successors and call
        # recursively minimax_rec for all of them. Return the best score
        # with the corresponding worst path
        if player == 1:
            min_score = math.inf
            successors = current.generateGhostSuccessors(1)
            for next_state, action in successors:
                next_score, next_path = self.minimax_rec(
                    next_state, not player, depth, closed.copy())
                if min_score > next_score:
                    min_score = next_score
                    chosen_next_path = next_path
            return min_score, chosen_next_path

        # It is the turn of pacman, generate it successors and call
        # recursively minimax_rec for all of them. Return the best score
        # with the corresponding best path
        if player == 0:
            max_score = -math.inf
            chosen_action = 'Stop'
            successors = current.generatePacmanSuccessors()
            for next_state, action in successors:
                next_score, next_path = self.minimax_rec(
                    next_state, not player, depth + 1, closed.copy())
                if max_score < next_score:
                    max_score = next_score
                    chosen_action = action
                    chosen_next_path = next_path
            return max_score, [chosen_action] + chosen_next_path
