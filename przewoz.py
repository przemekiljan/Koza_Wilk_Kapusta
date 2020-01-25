# Chcemy doporowadzić do sytuacji w której wszystko znajduje się na wschodnim brzegu
#
# Klasa transfer określa dwie rzeczy - załadunek łódki oraz jej kierunek
#
# Z każdym kursem musi być wygenerowany set możliwych kombinacji pasażerów który nie zagraża życiu zwierzaków
# Jeżeli dwa kursy pod rząd zaproponują żeby nie zabierać niczego to skrypt jest przerywany błędem - "pat"
# Jeżeli skrypt zaczyna się zapętlać i cyklicznie powatarzać kursy to również zakończy się błędem
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
# Funkcji, która zaktualizuje stan brzegu po zabraniu odpowiednich pasażerów
#
# Zaczynamy kilka różnych grafów, ze względu na wszystkie możliwe kombinacje pierwszego kursu,
# z tych początków rozwidlają się pozostałe kombinacje


import copy
import sys
import itertools

# Creating class for each course, with unique id and direction
# Direction: - True = transfer to east shore
#           - False = transfer to west shore

# Creating a powerset from given set of objects
def powerset(s):
    x = len(s)
    masks = [1 << i for i in range(x)]
    for i in range(1 << x):
        yield [ss for mask, ss in zip(masks, s) if i & mask]

class Transfer():
    newid = itertools.count()
    def __init__(self,name = str, direction = bool):
        self.name = name
        self.id = next(self.newid)
        self.direction = direction

    def change_direction(self):
        if self.direction:
            self.direction = False
        else:
            self.direction = True

# Loading a file and preparing for further use
def load_file(a = sys.argv[1]):
    pre = open(a, 'r').readlines()
    sep = [i.strip('\n').split(" ") for i in pre]
    return sep
f = load_file()

# Defining capacity of a boat, default capacity is set at 2
if sys.argv[2]:
    cap = int(sys.argv[2])
else:
    cap = 2

# Loading info about number of animals on starting, west shore and their eating habits from file
def load_dicts(input):
    w_shore = {}
    habits = {}
    for i in input:
        if len(i) > 1:
            if not i[0].isdigit():
                k = i[0]
                v = i[1:]
                habits[k] = v
        if len(i) == 2:
            if i[0].isdigit():
                k = i[1]
                v = int(i[0])
                w_shore[k] = v
        elif len(i) == 1:
            k = i[0]
            w_shore[k] = 1
    return habits, w_shore

menagerie, w_shore = load_dicts(f)

# Creating empty, east shore
def create_empty_shore(start):
    e_shore = {k:0 for k in start}
    return e_shore

e_shore = create_empty_shore(w_shore)

# Stating our goal for number of animals on east shore
def create_goal(start):
    goal = copy.deepcopy(start)
    return goal

goal = create_goal(w_shore)

# Creating full list of animals on shore from shore dictionary for further combination
def create_shore_list(dict):
    current_shore = []
    for i in dict:
        for j in range(dict[i]):
            current_shore.append(i)
    return current_shore

current_w_shore = create_shore_list(w_shore)

# Combinating all possible configurations of passangers that might leave given shore. Empty boat is taken into account.
# Any combinations that exceed boat capacity are discarded
def possible_passengers(shore_list):
    all = powerset(shore_list)
    unique = [list(x) for x in set(tuple(x) for x in all)]
    passenger_combinations = [i for i in sorted(unique) if len(i) < cap]
    return passenger_combinations

comb = possible_passengers(current_w_shore)

# Function returning boolean value depending on eating habits and current state of given shore. If farmer is not paying
# attention to the given shore, some animals might get hungry. Should there be a health hazard for any animal, function
# will return adequate result
def frenzy_check(dict_shore, relations):
    # state = create_shore_list(to_co_robi_iwona)
    list_of_keys = list(relations.keys())
    list_of_values = copy.deepcopy(list(relations.values()))
    for i in list_of_values:
        i.append(list_of_keys[list_of_values.index(i)])
    all = powerset(dict_shore)
    unique = [list(x) for x in set(tuple(x) for x in all)]
    passenger_combinations = [sorted(i) for i in sorted(unique) if len(i) == 2]
    for i in (list_of_values):
        if sorted(i) in (passenger_combinations):
            return False
        else:
            pass
    return True

