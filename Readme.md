# Missionary and Cannibal

### Introduction

Through missionary and cannibal game, we intend to explore the most fundamental element in understanding artificial intelligence: states. In brief, a program would compute in order to meet the desired end state from the provided start state.

The total number of possible states for missionary and cannibal would be `(m+1) * (c+1) * b` where `m` refers the number of missionaries, `c` refers to the number of cannibals, `b` refers to the number of boat's destinations). For instance, if there were 3 missionaries, 3 cannibals, and 2 boat destinations, the total number of possible states would be 32. When broken down to steps, the procedure of computing total number of states is as follows:
> **1. There are `m + 1` possible states for missionaries.**  
```[0, 1, 2, 3] when m = 3```
>
> **2. There are `c + 1` possible states for cannibals.**  
```[0, 1, 2, 3] when c = 3```
>
> **3. There are `b` possible states for boat's destinations.**  
```[bank #1, bank #2] when b = 2```
>
> **4. There are `(m + 1)(c + 1)` possible ways of aligning different combinations of m and c.**  
```{(0,0),(0,1),(0,2),(0,3),(1,0),(1,1),(1,2),(1,3),(2,0),(2,1),(2,2)(2,3),(3,0),(3,1),(3,2),(3,3)}```
>
> **5. There are `(m+1)(c+1)(b)` possible ways of aligning different combination of m and c and b.**  
```{(0,0,-1),(0,1,-1),(0,2,-1),(0,3,-1),(1,0,-1),(1,1,-1),(1,2,-1),(1,3,-1),(2,0,-1),(2,1,-1),(2,2,-1)(2,3,-1),(3,0,-1),(3,1,-1),(3,2,-1),(3,3,-1),(0,0,1),(0,1,1),(0,2,1),(0,3,1),(1,0,1),(1,1,1),(1,2,1),(1,3,1),(2,0,1),(2,1,1),(2,2,1)(2,3,1),(3,0,1),(3,1,1),(3,2,1),(3,3,1)}```



That being said, this program implements a design, where a state can be described with a tuple of 3 elements, under a premise that boat's destinations are limited to two locations: bank_1 and bank_2. The first element (_m1_) and the second element (_c1_) capture respectively the number of missionaries and cannibals on bank_1. Accordingly, the number of missionaries and cannibals on bank_2 can be easily calculated by subtracting _m1_ and _c1_ from the the total number of missionaries and cannibals. The third element (_b_) is constrained to having two possible states -1 and 1: _b_=1 when the boat is at bank_1 and _b_=-1 when the boat is at bank_2.

Throughout the run time, program actively searches for a set of possible states from its current state, and keeps on searching until it's found its way to the desired end state or discovers that there is no way of reaching one. Here is an example of the first few steps in Missionary and Cannibal Game when `m`=3, `c`=3:

The program starts at (3,3,1) and makes its way onward. That is, it first searches for every possible state that can be reached from (3,3,1), and repeats the same procedure as it moves onto its list of next states. As the diagram shows, not all possible states are legal states. That is why we have to throw a legality test for every node. For instance, in the diagram, those that are colored in red are those that do not qualify as legal states. (2,3,-1), (1,3,-1), and (2,3,1) all represent a situation where the missionaries are outnumbered by the cannibals at bank_1. In other words, the missionaries on bank_1 are going to be eaten by the cannibals, and it would be a game over. That is why, the red nodes don't have any child node (the game will come to an end before it can be led to a group of new states). On the other hand, all the green nodes (states that have passed the legality test) have at least one child node; some go straight back to where they came from, but some make their ways to new nodes that have not been visited yet. And these steps are repeated either until it makes its way to the goal state or until it has explored every possible legal state.

### Codes Revisited
#### get_successors(self, state)
This function peeks at every possible state, runs a legality test, appends onto a list the ones that pass the legality test, and returns the computed list.  

