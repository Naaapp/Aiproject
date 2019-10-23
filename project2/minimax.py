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

        final_score, final_path = self.minimax_rec(state, 0)
        return final_path

    def minimax_rec(self, current, player):

        if current.isLose():
            return -1, []

        if current.isWin():
            return 1, []

        counter = 0
        chosen_action = 0
        chosen_next_path = []

        if player == 1:
            min_score = 100000
            successors = current.generateGhostSuccessors(1)
            for next_state, action in successors:
                next_score, next_path = self.minimax_rec(next_state,
                                                         not player)
                if min_score > next_score:
                    min_score = next_score
                    chosen_action = action
                    chosen_next_path = next_path
                counter += 1
            return min_score, [chosen_action] + chosen_next_path

        if player == 0:
            max_score = 0
            successors = current.generatePacmanSuccessors()
            for next_state, action in successors:
                next_score, next_path = self.minimax_rec(next_state,
                                                         not player)
                if max_score < next_score:
                    max_score = next_score
                    chosen_action = action
                    chosen_next_path = next_path
                counter += 1
            return max_score, [chosen_action] + chosen_next_path
