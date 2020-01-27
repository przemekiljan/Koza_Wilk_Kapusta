# Chcemy doporowadzić do sytuacji w której wszystko znajduje się na wschodnim brzegu
#
# Klasa transfer określa dwie rzeczy - załadunek łódki oraz jej kierunek
#
# Z każdym kursem musi być wygenerowany set możliwych kombinacji pasażerów który nie zagraża życiu zwierzaków
# Jeżeli dwa kursy pod rząd zaproponują żeby nie zabierać niczego to skrypt jest przerywany błędem - "pat"
# Jeżeli skrypt zaczyna się zapętlać i cyklicznie powatarzać kursy to również zakończy się błędem
# Skrypt nie może doprowadzić do sytuacji w której zawożąc zwierzę na jeden brzeg, zabierze to samo zwierze z powrotem
# Unikalne id pozwalają na odróżnienie zwierząt tego samego rodzaju
# Jeżeli więcej niż jedna z kombinacji pozwala na przewóz zwierzątka to skrypt przetestuje wszystkie możliwe sytuacje
# aż nie dojdzie to sytuacji w której na prawym brzegu znajdzie się cały inwentarz
#
# Model z kombinacjami i "drzewkiem decyzyjnym" sugeruje użycie grafów

# Węzłami w grafie są kolejne kombinacje pasażerów, postępują tylko te ścieżki które nie kolidują z zależnościami
# kto zjada kogo
#
# Grafy tworzone z pomocą pakietu Networkx, który pozwala na łatwą integrację kolejnych węzłów
#
# Każdy węzeł cechuje się id któremu odpowiada odpowiedni załadunek na łódce
#
# Dzięki pakietowi Networkx można generować wierzchołki grafu, tzw. liście
# Trzeba napisać funkcję która skacze po liściach i dodaje kolejne kroki tylko do tych, które nie są błędami
#
#

import copy
import sys
import itertools
import networkx as nx
import matplotlib.pyplot as plt



# Creating class for each course, with unique id and direction
# Direction: - True = transfer to east shore
#           - False = transfer to west shore
# Creating a powerset from given set of objects
def powerset(s):
    x = len(s)
    masks = [1 << i for i in range(x)]
    for i in range(1 << x):
        yield [ss for mask, ss in zip(masks, s) if i & mask]


class Transfer:
    new_id = itertools.count()

    def __init__(self, name: list, direction: int):
        self.name = name
        self.id = next(self.new_id)
        self.direction = direction

    # def change_direction(self):
    #     if self.direction:
    #         self.direction = False
    #     else:
    #         self.direction = True

    def store_data(self, state1, state2):
        storage[self.id] = [self.name,state1,state2, self.direction]


class Shore:

    def __init__(self, inv: dict):
        self.inv = inv

    # Subtracting number of animals on given shore
    def minus(self, passengers):
        list_of_passengers = [i for i in passengers]
        for i in list_of_passengers:
            self.inv[i] = self.inv[i] - 1
            if self.inv[i] < 0:
                raise Exception('Number of animals became less than 0')
        return self.inv

    # Adding number of animals to given shore
    def plus(self, passengers):
        list_of_passengers = [i for i in passengers]
        for i in list_of_passengers:
            self.inv[i] = self.inv[i] + 1
        return self.inv

    # Function returning boolean value depending on eating habits and current state of given shore.
    # If farmer is not paying attention to the given shore, some animals might get hungry.
    # Should there be a health hazard for any animal, function will return adequate result
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

    # Creating full list of animals on shore from shore dictionary for further combination
    def create_shore_list(self):
        current_shore = []
        for i in self.inv:
            for j in range(self.inv[i]):
                current_shore.append(i)
        return current_shore

    # Combinating all possible configurations of passangers that might leave given shore.
    # Empty boat is taken into account. Any combinations that exceed boat capacity are discarded
    def possible_passengers(self):
        all = powerset(self.create_shore_list())
        unique = [list(x) for x in set(tuple(x) for x in all)]
        passenger_combinations = [i for i in sorted(unique) if len(i) < cap]
        return passenger_combinations

    # Creating empty, east shore
    def create_empty_shore(self):
        blank = {k: 0 for k in self.inv}
        return Shore(blank)


# Loading a file and preparing for further use
def load_file(a=sys.argv[1]):
    pre = open(a, 'r').readlines()
    sep = [i.strip('\n').split(" ") for i in pre]
    return sep


f = load_file()

# Defining capacity of a boat, default capacity is set at 2
if sys.argv[2]:
    cap = int(sys.argv[2])
else:
    cap = 2