Along with the missionaries and cannibals either leaving or entering bank #1, the number of missionaries and cannibals will alter by maximum total number of people that can fit into the boat (which is, in this case, 2). That is, the number of missionary will either increase or decrease by a number in range of 0 to the max. capacity of the boat and the number of cannibals will either increase or decrease by a number in range of 0 to max. capacity - the number of missionaries on the boat. Of course, not all these states are legal because whenever the missionaries are outnumbered by the cannibals on either bank, the missionaries would get eaten. That is why is_legal method is called within get_successor method and only appends the ones pass the legality test.
#### is_legal(self, state)
Given a state `(m1, c1, b)`, this function checks for three things:
1. Does either `m1` or `c1` exceed the total number of missionaries or cannibals?  
```e.g. (4,1,-1) when m = 3, c = 3```
2. Is the missionary on either bank outnumbered by the cannibals?  
```e.g. (2,3,1)```
3. If the missionary is outnumbered, is there more than 0 missionary at the bank?
```e.g. (2,3,1)```  

If the answer to any of the listed question is a 'yes,' then the state has failed the legality test.  

Questions #1, #2 are pretty much self-explanatory. The number of missionaries and cannibals on either bank should never exceed the number they started off with. And if there are more cannibals than missionaries on either side of the bank, the missionaries would get eaten, which, in other words, is a 'game over' (There is an exception to this rule, which I will be explaining very soon). Question #3 might need a supplementary explanation. Let's say that there are 3 cannibals and 0 missionaries on bank #1; the cannibals outnumbers the missionaries here. However, even though the cannibals outnumber the missionaries, they don't have any missionary to eat, and it's not a 'game over!' That is, even if the cannibals outnumber the missionaries, if the number of missionary is 0, the game will not come to an end, for the outnumbering cannibals won't have any missionary to eat.

#### back_track(self)
This function simply takes a search node, and traces up its parent ladder until it reaches the very top. It records its track and returns it as a list.

#### bfs_search(search_problem)
    def bfs_search(search_problem):

        final_node = None
        to_be_visited = deque()
        visited = set()
        root_node = SearchNode(search_problem.start_state)
        to_be_visited.append(root_node)

        while to_be_visited:

          current_node = to_be_visited.popleft()
          visited.add(current_node.state)

          if search_problem.is_goal(current_node.state):
              final_node = current_node
              break

          successors = search_problem.get_successors(current_node.state)

          while successors:
              next_state = successors.pop(0)
              next_node = SearchNode(next_state, current_node)

              if next_state in visited or next_node in to_be_visited:
                  continue

              to_be_visited.append(next_node)

          solution = SearchSolution(search_problem, "BFS")
          solution.nodes_visited = len(visited)

          if final_node:
              solution.path = final_node.backtrack()

          return solution

This function starts from the root node and searches for the goal state floor by floor. The visiting order is preserved by using a queue data structure. Initially, the root node is appended onto the queue. And the method enters a loop that ends once the queue is empty. Within the loop, a node is popped from the queue, and the children of the popped node is appended onto the queue. Because a queue structure follows the 'First in First out' rule, the method will never search for a node at a different depth until it's fully visited the nodes at a previous depth. And at every loop, the method checks whether the goal has been reached, and if it has, it escapes the loop, calls *back_track* method to iron out a path from the root node to the goal, and returns the solution.

Below is the result I get when I test for (3, 3, 1):

    Missionaries and cannibals problem: (3, 3, 1)  
    attempted with search method BFS  
    number of nodes visited: 15  
    solution length: 12  
    path: [(3, 3, 1), (3, 1, -1), (3, 2, 1), (3, 0, -1), (3, 1, 1), (1, 1, -1), (2, 2, 1), (0, 2, -1), (0, 3, 1), (0, 1, -1), (0, 2, 1), (0, 0, -1)]

