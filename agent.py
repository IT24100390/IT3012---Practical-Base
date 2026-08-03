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