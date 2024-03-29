# Complete this class for all parts of the project

from pacman_module.game import Agent
import numpy as np
from pacman_module import util


class BeliefStateAgent(Agent):
    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args
        """
            Variables to use in 'update_belief_state' method.
            Initialization occurs in 'get_action' method.
        """
        # Current list of belief states over ghost positions
        self.beliefGhostStates = None

        # Grid of walls (assigned with 'state.getWalls()' method)
        self.walls = None

        # Hyper-parameters
        self.ghost_type = self.args.ghostagent
        self.sensor_variance = self.args.sensorvariance
        self.counter = 0
        self.metrics = 0

    def update_belief_state(self, evidences, pacman_position):
        """
        Given a list of (noised) distances from pacman to ghosts,
        returns a list of belief states about ghosts positions

        Arguments:
        ----------
        - `evidences`: list of distances between
          pacman and ghosts at state x_{t}
          where 't' is the current time step
        - `pacman_position`: 2D coordinates position
          of pacman at state x_{t}
          where 't' is the current time step

        Return:
        -------
        - A list of Z belief states at state x_{t}
          as N*M numpy mass probability matrices
          where N and M are respectively width and height
          of the maze layout and Z is the number of ghosts.

        N.B. : [0,0] is the bottom left corner of the maze
        """

        beliefStates = self.beliefGhostStates

        # XXX: Your code here

        width = 21
        height = 12

        # Variable in which we will accumulate probabilities
        beliefStates = np.zeros((len(evidences), width, height))

        # Transition step
        for k in range(len(evidences)):
            for i in range(1, width - 1):
                for j in range(1, height - 1):
                    # For each no wall position, we add to the neighbour
                    # the probabilities of being in the position * the
                    # probability to go to a neighbour,
                    # for each neighbour
                    if self.walls[i][j] is False:
                        j_p = pacman_position[1]
                        i_p = pacman_position[0]
                        current_prob = self.beliefGhostStates[k][i][j]
                        current_prob_norm = 0
                        c = 1
                        if self.ghost_type == 'afraid':
                            c = 2
                        if self.ghost_type == 'scared':
                            c = 2 ** 3

                        norm = self.compute_norm(i, j, i_p, j_p, c)
                        if norm > 0:
                            current_prob_norm = current_prob / norm

                        self.compute_belief_states(beliefStates, k, i, j, i_p,
                                                   j_p, current_prob_norm,
                                                   c)
            # If first step, the sum of probabilities is not 0, so we normalize
            if self.counter is 0:
                beliefStates[k] = beliefStates[k] * 1 / sum(
                    sum(beliefStates[k]))

        # Update step
        for k in range(len(evidences)):
            for i in range(1, width - 1):
                for j in range(1, height - 1):
                    # For each no wall position, we multiply the probability by
                    # a factor inversely proportional to the diff between
                    # the current distance to pacman and the noisy distance
                    # between pacman and ghost
                    if self.walls[i][j] is False:
                        current_dist = util.manhattanDistance(pacman_position,
                                                              (i, j))
                        dist_diff = current_dist - evidences[k]
                        prob = 1 - abs(dist_diff) / (width + height)
                        if prob < 0:
                            prob = 0.0001

                        beliefStates[k][i][j] = beliefStates[k][i][j] * prob

            # We normalize the probabilities
            beliefStates[k] = beliefStates[k] * 1 / sum(sum(beliefStates[k]))

        # XXX: End of your code

        self.beliefGhostStates = beliefStates
        self.counter += 1

        return beliefStates

    def compute_norm(self, i, j, i_p, j_p, c):
        """
        For a given current position and pacman position and a c value,
        Gives the norm (see the definition in report)

        Arguments:
        ----------
        - `i' and 'j' : current position
        - 'i_p' and 'j_p' : pacman position
        - 'c' : 1 if confused, 2 if afraid, 2 ** 3 if scared

        Return:
        -------
        - The norm of c's  (see the definition in report)
        """
        norm = 0
        if not self.walls[i][j - 1]:
            norm += (c if j_p >= j else 1)
        if not self.walls[i][j + 1]:
            norm += (c if j_p <= j else 1)
        if not self.walls[i + 1][j]:
            norm += (c if i_p <= i else 1)
        if not self.walls[i - 1][j]:
            norm += (c if i_p >= i else 1)

        return norm

    def compute_belief_states(self, beliefStates, k, i, j, i_p, j_p,
                              prob, c):
        """
        For a given current position, pacman position, a c value and a
        normalised probablity,
        Add the computed probability values to belief states of neighbours
        (after apply this function to all positions, we obtain the
        transition model defines in the report)

        Arguments:
        ----------
        - 'k' : ghost number
        - `i' and 'j' : current position
        - 'i_p' and 'j_p' : pacman position
        - 'prob  definition in report
        - 'c' : 1 if confused, 2 if afraid, 2 ** 3 if scared
        """

        if not self.walls[i][j - 1]:
            beliefStates[k][i][j - 1] += (prob * c if j_p >= j
                                          else prob)
        if not self.walls[i][j + 1]:
            beliefStates[k][i][j + 1] += (prob * c if j_p <= j
                                          else prob)
        if not self.walls[i + 1][j]:
            beliefStates[k][i + 1][j] += (prob * c if i_p <= i
                                          else prob)
        if not self.walls[i - 1][j]:
            beliefStates[k][i - 1][j] += (prob * c if i_p >= i
                                          else prob)

    def _get_evidence(self, state):
        """
        Computes noisy distances between pacman and ghosts.

        Arguments:
        ----------
        - `state`: The current game state s_t
                   where 't' is the current time step.
                   See FAQ and class `pacman.GameState`.


        Return:
        -------
        - A list of Z noised distances in real numbers
          where Z is the number of ghosts.

        XXX: DO NOT MODIFY THIS FUNCTION !!!
        Doing so will result in a 0 grade.
        """
        positions = state.getGhostPositions()
        pacman_position = state.getPacmanPosition()
        noisy_distances = []

        for p in positions:
            true_distance = util.manhattanDistance(p, pacman_position)
            noisy_distances.append(
                np.random.normal(loc=true_distance,
                                 scale=np.sqrt(self.sensor_variance)))

        return noisy_distances

    def _record_metrics(self, belief_states, state):
        """
        Use this function to record your metrics
        related to true and belief states.
        Won't be part of specification grading.

        Arguments:
        ----------
        - `state`: The current game state s_t
                   where 't' is the current time step.
                   See FAQ and class `pacman.GameState`.
        - `belief_states`: A list of Z
           N*M numpy matrices of probabilities
           where N and M are respectively width and height
           of the maze layout and Z is the number of ghosts.

        N.B. : [0,0] is the bottom left corner of the maze
        """
        if self.metrics is 0:
            self.metrics = np.zeros((len(belief_states), 10000))
        true_ghost_position = state.getGhostPosition(1)
        for k in range(len(belief_states)):
            belief_state = belief_states[k]
            self.metrics[k, self.counter % 10000] = util.manhattanDistance(
                true_ghost_position, np.unravel_index(belief_state.argmax(),
                                                      belief_state.shape))
        if self.counter > 10000:
            print(np.mean(self.metrics[0]))

    def get_action(self, state):
        """
        Given a pacman game state, returns a legal move.

        Arguments:
        ----------
        - `state`: the current game state.
                   See FAQ and class `pacman.GameState`.

        Return:
        -------
        - A legal move as defined in `game.Directions`.
        """

        """
           XXX: DO NOT MODIFY THAT FUNCTION !!!
                Doing so will result in a 0 grade.
        """
        # Variables are specified in constructor.
        if self.beliefGhostStates is None:
            self.beliefGhostStates = state.getGhostBeliefStates()
        if self.walls is None:
            self.walls = state.getWalls()

        newBeliefStates = self.update_belief_state(self._get_evidence(state),
                                                   state.getPacmanPosition())
        self._record_metrics(self.beliefGhostStates, state)

        return newBeliefStates
