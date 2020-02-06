# Skrpyt pobiera dane przewozu. Dane muszą zostać podane w formie listy list, ze
# względu na możliwość przejazdu więcej niż dwóch zwierząt na raz.
#
# Skrypt rozpoznaje czy sekwencja jest typowa dla skryptu przewoz.py - mianowicie
# czy rozpoczyna się wyrazem "POCZĄTEK" i kończy wyrazem "KONIEC". Ponadto
# zwraca odpowiedni komunikat jeżeli otrzyma komunikat "NIEMOŻLIWE" ze skrpytu
# przewoz.py
#
# Sekwencja przewozu zostaje wyświetlona graficznie. Są wyświetlane dwa brzegi
# Wypełnione odpowiednim inwentarzem. Wciśnięcie klawisza enter przechodzi do
# kolejnego kroku.
#
#


import copy
import sys
import cabbage as cbg
import time

f = cbg.load_file()

# Defining capacity of a boat, default capacity is set at 2
if sys.argv[2]:
    cap = int(sys.argv[2])
else:
    cap = 2

pre_order = sys.stdin.read().strip('\n')
order = eval(pre_order)

# Constructing sequence from input
if order == ['NIEMOŻLIWE']:
    print('Transport jest niemożliwy, podaj sekwencję lub zmień parametry poprzeniego skryptu.')
    sys.exit()
elif type(order) == list:
    if ['KONIEC'] in order:
        sequence = order[1:-1]
    else:
        sequence = order
elif type(order) == str:
    print('Sekwencję przewozu pasażerów należy podać w formie listy.')
    sys.exit()
else:
    print('Invalid input, check readme for valid input types.')

# Defining shores
w_shore = cbg.Shore(cbg.load_dicts(f))
e_shore = w_shore.create_empty_shore()

# Stating our goal for number of animals on east shore.
goal = copy.deepcopy(w_shore)

# Defining number of letters in longest animal name for cosmetic purposes.
# Also defining number of lines for graphical representation.
max_char = max([len(k) for k in w_shore.inv])
number_of_lines = len(w_shore.create_shore_list())

del pre_order


# Defining function that prints message containing shore states in each step
def statement(transfer):
    w_list = w_shore.create_shore_list()
    e_list = e_shore.create_shore_list()
    print(15 * '🚢 ')
    print((max_char - 2) * ' ' + 'Zachód ↤ ' + '✵' + ' ↦ Wschód\n')
    for line in range(number_of_lines):
        w_item = cbg.safe_list_get(w_list, line, max_char * " ")
        e_item = cbg.safe_list_get(e_list, line, max_char * " ")
        print(w_item + (max_char - len(w_item)) * " " + "|" + 14 * " " + "|" + (max_char - len(e_item)) * " " + e_item)
    if transfer:
        print('\n' + direction + str(transfer) + '\n')


# Printing out starting inventory on both shores
print((max_char) * ' ' + 'Stan początkowy')
statement(None)
time.sleep(5)
# Creating a loop that'll iterate over next steps in given sequence
for course_number in range(len(sequence)):
    transfer = sequence[course_number]
    if not transfer:  # Stating what will happen if the boat doesn't take any passengers on board
        print(15 * '🚢 ' + '\n')
        print(2 * '🚢 ' + "Łódka przepłynęła bez załadunku  " + 2 * '🚢 ' + '\n')
        time.sleep(5)
    else:
        if (course_number % 2) == 0:  # Index numbers in list containing sequence ensure that boat goes back and forth
            w_shore.minus(transfer)
            e_shore.plus(transfer)
            direction = 'Łódka przepływając z zachodniego brzegu na wschodni przewiozła następujący ładunek: '
            statement(transfer)
            time.sleep(5)
            if course_number > 1:
                if not w_shore.frenzy_check():  # After each step shore that the boat is leaving will be checked for
                    print(max_char * ' ' + 'Niestety doszło do konfliktu żywieniowego na wschodnim brzegu')
                    sys.exit()
        elif (course_number % 2) != 0:
            w_shore.plus(transfer)
            e_shore.minus(transfer)
            direction = 'Łódka przepływając z wschodniego brzegu na zachodni przewiozła następujący ładunek: '
            statement(transfer)
            time.sleep(5)
            if course_number > 1:
                if not e_shore.frenzy_check():
                    print(max_char * ' ' + 'Niestety doszło do konfliktu żywieniowego na zachodnim brzegu')
                    sys.exit()
        if e_shore.inv == goal.inv:  # Stating where to go to summary
            break

# Final celebratory message
statement(None)
print('Udało się przewieźć wszystkie zwierzęta na drugą stronę!\n')
if 'WILK' in e_shore.create_shore_list():
    print('Tylko po co rolnikowi wilk...\n')
