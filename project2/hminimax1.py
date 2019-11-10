from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module.util import manhattanDistance
import math
import random


class PacmanAgent(Agent):
    """
    A Pacman agent based on Hminimax algorithm (Second Best version).
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
        self.state_list = set()
        self.init_number_food = 0
        self.chosen_depth = 4

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
            state.getGhostPosition(1)) + tuple(
            [(1 if state.hasFood(food[0], food[1]) else 0) for food in
             self.init_food_list])

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
            self.moves = self.hminimax(state)
        try:
            return self.moves.pop(0)

        except IndexError:
            return Directions.STOP

    def hminimax(self, state):
        """
        Given a pacman game state,
        returns a list of legal moves to solve the search layout
        using the hminimax algorithm.
        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.
        Return:
        -------
        - A list of legal moves as defined in `game.Directions`.
        """
        # Initialization
        self.init_food_list = state.getFood().asList()
        self.init_number_food = state.getNumFood()
        closed = set()

        # If the initial state as already been an initial state previously,
        # it is worthless to use hminimax, it will send the same path.
        # So we unblock the situation by doing one random step in a legal
        # position. This situation does not occur with these layouts.
        if self.key(state) not in self.state_list:
            self.state_list.add(self.key(state))
            final_score, final_path = self.hminimax_rec(
                state, 0, 0, self.chosen_depth,
                closed, state.getPacmanPosition())
        else:
            paths = state.getLegalActions(0)
            final_path = [random.choice(paths)]

        return final_path

    def hminimax_rec(self, current, player, depth, l_depth, closed,
                     init_position):
        """
        Recursive function which implements the hminimax algorithm
        Arguments:
        ----------
        - 'current' :       the current game state.
        - 'player'  :       boolean value, 0 if pacman turn, 1 if ghost turn
        - 'depth'   :       current depth of the tree
        - 'ldepth'  :       limit of depth of the tree
        - 'closed'  :       set of states already visited in the tree branch
        - 'init_position' : initial position of pacman

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

        # Cutoff case
        if depth >= self.chosen_depth:

            # All the simple calculations needed to compute the result
            #   -min dist between pacman and foods
            #   -mean dist between pacman and foods
            #   -min dist between the initial position of pacman and foods
            #   -min dist between ghost and foods
            #   -dist between pacman and ghost
            food_list = current.getFood().asList()
            current_position = current.getPacmanPosition()
            current_ghost_position = current.getGhostPosition(1)
            dist_pacman_food = math.inf
            init_dist_pacman_food = math.inf
            mean_dist_pacman_food = 0
            dist_ghost_food = 0
            n_same_dist_food = 1
            for food_position in food_list:
                dist = manhattanDistance(current_position, food_position)
                if dist_pacman_food > dist:
                    dist_pacman_food = dist
                    n_same_dist_food = 1
                elif dist_pacman_food == dist:
                    n_same_dist_food += 1
                init_dist_pacman_food = min(init_dist_pacman_food, (
                    manhattanDistance(init_position, food_position)))
                mean_dist_pacman_food += (
                    manhattanDistance(current_position, food_position))
                dist_ghost_food = min(dist_ghost_food, (
                    manhattanDistance(current_ghost_position, food_position)))

            mean_dist_pacman_food = mean_dist_pacman_food / len(food_list)
            dist_pacman_ghost = manhattanDistance(current_position,
                                                  current_ghost_position)

            # Compute the resulting score using the values computed
            result = 0
            if current.getNumFood() == 1:
                if dist_pacman_food <= dist_ghost_food:
                    result = 4 - dist_pacman_food
                elif dist_pacman_food > dist_ghost_food:
                    result = 1
                result += dist_pacman_ghost
                result += (init_dist_pacman_food - dist_pacman_food) * 5
            else:
                result = - mean_dist_pacman_food
                result += - dist_pacman_food + n_same_dist_food
                result += (self.init_number_food - current.getNumFood()) * 10

            return result, []

        # Recursive case
        chosen_next_path = []

        # It is the turn of ghost, generate it successors and call
        # recursively hminimax_rec for all of them. Return the best score
        # with the corresponding worst path
        if player == 1:
            min_score = math.inf
            successors = current.generateGhostSuccessors(1)
            for next_state, action in successors:
                next_score, next_path = self.hminimax_rec(
                    next_state, not player, depth + 1, l_depth,
                    closed.copy(), init_position)
                if min_score > next_score:
                    min_score = next_score
                    chosen_next_path = next_path
            return min_score, chosen_next_path

        # It is the turn of pacman, generate it successors and call
        # recursively hminimax_rec for all of them. Return the best score
        # with the corresponding best path
        if player == 0:
            max_score = -math.inf
            chosen_action = 'Stop'
            successors = current.generatePacmanSuccessors()
            for next_state, action in successors:
                next_score, next_path = self.hminimax_rec(
                    next_state, not player, depth + 1, l_depth,
                    closed.copy(), init_position)
                if max_score < next_score:
                    max_score = next_score
                    chosen_action = action
                    chosen_next_path = next_path
            return max_score, [chosen_action] + chosen_next_path
