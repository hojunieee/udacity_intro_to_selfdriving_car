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

#Test Code
from helpers import load_map_40

MAP_40_ANSWERS = [
    (5, 34, [5, 16, 37, 12, 34]),
    (5, 5,  [5]),
    (8, 24, [8, 14, 16, 37, 12, 17, 10, 24])
]

def test(shortest_path_function):
    map_40 = load_map_40()
    correct = 0
    for start, goal, answer_path in MAP_40_ANSWERS:
        path = shortest_path_function(map_40, start, goal).path
        if path == answer_path:
            correct += 1
        else:
            print("For start:", start, 
                  "Goal:     ", goal,
                  "Your path:", path,
                  "Correct:  ", answer_path)
    if correct == len(MAP_40_ANSWERS):
        print("All tests pass! Congratulations!")
    else:
        print("You passed", correct, "/", len(MAP_40_ANSWERS), "test cases")
        
        
#helpers

import networkx as nx
import pickle
import plotly.plotly as py
import random
from plotly.graph_objs import *
from plotly.offline import init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)


map_10_dict = {
	0: {'pos': (0.7798606835438107, 0.6922727646627362), 'connections': [7, 6, 5]}, 
	1: {'pos': (0.7647837074641568, 0.3252670836724646), 'connections': [4, 3, 2]}, 
	2: {'pos': (0.7155217893995438, 0.20026498027300055), 'connections': [4, 3, 1]}, 
	3: {'pos': (0.7076566826610747, 0.3278339270610988), 'connections': [5, 4, 1, 2]}, 
	4: {'pos': (0.8325506249953353, 0.02310946309985762), 'connections': [1, 2, 3]}, 
	5: {'pos': (0.49016747075266875, 0.5464878695400415), 'connections': [7, 0, 3]}, 
	6: {'pos': (0.8820353070895344, 0.6791919587749445), 'connections': [0]}, 
	7: {'pos': (0.46247219371675075, 0.6258061621642713), 'connections': [0, 5]}, 
	8: {'pos': (0.11622158839385677, 0.11236327488812581), 'connections': [9]}, 
	9: {'pos': (0.1285377678230034, 0.3285840695698353), 'connections': [8]}
}

map_40_dict = {
	0: {'pos': (0.7801603911549438, 0.49474860768712914), 'connections': [36, 34, 31, 28, 17]}, 
	1: {'pos': (0.5249831588690298, 0.14953665513987202), 'connections': [35, 31, 27, 26, 25, 20, 18, 17, 15, 6]}, 
	2: {'pos': (0.8085335344099086, 0.7696330846542071), 'connections': [39, 36, 21, 19, 9, 7, 4]}, 
	3: {'pos': (0.2599134798656856, 0.14485659826020547), 'connections': [35, 20, 15, 11, 6]}, 
	4: {'pos': (0.7353838928272886, 0.8089961609345658), 'connections': [39, 36, 21, 19, 9, 7, 2]}, 
	5: {'pos': (0.09088671576431506, 0.7222846879290787), 'connections': [32, 16, 14]}, 
	6: {'pos': (0.313999018186756, 0.01876171413125327), 'connections': [35, 20, 15, 11, 1, 3]}, 
	7: {'pos': (0.6824813442515916, 0.8016111783687677), 'connections': [39, 36, 22, 21, 19, 9, 2, 4]}, 
	8: {'pos': (0.20128789391122526, 0.43196344222361227), 'connections': [33, 30, 14]}, 
	9: {'pos': (0.8551947714242674, 0.9011339078096633), 'connections': [36, 21, 19, 2, 4, 7]}, 
	10: {'pos': (0.7581736589784409, 0.24026772497187532), 'connections': [31, 27, 26, 25, 24, 18, 17, 13]}, 
	11: {'pos': (0.25311953895059136, 0.10321622277398101), 'connections': [35, 20, 15, 3, 6]}, 
	12: {'pos': (0.4813859169876731, 0.5006237737207431), 'connections': [37, 34, 31, 28, 22, 17]}, 
	13: {'pos': (0.9112422509614865, 0.1839028760606296), 'connections': [27, 24, 18, 10]}, 
	14: {'pos': (0.04580558670435442, 0.5886703168399895), 'connections': [33, 30, 16, 5, 8]}, 
	15: {'pos': (0.4582523173083307, 0.1735506267461867), 'connections': [35, 31, 26, 25, 20, 17, 1, 3, 6, 11]}, 
	16: {'pos': (0.12939557977525573, 0.690016328140396), 'connections': [37, 30, 5, 14]}, 
	17: {'pos': (0.607698913404794, 0.362322730884702), 'connections': [34, 31, 28, 26, 25, 18, 0, 1, 10, 12, 15]}, 
	18: {'pos': (0.719569201584275, 0.13985272363426526), 'connections': [31, 27, 26, 25, 24, 1, 10, 13, 17]}, 
	19: {'pos': (0.8860336256842246, 0.891868301175821), 'connections': [21, 2, 4, 7, 9]}, 
	20: {'pos': (0.4238357358399233, 0.026771817842421997), 'connections': [35, 26, 1, 3, 6, 11, 15]}, 
	21: {'pos': (0.8252497121120052, 0.9532681441921305), 'connections': [2, 4, 7, 9, 19]}, 
	22: {'pos': (0.47415009287034726, 0.7353428557575755), 'connections': [39, 37, 29, 7, 12]}, 
	23: {'pos': (0.26253385360950576, 0.9768234503830939), 'connections': [38, 32, 29]}, 
	24: {'pos': (0.9363713903322148, 0.13022993020357043), 'connections': [27, 10, 13, 18]}, 
	25: {'pos': (0.6243437191127235, 0.21665962402659544), 'connections': [34, 31, 27, 26, 1, 10, 15, 17, 18]}, 
	26: {'pos': (0.5572917679006295, 0.2083567880838434), 'connections': [34, 31, 27, 1, 10, 15, 17, 18, 20, 25]}, 
	27: {'pos': (0.7482655725962591, 0.12631654071213483), 'connections': [31, 1, 10, 13, 18, 24, 25, 26]}, 
	28: {'pos': (0.6435799740880603, 0.5488515965193208), 'connections': [39, 36, 34, 31, 0, 12, 17]}, 
	29: {'pos': (0.34509802713919313, 0.8800306496459869), 'connections': [38, 37, 32, 22, 23]}, 
	30: {'pos': (0.021423673670808885, 0.4666482714834408), 'connections': [33, 8, 14, 16]}, 
	31: {'pos': (0.640952694324525, 0.3232711412508066), 'connections': [34, 0, 1, 10, 12, 15, 17, 18, 25, 26, 27, 28]}, 
	32: {'pos': (0.17440205342790494, 0.9528527425842739), 'connections': [38, 5, 23, 29]}, 
	33: {'pos': (0.1332965908314021, 0.3996510641743197), 'connections': [8, 14, 30]}, 
	34: {'pos': (0.583993110207876, 0.42704536740474663), 'connections': [0, 12, 17, 25, 26, 28, 31]}, 
	35: {'pos': (0.3073865727705063, 0.09186645974288632), 'connections': [1, 3, 6, 11, 15, 20]}, 
	36: {'pos': (0.740625863119245, 0.68128520136847), 'connections': [39, 0, 2, 4, 7, 9, 28]}, 
	37: {'pos': (0.3345284735051981, 0.6569436279895382), 'connections': [12, 16, 22, 29]}, 
	38: {'pos': (0.17972981733780147, 0.999395685828547), 'connections': [23, 29, 32]}, 
	39: {'pos': (0.6315322816286787, 0.7311657634689946), 'connections': [2, 4, 7, 22, 28, 36]}
}


