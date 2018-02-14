class CannibalProblem:
    def __init__(self, start_state=(3, 3, 1)):
        self.start_state = start_state
        self.goal_state = (0, 0, -1)
        self.missionary = start_state[0]
        self.cannibal = start_state[1]

    # get a set of successor states for a given state
    def get_successors(self, state):
        successors = []

        # Loop from 0 to 2 for both x and y to explore all possible combinations of missionaries and cannibals on boat
        for x in range(0, 3):
            for y in range(0, 3):
                if 0 < x + y <= 2:
                    new_state = state
                    boat_state = state[2]
                    new_state = (state[0] - (boat_state * x), state[1] - (boat_state * y), -1 * state[2])

                    # Check if the new state is legal and has not already been appended to the successor list
                    # and append it to the successor if it qualifies
                    if self.is_legal(new_state) and new_state not in successors:
                        successors.append(new_state)

        return successors

    # return a boolean value of whether the inputted state is a legal state or not
    def is_legal(self, state):

        # the number of missionaries and cannibals on both bank cannot be larger than the number they started with
        # and cannot be smaller than 0.
        if state[0] > self.missionary or state[1] > self.cannibal or state[0] < 0 or state[1] < 0:
            return False

        # If there is at least one missionary and that missionary[s] is outnumbered by the cannibals, the game is over
        if state[0] != 0 and state[0] != self.missionary:
            if state[0] < state[1] or self.missionary - state[0] < self.cannibal - state[1]:
                return False

        return True

    # return a boolean value of whether the inputted state is equal to the goal state
    def is_goal(self, state):
        return state == self.goal_state

    def __str__(self):
        string = "Missionaries and cannibals problem: " + str(self.start_state)
        return string


# A bit of test code

if __name__ == "__main__":
    test_cp = CannibalProblem((3, 3, 1))
    print(test_cp.get_successors((3, 1, -1)))
    print(test_cp)

