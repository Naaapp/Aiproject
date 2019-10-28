from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module.util import manhattanDistance
import math

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
            state.getGhostPosition(1))+tuple([(1 if state.hasFood(food[0], food[1]) else 0) for food in self.init_food_list])


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
        final_score, final_path = self.minimax_rec(state, 0, 0, closed)

        print(final_path)
        return final_path

    def minimax_rec(self, current, player, depth, closed):

        if current.isLose():
            return current.getScore(), []

        if current.isWin():
            return current.getScore(), []

        if depth >= 1:
            food_list = current.getFood().asList()
            if len(food_list) == 0:
                return 0
            current_position = current.getPacmanPosition()
            result = math.inf
            for food_position in food_list:
                result = min(result,(manhattanDistance(current_position, food_position)))
            result_gost = manhattanDistance(current_position, current.getGhostPosition(1))
            print("result_gost: ",result_gost)
            print("result :",result)
            print("current_position :",current.getNumFood())
            if current.getNumFood()!= 0:
                result=1/result+1/current.getNumFood()+result_gost
            else:
                result=1/result+1/result_gost
            #print("result :",result)
            return result,[]


        current_key = self.key(current)

        if current_key in closed:
            return 0, []
        else:
            closed.add(current_key)
            chosen_action = 0
            chosen_next_path = []

            if player == 1:
                min_score = 100000
                successors = current.generateGhostSuccessors(1)
                for next_state, action in successors:
                    print(self.key(next_state),action,depth + 1)
                    next_score, next_path = self.minimax_rec(
                        next_state, not player, depth, closed.copy())
                    if min_score > next_score:
                        min_score = next_score
                        chosen_next_path = next_path
                return min_score, chosen_next_path

            if player == 0:
                max_score = 0
                successors = current.generatePacmanSuccessors()
                for next_state, action in successors:
                    print(self.key(next_state),action,depth + 1)
                    next_score, next_path = self.minimax_rec(
                        next_state, not player, depth + 1, closed.copy())
                    if max_score < next_score:
                        max_score = next_score
                        chosen_action = action
                        chosen_next_path = next_path
                return max_score, [chosen_action] + chosen_next_path
