class PathPlanner():
    """Construct a PathPlanner Object"""
    def __init__(self, M, start=None, goal=None):
        """ """
        self.map = M
        self.start= start
        self.goal = goal
        self.closedSet = self.create_closedSet() if goal != None and start != None else None
        self.openSet = self.create_openSet() if goal != None and start != None else None
        self.cameFrom = self.create_cameFrom() if goal != None and start != None else None
        self.gScore = self.create_gScore() if goal != None and start != None else None
        self.fScore = self.create_fScore() if goal != None and start != None else None
        self.path = self.run_search() if self.map and self.start != None and self.goal != None else None
    
    def reconstruct_path(self, current):
        """ Reconstructs path after search """
        total_path = [current]
        while current in self.cameFrom.keys():
            current = self.cameFrom[current]
            total_path.append(current)
        return total_path
    
    def _reset(self):
        """Private method used to reset the closedSet, openSet, cameFrom, gScore, fScore, and path attributes"""
        self.closedSet = None
        self.openSet = None
        self.cameFrom = None
        self.gScore = None
        self.fScore = None
        self.path = self.run_search() if self.map and self.start and self.goal else None

    def run_search(self):
        """ """
        if self.map == None:
            raise(ValueError, "Must create map before running search. Try running PathPlanner.set_map(start_node)")
        if self.goal == None:
            raise(ValueError, "Must create goal node before running search. Try running PathPlanner.set_goal(start_node)")
        if self.start == None:
            raise(ValueError, "Must create start node before running search. Try running PathPlanner.set_start(start_node)")

        self.closedSet = self.closedSet if self.closedSet != None else self.create_closedSet()
        self.openSet = self.openSet if self.openSet != None else  self.create_openSet()
        self.cameFrom = self.cameFrom if self.cameFrom != None else  self.create_cameFrom()
        self.gScore = self.gScore if self.gScore != None else  self.create_gScore()
        self.fScore = self.fScore if self.fScore != None else  self.create_fScore()

        while not self.is_open_empty():
            current = self.get_current_node()

            if current == self.goal:
                self.path = [x for x in reversed(self.reconstruct_path(current))]
                return self.path
            else:
                self.openSet.remove(current)
                self.closedSet.add(current)

            for neighbor in self.get_neighbors(current):
                if neighbor in self.closedSet:
                    continue    # Ignore the neighbor which is already evaluated.

                if not neighbor in self.openSet:    # Discover a new node
                    self.openSet.add(neighbor)
                
                # The distance from start to a neighbor
                #the "dist_between" function may vary as per the solution requirements.
                if self.get_tentative_gScore(current, neighbor) >= self.get_gScore(neighbor):
                    continue        # This is not a better path.

                # This path is the best until now. Record it!
                self.record_best_path_to(current, neighbor)
        print("No Path Found")
        self.path = None
        return False

    
    
    
    #Data Structures
    
    def create_closedSet(self):
    """ Creates and returns a data structure suitable to hold the set of nodes already evaluated"""
        return set()

    def create_openSet(self):
    """ Creates and returns a data structure suitable to hold the set of currently discovered nodes 
    that are not evaluated yet. Initially, only the start node is known."""
        if self.start != None:
        # TODO: return a data structure suitable to hold the set of currently discovered nodes 
        # that are not evaluated yet. Make sure to include the start node.
            notEvalYet = set()
            notEvalYet.add(self.start)
            return notEvalYet
        raise(ValueError, "Must create start node before creating an open set. Try running PathPlanner.set_start(start_node)")
        
    def create_cameFrom(self):
        # TODO: return a data structure that shows which node can most efficiently be reached from another, for each node. 
        return dict()
    
    
    def create_gScore(self):
        # TODO:  return a data structure that holds the cost of getting from the start node to that node, for each node.
        # for each node. The cost of going from start to start is zero. The rest of the node's values should 
        # be set to infinity.
        ddd=dict()
        for i in self.map.intersections:
            ddd[i]=float("inf")
        ddd[self.start] = 0.0
        return ddd
    
    def create_fScore(self):
        # TODO: return a data structure that holds the total cost of getting from the start node to the goal
        # by passing by that node, for each node. That value is partly known, partly heuristic.
        # For the first node, that value is completely heuristic. The rest of the node's value should be set to infinity.
        ddd=dict()
        for i in self.map.intersections:
            ddd[i]=float("inf")
        ddd[self.start] = 0.0
        return ddd
    
    
    
    
    #Set certain variables
    
    def set_map(self, M):
        # TODO: Set map to new value. 
        self._reset(self)
        self.start = None
        self.goal = None
        self.map = M

    def set_start(self, start):
        # TODO: Set start value. Remember to remove goal, closedSet, openSet, cameFrom, gScore, fScore, and path attributes' values.
        self._reset(self)
        self.start = start
        
    def set_goal(self, goal):
        # TODO: Set goal value
        self._reset(self)
        self.goal = goal
    
    
    
    
    #Get node information
    
    def is_open_empty(self):
        # TODO: Return True if the open set is empty. False otherwise.
        return len(self)==0
    
    def get_current_node(self):
        # TODO: Return the node in the open set with the lowest value of f(node).
        #Got inspiration from https://github.com/wgcv/Intro-to-Self-Driving-Cars/blob/master/Project%205%20-%20Implement%20Route%20Planner/project_notebook.ipynb
        current_min = self.calculate_fscore(self.openSet[0])
        for node in self.openSet:
            if self.calculate_fscore(node) < current_min:
                current_node = node
                current_min = self.calculate_fscore(node)
        return current_node
    
    def get_neighbors(self, node):
        # TODO: Return the neighbors of a node
        return(self.map.roads[node])
    
    
    
    #Scores and Costs
    
    def get_gScore(self, node):
        # TODO: Return the g Score of a node
        return self.gScore[node]
    
    def distance(self, node_1, node_2):
        # TODO: Compute and return the Euclidean L2 Distance
        import math
        x=self.map.intersections[node_1][0]-self.map.intersections[node_2][0]
        y=self.map.intersections[node_1][1]-self.map.intersections[node_2][1]
        return math.sqrt(x*x+y*y)
    
    def get_tentative_gScore(self, current, neighbor):
        # TODO: Return the g Score of the current node plus distance from the current node to it's neighbors
        return self.gScore[current] + self.distance(current,neighbor)
    
    def heuristic_cost_estimate(self, node):
        # TODO: Return the heuristic cost estimate of a node
        return self.distance(node,self.goal)
    
    def calculate_fscore(self, node):
        # TODO: Calculate and returns the f score of a node. 
        # REMEMBER F = G + H
        self.fScore[node]=self.get_gScore(node)+self.heuristic_cost_estimate(node)
        return self.fScore[node]

    def record_best_path_to(self, current, neighbor):
        # TODO: Record the best path to a node, by updating cameFrom, gScore, and fScore
        self.cameFrom[neighbor] = current
        self.gScore[neighbor] = self.get_tentative_gScore(current, neighbor)
        self.calculate_fscore(neighbor)
