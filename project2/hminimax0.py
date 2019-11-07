from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module.util import manhattanDistance
import math
import random


class PacmanAgent(Agent):
    """
    A Pacman agent based on Depth-First-Search.
    """
    ls_score = []
    smart_depth = 10
    final_score = 0
    bool = False
    cpt = 1

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
            self.moves = self.minimax(state)

        try:
            return self.moves.pop(0)

        except IndexError:
            return Directions.STOP

    def minimax(self, state):
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
        closed = set()

        if self.key(state) not in self.state_list:
            self.state_list.add(self.key(state))
            self.final_score, final_path = self.minimax_rec(
                                            state, 0, 0, self.smart_depth,
                                            closed, self.food_score(state))
            self.ls_score.append(self.final_score)
        else:
            print('random path')
            paths = state.getLegalActions(0)
            final_path = [random.choice(paths)]

        # if self.bool:
        #     self.cpt += 1
        #     print("old final score: ", self.ls_score[-2], self.smart_depth)
        #
        #     if self.ls_score[-2] == self.final_score:
        #         # if self.smart_depth < 3:
        #         #     self.smart_depth = 4
        #         # elif self.smart_depth < 5:
        #         #     self.smart_depth = 5
        #         self.smart_depth += 1
        #
        #     elif self.ls_score[-2] > self.final_score:
        #         # self.smart_depth = 6 - self.smart_depth
        #         self.smart_depth = 6 - self.smart_depth
        #
        #     else:
        #         # if self.smart_depth < 5:
        #         #     self.smart_depth -= 1
        #         # elif self.smart_depth < 7:
        #         #     self.smart_depth -= 2
        #         self.smart_depth -= 1
        #
        # self.bool = True
        print(final_path)
        return final_path

    def minimax_rec(self, current, player, depth, l_depth, closed,
                    prev_food_score):

        if current.isLose():
            return current.getScore(), []

        if current.isWin():
            return current.getScore(), []

        current_food_score = self.food_score(current)
        # if current_food_score < prev_food_score:
        #     l_depth += 1
        # print('ldepth', l_depth)
        # min distance to food + distance to ghost + num of food
        if depth >= l_depth:
            food_list = current.getFood().asList()
            current_position = current.getPacmanPosition()
            current_ghost_position = current.getGhostPosition(1)

            dist_pacman_food = math.inf
            for food_position in food_list:
                dist_pacman_food = min(dist_pacman_food, (
                    manhattanDistance(current_position, food_position)))

            dist_ghost_food = math.inf
            for food_position in food_list:
                dist_ghost_food = min(dist_ghost_food, (
                    manhattanDistance(current_ghost_position, food_position)))

            dist_pacman_ghost = manhattanDistance(current_position,
                                                  current_ghost_position)
            # check_direction = last_action != current.getGhostDirection(1)
            # print("dist_ghost: ", dist_ghost)
            # print("dist_food :", dist)
            # print("current_position :", current.getNumFood())
            # print(check_direction)

            result = dist_pacman_ghost - dist_pacman_food

            # print("result :",result)
            return result, []

        current_key = self.key(current)

        if current_key in closed:
            return 0, []
        else:
            closed.add(current_key)
            chosen_action = 0
            chosen_next_path = []

            if player == 1:
                min_score = math.inf
                successors = current.generateGhostSuccessors(1)
                for next_state, action in successors:
                    # print(self.key(next_state), action, depth + 1)
                    next_score, next_path = self.minimax_rec(
                        next_state, not player, depth + 1, l_depth,
                        closed.copy(), prev_food_score)
                    if min_score > next_score:
                        min_score = next_score
                        chosen_next_path = next_path
                return min_score, chosen_next_path

            if player == 0:
                max_score = -math.inf
                successors = current.generatePacmanSuccessors()
                for next_state, action in successors:
                    # print(self.key(next_state), action, depth + 1)
                    next_score, next_path = self.minimax_rec(
                        next_state, not player, depth + 1, l_depth,
                        closed.copy(), current_food_score)
                    if max_score < next_score:
                        max_score = next_score
                        chosen_action = action
                        chosen_next_path = next_path
                return max_score, [chosen_action] + chosen_next_path

    def food_score(self, state):
        # food_list = state.getFood().asList()
        # current_position = state.getPacmanPosition()
        # dist_pacman_food = 0
        # for food_position in food_list:
        #     dist_pacman_food += manhattanDistance(current_position,
        #                                           food_position) ^ 2
        return state.getNumFood()