For the following example, `(3, 3, 1)` is initially appended onto the to_be_visited deque. Then, the function enters a loop that ends once the deque is empty. Within the loop, a node is popped from the deque (in this case, `(3, 3, 1)`). And the node is appended to the visited set so that the function does not revisit the same node. Then, it checks whether the node is the goal node. If goal has been reached, we'd mark the final node and break from the loop. Otherwise, we'd look for the current node's legal successors `((3,2,-1), (3,1,-1), (2,2,-1))`, iterate through each one of them, check whether its state has already been visited or been appended to the deque or not, and append it to the deque if it hasn't. The aforementioned steps are repeated until we've run through the entire graph or have found the goal state. If a goal state has been found, we call back_track function to get the path. In the case of (3,3,1), the function was able to reach the goal state, and figure out the path `((3, 3, 1), (3, 1, -1), (3, 2, 1), (3, 0, -1), (3, 1, 1), (1, 1, -1), (2, 2, 1), (0, 2, -1), (0, 3, 1), (0, 1, -1), (0, 2, 1), (0, 0, -1))`.

#### dfs_search(search_problem, path_set=None, depth_limit=100, node=None, solution=None)
This function digs down the ladder and searches for the goal state. It constantly checks its current path and recursively calls itself passing on the child node popped from the deque.

The most significant thing to note for this function would be that the method constantly keeps track of its current path from the root node. The very purpose is to prevent the method from visiting the already visited nodes. For a tree, current path checking would prevent the method from ever revisiting a node because every child node has one parent node and the very child node that has been visited will never be appended onto the successor deque of any other node. However, the same does not apply to graphs: a node can have multiple parent nodes. That being said, a node can be appended onto the successor deque of other nodes that qualify as its parent node and may be revisited when it's no longer a part of the current path that is being explored.  

Also, one thing to note about this function is that in keeping track of the current path, it implements a hybrid data structure: a list and a set. A list is an ordered data, so it remembers the visited nodes in an orderly manner, which can be returned at the end of the function. On the other hand, a set is not an ordered data, but it has a linear average search time, and, therefore, whenever we check whether a given node is already in our current path or not, we can make a good use of a set's linear search time. Consequently using the two data structures will guarantee us a better run time.

#### ids_search(search_problem)
    def ids_search(search_problem, depth_limit=100):
        depth = 0
        total_num_of_visited = 0
        num_of_visited = 0
        solution = SearchSolution(search_problem, "IDS")
        root_node = SearchNode(search_problem.start_state)
        path_set = set()

        while depth < depth_limit and (not solution.path or not search_problem.is_goal(solution.path[-1])):
            solution = dfs_search(search_problem, path_set, depth, root_node, solution)
            depth += 1

            if solution.nodes_visited - total_num_of_visited == num_of_visited:
                break

            num_of_visited = solution.nodes_visited - total_num_of_visited
            total_num_of_visited = solution.nodes_visited

        return solution
This function starts off by calling dfs at depth = 0. And it keeps incrementing the depth by 1, until it has reached the depth limit, has no more node to search, or has reached the goal state. As can be observed in the provided code above, I determine whether the function has any more node to traverse or not by keeping track of the number of visited nodes for every loop (`num_of_visited = solution.nodes_visited - total_num_of_visited`). If the number of visited nodes has not changed (`if solution.nodes_visited - total_num_of_visited == num_of_visited`), there obviously is no more node to be explored, and, therefore, it would be reasonable to break out of loop instead of repeating the entire thing until depth limit has been reached. Depth first search, despite its incapability of computing an optimal answer, uses up a very small amount of memory. On the other hand, bfs, which is capable of coming up with an optimal answer, takes up a huge memory to run. As a resolution, ids is used. Because ids essentially is a bfs, it uses up a small amount of memory, and because it searches upto a given depth at a time, it will derive an optimal answer. However, as I pointed out for path-checking dfs, run time of ids will be compromised. It will revisit the same node over and over again because there is no data structure keeping track of nodes visited in order to save memory.

### Essential Discussion Questions

For the answers to the following questions, let's assume the below:
1) Total number of nodes = `n`
2) The longest possible path = `p`

#### Does memoized dfs save significant memory in respect to bfs?
No, theoretically, for both cases, the worst case would be when the goal_state is at the rightmost leaf node, and if so, its "visited set" would have as many states as the total number of nodes present in the graph. That is, in worst case, both methods will need O(n) memory.

