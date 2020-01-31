import copy
import sys
import itertools
import networkx as nx


# Creating class for each course, with unique id and direction
# Direction: - True = transfer to east shore
#           - False = transfer to west shore
# Creating a powerset from given set of objects.
def powerset(s):
    x = len(s)
    masks = [1 << i for i in range(x)]
    for i in range(1 << x):
        yield [ss for mask, ss in zip(masks, s) if i & mask]

def safe_list_get (l, idx, default):
  try:
    return str(l[idx])
  except IndexError:
    return default

# Defining class for each transfer with two attributes: name - passengers and direction.
class Transfer:
    new_id = itertools.count()

    def __init__(self, name: list, direction: int):
        self.name = name
        self.id = next(self.new_id)
        self.direction = direction


class Shore:

    def __init__(self, inv: dict):
        self.inv = inv

    # Subtracting number of animals on given shore.
    def minus(self, passengers):
        list_of_passengers = [i for i in passengers]
        for i in list_of_passengers:
            self.inv[i] = self.inv[i] - 1
            if self.inv[i] < 0:
                raise Exception('Number of animals became less than 0')
        return self.inv

    # Adding number of animals to given shore.
    def plus(self, passengers):
        list_of_passengers = [i for i in passengers]
        for i in list_of_passengers:
            self.inv[i] = self.inv[i] + 1
        return self.inv

    # Function returning boolean value depending on eating habits and current state of given shore.
    # If farmer is not paying attention to the given shore, some animals might get hungry.
    # Should there be a health hazard for any animal, function will return adequate result.
    def frenzy_check(self):
        list_of_keys = list(habits.keys())
        list_of_values = copy.deepcopy(list(habits.values()))
        vore = []
        for i in list_of_values:
            for j in i:
                element = [j, list_of_keys[list_of_values.index(i)]]
                vore.append(element)
        all_comb = powerset(self.create_shore_list())
        unique = [list(x) for x in set(tuple(x) for x in all_comb)]
        animal_pairs = [sorted(i) for i in sorted(unique) if len(i) == 2]
        for i in vore:
            if sorted(i) in animal_pairs:
                return False
            else:
                pass
        return True

    # Creating full list of animals on shore from shore dictionary for further combination.
    def create_shore_list(self):
        current_shore = []
        for i in self.inv:
            for j in range(self.inv[i]):
                current_shore.append(i)
        return current_shore

    # Combinating all possible configurations of passangers that might leave given shore.
    # Empty boat is taken into account. Any combinations that exceed boat capacity are discarded.
    def possible_passengers(self, cap):
        all = powerset(self.create_shore_list())
        unique = [list(x) for x in set(tuple(x) for x in all)]
        passenger_combinations = [i for i in sorted(unique) if len(i) < cap]
        return passenger_combinations

    # Creating empty, east shore
    def create_empty_shore(self):
        blank = {k: 0 for k in self.inv}
        return Shore(blank)


# Loading a file and preparing for further use.
def load_file(a=sys.argv[1]):
    pre = open(a, 'r').readlines()
    sep = [i.strip('\n').split(" ") for i in pre]
    return sep


global habits
habits = {}


# Loading info about number of animals on starting shore and their eating habits from file.
def load_dicts(fn):
    start = {}
    for i in fn:
        if len(i) > 1:
            if not i[0].isdigit():
                k = i[0]
                v = i[1:]
                habits[k] = v
        if len(i) == 2:
            if i[0].isdigit():
                k = i[1]
                v = int(i[0])
                start[k] = v
        elif len(i) == 1:
            k = i[0]
            start[k] = 1
    return start


# Checking history allows us to spot possible loops. Function forbids repeating same shore patterns with same
# passengers on board.
def check_history(graph, node, course, c_shore, o_shore):
    check_in = {str(c_shore.inv): str(o_shore.inv)}
    if sorted(course.name) in list(graph.nodes[node]['name_history']) and \
            list(check_in.items())[0] in list(graph.nodes[node]['shore_history'].items()):
        return False
    else:
        return True


# Returns all leaf nodes that aren't already completed in some way or are initial node.
leaf_labels = [['ZAPĘTLENIE'], ['POŻARCIE'], ['KONIEC'], ['POCZĄTEK']]


def return_leafs(graph):
    leaf_nodes = [node for node in graph.nodes() if graph.degree(node) == 1
                  and graph.nodes[node]['label'] not in leaf_labels]
    # if 0 in leaf_nodes:
    #     leaf_nodes.remove(0)
    return leaf_nodes


# Just as the name suggest - it finds all shortest paths, if those are equal it'll choose one
def find_shortest(graph, list_of_ends):
    all_paths = [nx.bidirectional_shortest_path(graph, 0, i) for i in list_of_ends]
    return min(all_paths, key=len)
