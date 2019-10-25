from pacman_module.game import Agent
from pacman_module.pacman import Directions


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
        self.closed = set()
        final_score, final_path = self.minimax_rec(state, 0, 0)

        print(final_path)
        return final_path

    def minimax_rec(self, current, player, depth):
        #
        # print(current.getGhostPosition(1))
        # print(current.getPacmanPosition())
        # print("/")

        if current.isLose():
            print("loose", depth)
            return -30, []

        if current.isWin():
            print(depth)
            return 30 - depth, []

        current_key = self.key(current)

        if current_key in self.closed:
            return 0, []
        else:
            self.closed.add(current_key)
            chosen_action = 0
            chosen_next_path = []

            if player == 1:
                min_score = 100000
                successors = current.generateGhostSuccessors(1)
                for next_state, action in successors:
                    next_score, next_path = self.minimax_rec(
                        next_state, not player, depth)
                    if min_score > next_score:
                        min_score = next_score
                        chosen_next_path = next_path
                # print("min ", min_score, depth )
                return min_score, chosen_next_path

            if player == 0:
                max_score = 0
                successors = current.generatePacmanSuccessors()
                for next_state, action in successors:
                    next_score, next_path = self.minimax_rec(
                        next_state, not player, depth + 1)
                    if max_score < next_score:
                        max_score = next_score
                        chosen_action = action
                        chosen_next_path = next_path
                # print("max ", max_score, depth)
                return max_score, [chosen_action] + chosen_next_path