#### Does path-checking depth-first search save significant memory with respect to breadth-first search? Draw an example of graph where path-checking dfs takes much more run time than breadth-first search; include in your report and discuss.  
The worst case for path-checking would be to store `p` number of nodes in memory. For breadth-first search though, the worst case would be to store `n` number of nodes in memory. Technically, `p` could equal `n`, but that would be very unlikely. For instance, if a graph is a linearly linked list, `p` would equal `n`, but that's not the case here. That being said, path-checking dfs will save significant amount of memory with respect to bfs.

Of course, run-time-wise, things would be different. The worst-case for bfs will be visiting every node before finally reaching the goal: therefore, `O(n)`. On the other hand, the worst-case for path-checking dfs will be going down the longest path for every node: therefore, `O(nˆd)`.
Below is an example of a graph where path-checking dfs takes much more run time than breadth-first search:
![example](./Example_1.svg)
Let's say that the program's objective is to get to node `G` starting from node A. Implementing path-checking dfs, we will have to visit total 6 nodes `A, B, C, D, E, F` before finally reaching node `G`, while implementing bfs, we only have to visit 2 nodes `A, B` before reaching `G`.

#### On a graph, would it make sense to use path checking dfs or would you prefer memoizing dfs in your iterative deepening search?
Memory-wise, path checking dfs will never exceed the total number of nodes `n` within the graph. Worst case, it will surmount to `p`. However, because graph has vertices with multiple edges, it occasionally revisits the nodes as it climbs up the recursion. Unlike in a tree, where a node has no more than one parent, in a graph, a node can have more than one parent. In a graph, when the search reaches a leaf node, it only ensures that there is no edge between the leaf node and the unvisited nodes; there can be edges between the leaf node and the already visited nodes. Therefore, once the leaf node is removed from the current path, it can be revisited as a child of some node in the current path list. Moreover, especially in ids, where a node has to return if it hits its depth limit regardless of it being a leaf node or not, it cannot be ensured that there is no edge between the node and the unvisited nodes. That being said, run-time-wise, it is very likely that memoizing dfs is faster than path-checking dfs.
However, memoizing dfs uses up a large sum of memory and if you are going to use the same span of memory, it'd be more reasonable to use bfs instead of memoizing dfs.

#### If up to E missionaries can be eaten in order to reach the goal state, what would the state for this problem be? What changes will you make to your code to implement such change? What would the upperbound be?

The state would be a tuple of four elements, and the fourth element, `e`, refers to the number of missionaries sacrificed. Moreover, a variable for the total number of sacrifices allowed need to be added to the instance variable of CannibalProblem.  

 Method-wise, a slight modification would have to be made to is_legal method. What used to be an illegal state would now become legal. Once the missionary is outnumbered by the cannibals, those missionaries will be eaten, and as long as, `e` does not sum up to its given constraint E, the total number of missionaries that can be sacrificed, the state can be viewed as legal. A brute upperbound, that is, the total number of possible states would be `(m+1)(c+1)(b)(E+1)`. However, the more optimized upperbound would be as follows:   

 `(m+1)(c+1)(b) + ... ((m+1)-E)(c+1)(b)`  
 In other words, `(m+1)(E+1)-(E+1)(E/2))(c+1)(b)`  
 Abbreviated, it would be `(E+1)((m+1)-(E/2))(c+1)(b)`  

 It is because the total number of missionaries decreases as the number of missionaries being sacrificed increases. The upperbound, therefore, would be a sum of `the total number of states for alive missionaries * the total number of states for cannibals * the total number of boat states` for every possible value of `e`, which ranges from 0 to E.  

