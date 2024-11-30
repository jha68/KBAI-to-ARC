from random import choice
from collections import deque

class ARCPuzzle:
    """
    An eight puzzle class that can be used to test different search algorithms.
    When first created the puzzle is in the solved state.
    """

    def __init__(self, state):
        self.state = tuple((tuple(row) for row in state))

    def __hash__(self):
        return hash(self.state)

    def __eq__(self, other):
        if isinstance(other, ARCPuzzle):
            return self.state == other.state
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return str(self)

    def __str__(self):
        out = ""
        for row in self.state:
            out += str(row) + "\n"
        return out

    def copy(self):
        """
        Makes a deep copy of an ARCPuzzle object.
        """
        new = ARCPuzzle(self.state)
        return new

    def randomize(self, num_shuffles):
        """
        Randomizes an ARCPuzzle by executing a random action `num_suffles`
        times.
        """
        for i in range(num_shuffles):
            actions = [a for a in self.legalActions()]
            a = choice([a for a in self.legalActions()])
            # print(actions, a)
            self.executeAction(a)

        return self

    def tophalf(self, grid):
        """ upper half """
        return grid[:len(grid) // 2]


    def rot90(self, grid):
        """ clockwise rotation by 90 degrees """
        return tuple(zip(*grid[::-1]))


    def hmirror(self, grid):
        """ mirroring along horizontal """
        return grid[::-1]

    def vmirror(self, grid):
        """ mirroring along horizontal """
        return tuple(reversed(grid))

    def lshift(self, grid):
        return tuple([tuple([e for e in row if e != 0] + [0]*row.count(0))
                      for row in grid])

    def compress(self, grid):
        """ removes frontiers """
        ri = [i for i, r in enumerate(grid) if len(set(r)) == 1]
        ci = [j for j, c in enumerate(zip(*grid)) if len(set(c)) == 1]
        return tuple([tuple([v for j, v in enumerate(r) if j not in ci])
                      for i, r in enumerate(grid) if i not in ri])

    def mapcolor(self, grid, a, b):
        return tuple(tuple(b if e == a else e for e in row) for row in grid)

    def trim(self, grid):
        """ removes border """
        return tuple(r[1:-1] for r in grid[1:-1])

    def executeAction(self, action):
        """
        Executes an action to the ARCPuzzle object.

        :param action: the action to execute
        :type action: "up", "left", "right", or "down"
        """
        if action == 'tophalf':
            self.state = self.tophalf(self.state)
        elif action == 'rot90':
            self.state = self.rot90(self.state)
        elif action == 'hmirror':
            self.state = self.hmirror(self.state)
        elif action == 'vmirror':
            self.state = self.vmirror(self.state)
        elif action == 'lshift':
            self.state = self.lshift(self.state)
        elif action == 'compress':
            self.state = self.compress(self.state)
        elif action[:8] == 'mapcolor':
            args = action[9:-1].split(',')
            self.state = self.mapcolor(self.state, int(args[0]), int(args[1]))

    def legalActions(self):
        """
        Returns an iterator to the legal actions that can be executed in the
        current state.
        """
        for action in ['tophalf', 'rot90', 'hmirror', 'vmirror', 'lshift', 'compress']:
            yield action

        for a in set(e for row in self.state for e in row):
            for b in range(10):
                if a == b:
                    continue
                yield f'mapcolor({a},{b})'


# Defining the arc_planning function below the ArcPuzzle class
def arc_planning(input_grid, output_grid) -> list[str]:
    """
    Searches for a sequence of transformations to convert the input_grid into
    the output_grid.
    
    Parameters:
    - input_grid: The initial grid that needs to be transformed.
    - output_grid: The target grid to achieve.
    - available_operations: List of primitive operations that can be used to transform the input grid.
    
    Returns:
    - A list of actions that transforms input_grid into output_grid.
    """
    # Your implementation here
    
    # # Example: Replace this with your actual search/planning logic.
    # available_operations = []
    # for action in ARCPuzzle(input_grid).legalActions():
    #     available_operations.append(action)
    
    # return []

    initial = ARCPuzzle(input_grid)
    goal = ARCPuzzle(output_grid)
    
    visited = set()
    queue = deque([(initial, [])])
    actions = ARCPuzzle(input_grid).legalActions()
    
    while queue:
        current_puzzle, current_actions = queue.popleft()
        
        # If we've reached the goal, return the sequence of actions
        if current_puzzle.__eq__(goal):
            return current_actions
        
        # Mark the current state as visited
        visited.add(current_puzzle.state)
        
        # Try each action to generate new states
        for action in ARCPuzzle(current_puzzle.state).legalActions():
            new_puzzle = current_puzzle.copy()
            new_puzzle.executeAction(action)
            
            if new_puzzle.state not in visited:
                new_actions = current_actions + [action]
                queue.append((new_puzzle, new_actions))
    
    # If no solution is found, return an empty list
    return []

if __name__ == "__main__":

    initial = ARCPuzzle([[7, 0, 7], [7, 0, 7], [7, 7, 0]])
    initial_copy = initial.copy()
    goal = initial.copy()
    goal.randomize(3)

    print("Puzzle being solved:")
    print(initial)
    print("Goal =====>")
    print(goal)
    print("-------------------")

    ans = arc_planning(initial.state, goal.state)
    print(ans)
    print(initial_copy)
    for action in ans:
        initial_copy.executeAction(action)
        print(initial_copy)