global habits
habits = {}


# Loading info about number of animals on starting shore and their eating habits from file
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

def check_path(end):
    path_nodes = sorted(nx.bidirectional_shortest_path(G, 0, end))[1:]
    all = list(powerset(path_nodes))
    unique = [list(x) for x in set(tuple(x) for x in all)]
    node_pairs = [sorted(i) for i in sorted(unique) if len(i) == 2]
    for i in node_pairs:
        if G.nodes[i[0]]['name'] == G.nodes[i[1]]['name'] and\
            G.nodes[i[0]]['direction'] == G.nodes[i[1]]['direction'] and\
                G.nodes[i[0]]['state'][0].inv == G.nodes[i[1]]['state'][0].inv and\
                    G.nodes[i[0]]['state'][1].inv == G.nodes[i[1]]['state'][1].inv:
                        return True
    return False


w_shore = Shore(load_dicts(f))
e_shore = w_shore.create_empty_shore()
storage = {}
G = nx.Graph()
# Stating our goal for number of animals on east shore
goal = copy.deepcopy(w_shore)

# And the journey has begun
G.add_node(0, name='POCZĄTEK', state = [w_shore,e_shore])

for possibility in G.nodes[0]['state'][0].possible_passengers():
    course = Transfer(possibility, 1)
    current_shore = copy.deepcopy(G.nodes[0]['state'][0])
    other_shore = copy.deepcopy(G.nodes[0]['state'][1])
    current_shore.minus(course.name)
    other_shore.plus(course.name)
    if current_shore.frenzy_check():
        course.store_data(current_shore.inv, other_shore.inv)
        G.add_node(course.id, name=course.name, direction=course.direction, state=[current_shore,other_shore])
        G.add_edge(0,course.id)

leaf_nodes = [node for node in G.nodes() if G.degree(node) == 1]
if 0 in leaf_nodes:
    leaf_nodes.remove(0)
# while len(G.nodes())<15:
no_repetitions = []
while (leaf_nodes):
    for i in leaf_nodes:
        if G.nodes[i]['direction'] == (-1):
            current_shore = copy.deepcopy(G.nodes[i]['state'][1])
            other_shore = copy.deepcopy(G.nodes[i]['state'][0])
            if other_shore.inv != goal.inv:
                for possibility in current_shore.possible_passengers():
                    course = Transfer(possibility,1)
                    c_shore = copy.deepcopy(current_shore)
                    o_shore = copy.deepcopy(other_shore)
                    c_shore.minus(course.name)
                    o_shore.plus(course.name)
                    if [course.name, c_shore.inv, o_shore.inv, 1] not in storage.values():
                        if c_shore.frenzy_check():
                            course.store_data(c_shore.inv,o_shore.inv)
                            G.add_node(course.id, name=course.name, direction=course.direction,
                                       state=[c_shore, o_shore])
                            G.add_edge(i, course.id)
                            # if check_path(course.id):
                            #     G.remove_node(course.id)
            else:
                G.add_node(1, name="KONIEC")
                G.add_edge(i, 1)
                no_repetitions.append(1)
        if G.nodes[i]['direction'] == 1:
            current_shore = copy.deepcopy(G.nodes[i]['state'][1])
            other_shore = copy.deepcopy(G.nodes[i]['state'][0])
            if other_shore.inv != e_shore.inv:
                for possibility in current_shore.possible_passengers():
                    course = Transfer(possibility, (-1))
                    c_shore = copy.deepcopy(current_shore)
                    o_shore = copy.deepcopy(other_shore)
                    c_shore.minus(course.name)
                    o_shore.plus(course.name)
                    if [course.name, c_shore.inv, o_shore.inv, -1] not in storage.values():
                        if c_shore.frenzy_check():
                            course.store_data(c_shore.inv, o_shore.inv)
                            G.add_node(course.id, name=course.name, direction=course.direction,
                                       state=[c_shore, o_shore])
                            G.add_edge(i, course.id)
                            # if check_path(course.id):
                            #     G.remove_node(course.id)
            else:
                G.add_node(3, name="KONIEC")
                G.add_edge(i, 3)
                no_repetitions.append(3)
        no_repetitions.append(i)
    leaf_nodes = [node for node in G.nodes() if G.degree(node) == 1]
    leaf_nodes = set(leaf_nodes) - set(no_repetitions)
    if 0 in leaf_nodes:
        leaf_nodes.remove(0)

labels=dict((n,d['name']) for n,d in G.nodes(data=True))
nx.draw(G,labels=labels,node_size=1000)
plt.savefig("graph1.png")
