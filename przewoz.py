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
import networkx as nx
import matplotlib.pyplot as plt
import random
import cabbage as cbg

f = cbg.load_file()

# Defining capacity of a boat, default capacity is set at 2.
if sys.argv[2]:
    cap = int(sys.argv[2])
else:
    cap = 2
pre_shore = cbg.load_dicts(f)
w_shore = cbg.Shore(cbg.earmarking(pre_shore))
e_shore = w_shore.create_empty_shore()
G = nx.Graph()
# Stating our goal for number of animals on east shore.
goal = copy.deepcopy(w_shore)
node_sizes = {}  # Creating dictionary to store and then modify size of given .

# And the journey has begun!

# Initializing graph with starting node and first possible transfers.
G.add_node(0, label=['POCZĄTEK'], state=[w_shore, e_shore])
node_sizes[0] = 50

for possibility in G.nodes[0]['state'][0].possible_passengers(cap):
    course = cbg.Transfer(possibility, 1)
    current_shore = copy.deepcopy(G.nodes[0]['state'][0])
    other_shore = copy.deepcopy(G.nodes[0]['state'][1])
    current_shore.minus(course.name)
    other_shore.plus(course.name)
    if current_shore.frenzy_check():
        G.add_node(course.id, label=course.name,
                   direction=course.direction,
                   state=[current_shore, other_shore],
                   shore_history={str(current_shore.inv): str(other_shore.inv)},
                   name_history=[list(course.name)])
        node_sizes[course.id] = 50
        G.add_edge(0, course.id)

    else:
        smallish = random.random()
        G.add_node(smallish, label=['POŻARCIE'])
        G.add_edge(0, smallish)
        node_sizes[smallish] = 50

# Acquiring first possible path ways.
leaf_nodes = cbg.return_leafs(G)
# Creating list with already visited nodes so that script doesn't check them again.
no_repetitions = []

# Script will jump around leaf nodes until there aren't any left that were either visited or labeled as error or
# meeting goal.
while leaf_nodes:
    for i in leaf_nodes:
        current_shore = copy.deepcopy(G.nodes[i]['state'][1])  # Repositioning shore so that with each iteration
        other_shore = copy.deepcopy(G.nodes[i]['state'][0])  # boat can transfer between shores.
        if G.nodes[i]['direction'] == (-1):
            break_point = goal.inv  # Specifing what kind of shore inventory should trigger end node,
        else:  # depending in which direction the boat is currently heading.
            break_point = e_shore.inv
        if other_shore.inv != break_point:
            for possibility in current_shore.possible_passengers(cap):
                if G.nodes[i]['direction'] == (-1):  # Changing direction of the boat.
                    course = cbg.Transfer(possibility, 1)
                else:
                    course = cbg.Transfer(possibility, (-1))
                c_shore = copy.deepcopy(current_shore)  # Ensuring that the shore inventory is changed just for
                o_shore = copy.deepcopy(other_shore)  # path we're currently on.
                c_shore.minus(course.name)
                o_shore.plus(course.name)
                c = str(c_shore.inv)
                o = str(o_shore.inv)
                reference = copy.deepcopy(G.nodes[i]['shore_history'])
                reference.update({c: o})  # Storing data about previous steps within same path.
                if course.name == [] and G.nodes[i]['label'] == []:  # Preventing from cruising with empty boat
                    pass  # back and forth.
                else:
                    if c_shore.frenzy_check():  # Caring about animals.
                        if cbg.check_history(G, i, course, c_shore, o_shore):  # Caring about history.
                            G.add_node(course.id,  # Finally adding a node to the graph, node number should be unique
                                       label=course.name,  # course.id.
                                       direction=course.direction,
                                       state=[c_shore, o_shore],
                                       shore_history=reference)
                            if len(course.name) > 1:  # Depending on boat capacity there had to be different name
                                G.nodes[course.id]['name_history'] = list(  # history storing techniques.
                                    G.nodes[i]['name_history'] + [sorted(course.name)])
                            elif len(course.name) == 1:
                                G.nodes[course.id]['name_history'] = list(
                                    G.nodes[i]['name_history'] + [[i] for i in sorted(course.name)])
                            else:
                                G.nodes[course.id]['name_history'] = list(G.nodes[i]['name_history'])
                            G.add_edge(i, course.id)  # Connecting nodes
                            node_sizes[course.id] = 50
                        else:
                            smallish = random.random()  # Creating float number so it can be distinguished from others.
                            G.add_node(smallish, label=['ZAPĘTLENIE'])
                            G.add_edge(i, smallish)
                            no_repetitions.append(smallish)
                            node_sizes[smallish] = 50
                    else:
                        smallish = random.random()
                        G.add_node(smallish, label=['POŻARCIE'])
                        G.add_edge(i, smallish)
                        no_repetitions.append(smallish)
                        node_sizes[smallish] = 50
        else:
            G.add_node((-1) * i, label=['KONIEC'])  # Negative id will highlight goal nodes.
            G.add_edge(i, (-1) * i)
            no_repetitions.append((-1) * i)
            node_sizes[(-1) * i] = 50
        no_repetitions.append(i)
    leaf_nodes = cbg.return_leafs(G)  # Finding new leaf nodes.
    leaf_nodes = set(leaf_nodes) - set(no_repetitions)

# Making list of all node labels for future reference.
list_of_labels = [G.nodes[i]['label'] for i in G.nodes()]

# Identifing goal nodes.
end_points = [i for i in G.nodes() if i < 0]

color_map = []

# Printing out final result and also highliting nodes in shortest path to goal.
if ['KONIEC'] in list_of_labels:
    shortest_path = cbg.find_shortest(G, end_points)
    for node in G:
        if node in shortest_path:
            color_map.append('green')
            node_sizes[node] = 1000
        else:
            color_map.append('red')
    final_stretch = [G.nodes[i]['label'] for i in shortest_path]
    print(cbg.remove_earmarking(final_stretch))

#    for i in shortest_path:
#        print(G.nodes[i]['label'], end=' ')
else:
    print('['+'\'NIEMOŻLIWE\''+']')

list_of_node_sizes = [node_sizes[k] for k in node_sizes]

# Drawing a graph and saving it as a .png file.
labels = dict((n, d['label']) for n, d in G.nodes(data=True))
plt.figure(figsize=(20, 10))
nx.draw(G, labels=labels, font_size=5, node_color=color_map, node_size=list_of_node_sizes, with_labels=True,
        node_shape='D', legend='label')
plt.savefig("graph1.png")
