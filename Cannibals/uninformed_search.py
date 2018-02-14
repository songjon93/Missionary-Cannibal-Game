from collections import deque
from SearchSolution import SearchSolution
from CannibalProblem import CannibalProblem


class SearchNode:
    # each search node except the root has a parent node
    # and all search nodes have state variables

    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent

    # climb up the ladder until you reach the root node, and return the list
    def backtrack(self):
        node_list = []
        state_list = []

        while self:
            node_list.append(self)
            self = self.parent

        while node_list:
            state_list.append(node_list.pop().state)

        return state_list


# search floor by floor until you either reach your desired state or hit the end
def bfs_search(search_problem):

    final_node = None  # Initialize a variable for the "goal node"
    to_be_visited = deque()  # Initialize a queue onto which the node to be visited shall be appended respectively
    visited = set()  # Create a set of visited states to keep track of what nodes have been visited
    root_node = SearchNode(search_problem.start_state)
    to_be_visited.append(root_node)

    # Loop until either when there is no more node to be visited or when you've reached the goal state
    while to_be_visited:

        # Pop from the queue a node, which we shall run a get_successor function on
        current_node = to_be_visited.popleft()

        # Mark the node as visited
        visited.add(current_node.state)

        # If the current node is the goal, save the instance to final_node variable and break out of the loop
        if search_problem.is_goal(current_node.state):
            final_node = current_node
            break
        # Else, get successors of the current node, and append them onto the to_be_visted queue accordingly
        successors = search_problem.get_successors(current_node.state)

        # Loop through the set of successors, and append only the ones that have not been added onto the queue and
        # not been visited onto the queue
        while successors:
            next_state = successors.pop(0)
            next_node = SearchNode(next_state, current_node)
            if next_state in visited or next_node in to_be_visited:
                continue
            to_be_visited.append(next_node)

    solution = SearchSolution(search_problem, "BFS")
    solution.nodes_visited = len(visited)

    # If final_node is None, there could not be found a path to the goal state
    # If not, a path has been found: backtrack it, and update the solution object with the path.
    if final_node:
        solution.path = final_node.backtrack()
    return solution


def dfs_search(search_problem, path_set=None, depth_limit=100, node=None, solution=None):

    # If node = None, make a node with a start state and initialize a solution object to be returned
    # at the end of the method
    if not node:
        node = SearchNode(search_problem.start_state)
        solution = SearchSolution(search_problem, "DFS")
        path_set = set()

    # Append the state to the current path tracker, which is an orderly list of a path from start state to end state
    solution.path.append(node.state)

    # Also keep a set composed of current path, so that I can look up whether the state has been visited or not
    # at linear search time
    path_set.add(node.state)

    solution.nodes_visited += 1  # Number of visited increased by 1

    # Base Case 1 : If the current node is at a desired state, return the solution with the updated current path
    if search_problem.is_goal(node.state):
        return solution

    # Base Case 2 : If we'e reached the depth limit, and yet have not found our goal, remove the current node
    # from the current path and return the updated solution.
    if depth_limit == 0:
        solution.path.pop()
        path_set.remove(node.state)
        return solution

    next_states = search_problem.get_successors(node.state)

    while next_states:
        next_state = next_states.pop()

        # If the adjacent nodes have already been visited, skip to the next adjacent node
        # Also search for the state in a set instead of a list, where it would cost a linear search time
        if next_state in path_set:
            continue

        next_node = SearchNode(next_state, node)
        dfs_search(search_problem, path_set, depth_limit - 1, next_node, solution)

        # if a rear end of our current path is the end state, then escape the loop and return the solution
        if search_problem.is_goal(solution.path[-1]):
            return solution

    # if the following line has been reached, it is a leaf node, and does not match our desired end state
    # so remove it from our current path and climb up to our previous node
    solution.path.pop()
    path_set.remove(node.state)
    return solution


def ids_search(search_problem, depth_limit=100):
    # initialize the variables
    depth = 0
    total_num_of_visited = 0
    num_of_visited = 0
    solution = SearchSolution(search_problem, "IDS")
    root_node = SearchNode(search_problem.start_state)
    path_set = set()

    # If the end of current path is the desired end state, goal has been reached, so exit
    # If the depth has reached its depth_limit, exit
    while depth < depth_limit and (not solution.path or not search_problem.is_goal(solution.path[-1])):
        solution = dfs_search(search_problem, path_set, depth, root_node, solution)
        depth += 1

        # If number of nodes visited has not changed, all the visits have been made, so exit
        if solution.nodes_visited - total_num_of_visited == num_of_visited:
            break

        # Compute noncumulative number of visited nodes by subtracting the current cumulative with the past cumulative
        num_of_visited = solution.nodes_visited - total_num_of_visited
        # Update the cumulative number of visited nodes.
        total_num_of_visited = solution.nodes_visited

    return solution