class Map:
	def __init__(self, G):
		self._graph = G
		self.intersections = nx.get_node_attributes(G, "pos")
		self.roads = [list(G[node]) for node in G.nodes()]

	def save(self, filename):
		with open(filename, 'wb') as f:
			pickle.dump(self._graph, f)

def load_map_graph(map_dict):
	G = nx.Graph()
	for node in map_dict.keys():
		G.add_node(node, pos=map_dict[node]['pos'])
	for node in map_dict.keys():
		for con_node in map_dict[node]['connections']:
			G.add_edge(node, con_node)
	return G

def load_map_10():
	G = load_map_graph(map_10_dict)
	return Map(G)

def load_map_40():
	G = load_map_graph(map_40_dict)
	return Map(G)

def show_map(M, start=None, goal=None, path=None):
    G = M._graph
    pos = nx.get_node_attributes(G, 'pos')
    edge_trace = Scatter(
    x=[],
    y=[],
    line=Line(width=0.5,color='#888'),
    hoverinfo='none',
    mode='lines')

    for edge in G.edges():
        x0, y0 = G.node[edge[0]]['pos']
        x1, y1 = G.node[edge[1]]['pos']
        edge_trace['x'] += [x0, x1, None]
        edge_trace['y'] += [y0, y1, None]

    node_trace = Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers',
        hoverinfo='text',
        marker=Marker(
            showscale=False,
            # colorscale options
            # 'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
            # Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu'
            colorscale='Hot',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=2)))
    for node in G.nodes():
        x, y = G.node[node]['pos']
        node_trace['x'].append(x)
        node_trace['y'].append(y)

    for node, adjacencies in enumerate(G.adjacency_list()):
        color = 0
        if path and node in path:
            color = 2
        if node == start:
            color = 3
        elif node == goal:
            color = 1
        # node_trace['marker']['color'].append(len(adjacencies))
        node_trace['marker']['color'].append(color)
        node_info = "Intersection " + str(node)
        node_trace['text'].append(node_info)

    fig = Figure(data=Data([edge_trace, node_trace]),
                 layout=Layout(
                    title='<br>Network graph made with Python',
                    titlefont=dict(size=16),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                   
                    xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)))

    iplot(fig)
