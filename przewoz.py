# Jesteśmy obserwatorem na lewym brzegu. Lewy brzeg - tu, prawy brzeg - tam
# Początkowy stan występuje na lewym brzegu.
# Chcemy doporowadzić do sytuacji w której wszystko znajduje się na prawym brzegu
#
# Obecność Charona na którymś z brzegów chroni zwierzęta
#
# Charon występuje tylko w dwóch stanach 1/0, 1 oznacza, że jest tu a 0 że jest tam
# 1 będzie oznaczać transport z tu do tam
# 0 będzie oznaczać transport z tam do tu
#
# Podróż może doprowadzać do zmainy stanu lub nie
# Podróż 1 (do tam) pozwala na zjadanie na tamtym brzegu
# Podróż 0 (do tu) pozwala na zjadanie na tym brzegu
#
# Zmiana stanu jednego brzegu powoduję zmianę na drugim
#
# 2 funkcje wysiadanie i wsiadanie, przy wysiadaniu zwierzęta mogą się zjadać, przy wsiadaniu już nie
# Stan Charona świadczy o tym na którym brzegu zachodzą funckje wysiadanie i wsiadanie
# Może dojść do sytuacji w której zwierze wysiadło ale żadne nie wsiadło, wtedy stan się nie zmienia, ale nadal musi się zgadzać
# Funckje wsiadanie i wysiadanie jako jeden z argumentów przyjmują ilość miejsc na łódce, jedno z nich zawsze zajmuje Charon
#
# Z każdym kursem musi być wygenerowany set możliwych kombinacji pasażerów który nie zagraża życiu zwierzaków
# Jeżeli dwa kursy pod rząd zaproponują żeby nie zabierać niczego to skrypt jest przerywany błędem - "pat"
#
# Jeżeli więcej niż jedna z kombinacji pozwala na przewóz zwierzątka to skrypt przetestuje wszystkie możliwe sytuacje
# aż nie dojdzie to sytuacji w której na prawym brzegu znajduje się cały inwentarz
#
# Model z kombinacjami i "drzewkiem decyzyjnym" sugeruje użycie grafów
#
# Czytanie z pliku zwraca listę zwierzaków oraz zależności między nimi
# Wilk
# Koza
# Surykatka
# Bas
# Brus
# Dzik
# .
# .
# .
#
# Węzłami w grafie są kolejne kombinacje pasażerów, postępują tylko te ścieżki które nie kolidują z zależnościami
# kto zjada kogo
#
# Tworzymy słownik z zależnościami gdzie kluczami są zwierzęta a wartościami zwierzęta, które mogą być przez nie zjedzone
# Recykling skryptu z wykładu który znajduje najkrótszą drogę od startu do ostatniego węzła
#
# Każdy węzeł nazywa się #poziomu.#kombinacji
# Nazwa ta koresponduje ze słownikiem w którym kluczem jest nazwa a wartością przewóz
#

import copy
import sys

if sys.argv[2]:
    cap = int(sys.argv[2])
else:
    cap = 2

def powerset(s):
    x = len(s)
    masks = [1 << i for i in range(x)]
    for i in range(1 << x):
        yield [ss for mask, ss in zip(masks, s) if i & mask]

fn = sys.argv[1]
pre = open(fn, 'r').readlines()
sep = [i.strip('\n').split(" ") for i in pre]
w_shore = {}
menagerie = {}
for i in sep:
    if len(i) > 1:
        if not i[0].isdigit():
            k = i[0]
            v = i[1:]
            menagerie[k] = v
    if len(i) == 2:
        if i[0].isdigit():
            k = i[1]
            v = int(i[0])
            w_shore[k] = v
    elif len(i) == 1:
        k = i[0]
        w_shore[k] = 1
e_shore = {k:0 for k in w_shore}
goal = copy.deepcopy(w_shore)

current_w_shore = []
for i in w_shore:
    for j in range(w_shore[i]):
        current_w_shore.append(i)
a = powerset(current_w_shore)
unique_data = [list(x) for x in set(tuple(x) for x in a)]
comb = [i for i in sorted(unique_data) if len(i) < cap]
print (comb)
#Sprawdzam czy potrafię aktualizować ten skrypt