For instance, given that E = 2 and the initial state = (3, 3, 1) & 0, possibles states would be:  

    {(3,3,1,0), (3,2,1,0), (3,1,1,0), (3,0,1,0), (2,3,1,0), (2,2,1,0), (2,1,1,0), (2,0,1,0), (1,3,1,0), (1,2,1,0), (1,1,1,0), (1,0,1,0), (0,3,1,0), (0,2,1,0), (0,1,1,0), (0,0,1,0), (3,3,-1,0), (3,2,-1,0), (3,1,-1,0), (3,0,-1,0), (2,3,-1,0), (2,2,-1,0), (2,1,-1,0), (2,0,-1,0), (1,3,-1,0), (1,2,-1,0), (1,1,-1,0), (1,0,-1,0), (0,3,-1,0), (0,2,-1,0), (0,1,-1,0), (0,0,-1,0), (2,3,1,1), (2,2,1,1), (2,1,1,1), (2,0,1,1), (1,3,1,1), (1,2,1,1), (1,1,1,1), (1,0,1,1), (0,3,1,1), (0,2,1,1), (0,1,1,1), (0,0,1,1), (2,3,-1,1), (2,2,-1,1), (2,1,-1,1), (2,0,-1,1), (1,3,-1,1), (1,2,-1,1), (1,1,-1,1), (1,0,-1,1), (0,3,-1,1), (0,2,-1,1), (0,1,-1,1), (0,0,-1,1), (1,3,1,2), (1,2,1,2), (1,1,1,2), (1,0,1,2), (0,3,1,2), (0,2,1,2), (0,1,1,2), (0,0,1,2), (1,3,-1,2), (1,2,-1,2), (1,1,-1,2), (1,0,-1,2), (0,3,-1,2), (0,2,-1,2), (0,1,-1,2), (0,0,-1,2)}

The upperbound would be, for this example, `(4 * 4 * 2) + (3 * 4 * 2) + (2 * 4 * 2) =  72`.

Lossy case is further discussed in the extra credit section; I have implemented changes in order to take care of the lossy case.

1. Boat Capacity modification:  
I made it possible to modify the number of people that can fit in the boat. Now you can have more than 2 people aboard. I made it so that if the cannibals outnumber the missionaries on the boat, the missionaries get eaten. I made a few tweaks at the instance variables of CannibalProblem and get_successor function.

2. Lossy case:  
Now the cannibal problem can handle the "lossy" case. I have made a few edits to the is_legal function, get_successor function, and to CannibalProblem's instance variables.

3. Memoized_DFS:  
Memoized_DFS keeps a separate set of visited nodes to prevent any revisiting of the nodes.

The test cases for all three implementations can be found on cannibals.py in the extra_credit package.

#### Boat Capacity modification
The following list are the changes made to enable modification of boat capacity:
1. The instance variable of Cannibal Problem now includes the number of people that can fit on the boat. ---> CannibalProblem(start_state, boat_capacity)

2. get_successor function now loops from 0 to boat_capacity instead of 0 to 2. And checks whether a sum of `x`, the number of missionary onboard, and `y, the number of cannibals onboard, is lower than or equal to the boat_capacity.

3. get_successor function checks whether the missionaries are outnumbered by the cannibals on the boat. If there is at least one missionary on the boat and is outnumbered by the cannibals, that state will not be appended to the successor list.

#### Lossy case
The following changes were made to explore possible cases where a certain number of missionaries are sacrificed in order to make it to the goal:

1. The state variable has been altered from `(m1,c1,b)` to `(m1,c1,b,e1)`

2. CannibalProblem's instance variable now contains a variable referring to the total number of sacrifice allowed, `E`. ---> CannibalProblem(start_state, E)

3. is_legal function now checks whether `e1` is smaller than or equal to the total number of missionaries that can be sacrificed `E`

4. get_successor function now has a separate variable, `sacrificed`, keeping track of the number of sacrifices occurring both on boat and on lands. Whenever, there is at least one missionary and that missionary[s] is outnumbered by the cannibals whether it be on boat or on land, `sacrificed` is updated and the number of missionary is also updated.

5. is_goal method now checks whether state[:3] is equal to the goal_state because the state is a tuple of 4 while goal state is a tuple of 3.

#### Memoized dfs
Memoized dfs is no different from the original path-checking dfs other than the fact that it keeps a cumulative set that keeps track of the visited nodes. Memoized DFS, therefore, will never revisit the same node. However, it uses up a lot of memory O(n) and, yet, can't even compute the shortest path. It'd be more reasonable to use bfs than to use memoized dfs.
