from collections import deque
import heapq
class SimpleReflexAgent:
    """
    Simple Reflex Agent:
    Uses only current percept and condition-action rules.
    """

    def sense_and_act(self, percept):

        # IF food_here THEN suck
        if percept["food_here"]:
            return "Stay"

        # IF wall_ahead THEN turn_left
        elif percept["wall_ahead"]:
            return "Left"

        # ELSE move_forward
        else:
            return "Up"



class ModelBasedAgent:
    """
    Model-Based Agent:
    Uses memory to avoid repeated failures.
    """

    def __init__(self):
        self.visited_cells = set()
        self.last_action = None


    def sense_and_act(self, percept):

        # Update internal state
        current_percept = str(percept)
        self.visited_cells.add(current_percept)


        # IF food_here THEN suck
        if percept["food_here"]:
            action = "Stay"


        # IF wall_ahead and already visited THEN choose alternative path
        elif percept["wall_ahead"] and current_percept in self.visited_cells:
            action = "Right"


        # IF wall_ahead THEN turn_left
        elif percept["wall_ahead"]:
            action = "Left"


        # ELSE move_forward
        else:
            action = "Up"


        # Store last action
        self.last_action = action

        return action

class SearchAgent:

    def bfs_search(self, start_pos, goal_pos, walls, grid_size):

        queue = deque()
        queue.append((start_pos, []))

        reached = set()
        reached.add(start_pos)

        width, height = grid_size

        while queue:

            current, path = queue.popleft()

            if current == goal_pos:
                return path

            x, y = current

            neighbors = [
                ((x, y + 1), "Up"),
                ((x, y - 1), "Down"),
                ((x - 1, y), "Left"),
                ((x + 1, y), "Right")
            ]

            for next_pos, action in neighbors:

                nx, ny = next_pos

                if (
                    0 <= nx < width
                    and 0 <= ny < height
                    and next_pos not in walls
                    and next_pos not in reached
                ):
                    reached.add(next_pos)
                    queue.append((next_pos, path + [action]))

        return None


    def dfs_search(self, start_pos, goal_pos, walls, grid_size):

        stack = [(start_pos, [])]
        reached = {start_pos}

        width, height = grid_size

        while stack:

            current, path = stack.pop()

            if current == goal_pos:
                return path

            x, y = current

            neighbors = [
                ((x, y + 1), "Up"),
                ((x, y - 1), "Down"),
                ((x - 1, y), "Left"),
                ((x + 1, y), "Right")
            ]

            for next_pos, action in neighbors:

                nx, ny = next_pos

                if (
                    0 <= nx < width
                    and 0 <= ny < height
                    and next_pos not in walls
                    and next_pos not in reached
                ):
                    reached.add(next_pos)
                    stack.append((next_pos, path + [action]))

        return None


    def ucs_search(self, start_pos, goal_pos, walls, grid_size):

        priority_queue = []
        heapq.heappush(priority_queue, (0, start_pos, []))

        reached = {start_pos: 0}

        width, height = grid_size

        while priority_queue:

            cost, current, path = heapq.heappop(priority_queue)

            if current == goal_pos:
                return path

            x, y = current

            neighbors = [
                ((x, y + 1), "Up"),
                ((x, y - 1), "Down"),
                ((x - 1, y), "Left"),
                ((x + 1, y), "Right")
            ]

            for next_pos, action in neighbors:

                nx, ny = next_pos

                if (
                    0 <= nx < width
                    and 0 <= ny < height
                    and next_pos not in walls
                ):

                    new_cost = cost + 1

                    if (
                        next_pos not in reached
                        or new_cost < reached[next_pos]
                    ):
                        reached[next_pos] = new_cost
                        heapq.heappush(
                            priority_queue,
                            (new_cost, next_pos, path + [action])
                        )

        return None
    def __init__(self):
        self.plan = []
        self.active_algo = "BFS"

    def sense_and_act(self, percept):

        if not self.plan:

            start_pos = tuple(percept.get("agent_pos", (0, 0)))

            food_positions = percept["all_food"]

            if not food_positions:
                return "Stay"

            closest_food = min(
                food_positions,
                key=lambda food: abs(food[0] - start_pos[0]) + abs(food[1] - start_pos[1])
            )

            goal_pos = tuple(closest_food)

            if self.active_algo == "BFS":
                self.plan = self.bfs_search(
                    start_pos,
                    goal_pos,
                    percept["walls"],
                    percept["grid_size"]
                )

            elif self.active_algo == "DFS":
                self.plan = self.dfs_search(
                    start_pos,
                    goal_pos,
                    percept["walls"],
                    percept["grid_size"]
                )

            elif self.active_algo == "UCS":
                self.plan = self.ucs_search(
                    start_pos,
                    goal_pos,
                    percept["walls"],
                    percept["grid_size"]
                )

            if self.plan is None:
                return "Stay"

        return self.plan.pop(0)